# internship-genzellab
First draft of making a github repository to store what I did during my internship

Here are the steps needed in order to install and run Trodes and the rec_to_binaries python package from the LorenFrankLab. These steps were done using Ubuntu 20.04.2 LTS.  

Fo now, the structure of the files is still the one from the LorenFrankLab, but it might change.

## Installation

1. Download and run the latest version of the Trodes toolbox (https://bitbucket.org/mkarlsso/trodes/downloads/). The version used in my case and in the examples is `Trodes_2-2-3_Ubuntu1804`. 
2. Download and install miniconda (https://docs.conda.io/en/latest/miniconda.html) if conda is not installed.

## Procedure

1. First of all, create a conda enviroment and activate it if it is not. In my case I called it`sleep_scoring`.
```bash
conda create --name sleep_scoring
conda activate sleep_scoring
```
2. Add Trodes to the path and download `trodesnetwork`. Trodes documentation can be found here (https://docs.spikegadgets.com/en/latest/index.html). In my case, I downloaded `Trodes` in the Desktop.
```bash
export PATH=/home/lisa/Desktop/Trodes_2-2-3_Ubuntu1804/:$PATH
```
I found this command to work better than the one found on the LorenFrankLab github page (https://github.com/LorenFrankLab/rec_to_binaries).
Now, to install trodesnetwork:
```bash
conda install pip
pip install trodesnetwork
```
Since in the new enviroment no libraries were previously installed, also `pip` is needed, and it is installed with `conda install`.
