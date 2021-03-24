import hashlib
import csv
import json
import pandas as pd
exp12 = open("exp_12_vids.txt","r")
looxcie = open("looxcie_vids.txt","r")
vox = open("vox.txt","r")
#onsets = list(csv.reader(open("verb_onset.csv", encoding="utf8")))
general = [["verb","subj","verb_id","instance","onset","length","version (original = 00, beep = 01, syntax = 02)","global_id","filename","hash"]]
#global id = exp# + instance# + version#; 12 + 0034 + 01
hash2name = {}
name2hash = {}
'''
df = pd.read_csv("csv file")
for s, subj in df.groupby("subID"):
    s = id
    subj = subset of things only with ID
    for o, onset in subj.groupby("onset"):
        o = given onset
        onset = subset
        onset = onset.query("somethign> 0 & somting etc.)
'''
df = pd.read_csv("verb_onset.csv")
def globid(subj,instance,version):
    exp = str(subj[:2])
    if len(instance) == 1:
        instance = "000"+instance
    elif len(instance) == 2:
        instance = "00"+instance
    elif len(instance) == 3:
        instance = "0" + instance
    if len(str(version)) == 1:
        version = '0'+str(version)
    return exp + instance+version
def basic_array(text):
    for i in text.readlines():
        if i != "":
            #print(i.rstrip())
            name = i.rstrip()
            hashed = hashlib.sha256(name.encode()).hexdigest()
            hashed = hashed[:7]+".mp4"
            #print(hashed)
            file = name.replace(".mp4","")
            arra = file.split("_")
            #print(arra)
            verb = arra[0]
            subj = arra[1]
            verb_id = ''
            instance = arra[2]
            #print(df['verb_onset'].where(df['instance']==instance))
            #print(df['verb'].where(df['instance']==instance))
            #print(df['subj_id'].where(df['instance']==instance))
            onset = df.loc[(df['instance']==int(instance)) & (df['subj_id']==int(subj)) & (df['verb']==verb)].values[0][4]
            #print(subj,instance,verb)
            #print()
            length = arra[3]
            if "beep" in name:
                version = 1
            elif "voc_syntax" in name:
                subj = arra[2]
                instance = arra[3]
                length = arra[4]
                version = 2
            else:
                version = 0

            global_id = globid(subj, instance,version)
            #print(global_id)
            general.append([verb,subj,verb_id,instance,onset,length,version,global_id,name,hashed])
            hash2name[hashed] = name
            name2hash[name] = hashed
basic_array(exp12)
#basic_array(looxcie)
#basic_array(vox)

with open("global_id_files_exp12.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(general)
#with open('hash2name_dict.json', 'w') as outfile:
#    json.dump(hash2name, outfile)
#with open("name2hash_dict.json","w") as f:
#    json.dump(name2hash,f)
