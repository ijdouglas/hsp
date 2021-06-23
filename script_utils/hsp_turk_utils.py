import pandas as pd
import os
import csv
import json
vid_database = pd.read_csv("video_information_11-9.csv")
unblinder_205 = json.load(open('./exp205_gIDs.json'))

short_verbs = ["be","go","do","up","ax","tip","ace","man","ice","end","air","eye","out","age","own","dog","key","cat","can","sun","ash","net","cup","ink","bed","tin","ray","see","ask","ail","sky","act","low","war","gin","bus","sin","bow","pen","boo","box","con","moo","ape","ram","pig","ham","web","let","win","tan","ban","eat","put","bar","bat","hat","cow","fly","oil","ski","cap","mar","tie","gas","rat","lie","don","nut","rap","top","pet","fox","arm","egg","fat","bay","try","toe","tar","bag","joy","par","pan","pot","toy","pat","use","set","say","log","die","pal","hop","mat","pin","dam","bet","tax","cut","row","sic","tap","cry","run","lap","bug","lay","get","vet","bin","gun","aim","cue","pay","fin","jam","gel","rip","dip","lot","axe","bob","jet","din","sue","pit","jar","rev","sip","zip","kit","lam","fan","bib","sit","aid","pod","arc","baa","mud","mix","hem","fit","coo","rob","bum","nap","pop","fix","sum","gee","cop","awe","pee","yen","kid","hoe","dot","sap","saw","dab","pad","rid","hug","job","dim","tee","sup","mop","hap","vie","lop","wax","wan","shy","bur","vex","sub","dig","ret","aby","beg","rag","buy","map","gag","hum","fee","hit","fog","wet","pup","zap","guy","bud","gum","hog","rot","cox","rue","jab","tat","peg","hue","mug","rig","rim","jaw","wag","wow","pun","hex","woo","nab","lag","wed","haw","rub","wad","sag","cod","add","cub","nag","eff","wee","fax","cog","owe","rut","dry","nod","pip","paw","sod","jag","opt","rib","nip","mow","tag","vow","sop","fib","gap","tow","dub","caw","tog","jig","hie","bid","lob","jog"]
filters = ["don't k ow","idk","im not sure"," ","i really dont know",'no idea',"i have no clue","not sure again","no clue","asdasd","winne","sup","verb","njnn","bute","dunno"]


def basic_corrections(guess):
    orig = guess
    guess = guess.lower()
    if guess == "fell" or guess == "gell":
        guess = "fall"
    elif guess == "movre":
        guess = "move"
    elif guess == "holf" or guess == "hild" or guess == "wold" or guess == "h old":
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
    elif guess == "stck":
        guess = "stick"
    elif guess == "h old":
        guess = "hold"
    elif guess == "scatch":
        guess = "scratch"
    elif guess == "put upright":
        guess = "put"
    elif guess == "squeez":
        guess = "squeeze"
    elif guess == "hold open":
        guess = "hold"
    elif guess == "hand to":
        guess = "hand"
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
    elif guess == "putdown ":
        guess = "put"
    elif guess == "laydown" or guess == "putdown":
        guess = guess[:guess.find("down")]
    elif " square" in guess or " together" in guess:
        guess = guess[:guess.find(" ")]
    elif "-down" in guess:
        guess = guess[:guess.find("-")]
    elif len(guess) <= 1 or guess in filters or "fuck" in guess or "bitch" in guess or "ass" == guess or "cunt" in guess or "shit" in guess:
        guess = "N/A"
    elif (len(guess) == 2 or len(guess) == 3) and guess not in short_verbs:
        guess = "N/A"
    elif len(guess) > 15:
        guess = "N/A"
    replacements = ["?"," to bed"," back"," hair"," up"," with","-up"," on"," top"," over"," around","to "," go"," is","it ","go ",","," into","inside"," in"," them"," knock"," stack"," blocks"," the ball"," there"," the"," it"," noise"," down for"," down"," things","\\"," off"," out","-you","don't"] #put inside -> putside
    for rep in replacements:
        guess = guess.replace(rep,"")
    guess = guess.strip()
    return guess

def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)


#Blinder and unblinder function to change between global id and normal, uses the vid_database imported csv
def unblinder(blinded, experiment):
    if experiment != "205":
        if "_" in blinded:
            return blinded[:blinded.find("_")]
        else:
            return vid_database.loc[(vid_database["global_id_name"]==blinded)].values[0][0]
    else:
        return unblinder_205[blinded.replace(".mp4","")]


def blinder(unblinded):
    if ".mp4" not in unblinded:
        unblinded = unblinded + ".mp4"
    i1 = unblinded
    if len(vid_database.loc[(vid_database["old_filename"]==unblinded)].values) ==0:
        i1 = unblinded
        for repl in ["_h","_l","_m","_s"]:
            i1 = i1.replace(repl,"")
            if len(vid_database.loc[(vid_database["old_filename"]==i1)].values)==0:
                i2 = unblinded.replace("beep","voc_syntax_final")
            else:
                i2 = i1
    else:
        i2 = unblinded
    return str(vid_database.loc[(vid_database["old_filename"]==i2)].values[0][13])

#Since the naming schemes changed between the different conditions, different methods are needed to extract the video file or verb from a given csv file
def extract_video(word, experiment):
    word = word.replace("sample/","")
    word = word.replace("hammer/h/","")
    if experiment == "204": #turk video syntax
        word = word.replace("../hsp_verbs_mturk12/data/new_vocaloid_clips/","")
    elif experiment == "201": #baseline video
        word = word.replace("../hsp_verbs_mturk3/","")
        word = word.replace("data/final_selection/","")
        word = word[word.find("/")+1:]
    elif experiment == "202": #cond45
        word = word.replace("data/final_selection/","")
        word = word.replace("../hsp_verbs_mturk3/","")
        word = word[word.find("/")+1:]
    elif experiment == "200": #rand_baseline
        word = word.replace("data/blinded/","")
        word = word.replace("data/final_selection/","")
        word = word.replace("random_baseline_1/","")
        word = word[word.find("/")+1:]
    elif experiment == "203":
        word = word.replace("./data/global_id_ver/","")
    elif experiment == "205":
        word = word.replace("data/vid_files/","")
    return word
    

def update_dict(not_in, maxx, word_dict):
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