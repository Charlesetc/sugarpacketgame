# The Main Model of the Sugar Packet Game.

class Vertex:
	self.data = "0b00000000000000000000000000000000000"
	# Formula: 1b Parity, 2b Win-State, 32b Board
    
	def __init__(self):
		
		self.color = self.is_winning_state()
		if not self.color == "0b00":
		    self.data[1:3] = self.color
		    return
		
		# setup children
    	self.children = self.get_children()
		
		# do something
		
		# assuming we have list of children done
		
		self.color = "0b0"
		self.player = self.data[0]
		for child in self.children:
		    self.color = self.color[0] or child.data[self.player+1]
		self.data[self.player+1] = self.color
    
    def is_winning_state(self):
        return 0
    
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