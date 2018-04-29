"""meta script to run agent container on test data set"""

import pandas as pd
import subprocess
import os
import numpy as np

# Where the list of games and states
testSetList = './data/sonic-test.csv'
agent = 'jerk-agent:v1'
# run time (based on system clock)
maxWallTime = 1200



gameList = pd.read_csv(testSetList)
lenList = len(gameList)

for ck in range(lenList):
	# save results in appropriate folder
	resultsDir = "./results/" + agent[0:4] +"/" + gameList.game[ck] + gameList.state[ck]
	# 
	bashCommand = "retro-contest run --agent $DOCKER_REGISTRY/" + agent + " --results-dir " + resultsDir + " --no-nv --use-host-data --wallclock-limit " + str(maxWallTime) + " " + gameList.game[ck] + " " + gameList.state[ck]
	print(bashCommand)
	subprocess.call(bashCommand,shell=True)
	#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
	#output, error = process.communicate()


myCurDir = os.listdir("./results/" + agent[0:4]+"/")
myTestScores = []
outFile = open("./results/"+ agent[0:4] + "/summary.txt","w")

for myFolder in myCurDir:
	print("./results/"+ agent[0:4] + myFolder)
	myScores = pd.read_csv("./results/"+ agent[0:4] + "/" + myFolder)

	# The score is based on the rewards during last n episodes
	n = 10 

	avgScore = np.sum(myScores.r[len(myScores)-10:len(myScores)-1]) / n
	stdScore = np.std(myScores.r[len(myScores)-10:len(myScores)-1])
	myTestScores.append(avgScore)

	# Write out text file with results
	text_file.write("Score for %s = %.2f +/- %.2f" % (myFolder,avgScore,stdScore))

print("avg test scores", myTestScores)
outFile.close()

