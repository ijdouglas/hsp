import csv
import pandas as pd
#from nltk.stem.wordnet import WordNetLemmatizer
#from spellchecker import SpellChecker
#from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from scipy.spatial import distance
import numpy as np
import itertools
from collections import Counter
from sklearn.manifold import MDS

pd.options.mode.chained_assignment = None  # default='warn'

#spell = SpellChecker()
#m = WordNetLemmatizer()


def write_data(arrayed,name):
    with open(name,mode="w",encoding="utf-8",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(arrayed)

#####################
#cf paragram loading#
#####################

cf_paragrams = pd.read_csv("./word_vectors/counter-fitted-vectors.txt", sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE, encoding = "utf-8")

hsp_nns = ['lid', 'lemon', 'seal', 'kettle', 'helmet', 'pants', 'mantis', 'baby', 'rattle', 'cube', 'phone', 'fish', 'pot', 'block', 'self', 'car', 'tiger', 'animals', 'turtle', 'giraffe', 'icecream', 'mango', 'bread', 'food', 'cake', 'napkin', 'key', 'ladybug', 'drop', 'jam', 'jacket', 'snowman', 'page', 'saw', 'rabbit', 'wheel', 'bed', 'hair', 'fabric', 'moose', 'buffalo', 'boy', 'people', 'blocks']


#Stop word filtering
stop = set(stopwords.words('english'))
def filtered(string):
    words = string.split(' ')
    filtr = [word for word in words if word not in stop]
    newt = " ".join(filtr)
    return newt

#Gets the last word
def last_word(item):
    #print(item)
    word = item.split(" ")[-1]
    return word

def epic_word(item):
    if ":" in item:
        word = item[:item.find(":")]
    else:
        word = item
    return word

#Simply retrieves the vector from a given db
def vec(db, word):
    #print(db.loc[word])
    return np.array(db.loc[word])

#Cos distance between two words given a db txt array of vectors
def cos_distance(db, word1, word2):
    vec1 = vec(db, word1)
        #print(word1 in db.index)
        #print(vec1)
    vec2 = vec(db, word2)
        #print(word2 in db.index)
        #print(vec2)
    return distance.cosine(vec1, vec2)

################################################
#Pairwise combinations of a unique_words list, #
# returns pairs along with cos distance        #
################################################
def combinatorial(db, unique_words):
    combos = list(itertools.combinations(unique_words,2))
    print(len(combos))
    holder = []
    for pair in combos:
        word1 = str(pair[0])
        word2 = str(pair[1])
        #print(word1, word2)
        holder.append([word1, word2, cos_distance(db,word1,word2)])
    return holder

#target_verbs = ["stack", "fit", "shake", "knock", "fall", "walk", "cut", "break", "turn", "drive", "sleep", "eat", "hold", "put", "open", "climb", "throw", "drop", "wipe", "wash"]
#lemmas = {'Holding':'hold','Putting':'put','Pushing':'push','Twisting':'twist','Dropping':'drop', 'Bending':'bend','Falling':'fall','Turning':'turn'}

##########################
#initial read in function#
##########################
def clean_data(name):
    print(name)
    data = pd.read_csv(name)
    print(pd.unique(data["verb"]))
    data['lemma_verb'] = data['verb'].map(lemmas)
    data['filtered'] = data['noun'].map(filtered)
    print(pd.unique(data['lemma_verb']))
    print(data)
    data.to_csv("sthsth_filtered.csv",index=False)


#clean_data("selected_action_object.csv")



'''
#########################################
#Checks differences in filtering methods#
#########################################
amt = 0
amt2 = 0
for item in pd.unique(df['filtered']):
    #print(item)
    if item in cf_paragrams.index:
        amt +=1
        #print(item)
    else:
        word = item.split(" ")[-1]
        #print(word in cf_paragrams.index)
        amt2 +=1
print(amt)
print(amt2)
'''

'''
################################
#Adding them to the original df#
################################

df['filtered_in_cf_par'] = df['filtered'].isin(cf_paragrams.index)
df["last_word"] = df["noun"].map(last_word)
df['last_word_in_cf_par'] = df['last_word'].isin(cf_paragrams.index)
print(df)
df.to_csv("sthsth_v2.csv",index=False)
'''

#df = pd.read_csv("v2_sthsth.csv")

###########################################
#Cf paragram calcs for the different verbs#
###########################################
'''
    hold = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='hold')]
    hold = hold[['id','verb','lemma_verb','noun','filtered']]
    hold = hold.dropna()
    print("Hold")
    hold_words = pd.unique(hold['filtered'])
    print("Filtered: ",len(hold))
    print("Filtered unique: ",len(hold_words))
    hold_combos = combinatorial(cf_paragrams,hold_words)
    hold.to_csv("hold_df.csv",index=False)
    write_data(hold_combos,"hold_pairwise.csv")


    put = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='put')]
    put = put[['id','verb','lemma_verb','noun','filtered']]
    put = put.dropna()
    print("put")
    put_words = pd.unique(put['filtered'])
    print("Filtered: ",len(put))
    print("Filtered unique: ",len(put_words))
    put_combos = combinatorial(cf_paragrams,put_words)
    put.to_csv("put_df.csv",index=False)
    write_data(put_combos,"put_pairwise.csv")



    push = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='push')]
    push = push[['id','verb','lemma_verb','noun','filtered']]
    push = push.dropna()
    print("push")
    push_words = pd.unique(push['filtered'])
    print("Filtered: ",len(push))
    print("Filtered unique: ",len(push_words))
    push_combos = combinatorial(cf_paragrams,push_words)
    push.to_csv("push_df.csv",index=False)
    write_data(push_combos,"push_pairwise.csv")


    turn = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='turn')]
    turn = turn[['id','verb','lemma_verb','noun','filtered']]
    turn = turn.dropna()
    print("turn")
    turn_words = pd.unique(turn['filtered'])
    print("Filtered: ",len(turn))
    print("Filtered unique: ",len(turn_words))
    turn_combos = combinatorial(cf_paragrams,turn_words)
    turn.to_csv("turn_df.csv",index=False)
    write_data(turn_combos,"turn_pairwise.csv")


    twist = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='twist')]
    twist = twist[['id','verb','lemma_verb','noun','filtered']]
    twist = twist.dropna()
    print("twist")
    twist_words = pd.unique(twist['filtered'])
    print("Filtered: ",len(twist))
    print("Filtered unique: ",len(twist_words))
    twist_combos = combinatorial(cf_paragrams,twist_words)
    twist.to_csv("twist_df.csv",index=False)
    write_data(twist_combos,"twist_pairwise.csv")

    dropp = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='drop')]
    dropp = dropp[['id','verb','lemma_verb','noun','filtered']]
    dropp = dropp.dropna()
    print("drop")
    drop_words = pd.unique(dropp['filtered'])
    print("Filtered: ",len(dropp))
    print("Filtered unique: ",len(drop_words))
    drop_combos = combinatorial(cf_paragrams,drop_words)
    dropp.to_csv("drop_df.csv",index=False)
    write_data(drop_combos,"drop_pairwise.csv")

    bend = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='bend')]
    bend = bend[['id','verb','lemma_verb','noun','filtered']]
    bend = bend.dropna()
    print("bend")
    bend_words = pd.unique(bend['filtered'])
    print("Filtered: ",len(bend))
    print("Filtered unique: ",len(bend_words))
    bend_combos = combinatorial(cf_paragrams,bend_words)
    bend.to_csv("bend_df.csv",index=False)
    write_data(bend_combos,"bend_pairwise.csv")

    fall = df[(df['filtered_in_cf_par']==True) & (df['lemma_verb']=='fall')]
    fall = fall[['id','verb','lemma_verb','noun','filtered']]
    fall = fall.dropna()
    print("fall")
    fall_words = pd.unique(fall['filtered'])
    print("Filtered: ",len(fall))
    print("Filtered unique: ",len(fall_words))
    fall_combos = combinatorial(cf_paragrams,fall_words)
    fall.to_csv("fall_df.csv",index=False)
    write_data(fall_combos,"fall_pairwise.csv")

'''
#####################
#Frequency filtering#
#####################

def top90freq(temp_df):
    print("\ntop90freq")
    cntr = Counter(temp_df['filtered'])
    srtd_cntr = sorted(cntr.items(), key = lambda item: item[1], reverse=True)
    diction = {k: v for k, v in srtd_cntr}
    total = len(temp_df['filtered'])
    holder = []
    summ = 0
    for key, item in diction.items():
        summ += diction[key]
        if summ/total <= 0.9:
            #print(key, summ/total)
            #print(diction[key])
            holder.append(key)
    print("length of top 90 percent: ",len(holder), " compared with the original: ", len(cntr))
    print(holder)
    return holder

'''
    hold_df = pd.read_csv('hold_df.csv')
    hold_top90 = top90freq(hold_df)
    hold_df['top_ninety'] = hold_df['filtered'].isin(hold_top90)
    print(hold_df)
    hold_df.to_csv('hold_df.csv',index=False)

    bend_df = pd.read_csv('bend_df.csv')
    bend_top90 = top90freq(bend_df)
    bend_df['top_ninety'] = bend_df['filtered'].isin(bend_top90)
    print(bend_df)
    bend_df.to_csv('bend_df.csv',index=False)

    dropp_df = pd.read_csv('drop_df.csv')
    dropp_top90 = top90freq(dropp_df)
    dropp_df['top_ninety'] = dropp_df['filtered'].isin(dropp_top90)
    print(dropp_df)
    dropp_df.to_csv('drop_df.csv',index=False)

    fall_df = pd.read_csv('fall_df.csv')
    fall_top90 = top90freq(fall_df)
    fall_df['top_ninety'] = fall_df['filtered'].isin(fall_top90)
    print(fall_df)
    fall_df.to_csv('fall_df.csv',index=False)

    push_df = pd.read_csv('push_df.csv')
    push_top90 = top90freq(push_df)
    push_df['top_ninety'] = push_df['filtered'].isin(push_top90)
    print(push_df)
    push_df.to_csv('push_df.csv',index=False)

    put_df = pd.read_csv('put_df.csv')
    put_top90 = top90freq(put_df)
    put_df['top_ninety'] = put_df['filtered'].isin(put_top90)
    print(put_df)
    put_df.to_csv('put_df.csv',index=False)

    turn_df = pd.read_csv('turn_df.csv')
    turn_top90 = top90freq(turn_df)
    turn_df['top_ninety'] = turn_df['filtered'].isin(turn_top90)
    print(turn_df)
    turn_df.to_csv('turn_df.csv',index=False)

    twist_df = pd.read_csv('twist_df.csv')
    twist_top90 = top90freq(twist_df)
    twist_df['top_ninety'] = twist_df['filtered'].isin(twist_top90)
    print(twist_df)
    twist_df.to_csv('twist_df.csv',index=False)
'''


##########################################################
#Re-filter the pairwise csv -> add Yayun's nouns from hsp#
##########################################################
def generate_epic(epic_file, verb):
    epic_df = pd.read_csv(epic_file)
    #narration_id -> ID, narration_timestamp, verb, noun
    #epic_df = epic_df[["narration_id","narration_timestamp","verb","noun"]]
    epic_df = epic_df.loc[:,("narration_id","narration_timestamp","verb","noun")]
    verb_df = epic_df.loc[(epic_df['verb'] == verb)]
    verb_df["filtered"] = verb_df["noun"].map(epic_word)
    verb_df["cf_paragrams"] = verb_df["filtered"].isin(cf_paragrams.index)
    verb_df = verb_df.loc[verb_df["cf_paragrams"]==True]
    top_ninety = top90freq(verb_df)
    verb_df['top_ninety'] = verb_df['filtered'].isin(top_ninety)
    if "-on" not in verb:
        verb_df['lemma_verb'] = verb_df['verb']
    else:
        verb_df["lemma_verb"] = "fall"
    verb_df = verb_df.loc[:,("narration_id","narration_timestamp","verb",'lemma_verb',"noun",'filtered','top_ninety')]
    return verb_df.rename(columns={"narration_id":"id","narration_timestamp":"timestamp","verb":"verb",'lemma_verb':'lemma_verb',"noun":'noun','filtered':'filtered','top_ninety':'top_ninety'})
    


'''
#epic kitchen -> insert/fit
fit_epic = generate_epic("selected_epic_verbs.csv","fit")
fit_epic.to_csv("fit_df.csv",index=False)

fit_subset = fit_epic.loc[fit_epic["top_ninety"]==True]
fit_words = pd.unique(fit_subset['filtered'])
fit_hsp = ['lid','lemon','seal','kettle','helmet','pants','mantis','baby']

fit_words = np.concatenate((fit_words, fit_hsp))
fit_combos2 = combinatorial(cf_paragrams, fit_words)
write_data(fit_combos2, "fit_pw_SS-EK_full.csv")


#epic kitchen -> shake
shake_epic = generate_epic("selected_epic_verbs.csv","shake")
shake_epic.to_csv("shake_df.csv",index=False)

shake_subset = shake_epic.loc[shake_epic["top_ninety"]==True]
shake_words = pd.unique(shake_subset['filtered'])
shake_hsp = ['rattle','cube','phone','fish','pot','kettle']

shake_words = np.concatenate((shake_words, shake_hsp))
shake_combos2 = combinatorial(cf_paragrams, shake_words)
write_data(shake_combos2, "shake_pw_SS-EK_full.csv")


#add epic kitchen -> drop/fall

fall_epic = generate_epic("selected_epic_verbs.csv","fall-on")
fall_df = pd.read_csv('fall_df.csv')
fall_df['timestamp'] = 0
fall_full_df = pd.concat([fall_epic, fall_df],sort=True)
fall_full_df.to_csv("fall_df.csv",index=False)

fall_subset = fall_full_df.loc[fall_full_df['top_ninety']==True]
fall_words = pd.unique(fall_subset['filtered'])

fall_hsp = ['block','self','cube','car','tiger','animals','turtle']

fall_words = np.concatenate((fall_words,fall_hsp))
fall_combos2 = combinatorial(cf_paragrams,fall_words)
write_data(fall_combos2, "fall_pw_SS-EK_full.csv")




eat_epic = generate_epic("selected_epic_verbs.csv","eat")
eat_epic.to_csv("eat_df.csv",index=False)

eat_subset = eat_epic.loc[eat_epic["top_ninety"]==True]
eat_words = pd.unique(eat_subset['filtered'])
eat_hsp = ['giraffe','icecream','mango','lemon','bread','food','fish','cake']

eat_words = np.concatenate((eat_words, eat_hsp))
eat_combos2 = combinatorial(cf_paragrams, eat_words)
write_data(eat_combos2, "eat_pw_SS-EK_full.csv")




hold_epic = generate_epic("selected_epic_verbs.csv","hold")
hold_df = pd.read_csv('hold_df.csv')
hold_df['timestamp'] = 0
hold_full_df = pd.concat([hold_epic, hold_df],sort=True)
hold_full_df.to_csv("hold_df.csv",index=False)

hold_subset = hold_full_df.loc[hold_full_df['top_ninety']==True]
hold_words = pd.unique(hold_subset['filtered'])

hold_hsp = ["seal","kettle","napkin",'paper','key',"rattle",'ladybug',"icecream","saw","tool"]

hold_words = np.concatenate((hold_words,hold_hsp))
hold_combos2 = combinatorial(cf_paragrams,hold_words)
write_data(hold_combos2, "hold_pw_SS-EK_full.csv")


#epic kitchen -> put
put_epic = generate_epic("selected_epic_verbs.csv","put")
put_df = pd.read_csv('put_df.csv')
put_df['timestamp'] = 0
put_full_df = pd.concat([put_epic, put_df],sort=True)
put_full_df.to_csv("put_df.csv",index=False)

put_subset = put_full_df.loc[put_full_df['top_ninety']==True]
put_words = pd.unique(put_subset['filtered'])

put_hsp = ['seal','drop','jam','jacket','cake','baby','phone','snowman']
put_words = np.concatenate((put_words,put_hsp))
put_combos2 = combinatorial(cf_paragrams,put_words)
write_data(put_combos2, "put_pw_SS-EK_full.csv")





#epic kitchen -> turn
turn_epic = generate_epic("selected_epic_verbs.csv","turn")
turn_df = pd.read_csv('turn_df.csv')
turn_df['timestamp'] = 0
turn_full_df = pd.concat([turn_epic, turn_df],sort=True)
turn_full_df.to_csv("turn_df.csv",index=False)

turn_subset = turn_full_df.loc[turn_full_df['top_ninety']==True]
turn_words = pd.unique(turn_subset['filtered'])

turn_hsp = ['page','saw','tool','rabbit','cube','wheel']

turn_words = np.concatenate((turn_words,turn_hsp))
turn_combos2 = combinatorial(cf_paragrams,turn_words)
write_data(turn_combos2, "turn_pw_SS-EK_full.csv")






break_epic = generate_epic('selected_epic_verbs.csv',"break")
bend_df = pd.read_csv('bend_df.csv')
bend_df['timestamp'] = 0
bendbreak_df = pd.concat([break_epic, bend_df],sort=True)
bendbreak_df.to_csv("bend_df.csv",index=False)

bend_subset = bendbreak_df.loc[bendbreak_df['top_ninety']==True]
bend_words = pd.unique(bend_subset['filtered'])

break_hsp = ['cube','rattle','helmet','bed','bread']

bend_words = np.concatenate((bend_words,break_hsp))
bend_combos2 = combinatorial(cf_paragrams,bend_words)
write_data(bend_combos2, "bend_pw_SS-EK_full.csv")




#epic kitchen -> cut
cut_epic = generate_epic("selected_epic_verbs.csv","cut")
cut_epic.to_csv("cut_df.csv",index=False)

cut_subset = cut_epic.loc[cut_epic["top_ninety"]==True]
cut_words = pd.unique(cut_subset['filtered'])
cut_hsp = ['bread','hair','block','car','fabric']

cut_words = np.concatenate((cut_words, cut_hsp))
cut_combos2 = combinatorial(cf_paragrams, cut_words)
write_data(cut_combos2, "cut_pw_SS-EK_full.csv")


#epic kitchen -> transition/walk
walk_epic = generate_epic("selected_epic_verbs.csv","walk")
walk_epic.to_csv("walk_df.csv",index=False)

walk_subset = walk_epic.loc[walk_epic["top_ninety"]==True]
walk_words = pd.unique(walk_subset['filtered'])
walk_hsp = ['moose','buffalo','boy','seal','people','animals']

walk_words = np.concatenate((walk_words, walk_hsp))
walk_combos2 = combinatorial(cf_paragrams, walk_words)
write_data(walk_combos2, "walk_pw_SS-EK_full.csv")


#epic kitchen -> sort/stack
stack_epic = generate_epic("selected_epic_verbs.csv","stack")
stack_epic.to_csv("stack_df.csv",index=False)

stack_subset = stack_epic.loc[stack_epic["top_ninety"]==True]
stack_words = pd.unique(stack_subset['filtered'])
stack_hsp = ["blocks"]

stack_words = np.concatenate((stack_words, stack_hsp))
stack_combos2 = combinatorial(cf_paragrams, stack_words)
write_data(stack_combos2, "stack_pw_SS-EK_full.csv")
'''



'''
#no epic kitchen, should it be combined with the latter?
drop_df = pd.read_csv('drop_df.csv')
drop_subset = drop_df[drop_df['top_ninety']==True]
drop_words = pd.unique(drop_subset['filtered'])
drop_words = np.concatenate((drop_words,hsp_nns))
drop_combos2 = combinatorial(cf_paragrams,drop_words)
write_data(drop_combos2, "drop_pw_SS-EK_full.csv")

#Nothing in HSP?
push_df = pd.read_csv('push_df.csv')
push_subset = push_df[push_df['top_ninety']==True]
push_words = pd.unique(push_subset['filtered'])
push_words = np.concatenate((push_words,hsp_nns))
push_combos2 = combinatorial(cf_paragrams,push_words)
write_data(push_combos2, "push_pw_SS-EK_full.csv")

#not in hsp???
twist_df = pd.read_csv('twist_df.csv')
twist_subset = twist_df[twist_df['top_ninety']==True]
twist_words = pd.unique(twist_subset['filtered'])
twist_words = np.concatenate((twist_words,hsp_nns))
twist_combos2 = combinatorial(cf_paragrams,twist_words)
write_data(twist_combos2, "twist_pw_SS-EK_full.csv")


'''










######################
#convert PW to 2dmat #
######################
def create_dict(word_list):
    stoi = {}
    itos = {}
    index = 0
    #word_list = np.concatenate((word_list))
    for word in word_list:
        stoi[word] = index 
        itos[index] = word
        index +=1
    return stoi, itos

def convert2d(filenam):
    #import
    print(filenam)
    bend_df = pd.read_csv(filenam)
    bend_df.columns = ['w1','w2','similarity']
    print(bend_df)
    #get unique words
    a = pd.unique(bend_df['w1'])
    b = pd.unique(bend_df['w2'])
    c = pd.unique(np.concatenate((a,b)))
    bend = bend_df.values

    #convert to dictionary
    bend_stoi, bend_itos = create_dict(c)

    #create empty array
    holder = np.zeros((len(bend_stoi),len(bend_stoi)))

    #go through and place the cos-distance at the id point (Should I do 1-cos_distance?)
    for row in bend:
        x = bend_stoi[row[0]]
        y = bend_stoi[row[1]]
        holder[x,y] = row[2]
        holder[y,x] = row[2] #symmetric

    #print(holder)

    #save the labels as a csv, 2nd column for color
    test = np.array(list(bend_stoi.keys()))
    test = pd.DataFrame(test.reshape(-1,1))
    test.columns = ['label']
    test['hsp'] = test['label'].isin(hsp_nns)
    noun = filenam.replace("_pw_SS-EK_full.csv",'')
    test.to_csv(noun+"_labels.csv",index=False)

    #save 2d matrix
    return holder

'''
holder = convert2d("fit_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/fit_2dm_symm.csv")

holder = convert2d("shake_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/shake_2dm_symm.csv")

holder = convert2d("fall_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/fall_2dm_symm.csv")

holder = convert2d("eat_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/eat_2dm_symm.csv")

holder = convert2d("hold_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/hold_2dm_symm.csv")

holder = convert2d("put_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/put_2dm_symm.csv")

holder = convert2d("turn_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/turn_2dm_symm.csv")

holder = convert2d("bend_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/bend_2dm_symm.csv")

holder = convert2d("cut_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/cut_2dm_symm.csv")

holder = convert2d("walk_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/walk_2dm_symm.csv")

holder = convert2d("stack_pw_SS-EK_full.csv")
write_data(holder,"twodim_mats/stack_2dm_symm.csv")
'''


#After this part, use MatLab to do MDS, seems to be better than sklearn or R mds


'''
print("sklearn mds")
embedding = MDS(n_components=2,dissimilarity='precomputed',metric=True, n_jobs=-1) #precomputed dissimilarity
#embedding = MDS(n_components=2)
X_transformed = embedding.fit_transform(holder)
print(X_transformed)
write_data(X_transformed,"bend_pyMDS.csv")
'''

infant = pd.read_csv("labels/infant_mcdi.csv")
toddler = pd.read_csv("labels/toddler_mcdi.csv")



infa = pd.unique(infant["definition"])
todd = pd.unique(toddler["definition"])

def which_mcdi(word):
    if word in infa:
        return 2
    if word in todd:
        return 3
    else:
        return 1

bend_lb = pd.read_csv("labels/bend_labels.csv")
bend_lb['mcdi'] = bend_lb['label'].map(which_mcdi)
bend_lb.to_csv("labels/bend_labels.csv",index=False)

cut_lb = pd.read_csv("labels/cut_labels.csv")
cut_lb['mcdi'] = cut_lb['label'].map(which_mcdi)
cut_lb.to_csv("labels/cut_labels.csv",index=False)

eat_lb = pd.read_csv("labels/eat_labels.csv")
eat_lb['mcdi'] = eat_lb['label'].map(which_mcdi)
eat_lb.to_csv("labels/eat_labels.csv",index=False)

fall_lb = pd.read_csv("labels/fall_labels.csv")
fall_lb['mcdi'] = fall_lb['label'].map(which_mcdi)
fall_lb.to_csv("labels/fall_labels.csv",index=False)

fit_lb = pd.read_csv("labels/fit_labels.csv")
fit_lb['mcdi'] = fit_lb['label'].map(which_mcdi)
fit_lb.to_csv("labels/fit_labels.csv",index=False)

hold_lb = pd.read_csv("labels/hold_labels.csv")
hold_lb['mcdi'] = hold_lb['label'].map(which_mcdi)
hold_lb.to_csv("labels/hold_labels.csv",index=False)

put_lb = pd.read_csv("labels/put_labels.csv")
put_lb['mcdi'] = put_lb['label'].map(which_mcdi)
put_lb.to_csv("labels/put_labels.csv",index=False)

shake_lb = pd.read_csv("labels/shake_labels.csv")
shake_lb['mcdi'] = shake_lb['label'].map(which_mcdi)
shake_lb.to_csv("labels/shake_labels.csv",index=False)

stack_lb = pd.read_csv("labels/stack_labels.csv")
stack_lb['mcdi'] = stack_lb['label'].map(which_mcdi)
stack_lb.to_csv("labels/stack_labels.csv",index=False)

turn_lb = pd.read_csv("labels/turn_labels.csv")
turn_lb['mcdi'] = turn_lb['label'].map(which_mcdi)
turn_lb.to_csv("labels/turn_labels.csv",index=False)

walk_lb = pd.read_csv("labels/walk_labels.csv")
walk_lb['mcdi'] = walk_lb['label'].map(which_mcdi)
walk_lb.to_csv("labels/walk_labels.csv",index=False)