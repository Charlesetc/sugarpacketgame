# The Main Model of the Sugar Packet Game.
from bitstring import *
from copy import *

class Vertex:
	def __init__(self, player, color, board):
		self.player = player
		self.color = color
		self.board = board
		self.children = []
	
	def __eq__(self, other):
		return self.player == other.player and self.color == other.color and self.board == other.board
	
	def __ne__(self, other):
		return not self == other
	
	def __str__(self):
		return str(self.player+self.color+self.board)+": "+str(self.children)
	


class Tree:
	def __init__(self, initial_vertex):
		self.unexplored_vertices = [initial_vertex]
		self.explored_pairs = {}
		while self.unexplored_vertices:
			self.current_vertex = self.unexplored_vertices.pop()
			
			if is_terminal_vertex(self.current_vertex):
				if self.current_vertex.player:
					self.current_vertex.color = BitArray('0b10')
				else:
					self.current_vertex.color = BitArray('0b01')
				continue
			
			self.data = self.current_vertex.player+self.current_vertex.color+self.current_vertex.board
			self.explored_pairs.update({str(self.data) : self.current_vertex})
			
			self.children_states = get_children(self.current_vertex)
			self.children = []
			
			# bit of a hack, here
			for child in self.children_states:
				self.children.append(Vertex(child[0], child[1:3], child[4:]))
			
			for child in self.children:
				self.child_data = child.player+child.color+child.board
				try:
					self.current_vertex.children.append(self.explored_pairs[str(self.child_data)])
				except KeyError:
					self.unexplored_vertices.append(child)
					self.current_vertex.children.append(child)
			
		self.explored_vertices = self.explored_pairs.values()
		while self.explored_vertices:
			self.current_vertex = self.explored_vertices.popLeft()
			
			for child in self.current_vertex.children:
				# find current_vertex's children's significant bit
				if self.current_vertex.player == BitArray('0b0'):
					self.child_color_index = 0
					self.child_other_index = 1
				else:
					self.child_color_index = 1
					self.child_other_index = 0

				# find current_vertex's win state
				self.win_state = False

				for child in self.current_vertex.children:
					self.win_state = self.win_state or child.color[self.child_color_index]
				if self.win_state:
					self.current_vertex.color[self.child_color_index] = BitArray('0b1')
					self.current_vertex.color[self.child_other_index] = BitArray('0b0')
				else:
					self.current_vertex.color[self.child_color_index] = BitArray('0b0')
					self.current_vertex.color[self.child_other_index] = BitArray('0b1')
	

def is_terminal_vertex(vertex):
	
	# check lines
	
	# check corners
	vertex.luc = vertex.board[0:2]
	vertex.ruc = vertex.board[6:8]
	vertex.llc = vertex.board[22:24]
	vertex.rlc = vertex.board[30:32]
	if not(vertex.luc == BitArray("0b00")):
			if (vertex.luc == vertex.ruc) and (vertex.luc == vertex.llc) and (vertex.luc == vertex.rlc):
				return True
	
	# check squares
	vertex.square_starts = [0, 2, 4, 8, 10, 12, 16, 18, 20]
	vertex.square_patterns = [
							BitArray('0b010100000101'),
							BitArray('0b010110000101'),
							BitArray('0b010110100101'),
							BitArray('0b010100100101'),
							BitArray('0b101000001010'),
							BitArray('0b101001001010'),
							BitArray('0b101001011010'),
							BitArray('0b101000011010')
							]
	
	for bit in vertex.square_starts:
		vertex.chunk = vertex.board[bit:bit+12]
		if vertex.chunk in vertex.square_patterns:
			return True
	
	# otherwise is not a terminal vertex
	return False	
	

	
def get_children(vertex):
	# returns the strings of all of the available child game states
	piece_dict = {False:BitArray('0b01'), True:BitArray('0b10')}
	other_player = {True:BitArray('0b0'), False:BitArray('0b1')}
	own_piece = piece_dict[bool(vertex.player)]
	next_player = other_player[bool(vertex.player)]
	legal_moves = []
	empties = [BitArray('0b00'), BitArray('0b0000'), BitArray('0b000000')]
	four_ways_dict = {0:vertex.board, 1:transpose(vertex.board), 2:horizontal_flip(vertex.board), 3:horizontal_flip(transpose(vertex.board))}
	print "********STARTING*********"
	visual_board(vertex.board)
	print "........................."
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
						visual_board(legal_move[3:])
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

if __name__ == "__main__":
	initial_vertex = Vertex(	player = BitArray('0b0'), color = BitArray('0b00'),
								board = BitArray('0b01000010000110000010010010000001') # i think..
							)
	game_tree = Tree(initial_vertex)