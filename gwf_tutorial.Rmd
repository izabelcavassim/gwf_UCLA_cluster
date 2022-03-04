---
title: "Using_gwf_smcpp"
author: "Maria Izabel Cavassim Alves"
date: "3/4/2022"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

## GWF

gwf (https://gwf.app/) is a flexible, pragmatic workflow tool for building and running large, scientific workflows. It runs on Python 3.5+ and is developed at the Bioinformatics Research Centre (BiRC), Aarhus University.

## Installation of GWF
```{bash}
conda config --add channels gwforg
conda create -n myproject python=3.5 gwf
conda activate myproject
```

## Running GWF within Hoffman 
Because the cluster at UCLA uses the SGE grid engine but the tool was developed to run in a slurm engine, we need to make some modifications in the config files. 

Go to the directory that the gwf folder is placed, in mine is placed in the following directory
```{bash}
/u/home/m/mica20/miniconda3/envs/myproject/lib/python3.5/site-packages/gwf/backends
```

And now in the file *sge.py* replace it with the one added [here](bla) in this repository.

So basically now we can run gwf with Hoffman. 

To get you started with the utilities of using gwf, I will give a tiny example so to see if it works.

I will be following the tutorial found [here]().

Let's say we wanna submit a job to the cluster, and the simple task we wanna submit is to produce a text file with 
something written in it, such as "Hello world".

To get started we must define a workflow file containing a workflow to which we can add targets. Unless gwf is told otherwise it assumes that the workflow file is called *workflow.py* and that the workflow is called gwf:

so create an empty file called workflow.py in your current directory by typing:

```{bash}
touch workflow.py
```

And then inside of this file paste the following command:

```{python}
from gwf import Workflow

gwf = Workflow()

gwf.target('MyTarget', inputs=[], outputs=[]) << """
echo hello world
"""
```

In the example above we define a workflow and then add a target called MyTarget. A target is a single unit of computation that uses zero or more files (inputs) and produces zero or more files (outputs).

The target defined above does not use any files and doesn’t produce any files either. However, it does run a single command (echo hello world), but the output of the command is thrown away. Let’s fix that! Change the target definition to this:

```{python}
gwf.target('MyTarget', inputs=[], outputs=['greeting.txt']) << """
echo hello world
"""
```

This tells gwf that the target will create a file called greeting.txt when it is run. However, the target does not actually create the file yet. Let’s fix that too:

```{python}
gwf.target('MyTarget', inputs=[], outputs=['greeting.txt']) << """
echo hello world > greeting.txt
"""
```
There you go! We have now declared a workflow with one target and that target creates the file greeting.txt with the line hello world in it. Now let’s try to run our workflow…

```{python}
from gwf import Workflow

gwf = Workflow()

gwf.target('MyTarget', inputs=[], outputs=['greeting.txt']) << """
echo hello world > greeting.txt
"""
```

Since we are running this script on the cluster we need to set a backend, to do so we type in the terminal

```{bash}
gwf config set backend sge
```


if you get any problems with utf8 then type the following on terminal
```{bash}
export LC_ALL=aa_DJ.utf8
```