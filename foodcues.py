#!/usr/bin/env python

### Food Cues Log Parsing Script
### Creator: Robert Kim
### Last Modifier: Robert Kim
### Version Date: 23 Feb 2017
### Python 2.7 

### Assumptions: 	Food Cues log file naming format is constant
###					Food Cues log file output format is constant

import csv
import glob
import os
import re
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

def analysis(in_file):
	with open(in_file) as txtfile: 
		content = txtfile.readlines()

	count = 0
	output = []
	# t1 = check if iterator has encountered row with condition
	# t2 = check if iterator has encountered hunger rating slide
	# t3 = check if iterator has encountered hunger response
	t1 = t2 = t3 = False
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

	subj = in_file.split('_', 1)[0]
	out_dir = "../foodcues_parsed_logs"
	out_file = os.path.join(out_dir, subj + "_foodcues_parsed.csv")

	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	with open(out_file, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = ',', quotechar = '"')
		writer.writerow(['Condition', 'Response_Key'])
		writer.writerows(output)

def main():
	print "Script file directory: %s" % home_dir
	log_list = glob.glob('*.txt')
	print "\nFood Cues log files found in script file directory: "
	for row in log_list:
		print '\t' + row
	print ""

	subj_input = raw_input("Please enter the desired subject code (or multiple indices separated by spaces): ")

	if not subj_input: 
		sys.exit(	"EXITING OPERATION\n" + 
					"No log files were properly selected"	)

	subj_list = subj_input.split()

	for s in subj_list:
		if not any(s.lower() in x[ :3].lower() for x in log_list):
			sys.exit(	"EXITING OPERATION\n" +
						"Subject " + s + " was not found")

	## More pythonic method but does not allow for specification of error source
	# if not all(any(s.lower() in x.lower() for x in log_list) for s in subj_list):
	# 	sys.exit(	"EXITING OPERATION\n" +
	# 				"INVALID ENTRY OF SUBJECTS"	)

	file_list = []
	for x in log_list:
		if any(s in x for s in subj_list) and '_maintime.txt' in x:
			file_list.append(x)

	run_analysis(file_list)

def run_analysis(arr):
	error_files = []
	for s in arr:
		try:
			print "\n::::: PARSING %s :::::" % s
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