# Author: Maria Izabel Cavassim Alves
# Date: March 11, 2022 
# Minimal workflow, introducing GWF

from gwf import Workflow

gwf = Workflow()


def first_step():
	inputs = []
	outputs = ['greetings.txt']
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo hello world > greetings.txt
	'''
	print(spec)
	return inputs, outputs, options, spec


## Estimating stats for each vcf file
gwf.target_from_template("Mytarget", first_step())