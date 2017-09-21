#!/usr/bin/env python

### Food Cues Log Parsing Script
### Creator: Robert Kim
### Last Modifier: Robert Kim
### Version Date: 23 Feb 2017
### Python 2.7 

### Assumptions: 	Food Cues log file naming format is constant
###					Food Cues log file output format is constant

import csv
import os
import sys
import time

### opens sys.stdout in unbuffered mode
### print (sys.stdout.write()) operation is automatically flushed after each instance
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

### set home directory
home_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(home_dir)

conditions = ['Neutral', 'HiCal', 'LoCal']
keys = ['1!', '2@', '3#', '4$']
question = 'images/question_screen.jpg'

def main():
	subject_input = raw_input("subject ID: ")
	log_list = []

	for root, dirs, files in os.walk(home_dir):
	    for f in files:
	        if subject_input.lower() in f.lower() and f.lower().endswith('_maintime.txt'):
	             log_list.append([root, f])

	f_index = 0
	if len(log_list) < 1:
		sys.exit("No foodcues task files for provided subject ID.")
	else:
		print "Search results: "
		for x in list(enumerate(log_list)):
			print "    ", 
			print ("%d : " % x[0]) + os.path.join(x[1][0], x[1][1])
			# print (x[0], "/".join(x[1].strip("/").split('/')[1:]))
		print ""

	log_input = raw_input("Please enter the desired log file index (or multiple indices separated by spaces): ")

	if not log_input:
		sys.exit(	"EXITING OPERATION\n" + 
					"No log files were properly selected"	)

	log_index = log_input.split()
	log_index = [int(a) for a in log_index]

	if not all(n in range(len(log_list)) for n in log_index):
		sys.exit(	"EXITING OPERATION\n" +
					"INVALID ENTRY OF FILE INDICES"	)

	input_list = [os.path.join(log_list[n][0], log_list[n][1][ :-len('_maintime.txt')]) for n in log_index]
	run_analysis(input_list)

	print "\nOPERATION COMPLETED " + time.strftime("%d %b %Y %H:%M:%S", time.localtime())

def analysis(in_file):
	with open(in_file + '_maintime.txt') as txtfile: 
		content = txtfile.readlines()

	count = 0
	output = []
	# t1 = check if iterator has encountered row with condition
	# t2 = check if iterator has encountered hunger question
	t1 = t2 = False
	for row in content:
		check = [k in row for k in keys]

		if any(check):
			count += 1

		if 'condition' in row:
			if not t1 and not t2:
				t1 = True
				output.append([row.split(' ', 1)[0]])
			elif t1 and t2:
				t2 = False
				output[-1].append('None')
				output.append([row.split(' ', 1)[0]])

		if t1 and question in row:
			t2 = True

		if t1 and t2 and any(check):
			t1 = t2 = False
			i = [i for i, x in enumerate(check) if x][0]
			output[-1].append(keys[i][0])

		if not t1 and t2:
			sys.exit(	"EXITING OPERATION\n" + 
						"THIS SHOULD HAVE NEVER HAPPENED!\n" +
						"WHAT DID YOU DO?"	)

	print "\tTotal Key Presses: %d" % count

	with open(in_file + '_foodcues_parsed.csv', 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = ',', quotechar = '"')
		writer.writerow(['Condition', 'Response_Key'])
		writer.writerows(output)

def run_analysis(arr):
	error_files = []
	for s in arr:
		try:
			print "\n::::: PARSING %s_maintime.txt :::::" % s
			analysis(s)
		except KeyError: 
			print ">> ERROR READING " + s
			print ">> CHECK FILE CONSTRUCTION"
			error_files.append(s)

	if error_files:
		print "\n>> TOTAL OF %d INVALID FILES" % len(error_files)
		print ">> LIST OF FILES THAT THREW EXCEPTION:\n>>",
		print '\n>>'.join(error_files)


if __name__ == '__main__':	
	main()