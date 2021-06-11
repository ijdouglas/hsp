import csv
import os
import json
from spellchecker import SpellChecker
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from datetime import datetime
import pandas as pd
import scipy.io as sio
import numpy as np
from hanziconv import HanziConv
from collections import Counter

#REQUIRES THESE TWO FILES IN THE SAME DIRECTORY
dictionary_csv = list(csv.reader(open("hsp_voc.csv")))
exp12 = pd.read_csv("video_information_11-9.csv")



demo = {"203":{"sex":[],"age":[]},"204":{1:{"sex":[],"age":[]},2:{"sex":[],"age":[]}}}
no_reply1 = 0
no_reply2 = 0

#Location where the data is saved. Must be a folder that has subfolders for each experiment
#Ex. .../hsp_data/exp200 has all of the exp200 experiment_data.csv
#.../hsp_data/exp201 has all of 201 etc
walk_location = "/mnt/c/Users/wkw/Documents/Lab/hsp_data/"
#walk_location = "/home/wkw/Desktop/"

#Set to where you want the files to be saved. Program will create exp_20# folders where it will save the cleaned data and split into subfolders to hold the individual data
target_dir = "/mnt/c/Users/wkw/Desktop/"
#target_dir = "/home/wkw/Desktop/"


wn_target_dict = {"eat":wn.synset("eat.v.01"),"stack":wn.synset("stack.v.02"),"knock":wn.synset("knock.v.01"),"shake":wn.synset("shake.v.01"),"fit":wn.synset("fit.v.02"),"drive":wn.synset("drive.v.01"),"cut":wn.synset("cut.v.01"),"put":wn.synset("put.v.01"),"turn":wn.synset("turn.v.04"),"fall":wn.synset("fall.v.01"),"hold":wn.synset("hold.v.02")}

spell = SpellChecker()

stemmer = SnowballStemmer("english")
lm = WordNetLemmatizer()
#dictionary_txt = open("voc.txt","r")

word_dict = {}
minn = 100
min_word = ""
maxx = 0
max_word = ""
ordering = {1:[1,2,3,4,5,6,7,8,9,10,11],2:[3,11,10,1,9,5,8,7,6,4,2]}

problems = []

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

#short verbs with 2 or 3 char, used to filter out short entries
short_verbs = ["be","go","do","up","ax","tip","ace","man","ice","end","air","eye","out","age","own","dog","key","cat","can","sun","ash","net","cup","ink","bed","tin","ray","see","ask","ail","sky","act","low","war","gin","bus","sin","bow","pen","boo","box","con","moo","ape","ram","pig","ham","web","let","win","tan","ban","eat","put","bar","bat","hat","cow","fly","oil","ski","cap","mar","tie","gas","rat","lie","don","nut","rap","top","pet","fox","arm","egg","fat","bay","try","toe","tar","bag","joy","par","pan","pot","toy","pat","use","set","say","log","die","pal","hop","mat","pin","dam","bet","tax","cut","row","sic","tap","cry","run","lap","bug","lay","get","vet","bin","gun","aim","cue","pay","fin","jam","gel","rip","dip","lot","axe","bob","jet","din","sue","pit","jar","rev","sip","zip","kit","lam","fan","bib","sit","aid","pod","arc","baa","mud","mix","hem","fit","coo","rob","bum","nap","pop","fix","sum","gee","cop","awe","pee","yen","kid","hoe","dot","sap","saw","dab","pad","rid","hug","job","dim","tee","sup","mop","hap","vie","lop","wax","wan","shy","bur","vex","sub","dig","ret","aby","beg","rag","buy","map","gag","hum","fee","hit","fog","wet","pup","zap","guy","bud","gum","hog","rot","cox","rue","jab","tat","peg","hue","mug","rig","rim","jaw","wag","wow","pun","hex","woo","nab","lag","wed","haw","rub","wad","sag","cod","add","cub","nag","eff","wee","fax","cog","owe","rut","dry","nod","pip","paw","sod","jag","opt","rib","nip","mow","tag","vow","sop","fib","gap","tow","dub","caw","tog","jig","hie","bid","lob","jog"]
filters = ["don't k ow","idk","im not sure"," ","i really dont know",'no idea',"i have no clue","not sure again","no clue","asdasd","winne","sup","verb","njnn","bute"]


video_list = {}

targets = []
other_words = []
words = {}
words_video = {}
words_correct = {}
words_incorrect = {}
total_count = 0
spaces = []
spaces_other = []
not_in = []
block_dictionary = {"shake":1,"hold":2,"eat":3,"fall":4,"drive":5,"turn":6,"put":7,"cut":8,"fit":9,"knock":10,"stack":11}
dict_201 = {"hold":1,"cut":2}

valid = {}

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

#Blinder and unblinder function to change between global id and normal, uses the exp12 imported csv
def unblinder(blinded):
    if "_" in blinded:
        return blinded[:blinded.find("_")]
    else:
        return exp12.loc[(exp12["global_id_name"]==blinded)].values[0][0]

def unblinder_205(blinded):
    blinded = blinded.replace("03.mp4","01.mp4")
    return exp12.loc[(exp12["global_id_name"]==blinded)].values[0][0]

def blinder(unblinded):
    #print("blinder")
    #print(unblinded)
    if ".mp4" not in unblinded:
        unblinded = unblinded + ".mp4"
    i1 = unblinded
    #print(i1)
    #print(exp12.loc[(exp12["old_filename"]==unblinded)].values)
    if len(exp12.loc[(exp12["old_filename"]==unblinded)].values) ==0:
        i1 = unblinded
        for repl in ["_h","_l","_m","_s"]:
            i1 = i1.replace(repl,"")
            #print(exp12.loc[(exp12["old_filename"]==i1)].values)
            if len(exp12.loc[(exp12["old_filename"]==i1)].values)==0:
                #print(i1)
                i2 = unblinded.replace("beep","voc_syntax_final")
            else:
                i2 = i1
    else:
        i2 = unblinded
    #print(exp12.loc[(exp12["old_filename"]==i2)].values)
    return str(exp12.loc[(exp12["old_filename"]==i2)].values[0][13])

#Since the naming schemes changed between the different conditions, different methods are needed to extract the video file or verb from a given csv file
def extract_turk_target_syntax(word):
    if "hammer" in word:
        return "hammer"
    if "sample/" in word:
        word = word.replace("sample/","")
    word = word.replace("../hsp_verbs_mturk12/data/new_vocaloid_clips/","")
    word = word.replace("_5sec_voc_syntax_final.mp4","")
    first_ = word.find("_")
    word = word[:first_]
    return word

def extract_turk_video_syntax(word):
    word = word.replace("sample/","")
    word = word.replace("../hsp_verbs_mturk12/data/new_vocaloid_clips/","")
    return word

def extract_baseline_video(word):
    word = word.replace("../hsp_verbs_mturk3/","")
    word = word.replace("sample/","")
    word = word.replace("hammer/h/","")
    word = word.replace("data/final_selection/","")
    word = word[word.find("/")+1:]
    return word

def extract_cond45_video(word):
    word = word.replace("sample/","")
    word = word.replace("hammer/h/","")
    word = word.replace("data/final_selection/","")
    word = word.replace("../hsp_verbs_mturk3/","")
    word = word[word.find("/")+1:]
    return word

def extract_rand_baseline_video(word):
    word = word.replace("data/blinded/","")
    word = word.replace("sample/","")
    word = word.replace("hammer/h/","")
    word = word.replace("data/final_selection/","")
    word = word.replace("random_baseline_1/","")
    word = word[word.find("/")+1:]
    return word

#Basic corrections that get ignored or messed up by the spell checker
def basic_corrections(guess):
    orig = guess
    guess = guess.lower()
    if guess == "fell" or guess == "gell":
        guess = "fall"
    elif guess == "movre":
        guess = "move"
    elif guess == "holf" or guess == "hild" or guess == "wold":
        guess = "hold"
    elif guess == "trun":
        guess = "turn"
    elif guess == "rolla":
        guess = "roll"
    elif guess == "askin":
        guess = "ask"
    elif guess == "dres":
        guess = "dress"
    elif guess == "drie":
        guess = "drive"
    elif guess == 'but it is fun to':
        guess = "is"
    elif guess == "ea t":
        guess = "eat"
    elif guess == "h old":
        guess = "hold"
    elif guess == "scatch":
        guess = "scratch"
    elif guess == "squeez":
        guess = "squeeze"
    elif guess == "ress":
        guess = "press"
    elif guess == "anwer":
        guess = "answer"
    elif guess == "talke":
        guess = "talk"
    elif guess == "playplay":
        guess = "play"
    elif guess == "busses":
        guess = "bus"
    elif guess == "cut/press":
        guess = "cut"
    elif guess == "car rev":
        guess = "rev"
    elif guess == "gallo[":
        guess = "gallop"
    elif guess == "spinn":
        guess = "spin"
    elif guess == "hangup":
        guess = "hang"
    elif guess == "pickup":
        guess = "pick"
    elif len(guess) <= 1 or guess in filters or "fuck" in guess or "bitch" in guess or "ass" == guess or "cunt" in guess or "shit" in guess:
        guess = "N/A"
    elif (len(guess) == 2 or len(guess) == 3) and guess not in short_verbs:
        guess = "N/A"
    elif len(guess) > 15:
        guess = "N/A"
    replacements = ["?"," to bed"," back"," hair"," up"," with","-up"," on"," top"," over"," around","to "," go"," is","it ","go ",","," into","inside"," in"," them"," knock"," stack"," blocks"," the ball"," there"," the"," it"," noise"," down for"," down"," things","\\"," off"," out","-you"] #put inside -> putside
    for rep in replacements:
        guess = guess.replace(rep,"")
    guess = guess.strip()
    return guess

#Used to initialize the different csv
def header():
    return [["subj","ip","condition","trial","global_id","instance_id","trial_id","block_set","block_id","trial_in_block","target","target ID","original_guess","corrected_guess","spell-check","candidates","wordprob","guess","guess_id","target_guess_match","verb_synset","wn_wup"]]

def slim_header():
    return [["subj","trial","global_id","instance_id","trial_id","block_set","block_id","trial_in_block","target","target_id","guess","guess_id","match"]]

def exp_205_header():
    return [["subj","global_id","instance_id","condition","trial_id","block_id","trial_in_block","top_choice","target","target_id","guess","guess_id","match"]]

#Goes through exp200 folder
def exp200(dir,target_dir, save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_200/" 
    filtered_lean = slim_header() #initialize the arrays
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder): #Checks if the target folder exists, creates one otherwise
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"") #gets condition
    condition = condition.replace("/","")
    subject = 200001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp200" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8"))) #loads csv
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = header() #per subject arrays
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30 #onset info for matlab
                offset = float(36.9800)
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0: #used to ignore the first row
                        #below grabs the different information from the file
                        ip = file[:file.find("_")] 
                        filename = json.loads(row[11])
                        video = filename["video"]
                        trial = extract_rand_baseline_video(video)
                        #print("1:",trial)
                        if "_" in trial:
                            target = trial[:trial.find("_")]
                            #print("2:",target)
                        else:
                            target = unblinder(trial.strip())
                            #print("3:",target)
                        global_id = trial.replace(".mp4","")
                        #print(global_id)
                        guess = basic_corrections(filename["words"][0].strip())
                        is_sample = "_s_" in trial
                        block_num = 0
                        block_set = 0
                        block_type = 0
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1
                        global total_count 
                        total_count = total_count + 1
                        if target not in word_dict.keys(): #dictionary part, sees if the file is in the hsp_dict file
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if lemma == "na":
                            lemma = "N/A"
                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(guess, lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                        if not is_sample:
                            cevent_guessed_word.append([onset,offset,int(lemma_id)])
                            onset +=8.0
                            offset+=8.0
                            instance_id = global_id[0:2]+global_id[4:-2]
                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_set,block_num,target,target_id,filename["words"][0],guess,corrected,candidates,spell.word_probability(corrected),lemma,lemma_id,int(target==lemma),int(verbs>0),""]

                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_set,block_num, target,target_id,lemma,lemma_id,int(target==lemma)]

                            input_data.append(full_row)
                            slim_data.append(slim_row)
                            trial_id+=1
                #Matlab part
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-200000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    #sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                #Filtering part, checks if it fulfills a given length
                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >25:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    entries = df.values
                    valid = entries[entries != "N/A"]
                    if len(valid) >25:
                        for row in df.values:
                            filtered_lean = np.vstack((filtered_lean,row))

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >25:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    entries = df["guess"].values
                    valid = entries[entries != "N/A"]
                    #print(len(valid))
                    if len(valid) >25:
                        for row in df.values:
                            filtered_full = np.vstack((filtered_full,row))
    print(filtered_full) #saves the data
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp200_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp200_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp200_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp200_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

#General format the same as exp200, see notes from that
def exp201(dir,target_dir,save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_201/"
    filtered_lean = slim_header()
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"")
    condition = condition.replace("/","")
    subject = 201001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp201" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = header()
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                for row in temp:
                    if row[0] != "rt" and len(row[9])!= 0:
                        ip = file[:file.find("_")]
                        filename = json.loads(row[9])
                        video = filename["video"]
                        trial = extract_baseline_video(video)
                        target = trial[:trial.find("_")]
                        guess = basic_corrections(filename["words"][0].strip())
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1
                        global total_count
                        total_count = total_count + 1
                        is_sample = "_s_" in trial
                        if target not in word_dict.keys():
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if lemma == "na":
                            lemma = "N/A"
                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                        block_num = 0
                        block_set = 0
                        block_type = 0
                        if not is_sample:
                            #print(lemma)
                            global_id = blinder(trial)
                            #print(global_id)
                            cevent_guessed_word.append([onset,offset,int(lemma_id)])
                            onset +=8.0
                            offset+=8.0
                            #if trial_id == 1:
                            #    block_type = dict_201[target]
                            instance_id = global_id[0:2]+global_id[4:-2]
                            '''
                            targ_synset = wn_target_dict[target]
                            if lemma == "N/A":
                                wn_wup = 999
                            elif lemma in wn_target_dict:
                                guess_synset = wn_target_dict[lemma]
                                wn_wup = targ_synset.wup_similarity(guess_synset)
                            else:
                                if len(wn.synsets(lemma, pos=wn.VERB)) != 0:
                                    guess_synset = wn.synsets(lemma, pos=wn.VERB)[0]
                                    wn_wup = targ_synset.wup_similarity(guess_synset)
                                else:
                                    print(lemma)
                                    print(wn.synsets(lemma))
                                    guess_synset = wn.synsets(lemma)[0]
                                    wn_wup = targ_synset.wup_similarity(guess_synset)
                            '''
                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_set,block_num,target,target_id,filename["words"][0],guess,corrected,candidates,spell.word_probability(corrected),lemma,lemma_id,int(target==lemma),int(verbs>0),""]

                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_set,block_num, target,target_id,lemma,lemma_id,int(target==lemma)]

                            input_data.append(full_row)

                            slim_data.append(slim_row)
                            trial_id+=1
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-201000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    entries = df.values
                    valid = entries[entries != "N/A"]
                    if len(valid) >33:
                        for row in df.values:
                            filtered_lean = np.vstack((filtered_lean,row))

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    entries = df["guess"].values
                    valid = entries[entries != "N/A"]
                    #print(len(valid))
                    if len(valid) >33:
                        for row in df.values:
                            filtered_full = np.vstack((filtered_full,row))
                        #demographic here
    print(filtered_full)
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp201_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp201_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp201_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp201_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

#General format the same as exp200, see notes from that
def exp202(dir,target_dir,save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_202/"
    filtered_lean = slim_header()
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"")
    condition = condition.replace("/","")
    subject = 202001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp202" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                source_file = os.path.join(root, file)
                #print(source_file)
                trial_id = 1
                input_data = header()
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                for row in temp:
                    if row[0] != "rt" and len(row[9])!= 0:
                        ip = file[:file.find("_")]
                        filename = json.loads(row[9])
                        video = filename["video"]
                        trial = extract_cond45_video(video)
                        target = trial[:trial.find("_")]
                        guess = basic_corrections(filename["words"][0].strip())
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1
                        global total_count
                        total_count = total_count + 1
                        is_sample = "_s_" in trial
                        if is_sample:
                            block_num = 0
                            block_set = 0
                        elif block_num == 6:
                            block_num = 1
                        else:
                            block_num = block_num +1
                        if block_num == 1:
                            block_set += 1
                        if target not in word_dict.keys():
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if lemma == "na":
                            lemma = "N/A"
                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                        if not is_sample:
                            if trial_id == 1:
                                if block_dictionary[target] == 1:
                                    block_type = 1
                                elif block_dictionary[target] == 3:
                                    block_type = 2
                            global_id = blinder(trial)
                            print(global_id)
                            if int(global_id)%2 == 0:
                                #print(trial)
                                if [trial, global_id] not in problems:
                                    problems.append([trial,global_id])
                                global_id = str(int(global_id)-1)
                            cevent_guessed_word.append([onset,offset,int(lemma_id)])
                            onset +=8.0
                            offset+=8.0
                            instance_id = global_id[0:2]+global_id[4:-2]

                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_dictionary[target],block_num,target,target_id,filename["words"][0],guess,corrected,candidates,spell.word_probability(corrected),lemma,lemma_id,int(target==lemma),int(verbs>0),""]

                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_dictionary[target],block_num, target,target_id,lemma,lemma_id,int(target==lemma)]

                            input_data.append(full_row)

                            slim_data.append(slim_row)
                            trial_id+=1
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-202000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1
                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    order = ordering[np.unique(df["block_set"].values)[0]]
                    for val in order:
                        entries = df.loc[df["block_id"]==val]["guess"].values
                        valid = entries[entries != "N/A"]
                        if len(valid) >3:
                            for row in df.loc[df["block_id"]==val].values:
                                filtered_lean = np.vstack((filtered_lean,row))

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    order = ordering[np.unique(df["block_set"].values)[0]]
                    for val in order:
                        entries = df.loc[df["block_id"]==val]["guess"].values
                        valid = entries[entries != "N/A"]
                        if len(valid) >3:
                            for row in df.loc[df["block_id"]==val].values:
                                filtered_full = np.vstack((filtered_full,row))
                            #demographic here
    print(filtered_full)
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp202_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp202_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp202_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp202_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

#General format the same as exp200, see notes from that
def exp203(dir,target_dir,save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_203/"
    filtered_lean = slim_header()
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"")
    condition = condition.replace("/","")
    subject = 203001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp203" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = header()
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0:
                        ip = file[:file.find("_")]
                        filename = json.loads(row[11])
                        video = filename["video"]
                        trial = video.replace("./data/global_id_ver/","")
                        trial = trial.replace("sample/","")
                        #print(trial)
                        if "_" in trial:
                            #print(trial)
                            target = trial[:trial.find("_")]
                        else:
                            #print(trial)
                            target = unblinder(trial.strip())
                        global_id = trial.replace(".mp4","")
                        print(global_id)
                        guess = basic_corrections(filename["words"][0].strip())
                        is_sample = "_s_" in trial
                        block_num = 0
                        block_set = 0
                        block_type = 0
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1
                        global total_count
                        total_count = total_count + 1
                        if lemma == "na":
                            lemma = "N/A"
                        if target not in word_dict.keys():
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                        if not is_sample:
                            cevent_guessed_word.append([onset,offset,int(lemma_id)])
                            onset +=8.0
                            offset+=8.0
                            #if trial_id == 1:
                            #    block_type = dict_201[target]
                            instance_id = global_id[0:2]+global_id[4:-2]

                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_set,block_num,target,target_id,filename["words"][0],guess,corrected,candidates,spell.word_probability(corrected),lemma,lemma_id,int(target==lemma),int(verbs>0),""]

                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_set,block_num, target,target_id,lemma,lemma_id,int(target==lemma)]


                            input_data.append(full_row)

                            slim_data.append(slim_row)
                            trial_id+=1
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-203000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    entries = df.values
                    valid = entries[entries != "N/A"]
                    if len(valid) >25:
                        for row in df.values:
                            filtered_lean = np.vstack((filtered_lean,row))
                        temp2 = pd.read_csv(os.path.join(root,file))
                        responses = temp2["responses"].dropna()
                        if len(responses) > 1: #Demographic part
                            sex = json.loads(responses.values[1])["Sex"]
                            age = json.loads(responses.values[2])["age"]
                            demo["203"]["sex"].append(sex)
                            demo["203"]["age"].append(int(age))
                        else:
                            global no_reply1
                            no_reply1+=1

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    entries = df["guess"].values
                    valid = entries[entries != "N/A"]
                    #print(len(valid))
                    if len(valid) >25:
                        for row in df.values:
                            filtered_full = np.vstack((filtered_full,row))
                        #demographic here
    print(filtered_full)
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp203_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp203_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp203_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp203_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

#General format the same as exp200, see notes from that

def exp204(dir,target_dir, save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_204/"
    filtered_lean = slim_header()
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"")
    condition = condition.replace("/","")
    subject = 204001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp204" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = header()
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0:
                        ip = file[:file.find("_")]
                        filename = json.loads(row[11])
                        video = filename["video"]
                        trial = extract_turk_video_syntax(video)
                        target = extract_turk_target_syntax(video)
                        global_id = blinder(trial)
                        print(global_id)
                        guess = basic_corrections(filename["words"][0].strip())
                        is_sample = "_s_" in trial
                        if is_sample:
                            block_num = 0
                        elif block_num == 6:
                            block_num = 1
                        else:
                            block_num = block_num +1
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1
                        global total_count
                        total_count = total_count + 1
                        if lemma == "na":
                            lemma = "N/A"
                        if target not in word_dict.keys():
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                        if not is_sample:
                            cevent_guessed_word.append([onset,offset,int(lemma_id)])
                            onset +=8.0
                            offset+=8.0
                            if trial_id == 1:
                                if block_dictionary[target] == 1:
                                    block_type = 1
                                elif block_dictionary[target] == 3:
                                    block_type = 2
                            instance_id = global_id[0:2]+global_id[4:-2]
                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_dictionary[target],block_num,target,target_id,filename["words"][0],guess,corrected,candidates,spell.word_probability(corrected),lemma,lemma_id,int(target==lemma),int(verbs>0),""]

                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_dictionary[target],block_num, target,target_id,lemma,lemma_id,int(target==lemma)]

                            input_data.append(full_row)
                            slim_data.append(slim_row)
                            trial_id+=1
                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                subj_folder = "subject_"+"{:03}".format(int(subject)-204000)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    order = ordering[np.unique(df["block_set"].values)[0]]
                    for val in order:
                        entries = df.loc[df["block_id"]==val]["guess"].values
                        valid = entries[entries != "N/A"]
                        if len(valid) >3:
                            for row in df.loc[df["block_id"]==val].values:
                                filtered_lean = np.vstack((filtered_lean,row))
                    temp2 = pd.read_csv(os.path.join(root,file))
                    responses = temp2["responses"].dropna()
                    if len(responses) > 1:
                        sex = json.loads(responses.values[1])["Sex"] #demographic part
                        age = json.loads(responses.values[2])["age"]
                        demo["204"][block_type]["sex"].append(sex)
                        demo["204"][block_type]["age"].append(int(age))
                    else:
                        global no_reply2
                        no_reply2+=1        

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    order = ordering[np.unique(df["block_set"].values)[0]]
                    for val in order:
                        entries = df.loc[df["block_id"]==val]["guess"].values
                        valid = entries[entries != "N/A"]
                        if len(valid) >3:
                            for row in df.loc[df["block_id"]==val].values:
                                filtered_full = np.vstack((filtered_full,row))

    print(filtered_full)
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp204_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp204_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp204_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp204_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)

def exp205(dir,target_dir,save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    folder_holder = "experiment_205/"
    filtered_lean = exp_205_header()
    unfiltered_lean = exp_205_header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    subject = 205001
    for root, dirs, files in os.walk(dir):
        condition = root[root.find("cond")+4]
        for file in files:
            if "exp205" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = exp_205_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                trial_id = 1
                block_id = 1
                trial_in_block = 1
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0:
                        ip = file[:file.find("_")]
                        filename = json.loads(row[11])
                        trial = filename["video"].replace("data/vid_files/","")
                        if "sample" not in trial:
                            #video = filename["video"]
                            #trial = video.replace("./data/global_id_ver/","")
                            #trial = trial.replace("sample/","")
                            #print("trial", trial)
                            target = unblinder_205(trial.strip())
                            #print("target", target)
                            target_id = word_dict[target]
                            global_id = trial.replace(".mp4","")
                            #print("global_id", global_id)
                            guesses = filename["words"]
                            top_choice = 1
                            #print("guesses", guesses)
                            for guess in guesses:
                                guess = basic_corrections(guess)
                                corrected = spell.correction(guess)
                                lemma = lm.lemmatize(corrected, wn.VERB)
                                if lemma == "na":
                                    lemma = "N/A"
                                if lemma not in word_dict.keys():
                                    lemma_id = "999999"
                                    if lemma not in not_in:
                                        print(guess.strip())
                                        print(lemma)
                                        not_in.append(lemma)
                                else:
                                    lemma_id = word_dict[lemma]
                                cevent_guessed_word.append([onset,offset,int(lemma_id)])
                                onset +=8.0
                                offset+=8.0
                                instance_id = global_id[0:2]+global_id[4:-2]
                                full_row = [subject, global_id, instance_id, condition, trial_id, block_id, trial_in_block,top_choice, target, target_id, lemma, lemma_id, int(lemma_id == target_id)]
                                input_data.append(full_row)
                                top_choice += 1
                            if trial_id != 1:
                                if target != last_target:
                                    block_id +=1
                                    trial_in_block == 1
                            last_target = target
                            trial_id+=1
                for row in input_data:
                    print(row)
                print("\n\n\n")
"""                 info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-205000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1 """

"""                 length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    entries = df.values
                    valid = entries[entries != "N/A"]
                    if len(valid) >25:
                        for row in df.values:
                            filtered_lean = np.vstack((filtered_lean,row))
                        temp2 = pd.read_csv(os.path.join(root,file))
                        responses = temp2["responses"].dropna()
                        if len(responses) > 1: #Demographic part
                            sex = json.loads(responses.values[1])["Sex"]
                            age = json.loads(responses.values[2])["age"]
                            demo["205"]["sex"].append(sex)
                            demo["205"]["age"].append(int(age))
                        else:
                            global no_reply1
                            no_reply1+=1 """

"""                 length = len(input_data[1:])
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    entries = df["guess"].values
                    valid = entries[entries != "N/A"]
                    #print(len(valid))
                    if len(valid) >25:
                        for row in df.values:
                            filtered_full = np.vstack((filtered_full,row))
                        #demographic here """
"""     today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_lean = target_dir+"exp205_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp205_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean) """

#General format the same as exp200, see notes from that
#Chinese hsp version
def exp205_Chinese(dir,target_dir,save):
    #print(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
    print("does not work with gitbash cli")
    folder_holder = "experiment_205/"
    filtered_lean = slim_header()
    filtered_full = header()
    unfiltered_lean = slim_header()
    unfiltered_full = header()
    if not os.path.isdir(target_dir+folder_holder):
        os.mkdir(target_dir+folder_holder)
    target_dir = target_dir + folder_holder
    global walk_location
    condition = dir.replace(walk_location,"")
    condition = condition.replace("/","")
    subject = 205001
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "exp205" in root and "ignore" not in file and "experiment" in file:
                #print(file)
                temp = pd.read_csv(os.path.join(root,file))
                #print(temp["response"])
                source_file = os.path.join(root, file)
                trial_id = 1
                input_data = header()
                slim_data = slim_header()
                cevent_guessed_word = []
                onset = 30
                offset = float(36.9800)
                for index, row in temp.iterrows():
                    if len(str(row["response"])) > 3 :
                        #print(json.loads(row["response"])["words"])
                        ip = file[:file.find("_")]
                        filename = json.loads(row["response"])
                        video = filename["video"]
                        trial = video.replace("./data/global_id/","")
                        trial = trial.replace("sample/","")
                        #print(trial)
                        if "_" in trial:
                            #print(trial)
                            target = trial[:trial.find("_")]
                        else:
                            #print(trial)
                            target = unblinder(trial.strip())
                        global_id = trial.replace(".mp4","")
                        #guess = basic_corrections(filename["words"][0].strip())
                        guess = (filename["words"][0])
                        #print(guess)
                        is_sample = "_s_" in trial
                        block_num = 0
                        block_set = 0
                        block_type = 0

                        '''
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected)
                        candidates = spell.candidates(guess)
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        verbs = len(wn.synsets(lemma, pos=wn.VERB))
                        if lemma not in words and verbs >0:
                            words[lemma] = 1
                        elif lemma in words and verbs>0:
                            words[lemma] = words[lemma] +1

                        global total_count
                        total_count = total_count + 1

                        if lemma not in word_dict.keys():
                            lemma_id = "999999"
                            if lemma not in not_in:
                                print(filename["words"][0].strip())
                                print(lemma)
                                not_in.append(lemma)
                        else:
                            lemma_id = word_dict[lemma]
                            '''
                        if target not in word_dict.keys():
                            target_id = "999999"
                            if target not in not_in:
                                not_in.append(target)
                        else:
                            target_id = word_dict[target]
                        if not is_sample:
                            print()
                            print("verb:")
                            simp_guess = HanziConv.toSimplified(guess).strip()
                            print(simp_guess)
                            print(wn.synsets(simp_guess, lang="cmn"))
                            print(wn.synsets(simp_guess, lang = "cmn", pos=wn.VERB))
                            if len(wn.synsets(simp_guess, lang = "cmn", pos=wn.VERB)) != 0:
                                zh_synset = wn.synsets(simp_guess, lang="cmn", pos=wn.VERB)[0]
                                print(target)
                                #print(wn.synsets(target, pos=wn.VERB))
                                en_synset = wn_target_dict[target]
                                print(en_synset)
                                wn_wup = en_synset.wup_similarity(zh_synset)
                            else:
                                wn_wup = 999
                            print(wn_wup)
                            cevent_guessed_word.append([onset,offset,""])
                            onset +=8.0
                            offset+=8.0
                            #if trial_id == 1:
                            #    block_type = dict_201[target]
                            instance_id = global_id[0:2]+global_id[4:-2]
                            verbs = len(wn.synsets(simp_guess, lang="cmn", pos=wn.VERB))
                            full_row = [subject,ip,condition,trial,global_id,instance_id,trial_id,block_type,block_set,block_num,target,target_id,filename["words"][0],guess,"","","","","","",int(verbs>0),wn_wup]
                            #print(full_row)
                            slim_row = [subject,trial, global_id, instance_id,trial_id,block_type,block_set,block_num, target,target_id,"","",""]


                            input_data.append(full_row)

                            slim_data.append(slim_row)
                            trial_id+=1

                info = {"timestamp":datetime.today().strftime("%d-%m-%Y %H:%M:%S"), "subject":subject,"path":source_file,"hostname":"laptop","user":"user"}
                inner_structure = {"variable":"cevent_guessed-word","data":cevent_guessed_word,"info":info}
                final_structure = {"sdata":inner_structure}
                #print(subject)
                subj_folder = "subject_"+"{:03}".format(int(subject)-205000)
                #print(target_dir)
                #print(subj_folder)
                given = ""
                if not os.path.isdir(target_dir+subj_folder):
                    os.mkdir(target_dir+subj_folder)
                given = target_dir + subj_folder
                savestring = given+"/cevent_guessed-word.mat"
                if save == 1:
                    sio.savemat(savestring, final_structure)
                    write_data(input_data,given+"/cleaned_data.csv")
                    write_data(slim_data,given+"/cleaned_slim_data.csv")
                    os.system("cp "+source_file+" "+given+"/raw_data.csv")
                subject+=1

                length = len(slim_data[1:])
                for row in slim_data[1:]:
                    unfiltered_lean.append(row)
                if length >33:
                    df = pd.DataFrame(data =slim_data[1:], columns = slim_data[0])
                    entries = df.values
                    valid = entries[entries != "N/A"]
                    if len(valid) >25:
                        for row in df.values:
                            filtered_lean = np.vstack((filtered_lean,row))

                length = len(input_data[1:])
                for row in input_data[1:]:
                    unfiltered_full.append(row)
                if length >33:
                    df = pd.DataFrame(data =input_data[1:], columns = input_data[0])
                    entries = df["guess"].values
                    valid = entries[entries != "N/A"]
                    #print(len(valid))
                    if len(valid) >25:
                        for row in df.values:
                            filtered_full = np.vstack((filtered_full,row))
    print(filtered_full)
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")

    filt_full = target_dir+"exp205_full_filt_"+Date+".csv"
    write_data(filtered_full, filt_full)

    unfilt_full = target_dir+"exp205_full_unfilt_"+Date+".csv"
    write_data(unfiltered_full, unfilt_full)

    filt_lean = target_dir+"exp205_lean_filt_"+Date+".csv"
    write_data(filtered_lean, filt_lean)

    unfilt_lean =target_dir+"exp205_lean_unfilt_"+Date+".csv"
    write_data(unfiltered_lean,unfilt_lean)


#Walks through a given dir and checks the subfolders
def general_walk(root_dir):
    dir = root_dir
    for root, dirs, files in os.walk(dir):
        if "exp205" in root:
            print()
            print("exp205")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp205(root, target_dir, save)
        elif "exp204" in root:
            print()
            print("exp204")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp204(root, target_dir, save)
        elif "exp203" in root:
            print()
            print("exp203")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp203(root, target_dir, save)
        elif "exp201" in root:
            print()
            print("exp201")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp201(root, target_dir, save)
        elif "exp202" in root:
            print()
            print("exp202")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp202(root, target_dir, save)
        elif "exp200" in root:
            print()
            print("exp200")
            x = input("run? (y/yes/1 for yes) ")
            #x = "y"
            if x == "y" or x == "yes" or x == "1":
                save = input("save the csv files? (y/yes/1 for yes)")
                #save = "n"
                if save == "y" or save == "yes" or save == "1":
                    save = 1
                else:
                    save = 0
                exp200(root, target_dir, save)

def update_dict(not_in, maxx):
    new_dict = []
    for item in not_in:
        maxx +=1
        if item == "N/A":
            word_dict[item] = 0
        else:
            word_dict[item] = maxx
    for key in word_dict:
        new_dict.append([key,word_dict[key]])
    write_data(new_dict,"hsp_voc.csv")

#walk call
general_walk(walk_location)
for row in problems:
    print(row)

#Checks if the dict needs updating
print()
if len(not_in) != 0:
    print(not_in)
    x = input("Should the dict be updated? (y for yes): ")
    if x == "y":
        update_dict(not_in, maxx)

print("exp203")
#print(demo["203"])
print("people",len(demo["203"]["sex"])+no_reply1)
print(Counter(demo["203"]["sex"]))
print("avg age ", np.average(demo["203"]["age"]))
print("sd age ", np.std(demo["203"]["age"]))

print("exp204")
#print(demo["204"])
print("people",len(demo["204"][1]["sex"])+no_reply2)
print(Counter(demo["204"][1]["sex"]))
print("avg age ", np.average(demo["204"][1]["age"]))
print("sd age ", np.std(demo["204"][1]["age"]))
print("people",len(demo["204"][2]["sex"])+no_reply2)
print(Counter(demo["204"][2]["sex"]))
print("avg age ", np.average(demo["204"][2]["age"]))
print("sd age ", np.std(demo["204"][2]["age"]))