import csv
import matplotlib.pyplot as plt
import os
import sys

walk_dir = sys.argv[1]
host = 'bing.com'  #Add your host here
run_once = True


def getColumn(filename, column, host):
	results = csv.reader(open(filename), dialect='excel')
	req = []
	for result in results:
		if host in result[0] and result[0] is not None:
			req.append(result[column])
	return req

for root,subdirs,files in os.walk(walk_dir):
	for filename in files:
		file_path = os.path.join(root,filename)
		with open(file_path,'r') as f:
			if run_once:
				frame_size = getColumn(file_path,1,host)
				plt.xlabel('Frame size')
				plt.ylabel('Average RTT')
				plt.title('Plot For ' + host)
			time = getColumn(file_path,6,host)
			print(time[0])
			run_once = False
			rtt_Avg = getColumn(file_path,3,host)
			plt.plot(frame_size,rtt_Avg,linewidth = 3, linestyle = 'dashed',marker='o',label=time[0][12:])
			plt.legend(loc='upper left')
plt.savefig(host[:-4])
plt.clf()


    
	                

