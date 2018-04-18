import gym_remote.exceptions as gre
import gym_remote.client as grc


def main():
    print('connecting to remote environment')
    env = grc.RemoteEnv('tmp/sock')
    print('starting episode')
    env.reset()
    
    while True:
        rewAcc = 0
        action = env.action_space.sample()
        action[7] = 1
        ob, reward, done, _ = env.step(action)
        rewAcc += reward
        if done:
            print('episode complete with reward = %.3f'%rewAcc)
            env.reset()


if __name__ == '__main__':
    try:
        main()
    except gre.GymRemoteError as e:
        print('exception', e)
