#!/usr/bin/python

import json
import urllib.request
import time

addr_list = []
x = 0
now = str(time.time())
now = now[:10]
print('Current Time:',now)

hres = urllib.request.urlopen('https://blockchain.info/rawaddr/1Lm8nJJDQVCw6sB7SRKw4qW9RC9izDn2Jq')

data = json.loads(hres.read().decode("utf-8"))

print('address: {}'.format(data['address']))
address = data['address']


print('n_tx: {}'.format(data['n_tx']))
n_tx = data['n_tx']
print('total_received: {}'.format(data['total_received']))
print('total_sent: {}'.format(data['total_sent']))
print('final_balance: {}'.format(data['final_balance']))
#print('txs: {}'.format(data['txs'][0]['time']))


#print('outs: {}'.format(data['txs'][0]['out'][0]['addr']))


txs =data['txs']

#is_out = data['txs'][x]['out']
#is_addr = data['txs'][0]['out'][0]['addr'] 
#print(is_addr)
y = 0

while x <  n_tx:
	outs = data['txs'][x]['out'] 
	for out in outs:
		try:
			out_addr = data['txs'][x]['out'][y]['addr']
			spent = data['txs'][x]['out'][y]['spent']
			value = data['txs'][x]['out'][y]['value']
			time = data['txs'][x]['time']
			bc_info_hist = "https://blockchain.info/frombtc?value=%s&currency=USD&time=%s000&textual=false&nosavecurrency=true"%(value,time)
			bc_info_curr = "https://blockchain.info/frombtc?value=%s&currency=USD&time=%s000&textual=false&nosavecurrency=true"%(value,now)
			if out_addr == address:
				#print(bc_info_API)
				get_stake = urllib.request.urlopen(bc_info_hist)
				fiat_invest = get_stake.read().decode("utf-8")
				get_stake = urllib.request.urlopen(bc_info_curr)
				fiat_curr = get_stake.read().decode("utf-8")
				print ("ADDR:",out_addr,"SPENT:",spent,"TIME:", time, "VALUE:", value, "Fiat Investment:", fiat_invest,"Fiat Current:",fiat_curr)
		except Exception as e:
			print (e)
		y = y + 1
	y = 0
	x = x + 1
