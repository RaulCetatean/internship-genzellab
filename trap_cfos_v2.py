import pandas as pd
import numpy as np
import math
import os

path = os.getcwd()

#cfos_path = '\\\\spinoza.science.ru.nl\\genzel\\Acquisitions Liz\\only_cFOS\\HMTRAP\\excel'
#trap_path = '\\\\spinoza.science.ru.nl\\genzel\\Acquisitions Liz\\HMTRAP_Ilastik\\excel'

#path to where the cFOS files and TRAP files are
cfos_path = 'C:\\Users\\Raul\\Desktop\\cFOS_excel'
trap_path = 'C:\\Users\\Raul\\Desktop\\TRAP_excel'

os.chdir(cfos_path)

files_cfos = [f.split('_') for f in os.listdir('.') if os.path.isfile(f)]


files_trap = [f.split('_') for f in os.listdir('.') if os.path.isfile(f)]


os.chdir(path) #so you get back at the path where this program is 

pairs = []
for x in files_cfos:
    for y in files_trap: 
        #if len(x) == 10 i can do this, if not I don't have to consider x[7]
        # So I have to check if len(x) = len(y) = 10, I will consider x[7]
        #if both have len = 9, I will not consider it 

        if x[1] == y[1] and x[4] == y[4] and x[6] == y[6] and x[7] == y[7]:

            t = ('_'.join(x),'_'.join(y))
            pairs.append(t)

#tuples will be: (cfos_file, trap_file)

#make directory for the storage of the new files. 
print(pairs)

os.mkdir(f'{path}\\comparison2')

os.chdir(f'{path}\\comparison2')

for tup in pairs:
    trap = pd.read_csv(f"{trap_path}\\{tup[1]}")
    cfos = pd.read_csv(f"{cfos_path}\\{tup[0]}")


    #consider only Label 1
    if cfos.shape[0] > 2:
        new_cfos = cfos[cfos["Predicted Class"] == "Label 1"]

        #in case also trap files have label 2
        #new_trap = trap[trap["Predicted Class"] == "Label 1"]

        l = [x for x in range(1,len(new_cfos["Center of the object_0"])+1)]

        new_cfos = new_cfos.set_index([pd.Index(l)])

        l = []
        i = 1
        x = 1

        while i < len(new_cfos["Center of the object_0"]):
            while x < len(trap["Center of the object_0"]):

                #computes the difference as an absolute value, if the difference is less than 20, it will be considered

                #error = abs(new_cfos["Center of the object_0"][i] - trap["Center of the object_0"][x])
                #error2 = abs(new_cfos["Center of the object_1"][i] - trap["Center of the object_1"][x])

                point1 = (new_cfos["Center of the object_0"][i], new_cfos["Center of the object_1"][i])
                point2 = (trap["Center of the object_0"][x], trap["Center of the object_1"][x])

                error = math.dist(point1, point2)

                #error = math.dist(new_cfos["Center of the object_0"][i], trap["Center of the object_0"][x])
                #error2 = math.dist(new_cfos["Center of the object_1"][i] - trap["Center of the object_1"][x])
                
                if error <= 20:
                #if error <= 20 and error2 <= 20:
                    id_cfos = new_cfos["object_id"][i] 
                    id_trap = trap["object_id"][x] 
                    c_zero_cfos = new_cfos["Center of the object_0"][i]
                    c_one_cfos = new_cfos["Center of the object_1"][i]
                    c_zero_trap = trap["Center of the object_0"][x]
                    c_one_trap = trap["Center of the object_0"][x]
                
                    #temporarily saved into a list that will be used to build the dataframe

                    tmp = [id_cfos, id_trap, c_zero_cfos, c_one_cfos, c_zero_trap, c_one_trap]
                    l.append(tmp)
            
            
                    x += 1
                x +=1
            i += 1
            x = 1

        df = pd.DataFrame(l,columns=["object_id_cFos","object_id_TRAP", "Center of the object_0_cFos","Center of the object_1_cFos",
                          "Center of the object_0_TRAP","Center of the object_1_TRAP"])

        #the names of these files is: mouse id, slice number, region of the image and corresponding hemisphere
        df.to_csv(f"{tup[0].split('_')[1]}_{tup[0].split('_')[4]}_{tup[0].split('_')[6]}_{tup[0].split('_')[7]}.csv", index=False)




