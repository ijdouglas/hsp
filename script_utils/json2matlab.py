import json
import os
import scipy.io as sio
import numpy as np

#Subject dict where the keys are "kid id" and the values are "subject id". Current version is only for experiment 15. Would need to be updated to include more experiments.
subj_dict = {"20241":"1501","20427":"1502","20142":"1503","21933":"1504","20582":"1505","20695":"1506","21633":"1507","20473":"1508","21278":"1509","21992":"1510","20674":"1511","23512":"1512","21840":"1513","24257":"1514","21501":"1515","21960":"1516","23639":"1517","22944":"1518","21699":"1519","21769":"1520","21625":"1521","19544":"1522","19946":"1523","22049":"1524","21908":"1525","23513":"1526","21827":"1527","22666":"1528","23363":"1529","21977":"1530","23376":"1531","21131":"1532","24234":"1533","23523":"1534","23674":"1535","21381":"1536","22655":"1537","22791":"1538","23778":"1539","23846":"1540","23301":"1541","23757":"1542","24642":"1543","23775":"1544","24031":"1545","24158":"1546","24335":"1547","24270":"1548","24836":"1549","24368":"1550","24414":"1551","24237":"1552","24842":"1553","24416":"1554"}

#creates the dictionaries where the data will be stored
child_frame_vals = {}
parent_frame_vals = {}
child_frame2bbox = {}
parent_frame2bbox = {}

#Directory where the frames are located
dir = "/data/aamatuni/code/postprocess_boxes/output/"

#if needed, can search the directory for a .json
'''
for root, dirs, files in os.walk(dir):
	for file in files:
		if ".json" in file:
			filepath = os.path.join(root, file)
			json_file = open(filepath)
			json_data = json.load(json_file)
'''
#dict_keys(['image_id', 'category_id', 'bbox', 'score', 'fnum', 'fname'])

#Loads the json file, should be changed to the path to the json file with the bounding box data.
#ex. json_filepath = "/data/aamatuni/code/postprocess_boxes/output/bbox_processed.json"
json_data = json.load(open("/data/aamatuni/code/postprocess_boxes/output/exp15_remaining/bbox.json"))

#cycles through the bbox.json data
for row in json_data:
	#print(dir, row["fname"])
	directory = dir+row["fname"]
	name = row["fname"]
	name = name[name.find("_")+1:]
	name = name[:name.find("_")]
	if name[-5:] in subj_dict.keys():
		subj_id = subj_dict[name[-5:]]
		#print(directory[directory.find("_"):])
		fnum = row["fnum"]
		#print(fnum)
		#print(row["bbox"])
		converted_bbox = []
		x = int(row["bbox"][0])
		y = int(row["bbox"][1])
		w = int(row["bbox"][2])
		h = int(row["bbox"][3])
		converted_bbox.append(x/640) #grabs/converts bbox coordinates & length and width
		converted_bbox.append(y/480)
		converted_bbox.append(w/640)
		converted_bbox.append(h/480)
		#print(converted_bbox)	
		cat = row["category_id"]
		index = int(cat) -1
		#child data, storing bbox for a given frame
		if subj_id in child_frame2bbox and "cam08" not in directory:
			if fnum in child_frame2bbox[subj_id]:
				child_frame2bbox[subj_id][fnum][index] = converted_bbox
			elif fnum not in child_frame2bbox[subj_id]:
				child_frame2bbox[subj_id][fnum] = np.zeros((12,4))
				child_frame2bbox[subj_id][fnum][index] = converted_bbox
		elif subj_id not in child_frame2bbox and "cam08" not in directory:
			child_frame2bbox[subj_id] = {}
			if fnum in child_frame2bbox[subj_id]:
				child_frame2bbox[subj_id][fnum][index] = converted_bbox
			elif fnum not in child_frame2bbox[subj_id]:
				child_frame2bbox[subj_id][fnum] = np.zeros((12,4))
				child_frame2bbox[subj_id][fnum][index] = converted_bbox
		#parent data, storing bbox for a given frame
		if subj_id in parent_frame2bbox and "cam08" in directory:
			if fnum in parent_frame2bbox[subj_id]:
				parent_frame2bbox[subj_id][fnum][index] = converted_bbox
			elif fnum not in parent_frame2bbox[subj_id]:
				parent_frame2bbox[subj_id][fnum] = np.zeros((12,4))
				parent_frame2bbox[subj_id][fnum][index] = converted_bbox
		elif subj_id not in parent_frame2bbox and "cam08" in directory:
			parent_frame2bbox[subj_id] = {}
			if fnum in parent_frame2bbox[subj_id]:
				parent_frame2bbox[subj_id][fnum][index] = converted_bbox
			elif fnum not in parent_frame2bbox[subj_id]:
				parent_frame2bbox[subj_id][fnum] = np.zeros((12,4))
				parent_frame2bbox[subj_id][fnum][index] = converted_bbox
		#child data, storing frame/directory
		if subj_id in child_frame_vals and "cam08" not in directory:
			if fnum not in child_frame_vals[subj_id]:
				child_frame_vals[subj_id][fnum] = directory
		elif subj_id not in child_frame_vals and "cam08" not in directory:
			child_frame_vals[subj_id] = {}
			if fnum not in child_frame_vals[subj_id]:
				child_frame_vals[subj_id][fnum] = directory
		#parent data, storing frame/directory
		if subj_id in parent_frame_vals and "cam08" in directory:
			if fnum not in parent_frame_vals[subj_id]:
				parent_frame_vals[subj_id][fnum] = directory
		elif subj_id not in parent_frame_vals and "cam08" in directory:
			parent_frame_vals[subj_id] = {}
			if fnum not in parent_frame_vals[subj_id]:
				parent_frame_vals[subj_id][fnum] = directory

#Grabbing the child frame vals and putting them in matlab ready format
#must manually set the date in the line before sio.savemat()
for subject in child_frame_vals.keys():
	final_mat_dict = []
	subj = subject
	save_string = subj+"_child_boxes.mat"
	frames = child_frame_vals[subj].keys()
	frames = sorted(frames)
	for frame in frames:
		direc = child_frame_vals[subj][frame]
		bboxes = child_frame2bbox[subj][frame]
		#[directory, -, fnum, [bboxes]]		
		final_mat_dict.append([[direc], [0], [frame], bboxes])
	dictionary = {'__header__': b'MATLAB 5.0 MAT-file, Platform: GLNXA64, Created on: Tue Mar 03 14:02:59 2020', '__version__': '1.0', '__globals__': [], 'box_data': final_mat_dict}
	sio.savemat(save_string, dictionary)

#Doing the same, with the parent data
for subject in parent_frame_vals.keys():
	final_mat_dict = []
	subj = subject
	save_string = subj+"_parent_boxes.mat"
	frames = parent_frame_vals[subj].keys()
	frames = sorted(frames)
	for frame in frames:
		direc = parent_frame_vals[subj][frame]
		bboxes = parent_frame2bbox[subj][frame]
		final_mat_dict.append([[direc], [0], [frame], bboxes])
	dictionary = {'__header__': b'MATLAB 5.0 MAT-file, Platform: GLNXA64, Created on: Tue Mar 03 14:02:59 2020', '__version__': '1.0', '__globals__': [], 'box_data': final_mat_dict}
	sio.savemat(save_string, dictionary)

