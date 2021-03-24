import os

targetVerbs = ["build","cut","drive","eat","fall","fit","hit","hold","knock","move","put","shake","stack","touch","turn"]


dir = "/cantor/space/Ellis/HSP_videos/syntax_frames/new_vocaloid_clips/"
target_dir = "/cantor/space/Ellis/HSP_videos/syntax_frames/compressed_vocaloid_clips/"
for root, dirs, files in os.walk(dir):
	for file in files:
		if "_voc_syntax.mp4" in file:
				newFile = str(file).replace(".mp4","_final.mp4")
				location = dir + file
				newFile = target_dir + newFile
				command =["ffmpeg","-i", location, "-b 750k" ,newFile, "-y"]
				command_string = " ".join(command)
				os.system(command_string)

'''
dir2 = "Z:/Ellis/HSP_videos/mp4_files_with_beep/looxcie_files/"

for root, dirs, files in os.walk(dir):
	for file in files:
		if "_5sec_beep.mp4" in file:
			for item in targetVerbs:
				if item in file:
					newFile = str(file).replace(".mp4","_reduc_more.mp4")
					location = dir + file
					command =["ffmpeg","-i", location, "-b 750k" ,newFile, "-y"]
					command_string = " ".join(command)
					os.system(command_string)
'''
