#!/bin/bash
ulimit -c unlimited
ulimit -s unlimited

source /home/${USER}/.bashrc
source /home/${USER}/miniconda3/bin/activate foams

python3 main.py
python3 correlations.py
