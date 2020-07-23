import csv
import os
import json
from spellchecker import SpellChecker
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from datetime import datetime

spell = SpellChecker()

stemmer = SnowballStemmer("english")

lm = WordNetLemmatizer()


dir = "c:/Users/Ellis/Desktop/Lab/hsp_results/cond9_syntax1/"
spaces = []
spaces_other = []

def extract_target_word_syntax(word):
    if "hammer" in word:
        return "hammer"
    if "sample/" in word:
        word = word.replace("sample/","")
    word = word.replace("./data/new_vocaloid_clips/","")
    word = word.replace("_5sec_voc_syntax_final.mp4","")
    first_ = word.find("_")
    word = word[:first_]
    return word
def extract_video_syntax(word):
    word = word.replace("sample/","")
    word = word.replace("./data/new_vocaloid_clips/","")
    return word
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
def extract_baseline_word(word):
    if "hammer" in word:
        return "hammer"
    word = word.replace("data/final_selection/","")
    word = word.replace("_5sec_beep.mp4","")
    first_ = word.find("_")
    word = word[:first_]
    firstslash = word.find("/")
    word = word[firstslash+1:]
    if "extra/" in word:
        word = word.replace("extra/","")
    return word
def extract_cond45_word(word):
    if "hammer" in word:
        return "hammer"
    word = word.replace("../hsp_verbs_mturk3/data/final_selection/","")
    word = word.replace("_5sec_beep.mp4","")
    first_ = word.find("_")
    word = word[:first_]
    firstslash = word.find("/")
    word = word[firstslash+1:]
    if "extra/" in word:
        word = word.replace("extra/","")
    return word
def basic_corrections(guess):
    guess = guess.lower()
    if guess == "fell":
        guess = "fall"
    elif guess == "movre":
        guess = "move"
    elif guess == "holf" or guess == "hild":
        guess = "hold"
    elif guess == "trun":
        guess = "turn"
    elif guess == 'but it is fun to':
        guess = "is"
    elif len(guess) <= 1 or guess == "idk" or guess == "im not sure" or guess == " " or guess == "i really dont know" or guess == 'no idea' or guess == "i have no clue" or guess == "not sure again" or guess == "no clue" or "fuck" in guess or "bitch" in guess or "ass" in guess or "cunt" in guess or "shit" in guess:
        guess = "N/A"
    replacements = [" with"," on"," top"," over"," around","to "," go"," is","it ","go ",","," into"," in"," them"," up"," knock"," stack"," blocks"," the ball"," there"," the"," it"," noise"," down for"," down"," things","\\"," off"," out"] #put inside -> putside
    for rep in replacements:
        guess = guess.replace(rep,"")
    return guess
def sona_generate(dir):
    input_data = [["subj#","condition","trial#","block_set","block_num","target","original_guess","corrected_guess","og_cg_match","spell-check","candidates","wordprob","cg_sc_match","stem","lemm","cg_st_match","target_stem_match","verb_synset"]] #block #, likely verb?
    condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
    condition = condition.replace("/","")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "syntax" in root and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                for row in temp:
                    if row[0] != "rt" and len(row[9])!= 0:
                        ip = row[7]
                        if len(row[7]) == 0:
                            ip = "undefined"
                        filename = json.loads(row[9])
                        video = filename["video"]
                        trial = extract_video_syntax(video)
                        target = extract_target_word_syntax(video)
                        guess = basic_corrections(filename["words"][0].strip()) #????????
                        if " " in filename["words"][0].strip() and filename["words"][0].strip() not in spaces:
                            spaces.append([filename["words"][0],guess])
                            spaces_other.append(row)
                            print("they enter: ",filename["words"][0])
                            print("we corrected to: ",guess)
                            x = input("Is that correct (y/n)? ")
                            if x.lower() == "y" or x.lower() == "yes":
                                print("Ok, we will save: ", guess)
                            elif x.lower() == "n" or x.lower() == "no":
                                y = input("Please enter the correction: ")
                                z = input("is ",y," correct? (y/n)")
                                if z.lower() == "y" or z.lower() == "yes":
                                    print("Ok, we will save: ", y)
                                else:
                                    print("We will save: ",guess)
                            print()
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
                        corrected = spell.correction(guess)
                        stemm = stemmer.stem(corrected) 
                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        input_data.append([ip,condition,trial,block_set,block_num,target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data
def turk_generate(dir):
    input_data = [["subj#","condition","trial#","block_set","block_num","target","original_guess","corrected_guess","og_cg_match","spell-check","candidates","wordprob","cg_sc_match","stem","lemma","cg_st_match","target_stem_match","verb_synset"]] #block #, likely verb?
    condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
    condition = condition.replace("/","")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "syntax" in root and "ignore" not in file and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0:
                        ip = row[7]
                        if len(row[7]) == 0:
                            ip = "undefined"
                        filename = json.loads(row[11])
                        video = filename["video"]
                        trial = extract_turk_video_syntax(video)
                        target = extract_turk_target_syntax(video)
                        #print("they enter",filename["words"][0])
                        guess = basic_corrections(filename["words"][0].strip())
                        if " " in filename["words"][0].strip() and filename["words"][0].strip() not in spaces:
                            spaces.append([filename["words"][0],guess])
                            spaces_other.append(row)
                            print("they enter: ",filename["words"][0])
                            print("we corrected to: ",guess)
                            x = input("Is that correct (y/n)? ")
                            if x.lower() == "y" or x.lower() == "yes":
                                print("Ok, we will save: ", guess)
                            elif x.lower() == "n" or x.lower() == "no":
                                y = input("Please enter the correction: ")
                                z = input("is ",y," correct? (y/n)")
                                if z.lower() == "y" or z.lower() == "yes":
                                    print("Ok, we will save: ", y)
                                else:
                                    print("We will save: ",guess)
                            print()
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
                        corrected = spell.correction(guess) 
                        stemm = stemmer.stem(corrected) 
                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        input_data.append([ip,condition,trial,block_set,block_num,target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data
def cond45_generate(dir):
    input_data = [["subj#","condition","trial#","block_set","block_num","target","original_guess","corrected_guess","og_cg_match","spell-check","candidates","wordprob","cg_sc_match","stem","lemm","cg_st_match","target_stem_match","verb_synset"]] #block #, likely verb?
    condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
    condition = condition.replace("/","")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "block" in root and "experiment" in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                for row in temp:
                    if row[0] != "rt" and len(row[9])!= 0:
                        ip = row[7]
                        if len(row[7]) == 0:
                            ip = "undefined"
                        filename = json.loads(row[9])
                        video = filename["video"]
                        print(video)
                        trial = extract_cond45_video(video)
                        target = extract_cond45_word(video)
                        guess = basic_corrections(filename["words"][0].strip()) #????????
                        if " " in filename["words"][0].strip() and filename["words"][0].strip() not in spaces:
                            spaces.append([filename["words"][0],guess])
                            spaces_other.append(row)
                            print("they enter: ",filename["words"][0])
                            print("we corrected to: ",guess)
                            x = input("Is that correct (y/n)? ")
                            if x.lower() == "y" or x.lower() == "yes":
                                print("Ok, we will save: ", guess)
                            elif x.lower() == "n" or x.lower() == "no":
                                y = input("Please enter the correction: ")
                                z = input("is ",y," correct? (y/n)")
                                if z.lower() == "y" or z.lower() == "yes":
                                    print("Ok, we will save: ", y)
                                else:
                                    print("We will save: ",guess)
                            print()
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
                        corrected = spell.correction(guess) 
                        stemm = stemmer.stem(corrected) 
                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        input_data.append([ip,condition,trial,block_set,block_num,target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data
def baseline_generate(dir):
    input_data = [["subj#","condition","trial#","block_set","block_num","target","original_guess","corrected_guess","og_cg_match","spell-check","candidates","wordprob","cg_sc_match","stem","lemma","cg_st_match","target_stem_match","verb_synset"]]
    condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
    condition = condition.replace("/","")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "experiment_data.csv" in file:
                filepath = os.path.join(root, file)
                print(filepath)
                temp = list(csv.reader(open(filepath, encoding="utf8")))
                for row in temp:
                    if row[0] != "rt" and len(row[9])!=0:
                        ip = row[7]
                        filename = json.loads(row[9])
                        video = filename["video"]
                        trial = extract_baseline_video(video)
                        target = extract_baseline_word(video)
                        guess = basic_corrections(filename["words"][0].strip())
                        if " " in filename["words"][0].strip() and filename["words"][0].strip() not in spaces:
                            spaces.append([filename["words"][0],guess])
                            spaces_other.append(row)
                            print("they enter: ",filename["words"][0])
                            print("we corrected to: ",guess)
                            x = input("Is that correct (y/n)? ")
                            if x.lower() == "y" or x.lower() == "yes" or len(x) == 0:
                                print("Ok, we will save: ", guess)
                            elif x.lower() == "n" or x.lower() == "no":
                                y = input("Please enter the correction: ")
                                z = input("is ",y," correct? (y/n)")
                                if z.lower() == "y" or z.lower() == "yes":
                                    print("Ok, we will save: ", y)
                                else:
                                    print("We will save: ",guess)
                            print()
                        corrected = spell.correction(guess) 
                        stemm = stemmer.stem(corrected) 
                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        input_data.append([ip,condition,trial,"n/a","n/a",target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

def general_walk(root_dir):
    today = datetime.today()
    Date = today.strftime("%d-%m-%Y")
    dir = root_dir
    for root, dirs, files in os.walk(dir):
        #condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
            #condition = condition.replace("/","")
        if "cond1" in root and "syntax" not in root:
            print("condition_1")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data = baseline_generate(root)
                filename = "cond1_"+Date+".csv"
                write_data(data,filename)
            #    for row in data:
            #        print(row)
        elif "cond2" in root:
            print("condition_2")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data2 = baseline_generate(root)
                filename = "cond2_"+Date+".csv"
                write_data(data2,filename)
            #    for row in data2:
            #        print(row)
        elif "cond3" in root:
            print("condition_3")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data3 = baseline_generate(root)
                filename = "cond3_"+Date+".csv"
                write_data(data3,filename)
            #    for row in data3:
            #        print(row)
        elif "cond4" in root: 
            print("condition_4")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data4 = cond45_generate(root)
                filename = "cond4_"+Date+".csv"
                write_data(data4,filename)
                #for row in data4:
                #    print(row)
        elif "cond5" in root:
            print("condition_5")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data5 = cond45_generate(root)
                filename = "cond5_"+Date+".csv"
                write_data(data5,filename)
        elif "cond7" in root:
            print("condition_7")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data7 = baseline_generate(root)
                filename = "cond7_"+Date+".csv"
                write_data(data7,filename)
                #for row in data7:
                #    print(row)
        elif "cond8" in root:
            print("condition_8")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                data8 = baseline_generate(root)
                filename = "cond8_"+Date+".csv"
                write_data(data8,filename)
                #for row in data8:
                #    print(row)
        elif "cond9_syntax1" in root and "turk" not in root:
            print("sona")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                sona_data = sona_generate(root)
                filename = "cond9_sona_"+Date+".csv"
                write_data(sona_data,filename)
                #for row in sona_data:
                #    print(row)
        elif "cond9_syntax1" in root and "turk" in root:
            print("turk")
            x = input("run?")
            if x == "y" or x == "yes" or x == "1":
                turk_data = turk_generate(root)
                filename = "cond9_turk_"+Date+".csv"
                write_data(turk_data,filename)
                #for row in turk_data:
                #    print(row)
            #write_data(turk_data, "new_turk_Data.csv")


general_walk("c:/Users/Ellis/Desktop/Lab/hsp_results/")