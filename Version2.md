Here are the steps needed in order to install and run Trodes and the rec_to_binaries python package from the LorenFrankLab. These steps were done using Ubuntu 20.04.2 LTS.  

Fo now, the structure of the files is still the one from the LorenFrankLab, but it might change.

## Installation

1. Download and run the latest version of the Trodes toolbox (https://bitbucket.org/mkarlsso/trodes/downloads/). The version used is `Trodes 1-9-1`. Download `Trodes_1-9-1_Ubuntu1604.tar.gz` and uncompress it. Then go into the folder and check if the file named `Trodes` has the correct permissions to be executed. This version of `Trodes` is not the most recent one, but it works.
2. Download and install miniconda (https://docs.conda.io/en/latest/miniconda.html) if conda is not installed.

## Procedure

1. First of all, create a conda enviroment and activate it if it is not. In my case I called it`sleep_scoring`.
```bash
conda create --name sleep_scoring
conda activate sleep_scoring
```
2. Add Trodes to the path and download `trodesnetwork`. Trodes documentation can be found here (https://docs.spikegadgets.com/en/latest/index.html). In my case, I downloaded `Trodes` in the Desktop.
```bash
export PATH=/home/lisa/Desktop/Trodes_1-9-1_Ubuntu1604/:$PATH
```
I found this command to work better than the one found on the LorenFrankLab github page (https://github.com/LorenFrankLab/rec_to_binaries).
Now, to install trodesnetwork:
```bash
conda install pip
pip install trodesnetwork
```
Since in the new enviroment no libraries were previously installed, also `pip` is needed, and it is installed with `conda install`.

3. Install `rec_to_binaries` by using `conda install`. More information on `rec_to_binaries` and how to run the package can be found on the github page (https://github.com/LorenFrankLab/rec_to_binaries).
```bash
conda install -c franklab rec_to_binaries
```
Now everything that is needed should be installed.

## Python script `conversion_genzellab.py` - Usage

This python script can be run from the command line, and it does not require any arguments. As soon as the script runs, the program will open a GUI and will ask the user to choose 
the `.rec` file to be converted. After that,  the script will generate the name and the directories needed for `rec_to_binaries` to run and will convert the data from the `.rec` file into
a new folder, called `preprocessing`. The script at last will change the name of the generated folders and files back to the previous one. For now, the program is able to ask for input of one
`.rec` file, but it should be able to automate the whole process. 

### 1. File selection and folder generation

The first part of the code asks for the .rec file to be converted and generates a new name for the file in order to be read by `rec_to_binaries`. It needs a particular name structure, as
well as folder structure, so the first thing the script does after getting the input is generating the new name and the needed folders. 

```python
usr_input = fd.askopenfilename()
filename = usr_input.split('/')[-1]
file_prefix = filename[:-3]

date = filename.split('_')[5]
animal = filename.split('_')[0]
last_part = '_01_r1.rec'
data_dir = usr_input[:len(usr_input)-len(filename)]
os.chdir(data_dir)
new_name = f"{date}_{animal}{last_part}"
if os.path.isfile(usr_input):    
    os.rename(os.path.join(data_dir, filename), os.path.join(data_dir, new_name))

dirs_needed = f"{data_dir}{animal}/raw/{date}"
os.makedirs(dirs_needed)

shutil.move(f"{data_dir}{new_name}", dirs_needed)
```

Now the script will start computing the various `.dat` files. The code is taken from the `rec_to_binaries` github page. For more information, please visit their github page (https://github.com/LorenFrankLab/rec_to_binaries)

```python
ogging.basicConfig(level='INFO', format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
                    
extract_trodes_rec_file(data_dir, animal, parallel_instances=4)
```
After the generation of the `.dat` files, the program will move the preprocessing folder and the original `.rec` file in the main folder, as well as changing the names of the files and removing unnecessary folders.
```python
generated_dir = f"{data_dir}{animal}/preprocessing/{date}"

for root, dirs, files in os.walk(generated_dir):
    for name in files:
        old_name = name.replace(new_name[:-3], file_prefix)
        os.rename(os.path.join(root, name), os.path.join(root, old_name))

    # Change also names of the generated folders
    for dir_name in dirs:
        inv = dir_name.index('.')
        preprocess_dir = dir_name.replace(new_name[:-3], file_prefix)
        os.rename(os.path.join(root, dir_name), os.path.join(root, preprocess_dir))

# Rename original file as before
shutil.move(f"{data_dir}{animal}/raw/{date}/{new_name}", data_dir)

if os.path.isfile(f"{data_dir}{new_name}"):
    os.rename(os.path.join(data_dir, new_name), os.path.join(data_dir, filename))

# Move preprocessing folder and delete rat/raw/date...

shutil.move(f"{generated_dir}", f"{data_dir}")
shutil.rmtree(f"{data_dir}{animal}")
```
