class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.wall = True
        self.obstacle = False
        self.key = False
        self.visited = False
        self.start_point = False
        self.end_point = False