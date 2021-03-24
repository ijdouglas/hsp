#csv to json
import csv
import json
import numpy as np
from itertools import combinations


source_file = list(csv.reader(open("new_90_dictionary.csv")))
combined_table = list(combinations(source_file,2)) #4005
np.random.shuffle(combined_table)
holder_array = []
temp_array = []
outer_shell = {}
x = 0
for i in range(len(combined_table)):
    if x == 150 and i <=3900:
        holder_array.append(temp_array)
        temp_array = []
        x = 0
    if i > 3900 and x == 104:
        holder_array.append(temp_array)
    temp_array.append(combined_table[i])
    temp_array.append([combined_table[i][1],combined_table[i][0]])
    x +=1
        

count = 0
for i in range(len(holder_array)):
    count += len(holder_array[i])


index = 1
for i in range(len(holder_array)):
    inner_array = holder_array[i]
    np.random.shuffle(inner_array)
    second_type = {"word_pair":[]}
    for row in inner_array:
        second_type["word_pair"].append(row)
    outer_shell[index] = second_type
    index +=1
with open("word_pairs_symmetric_combined.json","w") as fp:
    json.dump(outer_shell, fp)

#cannot move forward unless you enter