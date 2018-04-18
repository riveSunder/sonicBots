from retro_contest.local import make
import matplotlib.pyplot as plt

def main():
	env = make(game='Vectorman-Genesis',state=-1) #'SonicTheHedgehog-Genesis', state='LabyrinthZone.Act1')
	obs = env.reset()
	c = 0
	maxRuns = 4
	while True:
		act = env.action_space.sample()
		act[7] = 1
		obs, rew, done, info = env.step(act) #env.action_space.sample()
		#env.render()
		if done:
			print(obs.shape,'\n',info)
			obs = env.reset()
			c += 1	
			plt.figure(figsize=(8,8))
			#plt.subplot(131)
			#plt.imshow(obs[:,:,0])
			#plt.subplot(132)
			#plt.imshow(obs[:,:,1])
			#plt.subplot(133)
			plt.imshow(obs[:,:,0]/3+obs[:,:,1]/3+obs[:,:,2]/3,cmap='gray')
			plt.savefig('./screens/sampleScreen%i.png'%c)
			if (c>maxRuns):
				env.close()
				break
if __name__ == '__main__':
	main()

