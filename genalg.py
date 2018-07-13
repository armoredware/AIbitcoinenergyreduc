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

#bin = "['0000000000000000000000000000000000000000000000000000100000010000000000000010000000000000100010000010100000000000000000000000100000000000100000000000000100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],"

with open("miner_LOG.txt", "a+") as logfile2:
    logfile2.write("%s,\n"%bin)


#with open("miner_results.txt", "a+") as logfile:
#    logfile.write("%s,\n"%bin)


def blacklist(addr):
	#penalty = (-30 * 86400)
	penalty = .25
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
        miners.append(OrderedDict(zip(headers, row)))


x= 0
poW= 0
poS=0


with open('/root/Desktop/mercy600/miner_results.txt','a+') as fx:	
	while x < 1:
		y = 0
		addr_idx_pos = []
		addr_idx_pow = []
		pop= bin.replace('[','')
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
					addr_idx_pos.append(y)
					penalty = float(miners[y]['Trust'])*.25*-1
					miners[y]['Trust']= str(float(miners[y]['Trust']) + penalty)
					pos_miner = pos_miner + 1
					reward_pos.append(miners[y]['Address'])
					
				else:
					print('ONLY PoW Miner')
					addr_idx_pow.append(y)
					reward_pow.append(miners[y]['Address'])
			y=y+1
		if pos_miner > 5:
			poS = poS + 1
			
			reward = reward_PoS(reward_pos)
			for idx in  addr_idx_pos:
				miners[idx]['Balance'] = str(float(miners[idx]['Balance']) + reward)
			BC_s= open("chainstatus","a+")
			BC_s.write("Block Mined with PoS\n")
			BC_s.write("%s\n"%(str(reward_pos)))
			BC_s.write("POW Miners: %s\n"%(str(reward_pow)))
			BC_s.write("POS Miners: %s\n"%(str(reward_pos)))
		else:
			poW = poW + 1
			reward = reward_PoW(reward_pow)
			print(reward, reward_pow)
			for idx in addr_idx_pow:
				miners[idx]['Balance'] = str(float(miners[idx]['Balance']) + reward)
			BC_s= open("chainstatus","a+")
			BC_s.write("Block Mined with PoW\n")
			BC_s.write("POW Miners: %s\n"%(str(reward_pow)))
			BC_s.write("POS Miners: %s\n"%(str(reward_pos)))
			
		x= x + 1
		fx.write("=========BLOCK FORGED=====\n")
		fx.write("Total Mined with PoS: %s\n"%(poS))
		fx.write("Total Mined with PoW: %s\n"%(poW))
		#break



logfile2.close()

#BC_csv.write("Address,Stake,Trust,Balance\n")

#os.remove('miner_results.txt')
os.remove('blockchainminers.csv')
BC_csv= open("blockchainminers.csv","a+")
BC_csv.write("Address,Stake,Trust,Balance\n")
print("Address,Stake,Trust,Balance\n")
z = 0
for m in miners:
	BC_csv.write("%s,%s,%s,%s\n"%(str(miners[z]['Address']),str(miners[z]['Stake']),str(miners[z]['Trust']),str(miners[z]['Balance'])))
	print(miners[z]['Address'],',',miners[z]['Stake'],',',miners[z]['Trust'],',',miners[z]['Balance'],'\n')
	z = z + 1
