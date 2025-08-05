from itertools import cycle

SIZES = cycle([15, 20, 25, 30, 35, 40, 10])
ALGORITHMS = cycle(["DFS", "BFS", "A*", "Dijkstra's"])

class GameState:
    def __init__(self):
        self.algorithm = "A*"
        self.rows = 10
        self.cols = 10