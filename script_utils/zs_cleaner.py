import json
import pandas as pd
import os
import csv
import numpy as np
from collections import Counter

obj_mappings = {'2050-600.jpg': 'a1', '2035-600.jpg': 'a2', '2060-600.jpg': 'a3', '2019-600.jpg': 'a4', '2026-600.jpg': 'a5', '2009-600.jpg': 'a6', '2030-600.jpg': 'b1', '2006-600.jpg': 'b2', '2012-600.jpg': 'b3', '2016 600dpi.jpg': 'b4', '2024-600.jpg': 'b5', '2047-600.jpg': 'b6', '2003-600.jpg': 'c1', '2015-600.jpg': 'c2', '2033-600.jpg': 'c3', '2056-600.jpg': 'c4', '2025-600.jpg': 'c5', '2029-600.jpg': 'c6', '2055-600.jpg': 'd1', '2040-600.jpg': 'd2', '2051-600.jpg': 'd3', '2023-600.jpg': 'd4', '2014-600.jpg': 'd5', '2034-600.jpg': 'd6', '2028-600.jpg': 'e1', '2045-600.jpg': 'f1', '2018-600.jpg': 'g1'}

audio_mappings = {'16.wav': 'A1', '60.wav': 'A2', '5.wav': 'A3', '57.wav': 'A4', '17.wav': 'A5', '6001.wav': 'A6', '9.wav': 'B1', '20.wav': 'B2', '58.wav': 'B3', '7.wav': 'B4', '19.wav': 'B5', '1.wav': 'B6', '10.wav': 'C1', '44.wav': 'C2', '36.wav': 'C3', '7001.wav': 'C4', '2.wav': 'C5', '3001.wav': 'C6', '8001.wav': 'D1', '51.wav': 'D2', '11.wav': 'D3', '1001.wav': 'D4', '50.wav': 'D5', '18.wav': 'D6', '5001.wav': 'E1', '13.wav': 'F1', '3.wav': 'G1'}

label_mappings = {'16': 'A1', '60': 'A2', '5': 'A3', '57': 'A4', '17': 'A5', '6001': 'A6', '9': 'B1', '20': 'B2', '58': 'B3', '7': 'B4', '19': 'B5', '1': 'B6', '10': 'C1', '44': 'C2', '36': 'C3', '7001': 'C4', '2': 'C5', '3001': 'C6', '8001': 'D1', '51': 'D2', '11': 'D3', '1001': 'D4', '50': 'D5', '18': 'D6', '5001': 'E1', '13': 'F1', '3': 'G1'}

trtst = {'45': ['a5', 'a1', 'a4', 'b3', 'c3', 'd2'], '46': ['b1', 'a2', 'd4', 'b6', 'b5', 'c4'], '47': ['B1', 'A1', 'A2', 'D1', 'C1', 'A3'], '48': ['B2', 'A4', 'C2', 'D2', 'B4', 'B3'], '49': ['d5', 'a3', 'c6', 'c2', 'b4', 'c1'], '50': ['d3', 'a6', 'c5', 'd6', 'b2', 'd1'], '51': ['D3', 'A5', 'B5', 'C3', 'C5', 'C4'], '52': ['D4', 'B6', 'D5', 'A6', 'D6', 'C6'], '53': ['a6', 'c4', 'a4', 'a5', 'd4', 'b5'], '54': ['b2', 'c5', 'b6', 'd5', 'a1', 'b1'], '55': ['D3', 'C2', 'B2', 'A3', 'A6', 'A2'], '56': ['B5', 'C3', 'A1', 'D1', 'B3', 'B4'], '57': ['c2', 'b3', 'd6', 'c1', 'c3', 'a2'], '58': ['c6', 'a3', 'd2', 'd3', 'b4', 'd1'], '59': ['C4', 'C5', 'A5', 'B6', 'D6', 'C6'], '60': ['D5', 'A4', 'D2', 'B1', 'C1', 'D4'], '102': ['b4', 'a2', 'c3', 'b5', 'd3', 'b1'], '103': ['b2', 'd4', 'c5', 'a4', 'c1', 'c6'], '104': ['D1', 'C1', 'B3', 'A1', 'B1', 'B2'], '105': ['C3', 'D2', 'C2', 'C4', 'A2', 'B4'], '106': ['b3', 'd1', 'a5', 'c4', 'd6', 'd2'], '107': ['a3', 'a6', 'b6', 'd5', 'a1', 'c2'], '108': ['D3', 'B5', 'C5', 'A3', 'D4', 'D5'], '109': ['A4', 'A5', 'D6', 'C6', 'B6', 'A6'], '110': ['b5', 'b6', 'b4', 'c5', 'd4', 'a4'], '111': ['d5', 'b1', 'c6', 'c1', 'a5', 'c2'], '112': ['C2', 'D2', 'B2', 'B3', 'B6', 'A3'], '113': ['C3', 'C5', 'B1', 'A1', 'D3', 'C4'], '114': ['d3', 'b2', 'd1', 'd2', 'a6', 'c3'], '115': ['a1', 'a2', 'a3', 'b3', 'd6', 'c4'], '116': ['D5', 'D6', 'A6', 'C6', 'D4', 'B5'], '117': ['B4', 'A2', 'A5', 'D1', 'C1', 'A4'], '156': ['d3', 'c5', 'c4', 'b2', 'c1', 'a3'], '157': ['b4', 'd5', 'd6', 'd1', 'a4', 'c2'], '158': ['D1', 'C3', 'C1', 'C2', 'B1', 'A1'], '159': ['A2', 'C4', 'D3', 'D2', 'D4', 'B2'], '160': ['d4', 'b5', 'a1', 'a2', 'c3', 'a6'], '161': ['b1', 'd2', 'b6', 'b3', 'a5', 'c6'], '162': ['B3', 'A4', 'A3', 'A5', 'C5', 'D5'], '163': ['A6', 'D6', 'B6', 'C6', 'B4', 'B5'], '164': ['b4', 'a4', 'd5', 'c6', 'c5', 'c4'], '165': ['d2', 'a5', 'b5', 'd1', 'd6', 'c1'], '166': ['C2', 'C6', 'A2', 'C3', 'D2', 'B3'], '167': ['C1', 'B1', 'A3', 'D5', 'D3', 'D4'], '168': ['a2', 'a1', 'c2', 'b6', 'a3', 'd3'], '169': ['a6', 'd4', 'b2', 'c3', 'b1', 'b3'], '170': ['B6', 'A6', 'D6', 'A5', 'A4', 'C5'], '171': ['A1', 'B4', 'C4', 'D1', 'B2', 'B5']}



#(n + 5) + 1
pd = {'10':0, '17':1, '23':0, '28':1, '32':1, '38':0, '70':0, '76':1, '83':1, '90':1, '96':0, '123':1, '129':0, '136':1, '143':0, '151':0}
ps = {'10': ['b4', 'b5', 'b6'], '17': ['b2', 'b3', 'b1'], '23': ['D4', 'D2', 'D1'], '28': ['c4', 'c3', 'c2'], '32': ['B1', 'B4', 'B6'], '38': ['d2', 'd6', 'd1'], '70': ['A3', 'A5', 'A6'], '76': ['c1', 'c5', 'c6'], '83': ['a2', 'a3', 'a1'], '90': ['C2', 'C3', 'C1'], '96': ['a5', 'a4', 'a6'], '123': ['A2', 'A4', 'A1'], '129': ['d5', 'd3', 'd4'], '136': ['D3', 'D5', 'D6'], '143': ['C4', 'C5', 'C6'], '151': ['B2', 'B3', 'B5']}

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

def find_maj(arr,whichh=1):
    dic = {"a":0,"b":0,"c":0,"d":0}
    for val in arr:
        dic[val[0].lower()]+=1
    if whichh == 0:
        return max(dic, key=lambda key:dic[key])
    else:
        return dic

def convarr(arr):
    new = []
    for item in arr:
        item = obj_mappings[item.replace("data/novel_objects/","")]
        new.append(item)
    return new

def convarr2(arr):
    new = []
    for item in arr:
        item = label_mappings[item.replace("data/output/test_stimuli/label_text/","").replace(".png","")]
        new.append(item)
    return new

dir = "/home/wkw/coding/results_zs3/"
save_loc = "/home/wkw/Desktop/"




probes = [["subj","prob1","prob2","prob3","target","response","accuracy"]]
training = [["subj","obj1","obj2","obj3","obj4","obj5","obj6","target_group","response","accuracy"]]
testing = [["subj","obj1","obj2","obj3","obj4","target_audio","response","accuracy"]]
idd = 1
for root, dirs, files in os.walk(dir):
    if "results" in root:
        for file in files:
            if "experiment_data.csv" in file and "ignore" not in file:
                #temp = pd.read_csv(os.path.join(root,file))
                temp = list(csv.reader(open(os.path.join(root,file))))
                #print(os.path.join(root,file))
                for row in temp:
                    trial_type = row[3] #probe trial, video button response, custom multiselect, audio button response
                    index = row[4]
                    responses = row[8]
                    button_pressed = row[10]
                    stimulus = row[1]
                    if trial_type == "probe-trial":
                        probes.append([idd, ps[index][0],ps[index][1],ps[index][2],pd[index],button_pressed,int(int(button_pressed)==pd[index])])
                    elif trial_type == "audio-button-response":
                        target = audio_mappings[row[16].replace("data/labels_digital/front_buffer/","")]
                        obj1 = obj_mappings[row[12].replace("data/novel_objects/","")]
                        obj2 = obj_mappings[row[13].replace("data/novel_objects/","")]
                        obj3 = obj_mappings[row[14].replace("data/novel_objects/","")]
                        obj4 = obj_mappings[row[15].replace("data/novel_objects/","")]
                        temp_dict = {"0":obj1,"1":obj2,"2":obj3,"3":obj4}
                        resp = temp_dict[button_pressed]
                        match = int(resp== target.lower())
                        testing.append([idd,obj1,obj2,obj3,obj4,target,resp,match])
                    elif trial_type == "custom-multiselect-object":
                        target_group = find_maj(trtst[index],0)
                        their_guess = convarr(json.loads(responses)["Q0"])
                        training.append([idd, trtst[index][0],trtst[index][1],trtst[index][2],trtst[index][3],trtst[index][4],trtst[index][5],target_group,their_guess, float(find_maj(their_guess)[target_group])/3 ])
                    elif trial_type == "custom-multiselect-label":
                        target_group = find_maj(trtst[index],0)
                        their_guess = convarr2(json.loads(responses)["Q0"])
                        print(their_guess)
                        print(target_group)
                        print(find_maj(their_guess)[target_group])
                        training.append([idd, trtst[index][0],trtst[index][1],trtst[index][2],trtst[index][3],trtst[index][4],trtst[index][5],target_group,their_guess, float(find_maj(their_guess)[target_group])/3 ])
                idd +=1

write_data(probes,save_loc+"zs3_probe_data.csv")
write_data(testing,save_loc+"zs3_f-test_data.csv")
write_data(training,save_loc+"zs3_training-test_data.csv")