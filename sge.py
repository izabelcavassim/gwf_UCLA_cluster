import logging
import re
from xml.etree import ElementTree

from ..utils import ensure_trailing_newline, retry
from .base import PbsLikeBackendBase, Status
from .exceptions import BackendError
from .utils import call

logger = logging.getLogger(__name__)


class SGEBackend(PbsLikeBackendBase):
    """Backend for Sun Grid Engine (SGE).

    To use this backend you must activate the `sge` backend. The backend
    currently assumes that a SGE parallel environment called "smp" is
    available. You can check which parallel environments are available on your
    system by running :command:`qconf -spl`.

    **Backend options:**

    None.

    **Target options:**

    * **cores (int):**
      Number of cores allocated to this target (default: 1).
    * **memory (str):**
      Memory allocated to this target (default: 1).
    * **walltime (str):**
      Time limit for this target (default: 01:00:00).
    * **queue (str):**
      Queue to submit the target to. To specify multiple queues, specify a
      comma-separated list of queue names.
    * **account (str):**
      Account to be used when running the target. Corresponds to the SGE
      project.
    """

    option_defaults = {
        "cores": 2,
        "memory": "1g",
        "walltime": "01:00:00",
        "queue": None,
        "account": None,
    }

    option_flags = {
        "cores": "-pe shared ", #ignoring cores
        "memory": "-l h_data=",
        "walltime": "-l h_rt=",
        "queue": "-q ",
        "account": "-P ",
    }

    @retry(on_exc=BackendError)
    def call_queue_command(self,):
        return call("qstat", "-f", "-xml")

    @retry(on_exc=BackendError)
    def call_cancel_command(self, job_id):
        # The --verbose flag here is necessary, otherwise we're not able to tell
        # whether the command failed. See the comment in call() if you
        # want to know more.
        return call("qdel", job_id)

    @retry(on_exc=BackendError)
    def call_submit_command(self, script, dependencies):
        args = ["-terse"]
        if dependencies:
            args.append("-hold_jid")
            args.append(",".join(dependencies))
        return call("qsub", *args, input=script)

    def parse_queue_output(self, stdout):
        job_states = {}
        root = ElementTree.fromstring(stdout)
        for job in root.iter("job_list"):
            job_id = job.find("JB_job_number").text
            state = job.find("state").text

            # Guessing job state based on
            # https://gist.github.com/cmaureir/4fa2d34bc9a1bd194af1
            if "d" in state or "E" in state:
                job_state = Status.UNKNOWN
            elif "r" in state or "t" in state or "s" in state:
                job_state = Status.RUNNING
            else:
                job_state = Status.SUBMITTED
            job_states[job_id] = job_state
        return job_states

    def compile_script(self, target):
        option_str = "#$ {0}{1}"

        out = []
        out.append("#!/bin/bash")
        out.append("# Generated by: gwf")

        out.append(option_str.format("-N ", target.name))
        out.append("#$ -V")
        #out.append("#$ -w v")
        out.append("#$ -cwd")
        
        print(out)
        for option_name, option_value in target.options.items():
            # SGE wants per-core memory, but gwf wants total memory.
            if option_name == "memory":
                number = int(re.sub(r"[^0-9]+", "", option_value))
                unit = re.sub(r"[0-9]+", "", option_value)
                cores = target.options["cores"]
                option_value = "{}{}".format(number // cores, unit)
            out.append(option_str.format(self.option_flags[option_name], option_value))

        out.append(option_str.format("-o ", self.log_manager.stdout_path(target)))
        out.append(option_str.format("-e ", self.log_manager.stderr_path(target)))

        out.append("")
        out.append("cd {}".format(target.working_dir))
        out.append("export GWF_JOBID=$SGE_JOBID")
        out.append('export GWF_TARGET_NAME="{}"'.format(target.name))
        out.append("set -e")
        out.append("")
        out.append(ensure_trailing_newline(target.spec))
        print("\n".join(out))
        return "\n".join(out)