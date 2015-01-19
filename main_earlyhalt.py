# The Main Model of the Sugar Packet Game.
from bitstring import *
from copy import *
import sys
import resource
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6) #heheheh

class Vertex:
	
	def __init__(self, data, tree):
		# Formula: 1b Parity, 2b Win-State, 32b Board
		self.data = data

		# setup board and player
		self.player = self.data[0]
		self.color = self.data[1:3]
		self.board = self.data[3:]

		tree.already_included_dict[self.data.bin] = self
		
		# deal with terminal condition
		if self.is_terminal_state():
			if self.player:
				self.color = BitArray('0b10') #if it's your turn to move and the game is over, you lose
			else:
				self.color = BitArray('0b01')
			return
		
		# initialize children
		self.children = self.get_children()
		self.children_vertices = []
		for child in self.children:
			if not(child in tree.already_included):
				self.children_vertices.append(Vertex(child, tree))
				tree.already_included.append(child)
			else:
				self.children_vertices.append(tree.already_included_dict[child.bin])

			if tree.already_included_dict[child.bin].color != BitArray('0b00'):
				if self.player and (tree.already_included_dict[child.bin].color ==  BitArray('0b01')):#
					self.color = BitArray('0b01')
					return

				if not(self.player) and (tree.already_included_dict[child.bin].color ==  BitArray('0b10')):#
					self.color = BitArray('0b10')
					return

		
		# find children's win state
		if self.player == BitArray('0b0'):
			self.child_color_index = 0
			self.child_other_index = 1
		else:
			self.child_color_index = 1
			self.child_other_index = 0
		
		# find self's win state
		self.win_state = False
		
		for child in self.children_vertices:
			self.win_state = self.win_state or child.color[self.child_color_index]
		if self.win_state:
			self.color[self.child_color_index] = True
			self.color[self.child_other_index] = False
		else:
			self.color[self.child_color_index] = False
			self.color[self.child_other_index] = True
	
	def is_terminal_state(self):
		
		# check lines
		two_ways = [self.board, transpose(self.board)]
		for way in two_ways:
			for i in range(4):
				row = way[(8*i):(8*(i+1))]
				if (row == BitArray('0b01')*4) or (row == BitArray('0b01')*4):
					return True
		# check corners
		self.luc = self.data[3:5]
		self.ruc = self.data[9:11]
		self.llc = self.data[27:29]
		self.rlc = self.data[33:35]
		if not(self.luc == BitArray("0b00")):
				if (self.luc == self.ruc) and (self.luc == self.llc) and (self.luc == self.rlc):
					return True
		
		# check squares
		self.square_starts = [3, 5, 7, 11, 13, 15, 19, 21, 23]
		self.square_patterns = [
								BitArray('0b010100000101'),
								BitArray('0b010110000101'),
								BitArray('0b010110100101'),
								BitArray('0b010100100101'),
								BitArray('0b101000001010'),
								BitArray('0b101001001010'),
								BitArray('0b101001011010'),
								BitArray('0b101000011010')
								]
		
		for bit in self.square_starts:
			self.chunk = self.data[bit:bit+12]
			if self.chunk in self.square_patterns:
				return True
		
		# otherwise is not a terminal state
		return False
		
	
	def __eq__(self, other):
		return self.data == other.data
	
	def __ne__(self, other):
		return not self.data == other.data
	
	def __str__(self):
		return str(self.data)
	
	
	def get_children(self):
		# returns the strings of all of the available child game states
		piece_dict = {False:BitArray('0b01'), True:BitArray('0b10')}
		other_player = {True:BitArray('0b0'), False:BitArray('0b1')}
		own_piece = piece_dict[self.player]
		next_player = other_player[self.player]
		legal_moves = []
		empties = [BitArray('0b00'), BitArray('0b0000'), BitArray('0b000000')]
		four_ways_dict = {0:self.board, 1:transpose(self.board), 2:horizontal_flip(self.board), 3:horizontal_flip(transpose(self.board))}
		#print "********STARTING*********"
		#visual_board(self.board)
		#print "........................."
		for l in range(4):
			way = deepcopy(four_ways_dict[l])
			for i in range(4):
				row = deepcopy(way[(8*i):(8*(i+1))])
				for j in range(4):
					if row[(2*j):(2*(j+1))] == own_piece:

						blanks_right = 0

						for k in range(3-j): #going to the right

							if row[(2*(j+1)):(2*(j+2+k))] == BitArray('0b00')*(k+1):
								blanks_right = k+1
								blanks = row[(2*(j+1)):(2*(j+1+k))]

						if blanks_right != 0:
							sub_move_in_row = BitArray('0b00')*(blanks_right+1)
							sub_move_in_row[-2:] = deepcopy(own_piece)
							move_in_row = deepcopy(row)
							move_in_row[(2*j):(2*(j+blanks_right+1))] = deepcopy(sub_move_in_row)
							move_noflip = deepcopy(way)
							move_noflip[(8*i):(8*(i+1))] = deepcopy(move_in_row)

							legal_move = BitArray('0b00000000000000000000000000000000000')
							legal_move[0:1] = deepcopy(next_player)

							if l == 1:
								legal_move[3:] = deepcopy(transpose(move_noflip))
							elif l == 2:
								legal_move[3:] = deepcopy(horizontal_flip(move_noflip))
							elif l == 3:
								legal_move[3:] = deepcopy(transpose(horizontal_flip(move_noflip)))
							else:
								legal_move[3:] = deepcopy(move_noflip)
							#visual_board(legal_move[3:])
							legal_moves.append(legal_move)

		return legal_moves
# Transposes bitarrays that represent a grid of 4x4 two-bit cells.
def transpose(old_array):
	new_array = BitArray('0b00000000000000000000000000000000')
	for i in range(4):
		for j in range(4):	
			n = (j * 4 + i) * 2
			m = (i * 4 + j) * 2
			new_array[(n):(n+2)] = old_array[(m):(m+2)]
	return new_array

def horizontal_flip(old_array):
	new_array = BitArray('0b00000000000000000000000000000000')
	for i in range(4):
		for j in range(4):
			n = (j * 4 + i) * 2
			m = (j * 4 + (-1-i)%4) * 2
			new_array[(n):(n+2)] = old_array[(m):(m+2)]
	return new_array

def visual_board(array):
	print "////"
	icon_dict = {'00':'_', '01':'X', '10':'0', '11':'E'}
	for i in range(4):
		line = ""
		for j in range(4):
			n = (j * 4 + i) * 2
			icon = icon_dict[array[(n):(n+2)].bin]
			line = line + icon
		print line
	print"////"

def visual_row(array):
	icon_dict = {'00':'_', '01':'X', '10':'0', '11':'E'}
	line = ""
	for i in range(4):
		line = line + icon_dict[array[(2*i):(2*i+2)].bin]
	print line

class Tree:
	def __init__(self, initial_state):
		player_dict = {'10':"Player 1!", '01':"Player 2!"}
		self.already_included = [initial_state]
		self.already_included_dict = {}
		self.root =  Vertex(initial_state, self)
		self.winner = player_dict[self.root.color.bin]

if __name__ == "__main__":
	print "And the winner is..."
	initial_state = BitArray('0b00001000010000110000010010010000001') # i think..
	#initial_state = BitArray('0b00001010101000000000010000010001010') #(player 2 win)
	#initial_state = BitArray('0b00001101001100000101000100101101000') #(player 1 win)
	game_tree = Tree(initial_state)
	print game_tree.winner