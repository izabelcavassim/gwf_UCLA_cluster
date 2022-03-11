from gwf import Workflow

gwf = Workflow()

def first_step():
	inputs = []
	outputs = ['greetings.txt'] # changed
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment (this will differ from user to user!!!!!!)
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo hello world > greetings.txt
	'''
	print(spec)
	return inputs, outputs, options, spec
	
def second_step():
	inputs = ['greetings.txt']
	outputs = ['farewell.txt'] # changed
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment (this will differ from user to user!!!!!!)
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo goodbye > farewell.txt
	'''
	print(spec)
	return inputs, outputs, options, spec

## Submitting your first step
gwf.target_from_template("Mytarget1", first_step())
gwf.target_from_template("Mytarget2", second_step())