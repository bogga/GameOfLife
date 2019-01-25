from operator import itemgetter
import sys

class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_neighbour(self, other_cell):
        if other_cell is not self:
            if other_cell.x >= self.x - 1 and other_cell.x <= self.x + 1:
                if other_cell.y >= self.y - 1 and other_cell.y <= self.y + 1:
                    return True
        return False

    def count_neighbours(self, live_cells):
        count = 0
        for key in live_cells:
            if key[0] > self.x + 1 or key[0] < self.x - 1 or key[1] > self.y + 1 or key[1] < self.y - 1:
                continue # skip this run - the other cell loc is out of bounds
            if self.is_neighbour(live_cells[key]):
                count += 1
        return count

class Game(object):

    def __init__(self, cells=None):
        '''
        Creates an instance of the game.
        cells can be either a dictionary (i.e. a pre-made cell structure) or a list of tuples, where each tuple is
        the location of each cell (e.g. [(2, 2), (2, 3)])
        '''
        if cells is not None:
            if isinstance(cells, dict):
                self.cells = cells
            elif isinstance(cells, list):
                self.cells = {}
                for loc in cells:
                    self.cells[loc] = Cell(loc[0], loc[1])
            else:
                print("Incompatible format of cells! Starting with blank.")
                self.cells = {}
        else:
            self.cells = {}

    def add_cells(self, locations):
        for loc in locations:
            self.cells[(loc[0], loc[1])] = Cell(loc[0], loc[1])

    def evolve(self):
        '''
        Progresses the game forwards by one iteration.
        '''
        surviving_cells = {}
        for key in self.cells:
            cell = self.cells[key]
            neighbours = cell.count_neighbours(self.cells)
            # print("Cell @ {0}, {1} has {2} neighbours".format(key[0], key[1], neighbours))
            if neighbours is 2 or neighbours is 3: # survival
                surviving_cells[key] = cell

        for key in self.cells:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = key[0] + i
                    y = key[1] + j
                    if (x, y) not in surviving_cells:
                        c = Cell(x, y)
                        if c.count_neighbours(self.cells) == 3: # generation
                            # print("New cell @ {0}, {1}".format(x, y))
                            surviving_cells[(x, y)] = c
        
        self.cells = surviving_cells

    def display(self):
        max_x = max(self.cells, key=itemgetter(0))[0] + 2
        max_y = max(self.cells, key=itemgetter(1))[1] + 2

        min_x = min(self.cells, key=itemgetter(0))[0] - 2
        min_y = min(self.cells, key=itemgetter(1))[1] - 2

        cells = [["." for col in range(min_x, max_x + 1)] for row in range(min_y, max_y + 1)]

        for key in self.cells:
            cells[key[1]- min_y][key[0] - min_x] = "X"

        for row in cells:
            for col in row:
                print(col, end="")
            print()


# cells = {(2, 2): Cell(2, 2), (2, 3): Cell(2, 3), (2, 4): Cell(2, 4), (5, 5): Cell(5, 5)}
# cells = [(2, 2), (2, 3), (2, 4), (5, 5), (8, 3), (9, 3), (10, 3), (7, 4), (8, 4), (9, 4)]

# right-moving ship
# cells = [(2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (4, 1), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (6, 2)]

# left-moving ship
cells = [(2, 4), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 5), (5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 3), (7, 4)]

g = Game(cells)

print("========== Initial State ==========")
g.display()

for i in range(1, 200):
    print("========== Gen {0} ==========".format(i))
    g.evolve()
    g.display()

# g.display()