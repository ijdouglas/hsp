import os
import pandas as pd
import csv
import math

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

exp200 = pd.read_csv("/mnt/c/Users/wkw/Desktop/experiment_200/exp200_full_filt_01-01-2021.csv")

frequency_dict = {}

for word in exp200["guess"].values:
    if word not in frequency_dict:
        frequency_dict[word] = 1
    elif word in frequency_dict:
        frequency_dict[word] +=1

#print(frequency_dict)

sort_freq = sorted(frequency_dict.items(),key=lambda x: x[1],reverse=True)
top50 = dict(sort_freq[0:51])
#print(top50.keys())

coca = {'stack':1116, 'put':500252, 'shake':24241, 'hold':178366, 'drive':120684, 'turn':219599, 'hit':175061, 'grab':29996, 'take':863956, 'twist':14335, 'press':138349, 'look':775881, 'pick':106309, 'move':230913, 'point':420320, 'touch':79821, 'talk':360768, 'spin':18844, 'give':462416, 'place':475252, 'saw':269368, 'hammer':12351, 'throw':61349, 'push':58799, 'play':286583, 'walk':122882, 'smell':40628, 'jump':42544, 'sleep':99970, 'sit':108786, 'lift':27554, 'roll':46181, 'squeeze':11367, 'build':96572, 'cut':190260, 'wear':60835, 'crawl':7139, 'get':1743680, 'rake':2342, 'show':407176, 'brush':19418, 'drop':68720, 'reach':88126, 'pull':72820, 'call':370931, 'stand':138342, 'flip':12906, 'bang':13650, 'tap':16095, 'hop':8274}

hsp_coca = [["verb","exp200","exp200_log","coca","coca_log"]]
for key in coca.keys():
    hsp_coca.append([key, top50[key],math.log(top50[key]),coca[key],math.log(coca[key])])

print(hsp_coca)
write_data(hsp_coca,"/mnt/c/Users/wkw/Documents/Lab/coca/hsp_coca.csv")