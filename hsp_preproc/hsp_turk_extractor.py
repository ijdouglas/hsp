import csv
import os
import json
import glob
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from datetime import datetime
import pandas as pd
import scipy.io as sio
import numpy as np
from supporting.hsp_turk_utils import basic_corrections, write_data, blinder, unblinder, extract_video, update_dict
from hanziconv import HanziConv
from collections import Counter



#REQUIRES THESE TWO FILES IN THE "supporting" DIRECTORY
dictionary_csv = list(csv.reader(open("supporting/hsp_voc.csv")))
video_information = pd.read_csv("supporting/video_information_11-9.csv")

demo = {"203":{"sex":[],"age":[]},"204":{1:{"sex":[],"age":[]},2:{"sex":[],"age":[]}}, "205":{"sex":[],"age":[]},"206":{"sex":[],"age":[]}, "207":{"sex":[],"age":[]}}
demo_no_reply = {"203":0,"204":0, "205":0, "206":0,"207":0}

#loading config files:
print("I found the following config files:")
jsons = glob.glob("*.json")
for i in range(len(jsons)):
    print(i, jsons[i])
config_file = int(input("Which config file would you like to use? (type index num) "))
print(os.path.isfile(jsons[config_file]))
config_data = json.load(open(os.getcwd()+"/"+jsons[config_file]))
config_data = config_data["Parameters"]



#Location where the data is saved. Must be a folder that has subfolders for each experiment
#Ex. .../hsp_data/exp200 has all of the exp200 experiment_data.csv
#.../hsp_data/exp201 has all of 201 etc


#Set to where you want the files to be saved. Program will create exp_20# folders where it will save the cleaned data and split into subfolders to hold the individual data


################################################################
experiment = str(config_data['exp'])
source_file_loc = config_data["source_file_loc"]
save_data = int(config_data['save_files']) == 1
target_dir = config_data["target_dir"]
col_val = config_data["col2check"]
target_len = config_data["minimum_responses"]
block_ordering = config_data["block_ordering"]
block_dictionary = config_data["block_dictionary"]
dict_201 = {"hold":1,"cut":2}
################################################################

spell = SpellChecker()
lm = WordNetLemmatizer()


## change this
word_dict = {}
minn = 100
min_word = ""
maxx = 0
max_word = ""


words = {}
#imports dictionary
for line in dictionary_csv:
    #line = line.strip()
    #arr = line.split("\t")
    arr = line
    word = arr[0]
    val = int(arr[1])
    if val < minn:
        minn = val
        min_word = word
    if val > maxx:
        maxx = val
        max_word = word
    word_dict[word] = val

not_in = []

#valid = {}


#Used to initialize the different csv
def header():
    return [["subj","global_id","instance_id","condition","trial_id","block_id","trial_in_block","top_choice","target","target_id","guess","guess_id","match"]]

#experiment would be "200", "201", etc
def extract_data(dir,target_dir,experiment, save):
    global col_val, target_len, block_ordering, block_dictionary
    filtered_lean = header() #initialize the arrays
    unfiltered_lean = header()
    subject = int(experiment + "001")

    folder_holder = "experiment_"+experiment+"/" 
    if not os.path.isdir(target_dir+folder_holder): #Checks if the target folder exists, creates one otherwise
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder

    for root, dirs, files in os.walk(dir):
        dirs.sort()
        
        for file in files:
            if ("exp"+experiment) in root and "ignore" not in file and "experiment" in file:
                if experiment == "205":
                    condition = int(root[root.find("cond")+4])
                    first_words = ["stack","hold","stack","hold"]
                    last_target = first_words[condition-1]
                    trial_id = 1
                    block_id = 1
                    trial_in_block = 1

                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8"))) #loads csv
                source_file = os.path.join(root, file)
                trial_id = 1
                slim_data = header()
                
                cevent_guessed_word = []
                onset = 30 #onset info for matlab
                offset = float(36.9800)

                ip = file[:file.find("_")]
                for row in temp:
                    if row[0] != "rt" and len(row[col_val])!= 0: #used to ignore the first row
                        #below grabs the different information from the file
                        filename = json.loads(row[col_val])
                        video = filename["video"]
                        if "sample" not in video:
                            trial = extract_video(video,experiment)
                            if "_" in trial:
                                target = trial[:trial.find("_")]
                                global_id = blinder(trial)
                            else:
                                target = unblinder(trial.strip(),experiment)
                                global_id = trial.replace(".mp4","") 
                            if target not in word_dict.keys(): #dictionary part, sees if the file is in the hsp_dict file
                                target_id = "999999"
                                if target not in not_in:
                                    not_in.append(target)
                            else:
                                target_id = word_dict[target]
                            

                            if experiment == "200" or experiment == "201" or experiment == "203" or experiment == "206":
                                trial_in_block = 0
                                block_id = 0
                                condition = 1

                            elif experiment == "202" or experiment == "204":
                                trial_in_block = 0
                                block_id = block_dictionary[target]
                                trial_in_block = trial_id%6
                                if trial_in_block ==0:
                                    trial_in_block = 6
                                if trial_id == 1:
                                    if block_dictionary[target] == 1:
                                        condition = 1
                                    elif block_dictionary[target] == 3:
                                        condition = 2

                            if experiment != "205":
                                top_choice = 0
                                if experiment != "206":
                                    guess = basic_corrections(filename["words"][0].strip())
                                    corrected = spell.correction(guess)
                                    lemma = lm.lemmatize(corrected, wn.VERB)
                                else:
                                    guess = filename["words"][0].strip()
                                    lemma = HanziConv.toSimplified(guess).strip()
                                
                                if lemma == "na":
                                    lemma = "N/A"
                                if lemma not in word_dict.keys():
                                    lemma_id = "999999"
                                    if lemma not in not_in:
                                        #print("Not in:","\""+filename["words"][0]+"\"")
                                        #print(lemma)
                                        not_in.append(lemma)
                                else:
                                    lemma_id = word_dict[lemma]

                                cevent_guessed_word.append([onset,offset,int(lemma_id)])
                                onset +=8.0
                                offset+=8.0

                                instance_id = global_id[0:2]+global_id[4:-2]

                                slim_row = [subject, global_id, instance_id, condition, trial_id, block_id, trial_in_block, top_choice,target,target_id,lemma,lemma_id,int(target==lemma)]

                                slim_data.append(slim_row)
                                trial_id+=1

                            elif experiment == "205":
                                guesses = filename["words"]
                                top_choice = 1
                                if target != last_target:
                                    block_id +=1
                                    trial_in_block = 1
                                for guess in guesses:
                                    orig = guess
                                    guess = basic_corrections(guess)
                                    corrected = spell.correction(guess)
                                    lemma = lm.lemmatize(corrected, wn.VERB)
                                    if lemma == "na":
                                        lemma = "N/A"
                                    if lemma not in word_dict.keys():
                                        lemma_id = "999999"
                                        if lemma not in not_in:
                                            #print("Not in:","\""+orig+"\"")
                                            #print("Corrected:", lemma)
                                            not_in.append(lemma)
                                    else:
                                        lemma_id = word_dict[lemma]
                                    cevent_guessed_word.append([onset,offset,int(lemma_id)])
                                    instance_id = global_id[0:2]+global_id[4:-2]
                                    slim_row = [subject, global_id, instance_id, condition, trial_id, block_id, trial_in_block,top_choice, target, target_id, lemma, lemma_id, int(lemma_id == target_id)]
                                    slim_data.append(slim_row)
                                    top_choice += 1
                                trial_in_block +=1
                                onset +=8.0
                                offset+=8.0
                                trial_id+=1   
                                last_target = target
                #Matlab part
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                subj_folder = "subject_"+"{:03}".format(int(subject)-int(experiment + "000"))
                given = ""

                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"

                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(slim_data,given+"/cleaned_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                #Filtering part, checks if it fulfills a given length
                #Note: for 202 condition 2, the order may seem jumbled, but when filtering, it will sort by block_id
                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if experiment in ["200", "201", "203", "205", "206"]:
                    if length >target_len:
                        df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                        entries = df.values
                        valid = entries[entries != "N/A"]
                        if len(valid) >target_len:
                            for row in df.values:
                                filtered_lean = np.vstack((filtered_lean,row))

                        if experiment in ["203","205"]:
                            print()
                            temp2 = pd.read_csv(os.path.join(root,file))
                            responses = temp2["responses"].dropna()
                            if len(responses) > 1: #Demographic part
                                sex = json.loads(responses.values[1])["Sex"]
                                age = json.loads(responses.values[2])["age"]
                                demo[experiment]["sex"].append(sex)
                                demo[experiment]["age"].append(int(age))
                            else:
                                demo_no_reply[experiment] +=1
                        if experiment =="206":
                            print()
                            temp2 = pd.read_csv(os.path.join(root,file))
                            print(temp2)
                            responses = temp2["responses"].dropna()
                            print(responses)
                elif experiment in ["202","204"]:
                    if length >target_len:
                        df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                        order = block_ordering[np.unique(df["block_id"].values)[0]]
                        for val in order:
                            entries = df.loc[df["block_id"]==val]["guess"].values
                            valid = entries[entries != "N/A"]
                            if len(valid) >3:
                                for row in df.loc[df["block_id"]==val].values:
                                    filtered_lean = np.vstack((filtered_lean,row))

                        if experiment == "204":
                            temp2 = pd.read_csv(os.path.join(root,file))
                            responses = temp2["responses"].dropna()
                            if len(responses) > 1:
                                sex = json.loads(responses.values[1])["Sex"] #demographic part
                                age = json.loads(responses.values[2])["age"]
                                demo[experiment][condition]["sex"].append(sex)
                                demo[experiment][condition]["age"].append(int(age))
                            else:
                                demo_no_reply[experiment] +=1


    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_lean = target_dir+"exp"+experiment+"_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp"+experiment+"_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

extract_data(source_file_loc, target_dir, experiment, save_data )

if len(not_in) != 0:
    print("Items not in dictionary:", not_in)
    x = input("Should the dict be updated? (y for yes): ")
    if x == "y":
        update_dict(not_in, maxx, word_dict)

#To do: check other conditions, adjust for 207?

