import sys, copy
from sys import maxsize
from copy import deepcopy

#global vars tracking repeat states and number of nodes expanded
seen_states = []
num_nodes_expanded = 0

#------- Question Class ---------
class Question:
  goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #end state in question class

  def __init__(self, puzzle_board, row_num):#puzzle board
    self.puzzle_board = puzzle_board
    self.row_num = row_num
    self.blank_y_pos, self.blank_x_pos = self.find_blank_tile()#order here is row->col

  def find_blank_tile(self):
    for row in range(len(self.puzzle_board)): #row
      for col in range(len(self.puzzle_board)): #col
        if self.puzzle_board[row][col] == 0: #blank
          return row, col

  def swap_tiles(self, new_y, new_x):
    temp_blank = self.puzzle_board[self.blank_y_pos][self.blank_x_pos] #blank
    self.puzzle_board[self.blank_y_pos][self.blank_x_pos] = self.puzzle_board[new_y][new_x]#old blank gets a new tile
    self.puzzle_board[new_y][new_x] = temp_blank #new blank 

#all the possible operators in the 8-puzzle
  def move_up(self):
    if 0 not in self.puzzle_board[0]:#blank is not in the top row
      self.swap_tiles(self.blank_y_pos - 1, self.blank_x_pos)#swap blank and number above it
      self.blank_y_pos = self.blank_y_pos - 1 #move the blank up
      return True

    else:
      return False

  def move_down(self):
    if 0 not in self.puzzle_board[2]:#blank is not in the bottom row
      self.swap_tiles(self.blank_y_pos + 1, self.blank_x_pos)#swap blank and number below it
      self.blank_y_pos = self.blank_y_pos + 1#move the blank down
      return True

    else:
      return False

  def move_left(self):
    in_left_col = False #blank is not in the left column
    for row in range(self.row_num):
      if self.puzzle_board[row][0] == 0:#if this is true, can't move left
        in_left_col = True
        break

    if in_left_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos - 1) #swap blank and number left of it
      self.blank_x_pos = self.blank_x_pos - 1 #move the blank left
      return True

    else:
      return False

  def move_right(self):
    in_right_col = False #blank is not in the right column
    for row in range(self.row_num):
      if self.puzzle_board[row][2] == 0:#if this is true, can't move right
        in_right_col = True
        break

    if in_right_col == False:
      self.swap_tiles(self.blank_y_pos, self.blank_x_pos + 1)#swap blank and number right of it
      self.blank_x_pos = self.blank_x_pos + 1 #move the blank right
      return True

    else:
      return False

  def print_board(self):
    to_print = []
    for row in range(len(self.puzzle_board)): #rows
      for col in range(len(self.puzzle_board)):#cols
        to_print.append(self.puzzle_board[row][col]) #save current row
      print(to_print) #print row
      to_print = [] #empty row to print

#--------- Node Class ---------
class Node:
  def __init__(self, question, path, heuristic): #node initialization
    self.question = question
    self.path = path
    self.heuristic = heuristic

#--------- Graph Search Functions ---------
def save_child(node, children):
  child = deepcopy(node) #child is based on last move
  child.path += 1 #increase path cost by one for each move (edges cost 1)
  children.append(child)

def explore_node(node):
  global num_nodes_expanded

  children = []

  if node.question.move_up(): #check if blank can move up
    seen_states.append(node.question.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.question.move_down() #reset to before move

  if node.question.move_down(): #check if blank can move down
    seen_states.append(node.question.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.question.move_up() #reset to before move

  if node.question.move_left():#check if blank can move left
    seen_states.append(node.question.puzzle_board) #append this possible move
    save_child(node, children) #deepcopy child to children
    node.question.move_right() #reset to before move

  if node.question.move_right():#check if blank can move right
    seen_states.append(node.question.puzzle_board) #append this possible move
    save_child(node, children)#deepcopy child to children
    node.question.move_left() #reset to before move

  num_nodes_expanded += len(children)
  return children

def remove_node(frontier): #remove cheapest node
  lowest_cost_seen = maxsize
  positition = maxsize #position of node to remove

  for n in range(len(frontier)):
    if frontier[n].path + frontier[n].heuristic < lowest_cost_seen:
      lowest_cost_seen = frontier[n].path + frontier[n].heuristic
      positition = n

  node = frontier.pop(positition)
  return node

def misplaced_tiles(node):
  total_misplaced_tiles = 0 #track number of misplaced tiles 

  for row in range(len(node.question.puzzle_board)):
    for col in range(len(node.question.puzzle_board)):
      if node.question.puzzle_board[row][col] != node.question.goal_state[row][col]: #found a misplaced tile
        if node.question.puzzle_board[row][col] != 0: #ignore blank tile
          total_misplaced_tiles += 1

  return total_misplaced_tiles

def find_in_goal_state(node, row, col):
  tile = node.question.puzzle_board[row][col] #find current tile

#output where tile belongs
  if tile == 1:
    row = 0
    col = 0

  elif tile == 2:
    row = 0
    col = 1

  elif tile == 3:
    row = 0
    col = 2

  elif tile == 4:
    row = 1
    col = 0

  elif tile == 5:
    row = 1
    col = 1

  elif tile == 6:
    row = 1
    col = 2

  elif tile == 7:
    row = 2
    col = 0

  elif tile == 8:
    row = 2
    col = 1

  return row, col

def euclidean_distance(node):
  heurisitic = 0 #default 0

  for row in range(len(node.question.puzzle_board)):
    for col in range(len(node.question.puzzle_board)):
      if node.question.puzzle_board[row][col] != node.question.goal_state[row][col]:#misplaced tile
        if node.question.puzzle_board[row][col] != 0: #ignnore blank tile
          row_diff, col_diff = find_in_goal_state(node, row, col) #where tile should be 
          distance = pow(pow((row - row_diff), 2) + pow(col - col_diff, 2), 0.5) #formula
          heurisitic += distance #add distance

  return heurisitic

def expand(set_list, node, choice):
  print("The best state to expand with a g(n) = " + str(node.path) + " and h(n) = " + str(node.heuristic) + " is...")
  node.question.print_board()
  print("Expanding this node...")
  print(" ")

  children = explore_node(node) #get children

  if choice == 1: #blind uniform search
    for child in children:
      if child.question.puzzle_board not in seen_states:#if not already a live state
        set_list.append(child)#insert to set
        seen_states.append(child.question.puzzle_board) #upadate live states

  elif choice == 2:
    for child in children:
      child.heuristic = misplaced_tiles(child)#update the heuristic for the childen
      if child.question.puzzle_board not in seen_states:#if not already a live state
        set_list.append(child)#insert to set
        seen_states.append(child.question.puzzle_board) #upadate live states

  elif choice == 3:
    for child in children:
      child.heuristic = euclidean_distance(child) #update the heuristic for the childen
      if child.question.puzzle_board not in seen_states:#if not already a live state
        set_list.append(child)#insert to set
        seen_states.append(child.question.puzzle_board) #upadate live states

  return set_list

def graph_search(question, choice):
  path = 0
  heuristic = 0

  node = Node(question, path, heuristic) #initial state

  if choice == 2: #update heuristic for misplaced tiles
    node.heuristic = misplaced_tiles(node)
  elif choice == 3: #update heuristic for euclidean distance
    node.heuristic = euclidean_distance(node)

  frontier = [node] #initialize with first state
  max_queue_size = 0

  while True: #loop until return
    max_queue_size = max(len(frontier), max_queue_size) #max size seen so far is the max queue size ever seen

    if not frontier:
      print("No solution can be found")
      return

    (node) = remove_node(frontier) #remove next node

    if node.question.puzzle_board == question.goal_state: #check if goal only after we remove
      print("Solution found!")
      print(" ")
      print("Number of nodes expanded: " + str(num_nodes_expanded))
      print("Max queue size: " + str(max_queue_size))
      return

    frontier = expand(frontier, node, choice)

#--------- Main Function ---------
def main():
  intro  = "Welcome to Aaron Hung's CS170 8-puzzle solver.\n"
  intro  += "Type '1' to use a default puzzle, or '2' to enter your own puzzle.\n"
  print(intro)

  first_choice = int(input())
  puzzle = []

  if first_choice == 1:
    intro2 = "Enter the depth you wish to start with.\n"
    intro2 += "Your choices are '0', '2', '4', '8', '12', '16', '20' and '24'.\n"
    print(intro2)

    second_choice = int(input())
    if second_choice == 0:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif second_choice == 2:
      puzzle = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    elif second_choice == 4:
      puzzle = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    elif second_choice == 8:
      puzzle = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
    elif second_choice == 12:
      puzzle = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
    elif second_choice == 16:
      puzzle = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]  
    elif second_choice == 20:
      puzzle = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
    elif second_choice == 24:
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
    question.print_board()
    print(" ")
    graph_search(question, third_choice)


  elif third_choice == 2:
    print("A* with Misplaced Tile Heuristic Algorithm")
    question.print_board()
    print(" ")
    graph_search(question, third_choice)


  elif third_choice == 3:
    print("A* with Euclidean Distance Heuristic Algorithm")
    question.print_board()
    print(" ")
    graph_search(question, third_choice)


  else:
    print("Please try again and select an a valid option")
    sys.exit(0)

main()
