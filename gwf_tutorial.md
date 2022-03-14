---
title: "Using_gwf_hoffman_cluster"
author: "Maria Izabel Cavassim Alves"
date: "3/4/2022"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## GWF

[gwf](https://gwf.app/) is a flexible, pragmatic workflow tool for building and running large, scientific workflows. It runs on Python 3.5+ and is developed at the Bioinformatics Research Centre (BiRC), Aarhus University.

In this tutorial I assume that you have access to [Hoffman2](https://www.hoffman2.idre.ucla.edu/), and that you are already logged in. 

## Installation of GWF
The easiest way to install gwf is through conda, if you do not have conda installed yet in the cluster, please look at the document [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to find the instructions on how to install it. 

Once you have conda set in, then you can simply create a new project-specific environment (in this case we are naming it "myproject") and have *gwf* installed inside of the new environment:

```{bash}
conda config --add channels gwforg
conda create -n myproject2 python=3.9 gwf
conda activate myproject2
```

To see if you successfully installed gwf try running it:
```{bash}
gwf
```

## Running GWF within Hoffman 
Because the cluster at UCLA uses the SGE grid engine but the tool was developed to run in a slurm engine by default, we need to make sure some modifications in the config files are made.

Go to the directory that the gwf folder is placed, in mine is placed in the following directory:

```{bash}
/u/home/m/mica20/miniconda3/envs/myproject2/lib/python3.9/site-packages/gwf/backends
```
I have miniconda installed in the Hoffman, and it is used as my base environment. 

To find out where your conda base environment is located you can try the following:

```{bash}
conda info | grep -i 'base environment'
```

And now in the file *sge.py* replace it with the one added [here](https://github.com/izabelcavassim/gwf_UCLA_cluster/blob/master/sge.py) in this repository.

So basically now we can run gwf with the settings of the Hoffman cluster. 

To get you started with the utilities of using gwf, I will give a tiny example so to see if it works.

I will be somewhat following the tutorial found [here](https://gwf.app/guide/tutorial/#a-minimal-workflow): a minimal workflow to run gwf.

Let's say we wanna submit a job to the cluster, and the simple task we wanna submit as a job is the creation of a text file with something written in it, such as "hello world".

To get started we must define a workflow file containing a workflow to which we can add targets. Unless gwf is told otherwise it assumes that the workflow file is called *workflow.py* and that the workflow is called gwf:

so create an empty file called workflow.py in your current directory by typing:

```{bash}
touch workflow.py
```

And then inside of this file paste (maybe through emacs or any text editor) the following set of commands:

```{python}
from gwf import Workflow

gwf = Workflow()

def first_step():
	inputs = []
	outputs = []
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment (this will differ from user to user!!!!!!)
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo hello world
	'''
	print(spec)
	return inputs, outputs, options, spec

## Submitting your first step
gwf.target_from_template("Mytarget", first_step())
```

In the example above we define a workflow and then add a target called *MyTarget*. A target is a single unit of computation that uses zero or more files (inputs) and produces zero or more files (outputs).

We have also set some properties about the job: 
- the amount of *memory* we wanna set for this specific job
- the number of cores
- the walltime

These specifications will of course change with demand, so you need to bare that in mind.

The target defined above does not use any files and doesn’t produce any files either. However, it does run a single command (**echo hello world**), but the output of the command is thrown away. Let’s fix that! Change the target definition to this:

```{python}
from gwf import Workflow

gwf = Workflow()

def first_step():
	inputs = []
	outputs = ['greetings.txt']  # changed
	options = {
	'memory':'1g',
	'cores':1,
	'walltime':'00:00:10',
	}
	# Here we need to activate our conda environment (this will differ from user to user!!!!!!)
	spec = f'''
        source "/u/home/m/mica20/miniconda3/etc/profile.d/conda.sh"
        conda activate myproject2

	echo hello world
	'''
	print(spec)
	return inputs, outputs, options, spec

## Submitting your first step
gwf.target_from_template("Mytarget", first_step())
```

This tells gwf that the target will create a file called greetings.txt when it is run. However, the target does not actually create the file yet. Let’s fix that too:

```{python}
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

## Submitting your first step
gwf.target_from_template("Mytarget", first_step())
```
There you go! We have now declared a workflow with one target and that target creates the file greetings.txt with the line hello world in it. Now let’s try to run our workflow…

```{python}
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

## Submitting your first step
gwf.target_from_template("Mytarget", first_step())
```

Since we are running this script on the cluster we need to set a backend, to do so we type in the terminal

```{bash}
gwf config set backend sge
```

Now to run the workflow, we just need to type:

```{bash}
gwf run
```
By default gwf assumes that the the workflow file is called *workflow.py* and that the workflow is called gwf.
But if you wanna instead call your workflow *something_else.py*, then you can just run with the flag *-f* as:

```{bash}
gwf -f something_else.py run
```

To check the status of your workflow.py you can type the following:

```{bash}
gwf status
```
What do you see?
I first see:

```{bash}
Mytarget    submitted     100.00% [0/0/0/1]
```

And then I see:
```{bash}
Mytarget    completed     100.00% [0/0/0/1]
```

## Defining Targets with Dependencies

Targets in gwf represent isolated units of work. However, we can declare dependencies between targets to construct complex workflows. A target B that depends on a target A will only run when A has been run successfully (that is, if all of the output files of A exist).

In gwf, dependencies are declared through file dependencies. This is best understood through an example ([workflow_dependencies.py](https://github.com/izabelcavassim/gwf_UCLA_cluster/blob/master/workflow_dependencies.py)):

```{python}
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
```

Let's now run this specific workflow:

What do you see when you run:

```{bash}
gwf -f workflow_dependencies.py status
```

I see:
```{bash}
Mytarget1    completed     100.00% [0/0/0/1]
Mytarget2    shouldrun      50.00% [1/0/0/1]
```
Mytarget2 is 50% complete because we have already produced the file 'greetings.txt'. 
Now try to run your job:

```{bash}
gwf -f workflow_dependencies.py run
```

## Submitting multiple jobs by looping through a function

OK, now that we already have a good idea of how gwf works, let's try a bit more complex pipelines.
Let's say we need to compute a specific measure for each chromosome of a given genome.
To make it simple, I will keep using the same structure as above and build from there.
And I will save this workflow as [workflow_chromosomes.py](https://github.com/izabelcavassim/gwf_UCLA_cluster/blob/master/workflow_chromosomes.py)

```{python}
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
```

What do you see if you run:
```{bash}
gwf -f workflow_chromosomes.py status
```
I see:
```{bash}
Analysis_chrm1    shouldrun       0.00% [1/0/0/0]
Analysis_chrm2    shouldrun       0.00% [1/0/0/0]
Analysis_chrm3    shouldrun       0.00% [1/0/0/0]
Analysis_chrm4    shouldrun       0.00% [1/0/0/0]
```
Now try to run these analyses, what results do you get?

```{bash}
gwf -f workflow_chromosomes.py run
```

## Troubleshooting

Sometimes your job won't run, and it is useful to investigate why it was unable to run.
In order to troubleshoot you jobs under the gwf workflow, you can look at the logs of each target.

To do so you can type:

```{bash}
gwf -f workflow_chromosomes.py logs -e Analysis_chrm1 [name of the Target]
```

As you can imagine by now, the sky is the limit in terms of what jobs one can submit with this tool. 
I hope you use it wisely :)

if you get any problems with utf8 then type the following on terminal
```{bash}
export LC_ALL=aa_DJ.utf8
```
