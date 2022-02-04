# internship-genzellab

## Part 1: Install Trodes and run `rec_to_binaries`

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

export PATH=/home/usr/path/to/trodes/:$PATH
```
I found this command to work better than the one found on the LorenFrankLab github page (https://github.com/LorenFrankLab/rec_to_binaries).
Now, to install trodesnetwork:
```bash
conda install pip
pip install trodesnetwork
```
Since in the new enviroment no libraries were previously installed, also `pip` is needed, and it is installed with `conda install`.

3. Install `rec_to_binaries` by using `conda install`. More information on `rec_to_binaries and how to run the package can be found on the github page (https://github.com/LorenFrankLab/rec_to_binaries).
```bash
conda install -c franklab rec_to_binaries
```
Now everything that is needed should be installed.

As of rigth now, there are a few things that need some changes in order for the program to run correctly.

## Challenges/Problems

### Challenge 1

First of all, in order to run the program correctly, the files and the folders need to be organized in the same format as the Loren Frank Lab. Examples are present on their github page, already linked above. 

### Problem 1 (Already solved by the authors)

The second problem, at the moment of writting, was corrected, so when you download the `rec_to_binaries` should work fine if the `.rec` files are in the proper folders. It should be noted, however, that it might still be useful to write the passages I did to solve this problem. 
With the previous version, when you tried to run the code using the `rec_to_binaries` package to convert the `.rec` files, the LFP files were not generated. This was due to the fact that the arguments given to the function `trodesexport -lfp` were not updated to the latest version, and in order to fix this, the code of the `rec_to_binaries` had to be changed. 

The file that needs to be modified was installed with the `conda install` command, and it can be found in the `miniconda` folder. Here I will put an example. `sleep_scoring` is the enviroment I'm working on, and `python3.9` is the version used in this case.
```bash
~/miniconda3/envs/sleep_scoring/lib/python3.9/site_packages/rec_to_binaries
```

Inside the `rec_to_binaries` folder, open the `core.py` file and find the `lfp_export_args` variables. They looked like this. Since the version of Trodes used was 2-2-3 the only part that needs to change is the `lfp_export_args` after the `else` function.

```python
if extract_lfps:
        logger.info('Extracting LFP...')
        if lfp_export_args is None:
            if trodes_version[0] < 2.0:
                lfp_export_args = ('-highpass', '0',
                                   '-lowpass', '400',
                                   '-interp', '0',
                                   '-userefs', '0',
                                   '-outputrate', '1500')
            else:
                lfp_export_args = ('-highpass', '0',
                                   '-lowpass', '400',
                                   '-interp', '0',
                                   '-userefs', '0',
                                   'sortingmode', '0',
                                   '-outputrate', '1500')
```

However, according to the Trodes documentation, most of the flags used by `trodesexport -lfp` had to be changed. Here below there is the correct `lfp_export_args`.

```python
if extract_lfps:
        logger.info('Extracting LFP...')
        if lfp_export_args is None:
            if trodes_version[0] < 2.0:
                lfp_export_args = ('-highpass', '0',
                                   '-lowpass', '400',
                                   '-interp', '0',
                                   '-userefs', '0',
                                   '-outputrate', '1500')
            else:
                lfp_export_args = ('-lfphighpass', '0',
                                   '-lfplowpass', '400',
                                   '-interp', '0',
                                   '-uselfprefs', '0',
                                   'sortingmode', '0',
                                   '-outputrate', '1500')
```

Note that you have access to the code so you can just change any parameter according to what you need.
