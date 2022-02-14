import os
from tkinter import filedialog as fd
import logging
from rec_to_binaries import extract_trodes_rec_file
import shutil 

# PRE-ANALYSIS PART

usr_input = fd.askopenfilename()
filename = usr_input.split('/')[-1]
file_prefix = filename[:-3]

date = filename.split('_')[5]
animal = filename.split('_')[0]
last_part = '_01_r1.rec'
data_dir = usr_input[:len(usr_input)-len(filename)]
os.chdir(data_dir)

# Now I need to generate the folders and change the name of the rec file
new_name = f"{date}_{animal}{last_part}"
if os.path.isfile(usr_input):    
    os.rename(os.path.join(data_dir, filename), os.path.join(data_dir, new_name))
    
# Now I have to put the renamed files in a folder that resembles the structure of lorenfrank directories

dirs_needed = f"{data_dir}{animal}/raw/{date}"
os.makedirs(dirs_needed)

# Move the .rec file in the directory and run rec_to_binaries to get the binary files

shutil.move(f"{data_dir}{new_name}", dirs_needed)

# ANAYSIS

logging.basicConfig(level='INFO', format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
                    
extract_trodes_rec_file(data_dir, animal, parallel_instances=4)

# POST-ANALYSIS

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
