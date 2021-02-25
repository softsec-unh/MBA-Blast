# MBA-Blast Code and Dataset for USENIX Security'20

MBA-Blast is a tool for simplification of MBA expressions.

## Prerequisites: 
### Python 3.6
1. Z3 solver: `pip3 install z3-solver`
2. sympy: `pip3 install sympy`
### Python 2.7
1. Z3 solver: `pip install z3-solver`
2. sympy: `pip install sympy`
1. ast: `pip install ast`
2. astunparse: `pip install astparse`
### Arybo
Download it and install it by the [link](https://github.com/quarkslab/arybo/blob/master/README.rst).
### SSPAM
Download it and install it by the [link](https://github.com/quarkslab/sspam/blob/master/README.md).
### Syntia
The source code is from the [link](https://github.com/RUB-SysSec/syntia/blob/master/README.md), but we have download and refine it in the related folder "syntia".

## Structure
MBA-Blast's code is structured in following parts: dataset, simplifying MBA expression in the dataset, peer simplification tools.

### dataset
The files storing MBA expression.
1. Dataset 1 is dataset1.txt
2. Dataset 2 is dataset2_xbit.txt

### mba-simplifier
Simplifying the mba expressions by the method describing in the paper.
Functions to analyze and manipulate MBA expressions are in "tools" folder.


## How to use

1. Run MBA-Blast on Dataset1: `make mba-simplify-1`
2. Run MBA-Blast on 8-bit dataset: `make mba-simplify-8`
3. Run MBA-Blast on 16-bit dataset: `make mba-simplify-16`
4. Run MBA-Blast on 32-bit dataset: `make mba-simplify-32`
5. Run MBA-Blast on 64-bit dataset: `make mba-simplify-64`


## Peer tools to do simplification:
### Arybo
Run Arybo on Dataset1: `make arybo-mba`
### SSPAM   
Run SSPAM on Dataset1: `make sspam-mba`
### Syntia
Run Syntia on Dataset1: `program-synthesis-64`, `json-transformation-64`, `syntia-evaluation-64`.
Note that the main module `mcts_synthesis` is from the open source code of paper -- Syntia: Synthesizing the Semantics of Obfuscated Code.









