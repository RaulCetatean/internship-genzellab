import os
import logging
from rec_to_binaries import extract_trodes_rec_file
import shutil 
import re


script_dir = os.getcwd()
folders = []
rats = os.listdir()

            
for root, dirs, files in os.walk(script_dir):
    for name in files:
        if '.analog_Headstage_' in name:
            index = name.index('Headstage_')
            new_name = name.replace(name[index:index+len('Headstage_')], '')
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
