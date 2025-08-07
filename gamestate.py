from itertools import cycle

class GameState:
    def __init__(self):
        self.algorithm = "DFS"
        self.rows = 8
        self.cols = 8
        self.cycle_algo = cycle(["BFS", "A*", "DFS"])
        self.cycle_size = cycle([16, 24, 32, 40, 8])