from retro_contest.local import make
import numpy as np

def main():
	env = make('SonicTheHedgehog-Genesis', state='LabyrinthZone.Act3')
	obs = env.reset()
	c = 0
	maxRuns = 4
	lenActions =len(env.action_space.sample())
	jerkQueue = np.reshape(env.action_space.sample(),(1,lenActions))
	myActions = jerkQueue	
	oldX = 0.
	bestReward = 0.
	rewAcc = 0.
	numRuns = 0.
	while True:
		if (c < len(jerkQueue)):
			#print(myActions.shape,jerkQueue.shape)
			act= jerkQueue[c,...]
		else:
			act = env.action_space.sample()
			#if (np.random.random()>0.5):
			#	act[7] = 1
		
		obs, reward, done, info = env.step(act)	
		dx = info['x'] - oldX
		oldX = np.max([oldX,info['x']])
		rewAcc += reward
		if ((dx > 0 or reward > 0)):# and (c > len(jerkQueue))):
			#print(dx,reward)
			#retain last action if it helped
			myActions = np.append(myActions,np.reshape(act,(1,lenActions)),axis=0)
		#elif(np.random.random() > 0.9):
		#	myActions = np.append(myActions,np.reshape(act,(1,lenActions))
		#print(info['x']/info['screen_x_end'],' and reward ', reward)
		if(numRuns %10 == 0):
			env.render()
		c += 1
		if done:
			if(rewAcc > bestReward):
				bestReward = rewAcc
				jerkQueue = myActions	
				print('new best reward: %.3f based on a %i action JERK queue'%(bestReward,len(jerkQueue)))
			print('acc. reward: %.3f, best reward: %.3f, current JERK queue %i vs actions length %i'%(rewAcc,bestReward,len(jerkQueue),len(myActions)))
			
			#Attenuate best reward (to diminish the effect of lucky runs)
			bestReward *= 0.995 #* bestReward
			obs = env.reset()
			rewAcc = 0.
			numRuns += 1
			oldX = 0.
			c = 0
			myActions = np.reshape(env.action_space.sample(),(1,lenActions))
			print('begin run %i'%numRuns)
main()

