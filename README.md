Here are the steps needed in order to install and run Trodes and the rec_to_binaries python package from the LorenFrankLab. These steps were done using Ubuntu 20.04.2 LTS. More detailed information on the procedure done with the Windows operating system are also written below. 

## Installation Procedure

1. Download the Trodes toolbox (https://bitbucket.org/mkarlsso/trodes/downloads/). The version used is `Trodes 1-9-1`. The older version, when compared to newer versions, didn't give any problem during the installation. Then go into the folder and check if the file named `Trodes` has the correct permissions to be executed. This version of `Trodes` is not the most recent one, but it works.
2. Install the FTDI D2XX Driver (https://ftdichip.com/drivers/d2xx-drivers/). If using Windows, you can use the "setup executable" file for an easy installation. On this page (https://docs.spikegadgets.com/en/latest/basic/Install.html) there are more information about how to properly install Trodes for Windows, Linux and MacOS. 
3. Download and install miniconda (https://docs.conda.io/en/latest/miniconda.html) if conda is not installed.

4. First of all, create a conda enviroment and activate it if it's not. In my case I called it `sleep_scoring`.
```bash
conda create --name sleep_scoring
conda activate sleep_scoring
```

5. Install `rec_to_binaries` by using `conda install`. More information on `rec_to_binaries` and how to run the package can be found on the github page (https://github.com/LorenFrankLab/rec_to_binaries).
```bash
conda install -c franklab rec_to_binaries
```
6. Add Trodes to the path. Trodes documentation can be found here (https://docs.spikegadgets.com/en/latest/index.html).

### Add Trodes to Path On Linux

```bash
export PATH=/path/to/Trodes/folder/:$PATH
```

### Add Trodes to Path On Windows

On Windows, you can add Trodes to the path in the following way: in the settings, look for `Edit environment variables for your account`. A new window should appear. In the user variables, double-click on the Path variable and another window will pop up. From there, click on `Browse...` and add the path to Trodes.

Now everything that is needed should be installed.

## Python script `conversion_genzellab.py` - Usage

This python script can be run from the command line, and it does not require any arguments. As soon as the script runs, the program will ask the user to choose  the the number of the animal for which all the`.rec` file will be converted. After that,  the script will generate the name and the directories needed for `rec_to_binaries` to run and will convert the data from the `.rec` file into a new folder, called `preprocessing`. The script at last will change the name of the generated folders and files back to the previous one. The process is automated for all the `.rec` files corresponding to the specific animal chosen.

### 1. File selection

As soon as the python script runs, it will ask for an input. The input should be an integer number representing the animal. Then the program will start converting all the `.rec` files associated with the selected animal. 

### 2. File conversion

The script right now is only extracting the analog and LFP files, however there are different parameters that can be modified.
```bash
lfp_export_args = ('-highpass', '0',
                                   '-lowpass', '400',
                                   '-interp', '0',
                                   '-userefs', '0',
                                   '-outputrate', '1000')

    extract_trodes_rec_file(data_folder, animal,
                            extract_analog=True,
                            extract_spikes=False,
                            extract_lfps=True,
                            extract_dio=False,
                            extract_time=False,
                            extract_mda=False,
                            lfp_export_args=lfp_export_args)
```

### 3. Running the Python script

In order to run the script, you just have to call it from the folder the script and the animal folders are. In this case, the script in order to run needs to be in `/mnt/genzel/Rat/HM/Rat_HM_Ephys/`.

```bash
python conversion_genzellab.py
```
In order to time the program, just add `time` before running the program.
```bash
time python conversion_genzellab.py
```
## Manual scoring Matlab script

Follow the first two steps of the `Installation procedure` section.
In order to use the TrodesToMatlab toolbox, it is best to download the source code from bitbucket. The source code contains a folder named `TrodesToMatlab`, which is needed by the script to run properly. 
```bash
git clone https://bitbucket.org/mkarlsso/trodes.git
```
Add to the Matlab path the following folders:
- trodes
- TrodesToMatlab
- TrodesToNeuroQuery

The Matlab file from this repository can be downloaded by cloning the repository, or download directly the 'ZIP' folder.
```bash
git clone https://github.com/RaulCetatean/internship-genzellab.git
```
Now, a few more files are needed for the manual scoring. These files can be found here: https://github.com/AbdelRayan/sleep_scoring 
```bash
git clone https://github.com/AbdelRayan/sleep_scoring.git
```
For the program to run properly, these files need to be inside the same directory as the `.rec` file and the analog and LFP folders:
- TheStateEditor.m
- ExtractLFPBinaryFilesAbdel.m
- manualscoring_script_Raul.m

`manualscoring_script_Raul.m` starts by asking the `rec` file to be analyzed. Then it will look for LFP and analog folders in the directory of the file; if these folders are found, the script will ask for the tetrode and channel numbers directly. If the folders are not present, it will start computing the movement data and the LFP files, and then it will ask for the tetrode and channel numbers. 
