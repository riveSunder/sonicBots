

import pandas as pd
import subprocess
import os
import numpy as np

# imports for reading in the agent name
import sys, getopt

# Where the list of games and states
testSetList = './data/sonic-test.csv'

# run time (based on system clock)
maxWallTime = 1200

# Setup the agent
opts, args = getopt.getopt(sys.argv[1:],"a:",["agent="])
agent = 'jerk-agent:v1'

for opt, arg in opts:
	if opt in ("-a","--agent"):
		agent = arg
print(agent)

gameList = pd.read_csv(testSetList)
lenList = len(gameList)

myCurDir = os.listdir("./results/" + agent[0:4]+"/")
myTestScores = []
outFile = open("./results/"+ agent[0:4] + "/summary.txt","w")
outFile.write("gamestate,score,std\n")
for myFolder in myCurDir:
	print("./results/"+ agent[0:4] + myFolder +"/monitor.csv")
	myScores = pd.read_csv("./results/"+ agent[0:4] + "/" + myFolder +"/monitor.csv")

	# The score is based on the rewards during last n episodes
	n = 10 

	avgScore = np.sum(myScores.r[len(myScores)-10:len(myScores)-1]) / n
	stdScore = np.std(myScores.r[len(myScores)-10:len(myScores)-1])
	myTestScores.append(avgScore)

	# Write out text file with results
	outFile.write("%s, %.2f, %.2f\n" % (myFolder,avgScore,stdScore))
outFile.write("%s, %.2f, %.2f\n" % ("aggregate",np.mean(myTestScores),np.std(myTestScores)))
print("avg test scores", myTestScores)
outFile.close()
