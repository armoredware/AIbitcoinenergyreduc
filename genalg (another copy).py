import csv
from collections import defaultdict
import sqlite3
import sys
from collections import OrderedDict
import os

#print sys.argv
#order of spreadsheet data matters TE under WR and RB

#columns = defaultdict(list) # each value in each column is appended to a list

bin = '%s'%(sys.argv[1:])

#bin='11000010000000000000001000001000000000000001100000000000000000000000000000000000001000010'

with open("miner_LOG.txt", "a+") as logfile2:
    logfile2.write("%s,\n"%bin)


with open("miner_results.txt", "a+") as logfile:
    logfile.write("%s,\n"%bin)


def blacklist(addr):
	penalty = (-30 * 86400)
	#blacklist = {}
	#blacklist.update(addr=penalty) 
	return penalty

def reward_PoS(rPOS):
	reward =  50.0 / len(rPOS)
	return reward

def reward_PoW(rPOW):
	reward =  10.0 / len(rPOW)
	return reward

def reduce_blpenalty():
	pass

miners = []
with open('/root/Desktop/mercy600/blockchainminers.csv', 'r') as fcsv:
    reader = csv.reader(fcsv)
    headers = next(reader)
    for row in reader:
        miners.append(defaultdict(zip(headers, row)))


x= 0
poW= 0
poS=0
with open('/root/Desktop/mercy600/miner_results.txt') as fx:	
	for line in fx:
		y = 0
		pop= line.replace('[','')
		pop = pop.replace('\'','')
		pop = pop.replace(']','')
		pop = pop.replace(',','') 
		pos_miner = 0
		reward_pos = []
		reward_pow = []
		print ("Miner Genome: ")
		for chromosome in pop: 
			if chromosome == '1':
				print (miners[y]['Address'],miners[y]['Balance'])
				if float(miners[y]['Balance']) > 32.0:
					print('PoS Eligible Miner')
					penalty = blacklist(miners[y]['Address'])
					miners[y]['Trust']= str(float(miners[y-1]['Trust']) + penalty)
					pos_miner = pos_miner + 1
					reward_pos.append(miners[y]['Address'])
					
				else:
					reward_pow.append(miners[y]['Address'])
				y=y+1
		if pos_miner > 5:
			poS = poS + 1
			reward = reward_PoS(reward_pos)
			miners[y-1]['Balance'] = str(float(miners[y-1]['Balance']) + reward)
			BC_s= open("chainstatus","a+")
			BC_s.write("Block Mined with PoS\n")
		else:
			poW = poW + 1
			reward = reward_PoW(reward_pow)
			miners[y-1]['Balance'] = str(float(miners[y-1]['Balance']) + reward)
			BC_s= open("chainstatus","a+")
			BC_s.write("Block Mined with PoW\n")
		#x= x + 1
		break



print("Total Mined Blocks:", x)
print("Total Mined with PoS:", poS)
print("Total Mined with PoW:", poW)
logfile.close()

#BC_csv.write("Address,Stake,Trust,Balance\n")

os.remove('miner_results.txt')
os.remove('blockchainminers.csv')
BC_csv= open("blockchainminers.csv","a+")
BC_csv.write("Address,Stake,Trust,Balance\n")
print("Address,Stake,Trust,Balance\n")
z = 0
for m in miners:
	BC_csv.write("%s,%s,%s,%s\n"%(str(miners[z]['Address']),str(miners[z]['Stake']),str(miners[z]['Trust']),str(miners[z]['Balance'])))
	print(miners[z]['Address'],',',miners[z]['Stake'],',',miners[z]['Trust'],',',miners[z]['Balance'],'\n')
	z = z + 1
