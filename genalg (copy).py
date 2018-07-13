import csv
from collections import defaultdict
import sqlite3
import sys

#print sys.argv
#order of spreadsheet data matters TE under WR and RB

columns = defaultdict(list) # each value in each column is appended to a list

bin = '%s'%(sys.argv[1:])

#bin='11000010000000000000001000001000000000000001100000000000000000000000000000000000001000010'


with open("miner_results.txt", "a+") as logfile:
    logfile.write("%s,\n"%bin)


#parse csv file
#def parse_nflcsv():
#	with open('/root/Desktop/mercy520/players.csv') as f:
#		    reader = csv.DictReader(f) # read rows into a dictionary format
#		    for row in reader: # read a row as {column1: value1, column2: value2,...}
#			for (k,v) in row.items(): # go over each column name and value 
#			    columns[k].append(v) # append the value into the appropriate list# based on column k
#			    #print v
#	elif((flex[4]=='TE') and (wr1[5]=='1') and (flex#[6]==wr1[9]) ):	
#		corr_score=corr_score + -0.09
#	elif((flex[4]=='TE')and (wr2[5]=='1') and (flex[6]==wr2#[9])):	
#		corr_score=corr_score + -0.09	
#	elif((flex[4]=='TE')and (wr3[5]=='1') and (flex[6]==wr3#[9])):	
#		corr_score=corr_score + -0.09

#\
