import pandas as pd
import csv
import os
import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from itertools import combinations

#req: glove pretrained vectors, compiled csv


#glove.840B.300d.txt
#glove.6B.100d.txt

words = pd.read_csv("glove.840B.300d.txt", sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)
def vec(word):
    return words.loc[word].as_matrix()


def glove_to_numpy(input="glove.840B.300d.txt", vec_out="vectors_output.txt", vocab_out="vocab_output.txt"):
    with open(input, "r") as glove_file:
        vocab = {}
        n = 0
        dim = 0
        for line in glove_file:
            if n == 0:
                dim = len(line.split()[1:])
            n+=1
        glove_file.seek(0)
        print(dim)
        vectors = np.zeros((n, dim), dtype=np.float32)
        print(vectors.shape)
        for i, line in enumerate(glove_file):
            split_line = line.split()
            vocab[split_line[0]] = i
            vec = [float(x) for x in split_line[1:]]
            vectors[i, :] = np.array(vec)
    np.save(vec_out, vectors)
    with open(vocab_out,"wb") as out:
        json.dump(vocab, out)
    return vocab, vectors
        

#cosine similarity, scipy.spatial.distance.cosine,   or cross-clusters, how it relates to their guesses or their confusability

def extract_word(word):
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

def gothedis(wordA, wordB):
    return distance.cosine(vec(wordA),vec(wordB))

def initialize_the_matrix():
    input_data = []
    Holder = ["subj","trial","target","guess","distance"]
    with open("compiled_data_baseline.csv",newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            input_data.append(row)
    print(len(input_data))
    basic_words = ["put","eat","press","drive","cut","knock","hold","fit","hit","stack","hammer","shake","turn","build","fall"]
    #video_stats = {}
    extracted_data = {"put":[],"eat":[],"press":[],"drive":[],"cut":[],"knock":[],"hold":[],"fit":[],"hit":[],"stack":[],"hammer":[],"shake":[],"turn":[],"build":[],"fall":[]}
    for row in input_data:
        target = row[2]
        guess = row[3]
        if guess not in basic_words:
            basic_words.append(guess)
        #remove -ing / tense, capital letter, no spaces, one word
        #data preprocessing, data storage
        extracted_data[target].append([guess, gothedis(target, guess),guess==target])
        row.append(gothedis(target, guess))
        Holder.append(row)
        #if target not in video_stats:
        #    video_stats[target] = 1
        #elif target in video_stats:
        #    video_stats[target] +=1
    combo = list(combinations(basic_words, 2))
    combos = []
    for subsets in combo:
        combos.append([subsets[0],subsets[1], gothedis(subsets[0],subsets[1])])
    #save them
    with open("csv_distribution_r_dec17.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(Holder)
    with open("pseudomatrix_dec17.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(combos)
    #with open("video_target_data.json","w") as f:
    #    json.dump(video_stats, f)
    #with open("everyword_data.json","w") as f:
    #    json.dump(basic_words, f)
    #with open("separated_vector_data_dec9.json","w") as f:
    #    json.dump(extracted_data,f)
    #with open("vectors_pseudo_matrix_indexical_dec17.json","w") as f:
    #    json.dump(combos,f)
    return extracted_data, basic_words

#file crawl:
extracted_data = []
basic_words = {}
extracted_data, basic_words = initialize_the_matrix()
print(basic_words)


#target = open("targets_data.json")
#targets = json.load(target)
#guesse = open("guesses_data.json")
#guesses = json.load(guesse)

#target_verbs = list(targets.keys())
#guess_verbs = list(guesses.keys())

#for key, value in targets:
#    csv_targets.append([key, value])
#with open("csv_targets.csv","w",newline="") as csvfile:
#    writer = csv.writer(csvfile,delimiter=",")
#    for word in target_verbs:
#        writer.writerow([word, targets[word]])

#with open("csv_guesses.csv","w",newline="") as csvfile:
#    writer = csv.writer(csvfile,delimiter=",")
#    for word in guess_verbs:
#        writer.writerow([word, guesses[word]])

'''

data = open("separated_vector_data_dec9.json")
vectord = json.load(data)
distances = pd.read_csv("pseudomatrix_dec9.csv",sep=",")


edge_distr = [["target","w1","w2","dist"]]

for key in vectord:
    G = nx.Graph()
    plt.figure(1,figsize=(15,15))
    guess_array = []
    weight_array = []
    for subarray in vectord[key]:
        guess_array.append(subarray[0].lower())
        weight_array.append(subarray[1])

    val_map ={}
    for item in guess_array:
        if item not in val_map.keys():
            val_map[item] = 1
        elif item in val_map.keys():
            val_map[item] +=1

    G.add_nodes_from(guess_array)
    
    for i in range(0,len(guess_array)):
        G.add_edge(key, guess_array[i], weight=weight_array[i])
        edge_distr.append([key,key, guess_array[i],weight_array[i]])
    

    for i, row in distances.iterrows():
        if row[0] in G and row[1] in G:
            G.add_edge(row[0].lower(),row[1].lower(),weight=row[2])
            edge_distr.append([key,row[0].lower(),row[1].lower(),row[2]])

    
    #thresholds
    weak = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.45]
    good = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.45 and d["weight"]>0.3]
    great = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.3]
    for item in guess_array:
            G.nodes[item]["count"] = val_map[item]
    pos = nx.kamada_kawai_layout(G)  # positions for all nodes
    #nx.draw(G, pos)
    nx.draw_networkx_nodes(G, pos, node_size = 700)
    # nodes

    #frequency of edge types
    #per target distribution of edge types
    #similarity distribution
    
    #    if item != key:
    #        nx.draw_networkx_nodes(G, pos, nodelist = [item],node_size=40*(val_map[item]), node_color="r")
    #    elif item == key:
    #        nx.draw_networkx_nodes(G, pos, nodelist = [item],node_size=40*(val_map[item]), node_color="g")

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=great,width=3, edge_color="b")
    nx.draw_networkx_edges(G, pos, edgelist=good,width=0.5, style="dashed")
    #nx.draw_networkx_edges(G, pos, edgelist=weak,width=2, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    
    plt.axis('off')
    plt.title(key)
    plt.savefig(key+"_weighted_graph.png")
    #plt.show()
    #print(G.nodes.data())
    print("done", key)
    plt.close()
#with open("edge_distribution_dec10.csv","w",newline="") as f:
#    writer = csv.writer(f)
#    writer.writerows(edge_distr)
'''
