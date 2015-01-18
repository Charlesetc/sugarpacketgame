# The Main Model of the Sugar Packet Game.
from bitstring import *

class Vertex:
	data = BitArray('0b00000000000000000000000000000000000')
	# Formula: 1b Parity, 2b Win-State, 32b Board
	
	def __init__(self):
		# setup board and player
		self.board = self.data[4:]
		self.player = self.data[0]
		
		if self.is_winning_state():
			if self.data[0]:
				self.data[1:3] = BitArray('0b10')
			else:
				self.data[1:3] = BitArray('0b01')
			return

		# setup children
		self.children = self.get_children()


		# do something
		
		# assuming we have list of children done
		
		self.color = ByteArray('0b0')
		for child in self.children:
			self.color = self.color[0] or child.data[self.player+1]
		self.data[self.player+1] = self.color
	
	def is_winning_state(self):
		self 
		# check lines
		
		# check corners
		self.corners = []
		self.value = -1
		for corner in self.corners:
			if self.value == -1:
				self.value = self.data[corner:corner+2]
			elif self.value == self.data[corner:corner+2]:
				pass	
		
		# check sqaures
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
		
		
	
	def __eq__(self, other):
		return self.data == other.data
	
	def __ne__(self, other):
		return not self.data == other.data
	
	def __str__(self):
		return self.data
	
	def player(self):
		return self.data[0]
	


if __name__ == "__main__":
	print "Hello world!"

# Transposes bitarrays that represent a grid of 4x4 two-bit cells.
def transpose(old_array):
	new_array = BitArray('0b00000000000000000000000000000000')
	for i in range(4):
		for j in range(4):	
			n = (j * 4 + i) * 2
			m = (i * 4 + j) * 2
			new_array[(n):(n+2)] = old_array[(m):(m+2)]
	return new_array
