# gym-kalaha
A gym environment for the board game Kalaha (also known as Kalah or Mancala).

## Usage
Install the package into your environment
```shell
$ pip install git+https://github.com/ebuehrle/gym-kalaha
```

Use from your Python script
```python
import gym

kalaha = gym.make('gym_kalaha:kalaha-v0')
kalaha.render()
print(kalaha.action_space)
observation, reward, done, info = kalaha.step(0)
```

## Rules
Different rule variants exist. This package currently contains only one environment, implementing the rules of the Playsino edition (see [ebuehrle.github.io/kalah](ebuehrle.github.io/kalah)). 
