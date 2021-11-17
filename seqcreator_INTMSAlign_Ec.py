#!/usr/bin/python

def NULLELIM(cvs):
	aft_data = []
	for i in range(len(cvs)):
		temp = []
		temp = cvs[i]
		if re.search('.*\w+.*',temp):
			aft_data.append(temp)
		else:
			continue
	return aft_data
	

def OpenProt(inputfile):
	data = [];data2 = []
	data = (file(inputfile).read()).split("\n")
	data2 = NULLELIM(data)
	del data2[0]
	return data2
	
def PickFreqRes(array):
	tmp_data1 = [];tmp_data2 = [];tmp_array = np.zeros(20,float)
	OneLetRes = {"0":"A","1":"C","2":"D","3":"E","4":"F","5":"G","6":"H","7":"I","8":"K","9":"L","10":"M","11":"N",\
			"12":"P","13":"Q","14":"R","15":"S","16":"T","17":"V","18":"W","19":"Y"}
	tmp_data1 = re.split(":",array)[1]
	tmp_data2 = re.split("\s+",tmp_data1)
	tmp_data2 = NULLELIM(tmp_data2)
	for i in range(len(tmp_data2)-1):
		tmp_val = float(0)
		tmp_val = float(tmp_data2[i])
		#print tmp_array
		tmp_array[i] = tmp_val
	param = int(0);param2 = []
	param = np.argmax(tmp_array)
	value = float(0)
	value = np.max(tmp_array)
	param2 = str(param)
	res = []
	res = OneLetRes[param2]
	return res,value


import os,sys,re
import numpy as np

ecflag = int(0)

while len(sys.argv) > 1:
	option = sys.argv[1]
	del sys.argv[1]
	if option == "-INPUT":
		input_file = sys.argv[1]	
		del sys.argv[1]
	elif option == "-INPUT2":
		input_file2 = sys.argv[1]
		del sys.argv[1]
	elif option == "-OUTPUT":
		output_file = sys.argv[1]
		del sys.argv[1]
	elif option == "-LABEL":
		label = sys.argv[1]	
		del sys.argv[1]
	elif option == "-THRESHOLD":
		threshold = sys.argv[1]
		del sys.argv[1]
	elif option == "-CALCEC":
		ecflag = int(1)
	
seq_data = OpenProt(input_file)
seq_data2 = OpenProt(input_file2)

threshold2 = float(0)
threshold2 = float(threshold)
#print seq_data2

comp_seq = [];value_ar = np.zeros(len(seq_data),float)

for i in range(len(seq_data)):
	tmp_res = [];tmp_array = [];value = float(0)
	tmp_array = seq_data[i]
	tmp_res,value = PickFreqRes(tmp_array)
	comp_seq.append(tmp_res)
	value_ar[i] = value

#print len(comp_seq)

for k in range(len(seq_data2)):
	tmp_res2 = [];tmp_array2 = [];value2 = float(0)                                                                                                                                                                                                                                                                                                                                                                                                                                            
	tmp_array2 = seq_data2[k]
	tmp_res2,value2 = PickFreqRes(tmp_array2)
	#print value2
	if value2 > float(threshold2):
		comp_seq[k] = tmp_res2
	if k != 0:
		if k % 50 == 0:
			comp_seq.append("\n")

if ecflag == int(1):
	Ecvalue = float(0);aamatrix = np.zeros(len(value_ar),float)
	for x in range(len(value_ar)):
		tmp_freq = float(0)
		tmp_freq = -np.log(float(value_ar[x])/100.0)
		Ecvalue = Ecvalue + tmp_freq
		aamatrix[x] = tmp_freq
	#print Ecvalue
	outputfile_log = open("%(output_file)s-Ecvalue.log"%vars(),"w")
	outputfile_log.write("#The input file name is followings: %(input_file)s\n"%vars())
	outputfile_log.write("#Ec value was: %(Ecvalue)5.3f\n"%vars())
	tmp_resnum = int(0)
	for y in range(len(aamatrix)):
		tmp_resnum = tmp_resnum + 1
		tmp_ecval = float(0)
		tmp_ecval = float(aamatrix[y])
		outputfile_log.write("%(tmp_resnum)i, %(tmp_ecval)5.3f\n"%vars())
	outputfile_log.close() 
	


#print np.average(value_ar)

print len(comp_seq)

comp_seq = ''.join(comp_seq)

outputfile = open(output_file,"w")
outputfile.write(">%(label)s\n"%vars())
outputfile.write("%(comp_seq)s\n"%vars())
#print comp_seq


