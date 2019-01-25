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
            self.cells = {}

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
                    if x >= 0 and y >= 0:
                        if (x, y) not in surviving_cells:
                            c = Cell(x, y)
                            if c.count_neighbours(self.cells) == 3: # generation
                                # print("New cell @ {0}, {1}".format(x, y))
                                surviving_cells[(x, y)] = c
        
        self.cells = surviving_cells

    def display(self):
        max_x = max(self.cells, key=itemgetter(0))[0] + 2
        max_y = max(self.cells, key=itemgetter(1))[1] + 2

        cells = [["." for col in range(max_x + 1)] for row in range(max_y + 1)]

        for key in self.cells:
            cells[key[1]][key[0]] = "X"

        for row in cells:
            for col in row:
                print(col, end="")
            print()


# cells = {(2, 2): Cell(2, 2), (2, 3): Cell(2, 3), (2, 4): Cell(2, 4), (5, 5): Cell(5, 5)}
cells = [(2, 2), (2, 3), (2, 4), (5, 5), (8, 3), (9, 3), (10, 3), (7, 4), (8, 4), (9, 4)]

g = Game(cells)

print("========== Initial State ==========")
g.display()

for i in range(1, 6):
    print("========== Gen {0} ==========".format(i))
    g.evolve()
    g.display()