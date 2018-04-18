

#from retro_contest.local import make
import numpy as np

#Imports for connecting to contest
import gym_remote.exceptions as gre
import gym_remote.client as grc


def main():
	# Connect to remote environment (from simple-agent.py)
	print('connecting to remote environment')
	env = grc.RemoteEnv('tmp/sock')
	print('starting episode')
	env.reset()

	# This bot is just a kludge that tries to remember things if it moves forward, and tries to remember the highest reward sequence of actions. 
	#obs = env.reset()
	c = 0
	lenActions =len(env.action_space.sample())
	jerkQueue = np.reshape(env.action_space.sample(),(1,lenActions))
	myActions = jerkQueue	
	oldX = 0.
	bestReward = 0.
	rewAcc = 0.
	numRuns = 0.
	avgReward = 0.
	while True:
		if (c < len(jerkQueue)):
			act= jerkQueue[c,...]
		else:
			act = env.action_space.sample()
			#if (np.random.random()>0.05):
			act[7] = 1
		
		obs, reward, done, info = env.step(act)	
		
		rewAcc += reward
		if (reward > 0):
			# Remember action when rewarded
			myActions = np.append(myActions,np.reshape(act,(1,lenActions)),axis=0)
		
		c += 1
		if done:
			print('episode complete')
			if(rewAcc > bestReward):
				bestReward = rewAcc
				jerkQueue = myActions	
				#print('new best reward: %.3f based on a %i action JERK queue'%(bestReward,len(jerkQueue)))
			avgReward = 0.95*avgReward+0.05*rewAcc			
			#print('avg. reward: %.3f, acc. reward: %.3f, best reward: %.3f, current JERK queue %i vs actions length %i'%(avgReward, rewAcc, bestReward, len(jerkQueue), len(myActions)))
			
			#Attenuate best reward (to diminish the effect of lucky runs)
			bestReward *= 0.95 #* bestReward
			env.reset()
			rewAcc = 0.
			numRuns += 1
			oldX = 0.
			c = 0
			myActions = np.reshape(env.action_space.sample(),(1,lenActions))
			#print('begin run %i'%numRuns)



if __name__ == '__main__':
    try:
        main()
    except gre.GymRemoteError as e:
        print('exception', e)
