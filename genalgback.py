import csv
from collections import defaultdict
import sqlite3
import sys

#print sys.argv
#order of spreadsheet data matters TE under WR and RB

columns = defaultdict(list) # each value in each column is appended to a list

bin = '%s'%(sys.argv[1:])

#bin='11000010000000000000001000001000000000000001100000000000000000000000000000000000001000010'


with open("lineuplog.txt", "a") as logfile:
    logfile.write(bin)


#bin='0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0'

#bin=' 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0'

#bin='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'

#bin=raw_input("Please enter something: ")

#connect to database
conn = sqlite3.connect('/root/Desktop/mercy520/nfl.db')
conn2 = sqlite3.connect('/root/Desktop/mercy520/lineup.db')
print ("Opened database successfully")




#parse csv file
def parse_nflcsv():
	with open('/root/Desktop/mercy520/players.csv') as f:
		    reader = csv.DictReader(f) # read rows into a dictionary format
		    for row in reader: # read a row as {column1: value1, column2: value2,...}
			for (k,v) in row.items(): # go over each column name and value 
			    columns[k].append(v) # append the value into the appropriate list# based on column k
			    #print v
#create nfl db    		            
def create_dbNFL():
	try:	
		conn.execute("DROP TABLE NFL;")
		print("Table Dropped!")
	except:
		print("table won't drop")	
	
	try:
    	    conn.execute('''CREATE TABLE NFL
            (ID INTEGER PRIMARY KEY       AUTOINCREMENT,
            Name            TEXT     NOT NULL,   
	    NewPts          TEXT     NOT NULL,
            Salary          TEXT     NOT NULL,
            Position        TEXT     NOT NULL,
	    Dominance	   TEXT     NOT NULL,
	    teamAbbrev      TEXT     NOT NULL,
	    scoringLvl      TEXT    NOT NULL,
	    isHome          TEXT    NOT NULL,
	    oppTeam	   TEXT    NOT NULL);''')
           
    	    print ("Table created successfully")
	except:
    	    print("Table Already Setup")

#create lineup db
def create_dbLINEUP():
	#try:	
	#	#conn2.execute("DROP TABLE LINEUP;")
	#	print("Table Exists!")
	#except:
	#	print("table won't drop")	
	
	try:
    	    conn2.execute('''CREATE TABLE LINEUP
            (ID INTEGER PRIMARY KEY       AUTOINCREMENT,
            QB            TEXT     NOT NULL,   
	    RB1           TEXT     NOT NULL,
            RB2           TEXT     NOT NULL,
            WR1           TEXT     NOT NULL,
	    WR2           TEXT     NOT NULL,
	    WR3           TEXT     NOT NULL,
	    TE            TEXT    NOT NULL,
	    Flex          TEXT    NOT NULL,
	    DST           TEXT    NOT NULL,
	    corrScore     TEXT     NOT NULL,
	    homeScore     TEXT     NOT NULL,
	    spreadScore   TEXT    NOT NULL,
	    totalScore    TEXT    NOT NULL,
	    totalCost     TEXT    NOT NULL,
	    projPts       TEXT    NOT NULL);''')
           
    	    print ("Table created successfully")
	except:
    	    print("Table Already Setup")

#convert csv to db
def csv_to_db(count):
	try:
		#print [count]
		#print "success"
		conn.execute("INSERT INTO NFL(Name,NewPts,Salary,Position,Dominance,teamAbbrev,scoringLvl,isHome,oppTeam)\
			VALUES (?,?,?,?,?,?,?,?,?)",(columns['Name'][count],columns['Pts'][count],columns['Salary'][count],columns['Position'][count],3,columns['Team'][count],0,0,0))#add values
	except:
		print "fail" ,[count]
	
	
query="SELECT id, Name, NewPts, Salary, Position, Dominance, teamAbbrev, scoringLvl, isHome, oppTeam from NFL WHERE id LIKE '4'"  

#view query for testing
def view_nflcsv(query):
    cursor = conn.execute( query )
    for row in cursor:
       print ("ID = %s")%(row[0])
       print ("Name = %s")%(row[1])
       print ("NewPts = %s")%(row[2])
       print ("Salary = %s")%(row[3])
       print ("Position = %s")%(row[4])
       print ("Dominance = %s")%(row[5])
       print ("teamAbbrev = %s")%(row[6])
       print ("scoringLvl = %s")%(row[7])
       print ("isHome = %s")%(row[8])
       print ("oppTeam = %s")%(row[9])

#always have to update teams away, home is the order
dom_team = ['JAX','NEP','MIN','PHI']
#['TBB','MIA','DET','CHI','JAX','CLE','BAL','GBP','ARI','HOU','LAR','MIN','WAS','NOS','KCC','NYG','BUF','LAC','CIN','DEN','NEP','OAK','PHI','DAL','ATL','SEA']
#dom_team =['NEP','TBB','BUF','CIN','NYJ','CLE','SFO','IND','TEN','MIA','LAC','NYG','ARI','PHI','JAX','PHI','SEA','LAR','BAL','OAK','GBP','DAL','KCC','HOU','MIN','CHI']

#dom_team = ['PHI','CAR','MIA','ATL','CHI','BAL','CLE','HOU','GBP','MIN','DET','NOS','NEP','NYJ','SFO','WAS','TBB','ARI','LAR','JAX','PIT','KCC','LAC','OAK','NYG','DEN','IND','TEN']


#['CHI','GBP','NOS','MIA','TEN','HOU','JAC','NYJ','CAR','NEP','DET','MIN','BUF','ATL','PIT','BAL','CIN','CLE','LAR','DAL','PHI','LAC','NYG','TBB','SFO','ARI','OAK','DEN','IND','SEA']

#set domainance level for each position player
def set_dominance(pos,team):
	query = "SELECT id, Name, NewPts, Salary, Position, Dominance, teamAbbrev from NFL WHERE Position Like '%s' AND teamAbbrev Like '%s'"%(pos,team)
	hi=0
	old_id = 0
	isset_POS2='false'
	cursor = conn.execute( query )
	for row in cursor:		
		dom='1'
		dom2='2'
		dom3='3'
		cur_id=row[0]		
		up_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom, cur_id)
		up_old_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom, old_id)
		if(row[5]=='3' and row[4]=='RB'):
			up_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom2, cur_id)
			conn.execute(up_dom)
			conn.commit() 		
		if (row[5]=='3' and hi == 0 or ((row[5]=='2' or row[5]=='3') and row[4]=='RB' and hi==0) ): #first pass
			up_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom, cur_id)
			hi = float(row[2])
			old_id = row[0]
             		conn.execute(up_dom)
			conn.commit()   
		elif (float(row[2])<hi and isset_POS2=='false'):
			up_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom2, cur_id)
			conn.execute(up_dom)
			conn.commit()
			isset_POS2 = 'true'			
		elif(float(row[2])>hi):	 	
			up_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom, cur_id)
			conn.execute(up_dom)
			conn.commit()
			up_old_dom="UPDATE NFL SET Dominance = '%s' WHERE ID =%d"%(dom2, old_id)
			conn.execute(up_old_dom)
			conn.commit()
		#print row		
			
#set home teams
def set_home(team):
	query = "SELECT id, Name, NewPts, Salary, Position, Dominance, teamAbbrev, scoringLvl, isHome from NFL WHERE teamAbbrev LIKE '%s'"%(team)
	cursor = conn.execute( query )
	for row in cursor:	
		if (row[6]==team):	
			up_home="UPDATE NFL SET isHome = '%s' WHERE ID =%d"%('1',row[0])
			conn.execute(up_home)
			conn.commit() 
			#print row	
#set away teams
def set_away(team,ateam):
	query = "SELECT id, Name, NewPts, Salary, Position, Dominance, teamAbbrev, scoringLvl, isHome, oppTeam from NFL WHERE teamAbbrev LIKE '%s'"%(team)
	cursor = conn.execute( query )
	for row in cursor:	
		if (row[6]==team):	
			up_home="UPDATE NFL SET oppTeam = '%s' WHERE ID =%d"%(ateam,row[0])
			conn.execute(up_home)
			conn.commit() 
			#print row		
		
	

#set_scoringlvl

create_dbNFL()	
create_dbLINEUP()
count = 0
lineup = []
for x in bin:
     parse_nflcsv()
     if (x == '1'):	
         #print("NameDK[%s]")%count		    
	print("Added:", columns['Name'][count],columns['Pts'][count],columns['Salary'][count],columns['Position'][count], columns['Team'][count])
        lineup.append(count+1)#was count +1
     if (x == '0' or x == '1'):
	  csv_to_db(count)
          count = count + 1 
     #print lineup

conn.commit()
conn2.commit()

team_count=0
pos_count=0
try:
	for x in dom_team:
		set_dominance('WR',dom_team[team_count])
		set_dominance('RB',dom_team[team_count])
		if ((team_count+1)%2==0):
			set_home(dom_team[team_count])
			set_away(dom_team[team_count],dom_team[team_count-1])
		else:
			set_away(dom_team[team_count],dom_team[team_count+1])
		team_count=team_count + 1
		#pos_count=pos_count + 1
except:
	print"end of row"


view_nflcsv(query)


	
        	 
#prefer lineup RB and DST same team
#prefer lineups with < 3 players from same team
#only home dst unless value > x
#prefer higher scoring games WR/RB/QB
#only home te unless value > x
#score lineup in terms of strength 
#prefer opposing WR same game from QB/WR combo

def lineup_corr(lu):
	print lu
	corr_score = 0
	qb = []
	te = []
	dst = []
	wr1 = []
	wr2 = []
	wr3 = []
	flex = []
	rb1 = []
	rb2 = []	
		
	query = "SELECT id, Name, NewPts, Salary, Position, Dominance, teamAbbrev, scoringLvl, isHome, oppTeam from NFL WHERE id =%d OR id=%d OR id=%d OR id=%d OR id=%d OR id=%d OR id=%d OR id=%d OR id=%d"%(lu[0],lu[1],lu[2],lu[3],lu[4],lu[5],lu[6],lu[7],lu[8])
	print query
	cursor = conn.execute( query )
	qb_set = 0	
	wr1_set = 0
	wr2_set = 0
	wr3_set = 0
	rb1_set = 0
	rb2_set = 0
        te_set = 0
	flex_set = 0
	dst_set = 0
	#while(qb_set == 0 or wr1_set == 0 or wr2_set == 0 or wr3_set == 0 or rb1_set == 0 or rb2_set == 0 or te_set == 0  or flex_set == 0 or dst_set == 0):	
	for row in cursor:
	       		#print ("%s %s %s %s %s %s %s")%(row[0],row[1],row[4],row[5],row[6],row[8],row[9])
			if (row[4]=='QB'):
				qb = row    
				qb_set = 1  
			if (row[4]=='RB'and rb1_set == 0):
				rb1 = row 
				rb1_set = 1
			elif (row[4]=='RB'and rb1_set == 1 and rb2_set == 0 and flex_set==0):
                                print ('rb2 found')
				rb2 = row 
				rb2_set = 1

			elif (row[4]=='WR' and wr1_set == 0):
				wr1 = row 
				wr1_set = 1

			elif (row[4]=='WR' and wr1_set == 1 and wr2_set == 0):
				wr2 = row
				wr2_set = 1 

			elif (row[4]=='WR' and wr1_set == 1 and wr2_set == 1 and wr3_set== 0 ):
				wr3 = row 
				wr3_set = 1
	
			elif (row[4]=='TE'and te_set == 0):
				te = row
				te_set = 1 
			elif ((row[4]=='WR') and wr3_set == 1 and flex_set==0):
				flex = row
				flex_set = 1 
			elif ((row[4]=='RB') and rb2_set == 1 and flex_set==0):
				flex = row
				flex_set = 1 
			elif ((row[4]=='TE') and te_set == 1 and flex_set==0):
				flex = row
				flex_set = 1 
			
			if (row[4]=='DST'):
				dst = row 
				dst_set = 1
		
						

			#print ("teamAbbrev = %s")%(row[6])
	       		#print ("scoringLvl = %s")%(row[7])
	       		#print ("isHome = %s")%(row[8])
	       		#print ("oppTeam = %s")%(row[9])	
	
	
	print qb[1]
	print rb1[1]
	print rb2[1]
	print wr1[1]
	print wr2[1]
	print wr3[1]
	print te[1]
	print flex[1]
	print dst[1]

	#QB  and DST opp teams negative
	if (qb[9]==dst[6]): 	
		corr_score=corr_score + -0.46

	#QB and WR2 same team is positive
	if ((qb[6]==wr1[6]) and wr1[5]=='2'):	
		corr_score=corr_score + 0.39
	elif ((qb[6]==wr2[6]) and wr2[5]=='2'):
		corr_score=corr_score + 0.39
	elif ((qb[6]==wr3[6]) and wr3[5]=='2'):
		corr_score=corr_score + 0.39
	elif ((qb[6]==flex[6]) and flex[4]=='WR' and flex[5]=='2'):
		corr_score=corr_score + 0.39

	#QB and WR3 same team is positive
	if ((qb[6]==wr1[6]) and wr1[5]=='3'):	
		corr_score=corr_score + 0.35
	elif ((qb[6]==wr2[6]) and wr2[5]=='3'):
		corr_score=corr_score + 0.35
	elif ((qb[6]==wr3[6]) and wr3[5]=='3'):
		corr_score=corr_score + 0.35
	elif ((qb[6]==flex[6]) and flex[4]=='WR' and flex[5]=='3'):
		corr_score=corr_score + 0.35

	#QB and WR1 same team is positive
	if ((qb[6]==wr1[6]) and wr1[5]=='1'):	
		corr_score=corr_score + 0.34
	elif ((qb[6]==wr2[6]) and wr2[5]=='1'):
		corr_score=corr_score + 0.34
	elif ((qb[6]==wr3[6]) and wr3[5]=='1'):
		corr_score=corr_score + 0.34
	elif ((qb[6]==flex[6]) and flex[4]=='WR' and flex[5]=='1'):
		corr_score=corr_score + 0.34

	#RB1 and RB1 opposing teams is negative
	if ((rb1[5]=='1' and rb2[5]=='1') and (rb1[6]==rb2[9])):
		corr_score=corr_score + -0.31
	elif ((rb1[5]=='1' and (flex[5]=='1' and flex[4]=='RB')) and (rb1[6]==flex[9])):
		corr_score=corr_score + -0.31
	elif ((rb2[5]=='1' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + -0.31



	#RB2 and opposing DST is negative
	if ((rb1[5]=='2') and (rb1[6]==dst[9])):
		corr_score=corr_score + -0.23
	elif ((flex[5]=='2' and flex[4]=='RB') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.23
	elif ((rb2[5]=='2') and (rb2[6]==dst[9])):
		corr_score=corr_score + -0.23

	#QB1 and RB2 same team is positive
	if((qb[6]==rb1[6]) and rb1[5]=='2'):
		corr_score=corr_score + 0.21
	elif((qb[6]==rb2[6]) and rb2[5]=='2'):
		corr_score=corr_score + 0.21
	elif((qb[6]==flex[6]) and (flex[4]=='RB' and flex[5]=='2')):
		corr_score=corr_score + 0.21


	#WR1 and DST opp team is negative
	if ((wr1[5]=='1') and (wr1[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((flex[5]=='1' and flex[4]=='WR') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((wr3[5]=='1') and (wr3[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((wr2[5]=='1') and (wr2[6]==dst[9])):
		corr_score=corr_score + -0.19

	#WR3 and DST opp team is negative
	if ((wr1[5]=='3') and (wr1[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((flex[5]=='3' and flex[4]=='WR') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((wr3[5]=='3') and (wr3[6]==dst[9])):
		corr_score=corr_score + -0.19
	elif ((wr2[5]=='3') and (wr2[6]==dst[9])):
		corr_score=corr_score + -0.18

	#WR2 and DST opp team is negative
	if ((wr1[5]=='3') and (wr1[6]==dst[9])):
		corr_score=corr_score + -0.16
	elif ((flex[5]=='3' and flex[4]=='WR') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.16
	elif ((wr3[5]=='3') and (wr3[6]==dst[9])):
		corr_score=corr_score + -0.16
	elif ((wr2[5]=='3') and (wr2[6]==dst[9])):
		corr_score=corr_score + -0.16
	
	
	#TE and QB1 same team positive
	if(te[6]==qb[6]):	
		corr_score=corr_score + 0.16
	elif((flex[4]=='TE') and (flex[6]==qb[6])):
		corr_score=corr_score + 0.16
	
	#RB1 and WR3 same team negative	
	if ((rb1[5]=='1' and wr1[5]=='3') and (rb1[6]==wr1[6])):
		corr_score=corr_score + -0.14
	elif ((rb1[5]=='1' and wr2[5]=='3') and (rb1[6]==wr2[6])):
		corr_score=corr_score + -0.14
	elif ((rb1[5]=='1' and wr3[5]=='3') and (rb1[6]==wr3[6])):
		corr_score=corr_score + -0.14
	elif ((rb1[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.14
	if ((rb2[5]=='1' and wr1[5]=='3') and (rb2[6]==wr1[6])):
		corr_score=corr_score + -0.14
	elif ((rb2[5]=='1' and wr2[5]=='3') and (rb2[6]==wr2[6])):
		corr_score=corr_score + -0.14
	elif ((rb2[5]=='1' and wr3[5]=='3') and (rb2[6]==wr3[6])):
		corr_score=corr_score + -0.14
	elif ((rb2[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.14
	elif ((wr1[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.14
	elif ((wr2[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.14
	elif ((wr3[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.14

	
	#WR2 and WR1 same team is positive
	if ((wr1[5]=='1' and wr2[5]=='2') and (wr1[6]==wr2[6])):
		corr_score=corr_score + 0.13
	elif ((wr1[5]=='1' and wr3[5]=='2') and (wr1[6]==wr3[6])):
		corr_score=corr_score + 0.13
	elif ((wr1[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + 0.13
	elif ((wr2[5]=='1' and wr3[5]=='2') and (wr2[6]==wr3[6])):
		corr_score=corr_score + 0.13
	elif ((wr2[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + 0.13
	elif ((wr3[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + 0.13
	elif ((wr1[5]=='2' and wr2[5]=='1') and (wr1[6]==wr2[6])):
		corr_score=corr_score + 0.13
	elif ((wr1[5]=='2' and wr3[5]=='1') and (wr1[6]==wr3[6])):
		corr_score=corr_score + 0.13
	elif ((wr1[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + 0.13
	elif ((wr2[5]=='2' and wr3[5]=='1') and (wr2[6]==wr3[6])):
		corr_score=corr_score + 0.13
	elif ((wr2[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + 0.13
	elif ((wr3[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + 0.13
	
	#TE and QB1 opp team negative
	if(te[6]==qb[9]):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE') and (flex[6]==qb[9])):
		corr_score=corr_score + -0.12	
	
	#TE1 and RB1 same team is negative
	if((te[6]==rb1[6])and rb1[5]=='1'):	
		corr_score=corr_score + -0.12
	elif((te[6]==rb2[6])and rb2[5]=='1'):	
		corr_score=corr_score + -0.12
	elif((te[6]==flex[6])and (flex[5]=='1' and flex[4]=='RB')):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE') and (rb1[5]=='1') and (flex[6]==rb1[6]) ):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE')and (rb2[5]=='1') and (flex[6]==rb2[6])):	
		corr_score=corr_score + -0.12	

	#WR2 and TE1 same team is negative
	if((te[6]==wr1[6])and wr1[5]==1):	
		corr_score=corr_score + -0.12
	elif((te[6]==wr2[6])and wr2[5]==1):	
		corr_score=corr_score + -0.12
	elif((te[6]==wr3[6])and wr3[5]==1):	
		corr_score=corr_score + -0.12
	elif((te[6]==flex[6])and (flex[5]==1 and flex[4]=='WR')):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE') and (wr1[5]==1) and (flex[6]==wr1[6]) ):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE')and (wr2[5]==1) and (flex[6]==wr2[6])):	
		corr_score=corr_score + -0.12	
	elif((flex[4]=='TE')and (wr3[5]==1) and (flex[6]==wr3[6])):	
		corr_score=corr_score + -0.12	

	#RB2 and RB1 same team is negative
	if ((rb1[5]=='1' and rb2[5]=='2') and (rb1[6]==rb2[6])):
		corr_score=corr_score + -0.02
	elif ((rb1[5]=='2' and rb2[5]=='1') and (rb1[6]==rb2[6])):
		corr_score=corr_score + -0.02
	elif ((rb1[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((rb2[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.02	
	elif ((rb1[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((rb2[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.02	
	

	
	#WR1 and WR3 same team is negative
	if ((wr1[5]=='1' and wr2[5]=='3') and (wr1[6]==wr2[6])):
		corr_score=corr_score + -0.02
	elif ((wr1[5]=='3' and wr2[5]=='1') and (wr1[6]==wr2[6])):
		corr_score=corr_score + -0.02
	elif ((wr1[5]=='1' and wr3[5]=='3') and (wr1[6]==wr3[6])):
		corr_score=corr_score + -0.02
	elif ((wr1[5]=='3' and wr3[5]=='1') and (wr1[6]==wr3[6])):
		corr_score=corr_score + -0.02
	elif ((wr1[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((wr1[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((wr2[5]=='1' and wr3[5]=='3') and (wr2[6]==wr3[6])):
		corr_score=corr_score + -0.02
	elif ((wr2[5]=='3' and wr3[5]=='1') and (wr2[6]==wr3[6])):
		corr_score=corr_score + -0.02
	elif ((wr2[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr2[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((wr2[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr2[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((wr3[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + -0.02
	elif ((wr3[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + -0.02

	#WR1 and WR3 opposing team is negative
	if ((wr1[5]=='1' and wr2[5]=='3') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and wr2[5]=='1') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='1' and wr3[5]=='3') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and wr3[5]=='1') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='1' and wr3[5]=='3') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='3' and wr3[5]=='1') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.01
	elif ((wr3[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.01
	elif ((wr3[5]=='3' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.01

	#WR2 and WR3 same team is negative
	if ((wr1[5]=='2' and wr2[5]=='3') and (wr1[6]==wr2[6])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and wr2[5]=='2') and (wr1[6]==wr2[6])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='2' and wr3[5]=='3') and (wr1[6]==wr3[6])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and wr3[5]=='2') and (wr1[6]==wr3[6])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + -0.01
	elif ((wr1[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr1[6]==flex[6])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='2' and wr3[5]=='3') and (wr2[6]==wr3[6])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='3' and wr3[5]=='2') and (wr2[6]==wr3[6])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr2[6]==flex[6])):
		corr_score=corr_score + -0.01
	elif ((wr2[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr2[6]==flex[6])):
		corr_score=corr_score + -0.01
	elif ((wr3[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + -0.01
	elif ((wr3[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[6])):
		corr_score=corr_score + -0.01
	

	#WR3 and TE1 same team is negative
	if((te[6]==wr1[6])and wr1[5]=='3'):	
		corr_score=corr_score + -0.12
	elif((te[6]==wr2[6])and wr2[5]=='3'):	
		corr_score=corr_score + -0.12
	elif((te[6]==wr3[6])and wr3[5]=='3'):	
		corr_score=corr_score + -0.12
	elif((te[6]==flex[6])and (flex[5]=='3' and flex[4]=='WR')):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE') and (wr1[5]=='3') and (flex[6]==wr1[6]) ):	
		corr_score=corr_score + -0.12
	elif((flex[4]=='TE')and (wr2[5]=='3') and (flex[6]==wr2[6])):	
		corr_score=corr_score + -0.12	
	elif((flex[4]=='TE')and (wr3[5]=='3') and (flex[6]==wr3[6])):	
		corr_score=corr_score + -0.12	

	#WR3 and opposing WR3 is positive
	if ((wr1[5]=='3' and wr2[5]=='3') and (wr1[6]==wr2[9])):
		corr_score=corr_score + 0.12
	elif ((wr1[5]=='3' and wr3[5]=='3') and (wr1[6]==wr3[9])):
		corr_score=corr_score + 0.12
	elif ((wr1[5]=='3' and (flex[5]=='3' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + 0.12
	elif ((wr2[5]=='3' and wr3[5]=='3') and (wr2[6]==wr3[9])):
		corr_score=corr_score + 0.12
	elif ((wr2[5]=='3' and (flex[5]=='3' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + 0.12
	elif ((wr3[5]=='3' and (flex[5]=='3' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + 0.12


	#WR1 and qb opposite teams is negative
	if ((qb[6]==wr1[9]) and wr1[5]=='1'):	
		corr_score=corr_score + -0.11
	elif ((qb[6]==wr2[9]) and wr2[5]=='1'):
		corr_score=corr_score + -0.11
	elif ((qb[6]==wr3[9]) and wr3[5]=='1'):
		corr_score=corr_score + -0.11
	elif ((qb[6]==flex[9]) and flex[4]=='WR' and flex[5]=='1'):
		corr_score=corr_score + -0.11

	#WR2 and TE1 opp team is positive
	if((te[6]==wr1[9])and wr1[5]=='2'):	
		corr_score=corr_score + 0.11
	elif((te[6]==wr2[9])and wr2[5]=='2'):	
		corr_score=corr_score + 0.11
	elif((te[6]==wr3[9])and wr3[5]=='2'):	
		corr_score=corr_score + 0.11
	elif((te[6]==flex[9])and (flex[5]=='2' and flex[4]=='WR')):	
		corr_score=corr_score + 0.11
	elif((flex[4]=='TE') and (wr1[5]=='2') and (flex[6]==wr1[9]) ):	
		corr_score=corr_score + 0.11
	elif((flex[4]=='TE')and (wr2[5]=='2') and (flex[6]==wr2[9])):	
		corr_score=corr_score + 0.11	
	elif((flex[4]=='TE')and (wr3[5]=='2') and (flex[6]==wr3[9])):	
		corr_score=corr_score + 0.11	


	#RB1 and opposing DST is negative
	if ((rb1[5]=='1') and (rb1[6]==dst[9])):
		corr_score=corr_score + -0.1
	elif ((flex[5]=='1' and flex[4]=='RB') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.1
	elif ((rb2[5]=='1') and (rb2[6]==dst[9])):
		corr_score=corr_score + -0.1

	#WR3 and qb opposite teams is negative
	if ((qb[6]==wr1[9]) and wr1[5]=='3'):	
		corr_score=corr_score + 0.1
	elif ((qb[6]==wr2[9]) and wr2[5]=='3'):
		corr_score=corr_score + 0.1
	elif ((qb[6]==wr3[9]) and wr3[5]=='3'):
		corr_score=corr_score + 0.1
	elif ((qb[6]==flex[9]) and flex[4]=='WR' and flex[5]=='3'):
		corr_score=corr_score + 0.1

	

	#TE and TE opp team negative
	if((flex[4]=='TE') and (flex[6]==te[9])):	
		corr_score=corr_score - 0.1
	

	#QB  and DST same teams pos
	if (qb[6]==dst[6]): 	
		corr_score=corr_score + 0.09


	#RB2 and DST same team is pos
	if ((rb1[5]=='2') and (rb1[6]==dst[6])):
		corr_score=corr_score + 0.09
	elif ((flex[5]=='2' and flex[4]=='RB') and (flex[6]==dst[6])):
		corr_score=corr_score + 0.09
	elif ((rb2[5]=='2') and (rb2[6]==dst[6])):
		corr_score=corr_score + 0.09




	#WR1 and DST same team is pos
	if ((wr1[5]=='1') and (wr1[6]==dst[6])):
		corr_score=corr_score + 0.09
	elif ((flex[5]=='1' and flex[4]=='WR') and (flex[6]==dst[6])):
		corr_score=corr_score + 0.09
	elif ((wr3[5]=='1') and (wr3[6]==dst[6])):
		corr_score=corr_score + 0.09
	elif ((wr2[5]=='1') and (wr2[6]==dst[6])):
		corr_score=corr_score + 0.09


	#QB1 and RB1 same team is positive
	if((qb[6]==rb1[6]) and rb1[5]=='1'):
		corr_score=corr_score + 0.09
	elif((qb[6]==rb2[6]) and rb2[5]=='1'):
		corr_score=corr_score + 0.09
	elif((qb[6]==flex[6]) and (flex[4]=='RB' and flex[5]=='1')):
		corr_score=corr_score + 0.09

	#WR2 and qb opposite teams is positive
	if ((qb[6]==wr1[9]) and wr1[5]=='2'):	
		corr_score=corr_score + 0.09
	elif ((qb[6]==wr2[9]) and wr2[5]=='2'):
		corr_score=corr_score + 0.09
	elif ((qb[6]==wr3[9]) and wr3[5]=='2'):
		corr_score=corr_score + 0.09
	elif ((qb[6]==flex[9]) and flex[4]=='WR' and flex[5]=='2'):
		corr_score=corr_score + 0.09

	#WR1 and opp team te is negative
	if((te[6]==wr1[9])and wr1[5]=='1'):	
		corr_score=corr_score + -0.09
	elif((te[6]==wr2[9])and wr2[5]=='1'):	
		corr_score=corr_score + -0.09
	elif((te[6]==wr3[9])and wr3[5]=='1'):	
		corr_score=corr_score + -0.09
	elif((te[6]==flex[9])and (flex[5]=='1' and flex[4]=='WR')):	
		corr_score=corr_score + -0.09
	elif((flex[4]=='TE') and (wr1[5]=='1') and (flex[6]==wr1[9]) ):	
		corr_score=corr_score + -0.09
	elif((flex[4]=='TE')and (wr2[5]=='1') and (flex[6]==wr2[9])):	
		corr_score=corr_score + -0.09	
	elif((flex[4]=='TE')and (wr3[5]=='1') and (flex[6]==wr3[9])):	
		corr_score=corr_score + -0.09


	#WR2 and WR3 opp team is pos
	if ((wr1[5]=='2' and wr2[5]=='3') and (wr1[6]==wr2[9])):
		corr_score=corr_score + 0.09
	elif ((wr1[5]=='3' and wr2[5]=='2') and (wr1[6]==wr2[9])):
		corr_score=corr_score + 0.09
	elif ((wr1[5]=='2' and wr3[5]=='3') and (wr1[6]==wr3[9])):
		corr_score=corr_score + 0.09
	elif ((wr1[5]=='3' and wr3[5]=='2') and (wr1[6]==wr3[9])):
		corr_score=corr_score + 0.09
	elif ((wr1[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + 0.09
	elif ((wr1[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + 0.09
	elif ((wr2[5]=='2' and wr3[5]=='3') and (wr2[6]==wr3[9])):
		corr_score=corr_score + 0.09
	elif ((wr2[5]=='3' and wr3[5]=='2') and (wr2[6]==wr3[9])):
		corr_score=corr_score + 0.09
	elif ((wr2[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + 0.09
	elif ((wr2[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + 0.09
	elif ((wr3[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + 0.09
	elif ((wr3[5]=='3' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + 0.09

	#TE and DST same team pos
	if(te[6]==dst[6]):	
		corr_score=corr_score + 0.08
	elif((flex[4]=='TE') and (flex[6]==dst[6])):
		corr_score=corr_score + 0.08	


	#TE1 and RB2 same team is negative
	if((te[6]==rb1[6])and rb1[5]=='2'):	
		corr_score=corr_score + -0.08
	elif((te[6]==rb2[6])and rb2[5]=='2'):	
		corr_score=corr_score + -0.08
	elif((te[6]==flex[6])and (flex[5]=='2' and flex[4]=='RB')):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE') and (rb1[5]=='2') and (flex[6]==rb1[6]) ):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE')and (rb2[5]=='2') and (flex[6]==rb2[6])):	
		corr_score=corr_score + -0.08		


	#RB2 and WR1 same team pos	
	if ((rb1[5]=='2' and wr1[5]=='1') and (rb1[6]==wr1[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and wr2[5]=='1') and (rb1[6]==wr2[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and wr3[5]=='1') and (rb1[6]==wr3[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + 0.08
	if ((rb2[5]=='2' and wr1[5]=='1') and (rb2[6]==wr1[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and wr2[5]=='1') and (rb2[6]==wr2[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and wr3[5]=='1') and (rb2[6]==wr3[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr1[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr2[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr3[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08

	#RB2 and WR2 same team neg	
	if ((rb1[5]=='2' and wr1[5]=='2') and (rb1[6]==wr1[6])):
		corr_score=corr_score + -0.08
	elif ((rb1[5]=='2' and wr2[5]=='2') and (rb1[6]==wr2[6])):
		corr_score=corr_score + -0.08
	elif ((rb1[5]=='2' and wr3[5]=='2') and (rb1[6]==wr3[6])):
		corr_score=corr_score + -0.08
	elif ((rb1[5]=='2' and (flex[5]=='2' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.08
	if ((rb2[5]=='2' and wr1[5]=='2') and (rb2[6]==wr1[6])):
		corr_score=corr_score + -0.08
	elif ((rb2[5]=='2' and wr2[5]=='2') and (rb2[6]==wr2[6])):
		corr_score=corr_score + -0.08
	elif ((rb2[5]=='2' and wr3[5]=='2') and (rb2[6]==wr3[6])):
		corr_score=corr_score + -0.08
	elif ((rb2[5]=='2' and (flex[5]=='2' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='2' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.08
	elif ((wr2[5]=='2' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.08
	elif ((wr3[5]=='2' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.08

	#RB2 and WR3 same team pos	
	if ((rb1[5]=='2' and wr1[5]=='3') and (rb1[6]==wr1[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and wr2[5]=='3') and (rb1[6]==wr2[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and wr3[5]=='3') and (rb1[6]==wr3[6])):
		corr_score=corr_score + 0.08
	elif ((rb1[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + 0.08
	if ((rb2[5]=='2' and wr1[5]=='3') and (rb2[6]==wr1[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and wr2[5]=='3') and (rb2[6]==wr2[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and wr3[5]=='3') and (rb2[6]==wr3[6])):
		corr_score=corr_score + 0.08
	elif ((rb2[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr1[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr2[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	elif ((wr3[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + 0.08
	
	

	#WR1 and TE same team is neg
	if((te[6]==wr1[6])and wr1[5]=='1'):	
		corr_score=corr_score + -0.08
	elif((te[6]==wr2[6])and wr2[5]=='1'):	
		corr_score=corr_score + -0.08
	elif((te[6]==wr3[6])and wr3[5]=='1'):	
		corr_score=corr_score + -0.08
	elif((te[6]==flex[6])and (flex[5]=='1' and flex[4]=='WR')):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE') and (wr1[5]=='1') and (flex[6]==wr1[6]) ):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE')and (wr2[5]=='1') and (flex[6]==wr2[6])):	
		corr_score=corr_score + -0.08	
	elif((flex[4]=='TE')and (wr3[5]=='1') and (flex[6]==wr3[6])):	
		corr_score=corr_score + -0.08	

	#WR3 and TE same team is neg
	if((te[6]==wr1[6])and wr1[5]=='3'):	
		corr_score=corr_score + -0.08
	elif((te[6]==wr2[6])and wr2[5]=='3'):	
		corr_score=corr_score + -0.08
	elif((te[6]==wr3[6])and wr3[5]=='3'):	
		corr_score=corr_score + -0.08
	elif((te[6]==flex[6])and (flex[5]=='3' and flex[4]=='WR')):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE') and (wr1[5]=='3') and (flex[6]==wr1[6]) ):	
		corr_score=corr_score + -0.08
	elif((flex[4]=='TE')and (wr2[5]=='3') and (flex[6]==wr2[6])):	
		corr_score=corr_score + -0.08	
	elif((flex[4]=='TE')and (wr3[5]=='3') and (flex[6]==wr3[6])):	
		corr_score=corr_score + -0.08	


	#WR2 and WR1 opp team is neg
	if ((wr1[5]=='2' and wr2[5]=='1') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='1' and wr2[5]=='2') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='2' and wr3[5]=='1') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='1' and wr3[5]=='2') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.08
	elif ((wr1[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.08
	elif ((wr2[5]=='2' and wr3[5]=='1') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.08
	elif ((wr2[5]=='1' and wr3[5]=='2') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.08
	elif ((wr2[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.08
	elif ((wr2[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.08
	elif ((wr3[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.08
	elif ((wr3[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.08

	#RB1 and WR1 same team neg	
	if ((rb1[5]=='1' and wr1[5]=='1') and (rb1[6]==wr1[6])):
		corr_score=corr_score + -0.07
	elif ((rb1[5]=='1' and wr2[5]=='1') and (rb1[6]==wr2[6])):
		corr_score=corr_score + -0.07
	elif ((rb1[5]=='1' and wr3[5]=='1') and (rb1[6]==wr3[6])):
		corr_score=corr_score + -0.07
	elif ((rb1[5]=='1' and (flex[5]=='1' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.07
	if ((rb2[5]=='1' and wr1[5]=='1') and (rb2[6]==wr1[6])):
		corr_score=corr_score + -0.07
	elif ((rb2[5]=='1' and wr2[5]=='1') and (rb2[6]==wr2[6])):
		corr_score=corr_score + -0.07
	elif ((rb2[5]=='1' and wr3[5]=='1') and (rb2[6]==wr3[6])):
		corr_score=corr_score + -0.07
	elif ((rb2[5]=='1' and (flex[5]=='1' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.07
	elif ((wr1[5]=='1' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.07
	elif ((wr2[5]=='1' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.07
	elif ((wr3[5]=='1' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.07


	#TE and DST opp team neg
	if(te[6]==dst[9]):	
		corr_score=corr_score + -0.06
	elif((flex[4]=='TE') and (flex[6]==dst[9])):
		corr_score=corr_score + -0.06	



	#TE1 and RB1 opp team is pos
	if((te[6]==rb1[9])and rb1[5]=='1'):	
		corr_score=corr_score + 0.06
	elif((te[6]==rb2[9])and rb2[5]=='1'):	
		corr_score=corr_score + 0.06
	elif((te[6]==flex[9])and (flex[5]=='1' and flex[4]=='RB')):	
		corr_score=corr_score + 0.06
	elif((flex[4]=='TE') and (rb1[5]=='1') and (flex[6]==rb1[9]) ):	
		corr_score=corr_score + 0.06
	elif((flex[4]=='TE')and (rb2[5]=='1') and (flex[6]==rb2[9])):	
		corr_score=corr_score + 0.06		


	#WR2 and opposing WR2 is neg
	if ((wr1[5]=='2' and wr2[5]=='2') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.6
	elif ((wr1[5]=='2' and wr3[5]=='2') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.6
	elif ((wr1[5]=='2' and (flex[5]=='2' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.6
	elif ((wr2[5]=='2' and wr3[5]=='2') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.6
	elif ((wr2[5]=='2' and (flex[5]=='2' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.6
	elif ((wr3[5]=='2' and (flex[5]=='2' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.6


	#QB1 and RB2 opp team is neg
	if((qb[6]==rb1[6]) and rb1[5]=='2'):
		corr_score=corr_score + -0.05
	elif((qb[6]==rb2[6]) and rb2[5]=='2'):
		corr_score=corr_score + -0.05
	elif((qb[6]==flex[6]) and (flex[4]=='RB' and flex[5]=='2')):
		corr_score=corr_score + -0.05

	#RB1 and WR2 same team neg	
	if ((rb1[5]=='1' and wr1[5]=='2') and (rb1[6]==wr1[6])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='1' and wr2[5]=='2') and (rb1[6]==wr2[6])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='1' and wr3[5]=='2') and (rb1[6]==wr3[6])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (rb1[6]==flex[6])):
		corr_score=corr_score + -0.05
	if ((rb2[5]=='1' and wr1[5]=='2') and (rb2[6]==wr1[6])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='1' and wr2[5]=='2') and (rb2[6]==wr2[6])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='1' and wr3[5]=='2') and (rb2[6]==wr3[6])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.05
	elif ((wr1[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.05
	elif ((wr2[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.05
	elif ((wr3[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[6])):
		corr_score=corr_score + -0.05


	#RB2 and WR1 opp team neg	
	if ((rb1[5]=='2' and wr1[5]=='1') and (rb1[6]==wr1[9])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='2' and wr2[5]=='1') and (rb1[6]==wr2[9])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='2' and wr3[5]=='1') and (rb1[6]==wr3[9])):
		corr_score=corr_score + -0.05
	elif ((rb1[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (rb1[6]==flex[9])):
		corr_score=corr_score + -0.05
	if ((rb2[5]=='2' and wr1[5]=='1') and (rb2[6]==wr1[9])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='2' and wr2[5]=='1') and (rb2[6]==wr2[9])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='2' and wr3[5]=='1') and (rb2[6]==wr3[9])):
		corr_score=corr_score + -0.05
	elif ((rb2[5]=='2' and (flex[5]=='1' and flex[4]=='WR')) and (rb2[6]==flex[9])):
		corr_score=corr_score + -0.05
	elif ((wr1[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + -0.05
	elif ((wr2[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + -0.05
	elif ((wr3[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + -0.05

	#RB1 and WR3 opp team pos	
	if ((rb1[5]=='1' and wr1[5]=='3') and (rb1[6]==wr1[9])):
		corr_score=corr_score + 0.05
	elif ((rb1[5]=='1' and wr2[5]=='3') and (rb1[6]==wr2[9])):
		corr_score=corr_score + 0.05
	elif ((rb1[5]=='1' and wr3[5]=='3') and (rb1[6]==wr3[9])):
		corr_score=corr_score + 0.05
	elif ((rb1[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.05
	if ((rb2[5]=='1' and wr1[5]=='3') and (rb2[6]==wr1[9])):
		corr_score=corr_score + 0.05
	elif ((rb2[5]=='1' and wr2[5]=='3') and (rb2[6]==wr2[9])):
		corr_score=corr_score + 0.05
	elif ((rb2[5]=='1' and wr3[5]=='3') and (rb2[6]==wr3[9])):
		corr_score=corr_score + 0.05
	elif ((rb2[5]=='1' and (flex[5]=='3' and flex[4]=='WR')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.05
	elif ((wr1[5]=='3' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.05
	elif ((wr2[5]=='3' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.05
	elif ((wr3[5]=='3' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.05


	#WR2 and DST same team is neg
	if ((wr1[5]=='2') and (wr1[6]==dst[6])):
		corr_score=corr_score + -0.04
	elif ((flex[5]=='2' and flex[4]=='WR') and (flex[6]==dst[6])):
		corr_score=corr_score + -0.04
	elif ((wr3[5]=='2') and (wr3[6]==dst[6])):
		corr_score=corr_score + -0.04
	elif ((wr2[5]=='2') and (wr2[6]==dst[6])):
		corr_score=corr_score + -0.04
	


	#RB2 and RB1 opp team is positive screwed up
	if ((rb1[5]=='1' and rb2[5]=='2') and (rb1[6]==rb2[9])):
		corr_score=corr_score + 0.04
	elif ((rb1[5]=='2' and rb2[5]=='1') and (rb1[6]==rb2[9])):
		corr_score=corr_score + 0.04
	elif ((rb1[5]=='1' and (flex[5]=='2' and flex[4]=='RB')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.04
	elif ((rb2[5]=='1' and (flex[5]=='2' and flex[6]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04	
	elif ((rb1[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.04
	elif ((rb2[5]=='2' and (flex[5]=='1' and flex[6]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04	

	#RB2 and WR3 opp team pos	
	if ((rb1[5]=='2' and wr1[5]=='3') and (rb1[6]==wr1[9])):
		corr_score=corr_score + 0.04
	elif ((rb1[5]=='2' and wr2[5]=='3') and (rb1[6]==wr2[9])):
		corr_score=corr_score + 0.04
	elif ((rb1[5]=='2' and wr3[5]=='3') and (rb1[6]==wr3[9])):
		corr_score=corr_score + 0.04
	elif ((rb1[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.04
	if ((rb2[5]=='2' and wr1[5]=='3') and (rb2[6]==wr1[9])):
		corr_score=corr_score + 0.04
	elif ((rb2[5]=='2' and wr2[5]=='3') and (rb2[6]==wr2[9])):
		corr_score=corr_score + 0.04
	elif ((rb2[5]=='2' and wr3[5]=='3') and (rb2[6]==wr3[9])):
		corr_score=corr_score + 0.04
	elif ((rb2[5]=='2' and (flex[5]=='3' and flex[4]=='WR')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04
	elif ((wr1[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04
	elif ((wr2[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04
	elif ((wr3[5]=='3' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.04

	#RB1 and WR2 opp team pos
	if ((rb1[5]=='1' and wr1[5]=='2') and (rb1[6]==wr1[9])):
		corr_score=corr_score + 0.03
	elif ((rb1[5]=='1' and wr2[5]=='2') and (rb1[6]==wr2[9])):
		corr_score=corr_score + 0.03
	elif ((rb1[5]=='1' and wr3[5]=='2') and (rb1[6]==wr3[9])):
		corr_score=corr_score + 0.03
	elif ((rb1[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.03
	if ((rb2[5]=='1' and wr1[5]=='2') and (rb2[6]==wr1[9])):
		corr_score=corr_score + 0.03
	elif ((rb2[5]=='1' and wr2[5]=='2') and (rb2[6]==wr2[9])):
		corr_score=corr_score + 0.03
	elif ((rb2[5]=='1' and wr3[5]=='2') and (rb2[6]==wr3[9])):
		corr_score=corr_score + 0.03
	elif ((rb2[5]=='1' and (flex[5]=='2' and flex[4]=='WR')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.03
	elif ((wr1[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.03
	elif ((wr2[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.03
	elif ((wr3[5]=='2' and (flex[5]=='1' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.03


	#RB2 and RB2 opp team is pos screwed up
	if ((rb1[5]=='2' and rb2[5]=='2') and (rb1[6]==rb2[9])):
		corr_score=corr_score + 0.03
	elif ((rb1[5]=='2' and (flex[5]=='2' and flex[4]=='RB')) and (rb1[6]==flex[9])):
		corr_score=corr_score + 0.03
	elif ((rb2[5]=='2' and (flex[5]=='2' and flex[4]=='RB')) and (rb2[6]==flex[9])):
		corr_score=corr_score + 0.03	
	
	#WR1 and opposing WR1 is neg
	if ((wr1[5]=='1' and wr2[5]=='1') and (wr1[6]==wr2[9])):
		corr_score=corr_score + -0.03
	elif ((wr1[5]=='1' and wr3[5]=='1') and (wr1[6]==wr3[9])):
		corr_score=corr_score + -0.03
	elif ((wr1[5]=='1' and (flex[5]=='1' and flex[4]=='WR')) and (wr1[6]==flex[9])):
		corr_score=corr_score + -0.03
	elif ((wr2[5]=='1' and wr3[5]=='1') and (wr2[6]==wr3[9])):
		corr_score=corr_score + -0.03
	elif ((wr2[5]=='1' and (flex[5]=='1' and flex[4]=='WR')) and (wr2[6]==flex[9])):
		corr_score=corr_score + -0.03
	elif ((wr3[5]=='1' and (flex[5]=='1' and flex[4]=='WR')) and (wr3[6]==flex[9])):
		corr_score=corr_score + -0.03



	#TE1 and RB2 opp team is pos
	if((te[6]==rb1[9])and rb1[5]=='2'):	
		corr_score=corr_score + -0.03
	elif((te[6]==rb2[9])and rb2[5]=='2'):	
		corr_score=corr_score + -0.03
	elif((te[6]==flex[9])and (flex[5]=='2' and flex[4]=='RB')):	
		corr_score=corr_score + -0.03
	elif((flex[4]=='TE') and (rb1[5]=='2') and (flex[6]==rb1[9]) ):	
		corr_score=corr_score + -0.03
	elif((flex[4]=='TE')and (rb2[5]=='2') and (flex[6]==rb2[9])):	
		corr_score=corr_score + -0.03		

	

	#WR3 and opposing DST No change same 
	#x.WR3 	x.DST 	0

	#RB1 and opp QB1 
	#y.RB1 	x.QB1 	0

	#WR1 and RB1 opp no change
	#y.WR1 	x.RB1 	0

	#WR1 and WR1 oppsite teams no change
	#x.WR1 	y.RB1 	0
	
	print "Line-up Score: ", corr_score

	tot_salary= int(qb[3])+int(rb1[3])+int(rb2[3])+int(wr1[3])+int(wr2[3])+int(wr3[3])+int(te[3])+int(flex[3])+int(dst[3])
	proj_pts=float(qb[2])+float(rb1[2])+float(rb2[2])+float(wr1[2])+float(wr2[2])+float(wr3[2])+float(te[2])+float(flex[2])+float(dst[2])
	home_score=int(qb[8])+int(rb1[8])+int(rb2[8])+int(wr1[8])+int(wr2[8])+int(wr3[8])+int(te[8])+int(flex[8])+int(dst[8])
	spread_score=int(qb[7])+int(rb1[7])+int(rb2[7])+int(wr1[7])+int(wr2[7])+int(wr3[7])+int(te[7])+int(flex[7])+int(dst[7])

	#print tot_salary
	#print proj_pts
	#print home_score
	#print spread_score

	sqb=str(qb[1])
	srb1=str(rb1[1])
	srb2=str(rb2[1])
	swr1=str(wr1[1])
	swr2=str(wr2[1])
	swr3=str(wr3[1])
	ste=str(te[1])
	sflex=str(flex[1])
	sdst=str(dst[1])

	tot_score= corr_score+(home_score*.10)+(spread_score*10)

	#scorr_score= str(corr_score)
	#stot_salary=str(tot_salary)
	#sproj_pts=str(proj_pts)
	#shome_score=str(home_score)
	#sspread_score=str(spread_score)

	print(sqb,srb1,srb2,swr1,swr2,swr3,ste,sflex,sdst,corr_score,home_score,spread_score,0,tot_salary,proj_pts)
	try:
		conn2.execute("INSERT INTO LINEUP(QB,RB1,RB2,WR1,WR2,WR3,TE,Flex,DST,corrScore,homeScore,spreadScore,totalScore,totalCost,projPts)\
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(sqb,srb1,srb2,swr1,swr2,swr3,ste,sflex,sdst,corr_score,home_score,spread_score,tot_score,tot_salary,proj_pts))#add values
		print "success"
		conn2.commit()
	except:
		print "fail"		

lineup_corr(lineup)
	       		

#print "Line-up", lineup
print ("Records created successfully")
conn.close()
conn2.close()
