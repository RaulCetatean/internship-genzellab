Here are the steps needed in order to install and run Trodes and the rec_to_binaries python package from the LorenFrankLab. These steps were done using Ubuntu 20.04.2 LTS.  

Fo now, the structure of the files is still the one from the LorenFrankLab, but it might change.

## Installation Procedure

1. Download the Trodes toolbox (https://bitbucket.org/mkarlsso/trodes/downloads/). The version used is `Trodes 1-9-1`. The older version, when compared to newer versions, didn't give any problem during the installation. Then go into the folder and check if the file named `Trodes` has the correct permissions to be executed. This version of `Trodes` is not the most recent one, but it works.
2. Install the FTDI D2XX Driver (https://ftdichip.com/drivers/d2xx-drivers/). If using Windows, you can use the "setup executable" file for an easy installation. On this page (https://docs.spikegadgets.com/en/latest/basic/Install.html) there are more information about how to properly install Trodes for Windows, Linux and MacOS. 
3. Download and install miniconda (https://docs.conda.io/en/latest/miniconda.html) if conda is not installed.

4. First of all, create a conda enviroment and activate it if it's not. In my case I called it `sleep_scoring`.
```bash
conda create --name sleep_scoring
conda activate sleep_scoring
```
5. Add Trodes to the path and download `trodesnetwork`. Trodes documentation can be found here (https://docs.spikegadgets.com/en/latest/index.html). In my case, I downloaded `Trodes` in the Desktop.
```bash
export PATH=/home/lisa/Desktop/Trodes_1-9-1_Ubuntu1604/:$PATH
```
Now, to install trodesnetwork:
```bash
conda install pip
pip install trodesnetwork
```
Since in the new enviroment no libraries were previously installed, also `pip` is needed, and it is installed with `conda install`.

6. Install `rec_to_binaries` by using `conda install`. More information on `rec_to_binaries` and how to run the package can be found on the github page (https://github.com/LorenFrankLab/rec_to_binaries).
```bash
conda install -c franklab rec_to_binaries
```
Now everything that is needed should be installed.

## On Windows

The command for adding Trodes to the enviromental variables is different on Windows:
```bash
set PATH=%PATH%;C:\your\path\here\
```

## Python script `conversion_genzellab.py` - Usage

This python script can be run from the command line, and it does not require any arguments. As soon as the script runs, the program will open a GUI and will ask the user to choose 
the `.rec` file to be converted. After that,  the script will generate the name and the directories needed for `rec_to_binaries` to run and will convert the data from the `.rec` file into
a new folder, called `preprocessing`. The script at last will change the name of the generated folders and files back to the previous one. For now, the program is able to ask for input of one
`.rec` file, but it should be able to automate the whole process. 

### 1. File selection

The first part of the code asks for the .rec file to be converted and generates a new name for the file in order to be read by `rec_to_binaries`. It needs a particular name structure, as
well as folder structure, so the first thing the script does after getting the input is generating the new name and the needed folders. 



Now the script will start computing the various `.dat` files. The code is taken from the `rec_to_binaries` github page. For more information, please visit their github page (https://github.com/LorenFrankLab/rec_to_binaries)

```python
ogging.basicConfig(level='INFO', format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
                    
extract_trodes_rec_file(data_dir, animal, parallel_instances=4)
```
After the generation of the `.dat` files, the program will move the preprocessing folder and the original `.rec` file in the main folder, as well as changing the names of the files and removing unnecessary folders.

