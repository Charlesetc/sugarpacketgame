# The Main Model of the Sugar Packet Game.
from bitstring import *

class Vertex:
	
	def __init__(self, data, tree):
		# Formula: 1b Parity, 2b Win-State, 32b Board
		self.data = data
		# setup board and player
		self.player = self.data[0]
		self.color = self.data[1:3]
		self.board = self.data[3:]

		self.tree.already_included_dict[self.data.uint] = self
		
		# deal with terminal condition
		if self.is_terminal_state():
			if self.player:
				self.color = BitArray('0b10')
			else:
				self.color = BitArray('0b01')
			return
		
		# initialize children
		self.children = self.get_children()
		self.children_vertices = []
		for child in self.children:
			if not(child in self.tree.already_included):
				self.children_vertices.append(Vertex(child, tree))
				self.tree.already_included.append(child)
			else:
				self.children_vertices.append(self.tree.already_included_dict[child.uint])
		
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
		four_ways = [self.board, transpose(self.board), horizontal_flip(self.board), horizontal_flip(transpose(self.board))]

		for way in four_ways:
			for i in range(4):
				row = way[(8*i):(8*(i+1))]
				for j in range(4):
					if row[(2*j):(2*(j+1))] == own_piece:

						blanks_right = 0
						right_move = None

						for k in range(4-j): #going to the right
							if row[(2*(j+1)):(2*(j+1+k))] in empties:
								blanks_right = k+1
								blanks = row[(2*(j+1)):(2*(j+1+k))]

						if blanks_right != 0:
							sub_move_in_row = blanks.append(own_piece)
							move_in_row = row
							move_in_row[(2*j):(2*(j+blanks_right))] = sub_move_in_row
							move_noflip = way
							move_noflip[(8*i):(8*(i+1))] = move_in_row

							if way == transpose(self.board):
								legal_move = next_player.append(BitArray('0b00').append(transpose(move_noflip)))
							elif way == horizontal_flip(self.board):
								legal_move = next_player.append(BitArray('0b00').append(horizontal_flip(move_noflip)))
							elif way == horizontal_flip(transpose(self.board)):
								legal_move = next_player.append(BitArray('0b00').append(transpose(horizontal_flip(move_noflip))))
							else:
								legal_move = next_player.append(BitArray('0b00').append(move_noflip))

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

class Tree:
	def __init__(self, initial_state):
		self.already_included = [initial_state]
		self.already_included_dict = {}
		self.root =  Vertex(initial_state, self)

if __name__ == "__main__":
	print "Hello world!"
	initial_state = BitArray('0b0000100000010000110000010010010000001') # i think..
	game_tree = Tree(initial_state)