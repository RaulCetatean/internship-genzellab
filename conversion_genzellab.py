import os
import logging
from rec_to_binaries import extract_trodes_rec_file
import shutil 
import re

'''The script should be in /mnt/genzel/Rat/HM/Rat_HM_Ephys/'''

usr_input = input("Please insert the number of the rat: ")
script_dir = os.getcwd()
folders = []
rats = os.listdir()
paths = []

for rat_n in rats:
    if f"Rat{usr_input}" in rat_n:
        new_dir = f"{script_dir}/{rat_n}"

            
for root, dirs, files in os.walk(new_dir):
    for name in files:
        if '.rec' == name[len(name)-4:]:
            rec = os.path.join(root, name)
            control = rec.split('/')[-1]
            control_dir = '/'.join(rec.split('/')[:-1])
            if control_dir not in paths:
                paths.append(control_dir)
                folders.append(rec)
            else:
                add_path = f"{rec[:-4]}"
                os.mkdir(add_path)
                shutil.move(rec, add_path)
                folders.append(f"{add_path}/{name}")
                
# From all the .rec files in the folder, I'm interested in only those with the date
# in the folder name. Index 7 is the date folder in our case

for f in folders:
    folder = f.split('/')[7]
    m = re.search(r'\d+$', folder)
    if m is not None:
        paths.append(f)


# PRE-ANALYSIS PART

def organization(rec_file):

    filename = rec_file.split('/')[-1]
    print(filename.split('_'))
    date = filename.split('_')[5]
    animal = filename.split('_')[0]
    last_part = '_01.rec'
    data_dir = rec_file[:len(rec_file)-len(filename)]
    os.chdir(data_dir)

    # Now I need to generate the folders and change the name of the rec file
    new_name = f"{date}_{animal}{last_part}"
    if os.path.isfile(rec_file):
        os.rename(os.path.join(data_dir, filename), os.path.join(data_dir, new_name))
    
    # Now I have to put the renamed files in a folder that resembles the structure of lorenfrank directories

    dirs_needed = f"{data_dir}{animal}/raw/{date}"
    os.makedirs(dirs_needed)

    # Move the .rec file in the directory and run rec_to_binaries to get the binary files

    shutil.move(f"{data_dir}{new_name}", dirs_needed)

    return filename, date, animal, data_dir

# ANALYSIS


def conversion(data_folder, animal):
    logging.basicConfig(level='INFO', format='%(asctime)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

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
                            

# POST-ANALYSIS

def cleanup(data_dir, animal, date, filename):
    generated_dir = f"{data_dir}{animal}/preprocessing/{date}"
    last_part = '_01.rec'
    new_name = f"{date}_{animal}{last_part}"
    file_prefix = filename[:-3]
  
    for root, dirs, files in os.walk(generated_dir):
        for dir_name in dirs:
            shutil.move(os.path.join(root,dir_name), data_dir)
    
    folders = next(os.walk(data_dir))[1]
      

            
    for ppdir in folders:
        for root, dirs, files in os.walk(os.path.join(data_dir, ppdir)):
            for name in files:
                old_name = name.replace(new_name[:-3], file_prefix)
                os.rename(os.path.join(root, name), os.path.join(root, old_name))
            
    for x in folders:
        if '.' in x:
            os.rename(os.path.join(data_dir, x), os.path.join(data_dir, f"{filename[:-4]}{x[x.index('.'):]}"))
            
    # Rename original file as before
    shutil.move(f"{data_dir}{animal}/raw/{date}/{filename}", data_dir)

    shutil.rmtree(f"{data_dir}{animal}")


# AUTOMATING IT FOR ALL REC FILES FOR A RAT

for recording in folders:
    control = recording.split('/')[-1]
    control_dir = '/'.join(recording.split('/')[:-1])
    if len(control.split('_')) >= 5:
        ls = next(os.walk(control_dir))[1]
        if f"{control[:-3]}analog" not in ls and f"{control[:-3]}LFP" not in ls:
            #this thing should check if folders were already generated. If not, it will start to work on it
            filename, date, animal, data_dir = organization(recording)
            conversion(data_dir, animal)
            cleanup(data_dir, animal, date, filename)
