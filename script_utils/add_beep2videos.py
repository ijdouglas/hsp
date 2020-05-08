import csv
import os


#dict_csv = list(csv.reader(open("num2vid_file.csv")))




dir = "/cantor/space/Ellis/HSP_videos/syntax_frames/source_clips/"
audio_dir = "/cantor/space/Ellis/HSP_videos/syntax_frames/audio_clips/"

#change mov to mp4
'''
for root, dirs, files in os.walk(dir):
	for file in files:
		if ".mov" in file:
			command = ["ffmpeg","-i",file,file.replace(".mov",".mp4")]
			commstring = " ".join(command)
			os.system(commstring)
'''


'''

#ffmpeg -i video.mp4 audio_extract.mp3 -- extract audio from video
for root, dirs, files in os.walk(dir):
	for file in files:
		if "_5sec.mp4" in file:
			audio_extract = str(file).replace(".mp4","_audio_track.mp3")
			audio_mixed = str(file).replace(".mp4","_audio_mixed.mp3")
			video_mute = str(file).replace(".mp4","_video_mute.mp4")
			completed_video = str(file).replace(".mp4","_syntax.mp4")
			comm1 = ["ffmpeg","-i",file,audio_extract]
			print(" ".join(comm1))
			os.system(" ".join(comm1))


#ffmpeg -i beep_audio.mp3 -i audio_extract.mp3 -filter_complex amerg -c:a libmp3lame -q:a 4 audiofinal.mp3 -- mix audio together (does not fully cover the verb)
for root, dirs, files in os.walk(dir):
	for file in files:
		if "_5sec.mp4" in file:
			audio_extract = str(file).replace(".mp4","_audio_track.mp3")
			audio_mixed = str(file).replace(".mp4","_audio_mixed.mp3")
			video_mute = str(file).replace(".mp4","_video_mute.mp4")
			completed_video = str(file).replace(".mp4","_syntax.mp4")
			comm2 = ["ffmpeg","-i","beep_5.mp3","-i",audio_extract,"-filter_complex","amerge","-c:a","libmp3lame","-q:a","4",audio_mixed]
			print(" ".join(comm2))
			os.system(" ".join(comm2))


#ffmpeg -i video.mp4 -an videofinal.mp4 -- mute video
for root, dirs, files in os.walk(dir):
	for file in files:
		if "_5sec.mp4" in file:
			audio_extract = str(file).replace(".mp4","_audio_track.mp3")
			audio_mixed = str(file).replace(".mp4","_audio_mixed.mp3")
			video_mute = dir+str(file).replace(".mp4","_video_mute.mp4")
			filed = dir + file
			completed_video = str(file).replace(".mp4","_syntax.mp4")
			comm3 = ["ffmpeg","-i",filed,"-an",video_mute]
			print(" ".join(comm3))
			os.system(" ".join(comm3))
'''
'''
#ffmpeg -i videofinal.mp4 -i audiofinal.mp3 -shortest final.mp4 -- mix audio back onto video
for root, dirs, files in os.walk(dir):
	for file in files:
		if "_5sec.mp4" in file:
			audio_extract = str(file).replace(".mp4","_audio_track.mp3")
			audio_mixed = str(file).replace(".mp4","_audio_mixed.mp3")
			video_mute = str(file).replace(".mp4","_video_mute.mp4")
			completed_video = str(file).replace(".mp4","_syntax.mp4")
			comm4 = ["ffmpeg","-i",video_mute,"-i",audio_mixed,"-shortest",completed_video]
			print(" ".join(comm4))
			os.system(" ".join(comm4))
'''
'''
#syntax frame version
for row in dict_csv:
	audio_file = audio_dir+row[0]+".mp3"
	video_file = dir+row[1]
	video_mute = video_file.replace(".mp4","_mute.mp4")
	command1 = ["ffmpeg","-i",video_file,"-an",video_mute]
	print(" ".join(command1))
	os.system(" ".join(command1))
	complete_video = video_file.replace(".mp4","_voc_syntax.mp4")
	complete_video = complete_video.replace("source_clips","new_vocaloid_clips")
	command2 = ["ffmpeg","-i",video_mute,"-i",audio_file,"-shortest",complete_video]
	print(" ".join(command2))
	os.system(" ".join(command2))
'''
'''
#syntax frame version - slicing the audio files
source_file = "/mnt/c/Users/Ellis/Desktop/Lab/beeps/speech_with_silence_edited.mp3"
onsets = list(csv.reader(open("slice_onsets.csv")))
for row in onsets:
	name = row[0]+".mp3"
	onset = str(float(row[1])-3)
	command = ["ffmpeg","-ss",onset,"-t 5","-i",source_file,name,"-y"]
	os.system(" ".join(command))
'''