import os

dir = "/marr/multiwork/experiment_15/included/"
#__date_id/cam01_video_r/cam01*
#__date_id/cam02_video_r/cam02*
#__date_id/cam03_video_r/cam03*
target_dir = "/marr/multiwork/experiment_19/included/*subj*/speech_r"
#/cam01.wav, others in sub

for root, dirs, files in os.walk(dir):
    #print(root)
    for file in files:
        if "cam01" in file:
            file_dir = root + "/" + file
            print(file_dir)
            subject = file_dir.replace(dir,"")[:file_dir.replace(dir,"").find("/")]
            print(subject)
            target_folder = "/marr/multiwork/experiment_15/included/"+subject+"/speech_r/"
            print(os.path.isdir(target_folder))
            command = ["ffmpeg","-i",file_dir,"-q:a","0","-map","a",target_folder+"cam01.wav"]
            print(" ".join(command))
            print()

for root, dirs, files in os.walk(dir):
    #print(root)
    for file in files:
        if "cam02" in file:
            file_dir = root + "/" + file
            print(file_dir)
            subject = file_dir.replace(dir,"")[:file_dir.replace(dir,"").find("/")]
            print(subject)
            target_folder = "/marr/multiwork/experiment_15/included/"+subject+"/speech_r/sub/"
            print(os.path.isdir(target_folder))
            command = ["ffmpeg","-i",file_dir,"-q:a","0","-map","a",target_folder+"cam02.wav"]
            print(" ".join(command))
            print()

for root, dirs, files in os.walk(dir):
    #print(root)
    for file in files:
        if "cam03" in file:
            file_dir = root + "/" + file
            print(file_dir)
            subject = file_dir.replace(dir,"")[:file_dir.replace(dir,"").find("/")]
            print(subject)
            target_folder = "/marr/multiwork/experiment_15/included/"+subject+"/speech_r/sub/"
            print(os.path.isdir(target_folder))
            command = ["ffmpeg","-i",file_dir,"-q:a","0","-map","a",target_folder+"cam03.wav"]
            print(" ".join(command))
            print()
