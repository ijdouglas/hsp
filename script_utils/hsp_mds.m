file1 = 'bend_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'bend_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'bend_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'cut_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'cut_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'cut_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'eat_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'eat_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'eat_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'fall_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'fall_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'fall_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'fit_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'fit_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'fit_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'hold_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'hold_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'hold_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'put_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'put_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'put_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'shake_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'shake_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'shake_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'stack_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'stack_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'stack_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'turn_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'turn_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'turn_matlab_mds.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear

file1 = 'walk_2dm_symm.csv';
D = readtable(file1); %2d symmetric matrix of the cos_distance values
D = table2array(D); %convert to array for cmdscale

file2 = 'walk_labels.csv';
labelss = readtable(file2); % reads in the labels, first column is text, 2nd column is hsp boolean
words = labelss.label';
hsps = labelss.hsp;

[Y, eigvals] = cmdscale(D); %mds calculations
writematrix(Y(:,1:2),'walk_matlab_mds.csv')