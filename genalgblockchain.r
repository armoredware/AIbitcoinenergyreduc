library(genalg)

#Infinite Loop
while( TRUE ){
#set working directory 
setwd("~/Desktop/mercy600")
#import csv file of miner data [account,stake,trust]
miners <- read.csv("blockchainminers.csv")

#set the budget 
stake.limit <- 60000
#sets the number of miner accounts 
potenial_miners <- length(miners[,1])
#set the amount of times we evaluate
iterations = 500
#set population size
popSize = 500
#set mutationChance
mutationChance = 0.02



#GA eval function
trustedminerBuilder <- function(GA) {
  #use selected potenial_miners
  trustedminer <- which(GA==1)
 
   #add up the projected points of the selected potenial_miners and store in trustedminer_trust 
  trustedminer_trust <- sum(miners[trustedminer,3]) 
  #add up the stake of selected potenial_miners and store in trustedminer_stake
  trustedminer_stake <- sum(miners[trustedminer,2])
   print(trustedminer_stake)
   print(trustedminer_trust)

   #check to see if there are not 11 potenial_miners , this is ineligible
   if(sum(GA) != 11 )  return(200*(abs(sum(GA)-11)))

   #check to see if trustedminer is over the budget limit
   if(trustedminer_stake > stake.limit) return(abs(60000 - trustedminer_stake))  
   return(-trustedminer_trust)
}


#Create a Genetic Algorithm Model for draft kings trustedminers
GAmodel <- rbga.bin(size = potenial_miners, popSize = popSize, iters = iterations, mutationChance = mutationChance,  evalFunc = trustedminerBuilder, showSettings=FALSE, verbose=FALSE)

cat(genalg:::summary.rbga(GAmodel,echo=T))

out = c(genalg:::summary.rbga(GAmodel,echo=T))
#isolate the binary solution of the output using regex
s1=gsub("\\D||500","",out)
string=gsub("^\\d{8}","",s1)
#print(s1)

#to python
#send the binary solution of the trustedminer values to python
command = "python3.5"

# Note the single + double quotes in the string (needed if paths have spaces)
path2script='"/root/Desktop/mercy600/genalg.py"'

args = c(string)

# Add path to script as first arg
allArgs = c(path2script, args)

#print output from python back to screen 
output = system2(command, args=allArgs, stdout=TRUE)

print(paste(output))

}

