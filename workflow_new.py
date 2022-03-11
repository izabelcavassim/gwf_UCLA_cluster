
# Workflow for the pyrho analyses of the wolves data

from gwf import Workflow
import glob
import os
import os.path
import itertools
#import pandas as pd

gwf = Workflow()


def test():
	inputs = []
	outputs = ['greetings.txt']
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo hello world > greetings.txt
	'''
	print(spec)
	return inputs, outputs, options, spec


## Estimating stats for each vcf file
gwf.target_from_template("Mytarget", test())
