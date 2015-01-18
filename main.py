# The Main Model of the Sugar Packet Game.

class Vertex:
	board = "0b00000000000000000000000000000000000"
	# Formula: 1b Parity, 2b Win-State, 32b Board
    
	def __init__(self):
		self.all_next = []
    
	def __eq__(self, other):
		return self.board == other.board
    
    def __ne__(self, other):
		return not self.board == other.board
    
    def __str__(self):
        return self.board
    
	def player(self):
		return self.board[0]
    


if __name__ == "__main__":
    print "Hello world!"