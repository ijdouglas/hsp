from itertools import combinations
import csv
import os
import json
import nltk
from nltk.corpus import wordnet as wn
import random
import numpy as np


#synset = wn.synsets("Travel")
#print(str(synset[0].examples()))
targets = ["eat","stack","knock","shake","fit","drive","cut","put","turn","fall","hold"]
targ_num = {"eat":1,"stack":2,"knock":3,"shake":4,"fit":5,"drive":6,"cut":7,"put":8,"turn":9,"fall":10,"hold":11}
target_dict = {"eat":wn.synset("eat.v.01"),"stack":wn.synset("stack.v.02"),"knock":wn.synset("knock.v.01"),"shake":wn.synset("shake.v.01"),"fit":wn.synset("fit.v.02"),"drive":wn.synset("drive.v.01"),"cut":wn.synset("cut.v.01"),"put":wn.synset("put.v.01"),"turn":wn.synset("turn.v.04"),"fall":wn.synset("fall.v.01"),"hold":wn.synset("hold.v.02")}



temp = list(csv.reader(open("dictionary.csv")))
'''
temp2 = list(csv.reader(open("dictionary_mod.csv")))
tempar = []
rand_distances = []
for row in temp2:
    tempar.append(row[0])
maxval = len(tempar)-1
i = 0
while i < 45:
    a = random.randint(0,maxval)
    print(tempar[a])
    b = random.randint(0,maxval)
    print(tempar[b])
    if a != b and len(wn.synsets(tempar[a],pos=wn.VERB))!=0 and len(wn.synsets(tempar[b],pos=wn.VERB))!=0:
        word1 = wn.synsets(tempar[a],pos=wn.VERB)[0]
        word2 = wn.synsets(tempar[b],pos=wn.VERB)[0]
        rand_distances.append(1/(word1.path_similarity(word2)))
        i+=1
#print(tempar)
print(rand_distances)
print(np.mean(rand_distances))
holder = []

for item in targets:
    print(item)
    for row in temp:
        if item != row[0]:
            if len(wn.synsets(row[0],pos=wn.VERB)) >= 3:
                a = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[0])
                b = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[1])
                c = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[2])
                holder.append([targ_num[item],row[1], (a+b+c)/3])
            elif len(wn.synsets(row[0],pos=wn.VERB))==2:
                a = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[0])
                b = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[1])
                holder.append([targ_num[item],row[1], (a+b)/2])
            elif len(wn.synsets(row[0],pos=wn.VERB))==1:
                a = target_dict[item].path_similarity(wn.synsets(row[0],pos=wn.VERB)[0])
                holder.append([targ_num[item],row[1], a])
                #holder.append([item, target_dict[item],row[0],wn.synsets(row[0],pos=wn.VERB)[0],wn.path_similarity(target_dict[item],wn.synsets(row[0],pos=wn.VERB)[0])])


    print("done")

#with open("targeted_combo_wup_values_1_16.csv","w") as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerows(holder)
'''

with open("updated_dictionary.csv","r",newline='') as infile:
    reader = csv.reader(infile)
    id_dict = {rows[0]:rows[1] for rows in reader}
temp = list(csv.reader(open("mds_sauce.csv")))

combo = list(combinations(temp, 2))
combos = []
for row in temp:
    #combos.append([row[0],row[0]])
    combos.append([id_dict[row[0]],id_dict[row[0]]])

for row in combo:
    #combos.append([row[0][0],row[1][0]])
    combos.append([id_dict[row[0][0]],id_dict[row[1][0]]])

with open("mds_id_combo.csv","w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(combos)

'''
new_dict = []
combodict = list(csv.reader(open("dict_combo.csv")))
for row in combodict:
    if len(wn.synsets(row[1],pos=wn.VERB)) != 0 and len(wn.synsets(row[0],pos=wn.VERB)) != 0:
        print(row[1])
        print(wn.synsets(row[1],pos=wn.VERB))
        print(wn.synsets(row[1],pos=wn.VERB)[0])
        print()
        #word1 = wn.synset(str(row[0])+".v.01")
        word1 = wn.synsets(row[0],pos=wn.VERB)[0]
        #word2 = wn.synset(str(row[1])+".v.01")
        word2 = wn.synsets(row[1],pos=wn.VERB)[0]
        new_dict.append([row[0],wn.synsets(row[0],pos=wn.VERB)[0],row[1],wn.synsets(row[1],pos=wn.VERB)[0],wn.path_similarity(word1,word2)])
    else:
        new_dict.append([row[0],"",row[1],"","pos error"])
        

with open("dict_combo_with_values.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(new_dict)
'''