from gwf import Workflow

gwf = Workflow()

def analysis(chrom):
	inputs = []
	outputs = [f'results_{chrom}.txt'] # changed
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment (this will differ from user to user!!!!!!)
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo analysing chromosome {chrom} > results_{chrom}.txt
	'''
	print(spec)
	return inputs, outputs, options, spec
	
chrms = range(1, 5)
# Submitting jobs per chromosome
for c in chrms:
	gwf.target_from_template(f"Analysis_chrm{c}", analysis(chrom=c))