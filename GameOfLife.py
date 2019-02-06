from operator import itemgetter
import sys, re

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
        '''
        Adds cells to the list of living cells.
        '''
        if isinstance(locations, list):
            for loc in locations:
                self.cells[loc] = Cell(loc[0], loc[1])
        elif isinstance(locations, tuple):
            self.cells[(locations[0], locations[1])] = Cell(locations[0], locations[1])

    def evolve(self):
        '''
        Progresses the game forwards by one iteration.
        '''
        surviving_cells = {}
        for key in self.cells:
            cell = self.cells[key]
            neighbours = cell.count_neighbours(self.cells)
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
                            surviving_cells[(x, y)] = c
        
        self.cells = surviving_cells

    def display(self):
        '''
        Displays the current state of the world to the console.
        Calculates the range of living cells and prints around them.
        '''
        if len(self.cells) > 0:
            max_x = max(self.cells, key=itemgetter(0))[0] + 2
            max_y = max(self.cells, key=itemgetter(1))[1] + 2

            min_x = min(self.cells, key=itemgetter(0))[0] - 2
            min_y = min(self.cells, key=itemgetter(1))[1] - 2
        else:
            max_x = 5
            max_y = 5

            min_x = 0
            min_y = 0


        cells = [["." for col in range(min_x, max_x + 1)] for row in range(min_y, max_y + 1)]

        for key in self.cells:
            cells[key[1] - min_y][key[0] - min_x] = "X"

        for row in cells:
            for col in row:
                print(col, end="")
            print()

right_moving_ship = [(2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (4, 1), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3), (6, 2)]
left_moving_ship = [(2, 4), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 5), (5, 2), (5, 3), (5, 4), (6, 2), (6, 3), (6, 4), (7, 3), (7, 4)]
blinker = [(1, 1), (1, 2), (1, 3)]
toad = [(2, 1), (3, 1), (4, 1), (1, 2), (2, 2), (3, 2)]
block = [(1, 1), (1, 2), (2, 1), (2, 2)]

print("Welcome to the Game of Life!\nPlease note that the display works by creating a 'screen' around the living cells, and as such the world may look less active.")
while True:
    while True:
        option = input("Please select an option by entering its number:\n1) User-specified setup\n2) Preset setup\n> ")
        if option == "1":
            start = input("Please enter a list of cell coordiantes, as such: '(1, 2), (8, 5), (4, 3)'. Non-valid characters will be filtered out.\n> ")
            nums = [int(i) for i in re.findall("[0-9+]", start)]
            cells = []
            for i in range(int(len(nums)/2)):
                cells.append((nums[i], nums[i+1]))
            break
        elif option == "2":
            setup_choices = [("Right-moving ship", right_moving_ship), ("Left-moving ship", left_moving_ship), ("Blinker", blinker), ("Toad", toad), ("Block", block)]
            setup_text = ""
            for i, item in enumerate(setup_choices):
                setup_text = setup_text + str(i + 1) + ") " + item[0] + "\n"
            while True:
                setup = int(input("Please select an option by entering its number:\n" + setup_text + "> ")) - 1
                if setup < len(setup_choices):
                    cells = setup_choices[setup][1]
                    break
                else:
                    print("Invalid input.")
            break

    g = Game(cells)

    print("========== Initial State ==========")
    g.display()

    print("Please press enter when you want to progress. Type 'quit' to quit or 'menu' to return to the menu. You can also type 'add' to add cells to the world.")
    iteration = 0

    while True:
        choice = input("> ").lower()
        if choice == "quit":
            sys.exit(0)
        elif choice == "menu":
            break
        elif choice == "add":
            start = input("Please enter a list of cell coordiantes, as such: '(1, 2), (8, 5), (4, 3)'. Non-valid characters will be filtered out.\n> ")
            nums = [int(i) for i in re.findall("-*[0-9]+", start)]
            cells = []
            for i in range(0, len(nums), 2):
                cells.append((nums[i], nums[i+1]))
            g.add_cells(cells)
            g.display()
        else:
            print("========== Gen {0} ==========".format(iteration))
            iteration += 1
            g.evolve()
            g.display()