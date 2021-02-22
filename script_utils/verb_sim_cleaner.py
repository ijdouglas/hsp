import json
import pandas as pd
import os
import csv
import numpy as np
from collections import Counter

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)


dictionary_csv = list(csv.reader(open("hsp_voc.csv")))
word_dict = {}
for line in dictionary_csv:
    arr = line
    val = int(arr[1])
    word = arr[0]
    word_dict[word] = val

avg_dict = {}
demo = {"sex":[],"age":[]}
noreply = 0

#Walk_location is the folder where all of the experiment_data.csv files are stored, must be organized into subfolders for part1, part2, and part3 conditions
#ex. .../verb_similarity_data/part1_results/ with all the files from part1
#.../verb_similarity_data/part2_results/ with all the files from part2
#This part is important for later to differentiate the different conditions, since they have different lengths
#If you need to exclude certain files, add "ignore" to the beginning of the filename
walk_location = "/mnt/c/Users/wkw/Documents/Lab/verb_similarity_data/"
#Location where you want the files to be saved
target_dir = "/mnt/c/Users/wkw/Desktop/"

#Initializes the holder arrays
full_norm = [["id","wordA","wordB","sim_distance"]]
full_norm_id = [["id","wordA_id","wordB_id","sim_distance"]]
avg_norm = [["wordA","wordB","avg_distance"]]
avg_norm_id = [["wordA_id","wordB_id","avg_distance"]]

dir = walk_location
idd = 1
#Walks through the folder indicated before
for root, dirs, files in os.walk(dir):
    if "results" in root:
        for file in files:
            if "experiment_data.csv" in file and "ignore" not in file:
                temp = pd.read_csv(os.path.join(root,file)) #loads the given file
                #print(root,file)
                if "part1" in root: #Since the different conditions have different lengths, the program uses the upperbound part to know where to subset the data. Grabbed from root path
                    upperbound = 167
                elif "part2" or "part3" in root:
                    upperbound = 168
                for row in temp["responses"].iloc[3:upperbound]:
                    dictt = json.loads(row) #Loads the dictionary of their response
                    for key, value in dictt.items():
                        wordA = key[:key.find(",")]
                        wordB = key[key.find(",")+1:]
                        #print(file, key, value)
                        similarity = 7 - int(value) #changes similarity rating to distance rating
                        full_norm.append([idd,wordA, wordB, similarity])
                        full_norm_id.append([idd,word_dict[wordA], word_dict[wordB], similarity])
                        if key not in avg_dict:
                            avg_dict[key] = []
                        avg_dict[key].append(similarity)
                demostuff = temp["responses"].iloc[upperbound:].dropna() #gets demo data
                if len(demostuff) > 0:
                    sex = json.loads(demostuff.values[0])["Sex"]
                    age = json.loads(demostuff.values[1])["Age"]
                    demo["sex"].append(sex)
                    demo["age"].append(int(age))
                else:
                    noreply +=1
                idd +=1


#print(avg_dict)
for key, value in avg_dict.items(): #organizes an average based array
    wordA = key[:key.find(",")]
    wordB = key[key.find(",")+1:]
    avg_norm.append([wordA, wordB, np.average(value)])
    avg_norm_id.append([word_dict[wordA], word_dict[wordB], np.average(value)])

#Uncomment following section to save data. Need to update the date so that it doesn't overwrite.
'''
write_data(full_norm,target_dir+"verb_sim_basic_1-12.csv")
write_data(full_norm_id,target_dir+"verb_sim_basic_id_1-12.csv")
write_data(avg_norm,target_dir+"verb_sim_avg_1-12.csv")
write_data(avg_norm_id,target_dir+"verb_sim_avg_id_1-12.csv")
'''
#Demographic section
print("Demographic information")
print("people",len(demo["sex"])+noreply)
print(Counter(demo["sex"]))
print("avg age ", np.average(demo["age"]))
print("sd age ", np.std(demo["age"]))