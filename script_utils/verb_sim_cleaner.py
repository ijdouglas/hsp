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

walk_location = "/mnt/c/Users/wkw/Documents/Lab/verb_similarity_data/"
target_dir = "/mnt/c/Users/wkw/Desktop/"


full_norm = [["id","wordA","wordB","sim_distance"]]
full_norm_id = [["id","wordA_id","wordB_id","sim_distance"]]
avg_norm = [["wordA","wordB","avg_distance"]]
avg_norm_id = [["wordA_id","wordB_id","avg_distance"]]

dir = walk_location
idd = 1
for root, dirs, files in os.walk(dir):
    if "results" in root:
        for file in files:
            if "experiment_data.csv" in file and "ignore" not in file:
                temp = pd.read_csv(os.path.join(root,file))
                #print(root,file)
                if "part1" in root:
                    upperbound = 167
                elif "part2" or "part3" in root:
                    upperbound = 168
                for row in temp["responses"].iloc[3:upperbound]:
                    dictt = json.loads(row)
                    for key, value in dictt.items():
                        wordA = key[:key.find(",")]
                        wordB = key[key.find(",")+1:]
                        #print(file, key, value)
                        similarity = 7 - int(value)
                        full_norm.append([idd,wordA, wordB, similarity])
                        full_norm_id.append([idd,word_dict[wordA], word_dict[wordB], similarity])
                        if key not in avg_dict:
                            avg_dict[key] = []
                        avg_dict[key].append(similarity)
                demostuff = temp["responses"].iloc[upperbound:].dropna()
                if len(demostuff) > 0:
                    sex = json.loads(demostuff.values[0])["Sex"]
                    age = json.loads(demostuff.values[1])["Age"]
                    demo["sex"].append(sex)
                    demo["age"].append(int(age))
                else:
                    noreply +=1
                idd +=1


#print(avg_dict)
for key, value in avg_dict.items():
    wordA = key[:key.find(",")]
    wordB = key[key.find(",")+1:]
    avg_norm.append([wordA, wordB, np.average(value)])
    avg_norm_id.append([word_dict[wordA], word_dict[wordB], np.average(value)])

'''
write_data(full_norm,target_dir+"verb_sim_basic_1-12.csv")
write_data(full_norm_id,target_dir+"verb_sim_basic_id_1-12.csv")
write_data(avg_norm,target_dir+"verb_sim_avg_1-12.csv")
write_data(avg_norm_id,target_dir+"verb_sim_avg_id_1-12.csv")
'''

print("Demographic information")
print("people",len(demo["sex"])+noreply)
print(Counter(demo["sex"]))
print("avg age ", np.average(demo["age"]))
print("sd age ", np.std(demo["age"]))