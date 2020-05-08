import csv
import os
import json

dir = "c:/Users/Ellis/Desktop/Lab/semantic_net/data/mturk_results/"
input_data = [["subj#","trial#","target","guess"]]

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

for root, dirs, files in os.walk(dir):
    for file in files:
        if "experiment_data.csv" in file:
            filepath = os.path.join(root, file)
            print(filepath)
            temp = list(csv.reader(open(filepath, encoding="utf8")))
            for row in temp:
                if row[0] != "rt" and len(row[9])!=0:
                    filename = json.loads(row[9])
                    video = filename["video"]
                    video = video.replace("data/final_selection/","")
                    video = video.replace("hammer/h/","")
                    video = video.replace(".mp4","")
                    video = video[video.find("/")+1:]
                    input_data.append([row[7],video,extract_word(video),filename["words"][0]])

with open("compiled_data_baseline.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(input_data)