#generate points, associate them with rows, columns, and squares.  Accept input
# from user to create board.  solve board: for each point, maintain a list of possible
#values.  assign final value once that list is down to one.
letters = ['A','B','C','D','E','F','G','H','I']
numbers = range(1,10)
class Cell:
    def __init__(self, cell_name):
        
        self.name = cell_name
        self.row = []
        self.column = []
        self.square = []
        self.neighbors = []
        self.possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.final_value = None
        
    def make_column(self, name):
        for cell in cells.keys():
            #if the letter part of any cell name matches the letter part of our cell,
            #add that matching cell instance to our cell's "row" list
            if cell[0] == name[0] and cell != name:
                self.column.append(cells[cell])

    def make_row(self, name):
        for cell in cells.keys():
            #if the number part of any cell name matches the number part of our cell,
            #add that matching cell to our cell's "row" list
            if cell[1] == name[1] and cell != name:
                self.row.append(cells[cell])
                
    def make_square(self, current_cell_name, cell_dict):
        
        #square by square of the board:
        for letter_subset in [letters[0:3], letters[3:6], letters[6:9]]:
            for number_subset in [numbers[0:3], numbers[3:6], numbers[6:9]]:
                #if our current cell name is in our current board square:
                if current_cell_name[0] in letter_subset:
                    if int(current_cell_name[1]) in number_subset:
                        #check all other cells to see if they're in this square also
                        for possible_neighbor_name in cell_dict.keys():
                            if (possible_neighbor_name[0] in letter_subset
                                and int(possible_neighbor_name[1]) in number_subset
                                #also check that we're not looking at the current cell
                                and possible_neighbor_name != current_cell_name):
                                #add the non-self neighboring cell to the square list
                                self.square.append(cell_dict[possible_neighbor_name])
    def set_final_value(self):
        if len(self.possible_values) == 1:
            self.final_value = int(self.possible_values[0])
            self.possible_values = []


def generate_cells():
    cells_dict = {}
    for letter in letters:
        for num in numbers:
            cells_dict[letter + str(num)] = Cell(letter + str(num))
    return cells_dict

#def populate_cells(cells_dict, puzzle_string):
    #takes a dict mapping cell names to cell objects and an 81-char puzzle string.
    #populates final values of each cell with 
    
def make_neighbors(cells):
    for cell_name in sorted(cells.keys()):
        cells[cell_name].make_column(cell_name)
    for cell_name in sorted(cells.keys()):
        cells[cell_name].make_row(cell_name)
    for cell_name in sorted(cells.keys()):
        cells[cell_name].make_square(cell_name, cells)
    for cell_name in sorted(cells.keys()):
        for neighbor in cells[cell_name].column:
            cells[cell_name].neighbors.append(neighbor)
        for neighbor in cells[cell_name].row:
            cells[cell_name].neighbors.append(neighbor)
        for neighbor in cells[cell_name].square:
            cells[cell_name].neighbors.append(neighbor)
    


#cells["I9"].possible_values = [8]
#cells["I9"].set_final_value(cells["I9"].possible_values)



def nones_in_board(cells):
    #takes a list of cell objects and returns True if any cell's final_value
    #is still None and False otherwise (meaning the board is solved)
    for cell in cells:
        if cell.final_value == None:
            return True
    return False

def solve(board):
    #takes a list of cell objects, fills in board until board is full
    while nones_in_board(board):
        #while board is not solved
        for cell in board:
            #print(cell.name, board)
            cell.set_final_value()
            for neighbor in cell.neighbors:
                #looking in turn at all the neighbors of each cell
                if neighbor.final_value != None and int(neighbor.final_value) in cell.possible_values:
                    #if our cell has a neighbor with a final value that our cell
                    #thinks is a possible value,relieve the cell of that thought
                    #print "removing neighbor's final value from cell's possible value" + cell.name + " / "+ str(cell.possible_values) + " / " + str(cell.final_value) + " / " + str(counter)
                    cell.possible_values.remove(int(neighbor.final_value))
                    cell.set_final_value()

            
            column_possible_values = []
            row_possible_values = []
            square_possible_values = []
            # check column
            for column_neighbor in cell.column:
                column_possible_values.append(column_neighbor.possible_values)
            for num in cell.possible_values:
                if num not in column_possible_values:
                    cell.final_value = num
                    cell.possible_values = []
            # check row
            
            for row_neighbor in cell.row:
                row_possible_values.append(row_neighbor.possible_values)
            for num in cell.possible_values:
                if num not in row_possible_values:
                    cell.final_value = num
                    cell.possible_values = []
            
            # check square
            
            for square_neighbor in cell.square:
                square_possible_values.append(square_neighbor.possible_values)
            for num in cell.possible_values:
                if num not in square_possible_values:
                    cell.final_value = num
                    cell.possible_values = []
    
                
        #update nones_in_board to see if board is solved yet
        
#def print_board_string()

def convert_string_to_board(string, sorted_cells):
    #takes an 81-character string, and sorted list of cell objects.
    #in string, replaces 0's or .'s with Nones,
    #maps characters to sorted cells, and assigns them to cells' final values
    index_counter = 0
    for char in string:
        if char == "0" or char == ".":
            char = None
        else:
            char = int(char)
        #else: print char
        # set final_value to num for the [index of num]-th object in sorted_cells
        #print char
        sorted_cells[index_counter].final_value = char
        index_counter += 1        

def print_board(sorted_cells):
    row_counter = 1
    while row_counter <= 9:
        cell_counter = 1
        cell_list = []
        for cell in sorted_cells:
            if ( (row_counter - 1) * 9 < cell_counter
            and cell_counter <= row_counter * 9 ):
                cell_list.append(cell.final_value)
            cell_counter += 1
        print cell_list
        row_counter += 1

#====Main====
puzzle_string = "...28.94.1.4...7......156.....8..57.4.......8.68..9.....196......5...8.3.43.28..."
cells = generate_cells()
# cells is a dict that maps cell names to cell instances
sorted_cells = cells.values()
def sort_key(cell):
    return cell.name[1] + cell.name[0]
sorted_cells.sort(key = sort_key)

make_neighbors(cells)
print cells["I7"].possible_values
convert_string_to_board(puzzle_string, sorted_cells)
'''
for cell in cells.values():
    print cell.final_value
'''

            
solve(sorted_cells)
'''
for cell in sorted_cells:
    for neighbor in cell.neighbors:
        print (cell.name, cell.possible_values, cell.final_value, neighbor.name, neighbor.final_value)
 '''       
printCells(cells)

print_board(sorted_cells)

#print cells["H7"].neighbors
#print_board(cells.values())


