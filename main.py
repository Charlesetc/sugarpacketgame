# The Main Model of the Sugar Packet Game.

class Vertex:
	board = "0b00000000000000000000000000000000000"
	# Formula: 1b Parity, 2b Win-State, 32b Board


	def __init__(self):
		self.all_next

	def equal_to(self, other):
		self.board == other.board	

	def player(self):
		self.board[0]
