import sys, copy
from sys import maxsize
from copy import deepcopy


live_states = []
num_nodes_expanded = 0

#------- Question Class ---------
class Question:
  goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

  def __init__(self, puzzle_board, row_num):
    self.puzzle_board = puzzle_board
    self.row_num = row_num
    self.blank_y_pos, self.blank_x_pos = self.find_blank_tile()

  def find_blank_tile(self):
    for row in range(len(self.puzzle_board)):
      for col in range(len(self.puzzle_board)):
        if self.puzzle_board[row][col] == 0:
          return row, col

  def swap_tiles(self, new_y, new_x):
    temp_blank = self.puzzle_board[self.blank_y_pos][self.blank_x_pos]
    self.puzzle_board[self.blank_y_pos][self.blank_x_pos] = self.puzzle_board[new_y][new_x]
    self.puzzle_board[new_y][new_x] = temp_blank


  def move_up(self):
    if 0 not in self.puzzle_board[0]:
      self.swap_tiles(self.blank_y_pos - 1, self.blank_x_pos)
      self.blank_y_pos = self.blank_y_pos - 1
      return True

    else:
      return False

  def move_down(self):
    if 0 not in self.puzzle_board[2]:
      self.swap_tiles(self.blank_y_pos + 1, self.blank_x_pos)
      self.blank_y_pos = self.blank_y_pos + 1
      return True

    else:
      return False

  def move_left(self):
    in_left_col = False
    for row in range(self.row_num):
      if self.puzzle_board[row][0] == 0:
        in_left_col = True
        break

    if in_left_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos - 1)
      self.blank_x_pos = self.blank_x_pos - 1
      return True

    else:
      return False

  def move_right(self):
    in_right_col = False
    for row in range(self.row_num):
      if self.puzzle_board[row][2] == 0:
        in_right_col = True
        break

    if in_right_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos + 1)
      self.blank_x_pos = self.blank_x_pos + 1
      return True

    else:
      return False

  def print_board(self):
    to_print = []
    for row in range(len(self.puzzle_board)):
      for col in range(len(self.puzzle_board)):
        to_print.append(self.puzzle_board[row][col])
      print(to_print)
      to_print = []
#--------- Main Function ---------
def main():
  intro  = "Welcome to Aaron Hung's CS170 8-puzzle solver.\n"
  intro  += "Type '1' to use a default puzzle, or '2' to enter your own puzzle.\n"
  print(intro)

  first_choice = int(input())
  puzzle = []

  if first_choice == 1:
    intro2 = "Enter the difficulty you wish to start with.\n"
    intro2 += "Your choices are '0', '1', '2', '3', '4', '5' and '6'.\n"
    print(intro2)

    second_choice = int(input())
    if second_choice == 0:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif second_choice == 1:
      puzzle = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    elif second_choice == 2:
      puzzle = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    elif second_choice == 3:
      puzzle = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
    elif second_choice == 4:
      puzzle = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
    elif second_choice == 5:
      puzzle = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
    elif second_choice == 6:
      puzzle = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]
    else:
      print ("Please try again and select an a valid option")
      sys.exit(0)

  elif first_choice == 2:
    print("Enter your puzzle, use a zero to represent the blank and press enter when done with each step.")
    first_row = input("Enter the first row, using a space between numbers: ")
    first_row = [int(d) for d in first_row.split() if d.isdigit()]
    second_row = input("Enter the second row, using a space between numbers: ")
    second_row = [int(d) for d in second_row.split() if d.isdigit()]
    third_row = input("Enter the third row, using a space between numbers: ")
    third_row = [int(d) for d in third_row.split() if d.isdigit()]

    puzzle = [first_row, second_row, third_row]

  else:
    print ("Please try again and select an a valid option")
    sys.exit(0)

  question = Question(puzzle, 3)

  intro2  = "Choice of algorithms to use:\n"
  intro2  += "1. Uniform Cost Search\n"
  intro2  += "2. A* with Misplaced Tile Heuristic\n"
  intro2  += "3: A* with Euclidean Distance Heuristic\n"
  print(intro2)

  third_choice = int(input())

  if third_choice == 1:
    print("Uniform Cost Search Algorithm")

    print(" ")


  elif third_choice == 2:
    print("A* with Misplaced Tile Heuristic Algorithm")

    print(" ")


  elif third_choice == 3:
    print("A* with Euclidean Distance Heuristic Algorithm")

    print(" ")


  else:
    print("Please try again and select an a valid option")
    sys.exit(0)

main()
