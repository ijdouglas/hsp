import csv
import os
import json
from spellchecker import SpellChecker
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

#dictionary part:



spell = SpellChecker()
stemmer = SnowballStemmer("english")
lm = WordNetLemmatizer()

dir = "c:/Users/Ellis/Desktop/Lab/hsp_results/cond9_syntax1/"
input_data = [["subj#","trial#","target","original_guess","corrected_guess","stem","match"]]
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
    elif len(guess) <= 1 or guess == "idk" or guess == "im not sure" or guess == " " or guess == "i really dont know" or guess == 'no idea' or guess == "i have no clue" or guess == "not sure again" or guess == "fuck bitch" or guess == "no clue":
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
            if "syntax" in root:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                #print(os.path.join(root, file))
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
                            '''
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
                            '''
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
                        corrected = spell.correction(guess) # no entry goes to a, a
                        stemm = stemmer.stem(corrected) #fell vs fall, fell a tree  --- alternate to altern?
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
            if "syntax" in root and "ignore" not in file:
                temp = list(csv.reader(open(os.path.join(root,file), encoding="utf8")))
                #print(os.path.join(root, file))
                for row in temp:
                    if row[0] != "rt" and len(row[11])!= 0:
                        #print()
                        #print(row[7])
                        #print(row[11])
                        ip = row[7]
                        if len(row[7]) == 0:
                            ip = "undefined"
                        #if ip not in ips:
                        #    ips.append(ip)
                        filename = json.loads(row[11])
                        video = filename["video"]
                        trial = extract_turk_video_syntax(video)
                        target = extract_turk_target_syntax(video)
                        #print("they enter",filename["words"][0])
                        guess = basic_corrections(filename["words"][0].strip())
                        if " " in filename["words"][0].strip() and filename["words"][0].strip() not in spaces:
                            spaces.append([filename["words"][0],guess])
                            spaces_other.append(row)
                            '''
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
                            '''
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
                        corrected = spell.correction(guess) # no entry goes to a, a
                        stemm = stemmer.stem(corrected) #fell vs fall, fell a tree  --- alternate to altern?

                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)

                        input_data.append([ip,condition,trial,block_set,block_num,target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data
def cond45_generate(dir):
    input_data = [["subj#","trial#","target","guess"]]
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "experiment_data.csv" in file:
                filepath = os.path.join(root, file)
                #print(filepath)
                temp = list(csv.reader(open(filepath, encoding="utf8")))
                for row in temp:
                    if row[0] != "rt" and len(row[9])!=0:
                        filename = json.loads(row[9])
                        video = filename["video"]
                        video = video.replace("../hsp_verbs_mturk3/data/final_selection/","")
                        video = video.replace("hammer/h/","")
                        video = video.replace(".mp4","")
                        video = video[video.find("/")+1:]
                        input_data.append([row[7],video,extract_cond45_word(video),filename["words"][0]])
    return input_data
def baseline_generate(dir):
    input_data = [["subj#","condition","trial#","block_set","block_num","target","original_guess","corrected_guess","og_cg_match","spell-check","candidates","wordprob","cg_sc_match","stem","lemma","cg_st_match","target_stem_match","verb_synset"]]
    condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
    condition = condition.replace("/","")
    for root, dirs, files in os.walk(dir):
        for file in files:
            if "experiment_data.csv" in file:
                filepath = os.path.join(root, file)
                #print(filepath)
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
                            '''
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
                            '''
                        corrected = spell.correction(guess) # no entry goes to a, a
                        stemm = stemmer.stem(corrected) #fell vs fall, fell a tree  --- alternate to altern?
                        candidates = spell.candidates(guess)
                        verbs = len(wn.synsets(stemm, pos=wn.VERB))
                        lemma = lm.lemmatize(corrected, wn.VERB)
                        input_data.append([ip,condition,trial,"n/a","n/a",target,filename["words"][0],guess,int(filename["words"][0]==guess),corrected,candidates,spell.word_probability(corrected),int(guess==corrected),stemm,lemma,int(guess==stemm),int(target==stemm),int(verbs>0)])
    return input_data

def write_data(arrayed,name):
    with open(name,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

def general_walk(root_dir):
    dir = root_dir
    for root, dirs, files in os.walk(dir):
        #condition = dir.replace("c:/Users/Ellis/Desktop/Lab/hsp_results/","")
            #condition = condition.replace("/","")
        if "cond1" in root and "syntax" not in root:
            print("condition_1")
            data = baseline_generate(root)
            #for row in data:
            #    print(row)
        elif "cond2" in root:
            print("condition_2")
            data2 = baseline_generate(root)
            #for row in data2:
            #    print(row)
        elif "cond3" in root:
            print("condition_3")
            data3 = baseline_generate(root)
            #for row in data3:
            #    print(row)
        elif "cond4" in root:
            print("condition_4")
            data4 = sona_generate(root)
            for row in data4:
                print(row)
            print(root)
        elif "cond5" in root:
            print("condition_5")
            print(root)
        elif "cond7" in root:
            print("condition_7")
            data7 = baseline_generate(root)
            for row in data7:
                print(row)
        elif "cond8" in root:
            print("condition_8")
            data8 = baseline_generate(root)
            for row in data8:
                print(row)
        elif "cond9_syntax1" in root and "turk" not in root:
            print("sona")
            #sona_data = sona_generate(root)
        elif "cond9_syntax1" in root and "turk" in root:
            print("turk")
            #turk_data = turk_generate(root)


general_walk("c:/Users/Ellis/Desktop/Lab/hsp_results/")

#sona portion
'''
sona_dir = "c:/Users/Ellis/Desktop/Lab/hsp_results/cond9_syntax1/"
sona_data = sona_generate(sona_dir)
#write_data(sona_data,"sona_syntax_data.csv")
#print(sona_data)


print()

#Turk portion

turk_dir = "c:/Users/Ellis/Desktop/Lab/hsp_results/cond9_syntax1_turk/"
turk_data = turk_generate(turk_dir)
#write_data(turk_data,"turk_syntax_data.csv")
#print(turk_data)
for row in spaces:
    print(row)
for row in turk_data:
    print(row)
'''

#flag space