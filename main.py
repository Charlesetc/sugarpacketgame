# The Main Model of the Sugar Packet Game.
from bitstring import *

class Vertex:
	
	def __init__(self, data=BitArray('0b00000000000000000000000000000000000'), tree):
		# Formula: 1b Parity, 2b Win-State, 32b Board
		
		# setup board and player
		self.player = self.data[0]
		self.color = self.data[1:3]
		self.board = self.data[3:]
		
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
			self.children_vertices.append(Vertex(child, self.tree))
			self.tree.already_included.append(child)
		
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
		if not self.luc == BitArray("0b00")
				self.luc == self.ruc and
				self.luc == self.llc and
				self.luc == self.rlc:
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
		own_piece = BitArray('0b11')
		own_piece[self.player] = 0
		legal_states = []

		for i in range(4):
			

		return BitArray('0b')
# Transposes bitarrays that represent a grid of 4x4 two-bit cells.
def transpose(old_array):
	new_array = BitArray('0b00000000000000000000000000000000')
	for i in range(4):
		for j in range(4):	
			n = (j * 4 + i) * 2
			m = (i * 4 + j) * 2
			new_array[(n):(n+2)] = old_array[(m):(m+2)]
	return new_array

class Tree:
	def __init__(self, initial_state):
		already_included = []
		root = Vertex(initial_state, self)

if __name__ == "__main__":
	print "Hello world!"
	initial_state = BitArray('0b0000100000010000110000010010010000001') # i think..
	game_tree = Tree(initial_state)