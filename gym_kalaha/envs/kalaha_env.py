import gym

class KalahaEnv(gym.Env):
    metadata = { 'render.modes': ['human'] }

    def __init__(self):
        self.action_space = list(range(6))
        self._holes = (0, 1, 2, 9, 10, 11)
        self.reset()

    def step(self, action):
        if not self._isvalidmove(action):
            raise ValueError('Invalid action {} in state {}'.format(action, self.state))

        pickup_hole = self._holes[action]

        # Redistribute stones
        next_board_state = list(self.state['board'])
        pickup_amount = next_board_state[pickup_hole]
        next_board_state[pickup_hole] = 0
        for i in range(pickup_amount):
            next_board_state[(pickup_hole + i + 1) % 12] += 1
        
        # Pickup stones
        final_hole = (pickup_hole + pickup_amount) % 12
        adjacent_holes = (
            final_hole,
            self._adjnext(final_hole),
            self._adjprev(final_hole),
            self._adjopposite(final_hole),
        )

        for idx in adjacent_holes:
            if 2 <= next_board_state[idx] <= 3:
                next_board_state[12] += next_board_state[idx]
                next_board_state[idx] = 0

        # Update state
        self.state = {
            'board': tuple(self._flip(next_board_state)), # current player is always "left"
            'turn': -self.state['turn'],
        }

        observation = self.state
        reward = self._winner() if self._isgameover() else 0
        done = self._isgameover()
        info = None

        return observation, reward, done, info
    
    @staticmethod
    def _adjnext(hole):
        return (hole + 1) % 12
    
    @staticmethod
    def _adjprev(hole):
        return (hole + 11) % 12
    
    @staticmethod
    def _adjopposite(hole):
        return (11 - hole % 12)

    @staticmethod
    def _flip(board):
        return board[6:12] + board[0:6] + board[13:14] + board[12:13]
    
    def _isvalidmove(self, action):
        return self.state['board'][self._holes[action]]
    
    def _isgameover(self):
        return not any(self._isvalidmove(a) for a in self.action_space)
    
    def _winner(self):
        if self.state['board'][12] > self.state['board'][13]:
            return self.state['turn'] # current player wins
        if self.state['board'][12] < self.state['board'][13]:
            return -self.state['turn'] # other player wins
        return 0 # draw

    def reset(self):
        self.state = {
            'board': (
                4, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4,
                0, 0,
            ),
            'turn': 1,
        }
        return self.state

    def render(self, mode='human'):
        board_state = self.state['board']

        print('{:2d}'.format(board_state[12]), end=' ')
        for s in board_state[:6]:
            print('{:2d}'.format(s), end=' ')
        print('{:2d}'.format(board_state[13]))

        print(' ' * 2, end=' ')
        for s in reversed(board_state[6:12]):
            print('{:2d}'.format(s), end=' ')
        print()

        print("Player", self.state['turn'], "'s turn.")

    def close(self):
        pass
