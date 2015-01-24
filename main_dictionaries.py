# Trying it with dictionaries 
from bitstring import *
from copy import *
import pickle
import os
import shutil
import itertools
#import sys
#sys.setrecursionlimit(10**6) #heheheh

#data format: 1b player id, 32b board

class Tree:

	def __init__(self, initial_state, interval):
		self.initial_state = initial_state
		self.dict_num = ((1000000) // interval) + 1
		self.interval = interval

		own_dir = os.path.dirname(__file__)
		self.dict_dir = os.path.join(own_dir, 'sugarpacket_dictionaries')

		if os.path.exists(self.dict_dir):
			shutil.rmtree(self.dict_dir)
			
		os.makedirs(self.dict_dir)
		self.init_dictionaries()

	def init_dictionaries(self):
		index = 0
		cur_dict = {}
		truth_dict = {0:False, 1:True}
		all_pieces = ([BitArray('0b00')]*8) + ([BitArray('0b10')]*4) + ([BitArray('0b01')]*4)

		for order in itertools.permutations(all_pieces):

			for player_n in range(2):
				if player_n == 0:
					new_state = BitArray('0b000000000000000000000000000000000')
				else:
					new_state = BitArray('0b100000000000000000000000000000000')
				for i in range(16):
					new_state[(1+2*i):(1+2*(i+1))] = order[i]

				print visual_board(new_state[1:])

				if is_terminal_board(new_state[1:]):
					if player_n == 0: #player 1's turn
						cur_dict[index] = [BitArray('0b01')] #player 2 wins
					else:
						cur_dict[index] = [BitArray('0b10')] #player 1 wins
				else:
					cur_dict[index] = [BitArray('0b00')] + get_children(new_state)#undecided

				index = index + 1
				if index % self.interval == 0:
					pickleloc = os.path.join(self.dict_dir, str(index) + ".p")
					pickle.dump(cur_dict, open(pickleloc, "wb"))
					cur_dict = {}

			#if index == self.interval:

def get_children(state):
	# returns the strings of all of the available child game states
	board = state[1:]
	piece_dict = {False:BitArray('0b01'), True:BitArray('0b10')}
	other_player = {True:BitArray('0b0'), False:BitArray('0b1')}
	own_piece = piece_dict[state[0]]
	next_player = other_player[state[0]]
	legal_moves = []
	empties = [BitArray('0b00'), BitArray('0b0000'), BitArray('0b000000')]
	four_ways_dict = {0:board, 1:transpose(board), 2:horizontal_flip(board), 3:horizontal_flip(transpose(board))}
	#print "********STARTING*********"
	#visual_board(board)
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

						legal_move = BitArray('0b000000000000000000000000000000000')
						legal_move[0:1] = deepcopy(next_player)

						if l == 1:
							legal_move[1:] = deepcopy(transpose(move_noflip))
						elif l == 2:
							legal_move[1:] = deepcopy(horizontal_flip(move_noflip))
						elif l == 3:
							legal_move[1:] = deepcopy(transpose(horizontal_flip(move_noflip)))
						else:
							legal_move[1:] = deepcopy(move_noflip)
						#visual_board(legal_move[3:])
						legal_moves.append(legal_move)

	return legal_moves

def is_legal_board(board):

	player1_count = 0
	player2_count = 0
	blank_count = 0

	for i in range(16):
		if board[(2*i):(2*(i+1))] == BitArray('0b00'):
			blank_count = blank_count + 1
		elif board[(2*i):(2*(i+1))] == BitArray('0b01'):
			player1_count = player1_count + 1
		elif board[(2*i):(2*(i+1))] == BitArray('0b10'):
			player2_count = player2_count + 1

	if (player1_count == 4) and (player2_count == 4) and (blank_count == 8):
		return True
	else:
		return False

def is_terminal_board(board):
		
	# check lines
	two_ways = [board, transpose(board)]
	for way in two_ways:
		for i in range(4):
			row = way[(8*i):(8*(i+1))]
			if (row == BitArray('0b01')*4) or (row == BitArray('0b01')*4):
				return True
	# check corners
	luc = board[0:2]
	ruc = board[6:8]
	llc = board[24:26]
	rlc = board[30:32]
	if not(luc == BitArray("0b00")):
			if (luc == ruc) and (luc == llc) and (luc == rlc):
				return True
	
	# check squares
	square_starts = [0, 2, 4, 8, 10, 12, 16, 18, 20]
	square_patterns = [
							BitArray('0b010100000101'),
							BitArray('0b010110000101'),
							BitArray('0b010110100101'),
							BitArray('0b010100100101'),
							BitArray('0b101000001010'),
							BitArray('0b101001001010'),
							BitArray('0b101001011010'),
							BitArray('0b101000011010')
							]
	
	for bit in square_starts:
		chunk = board[bit:bit+12]
		if chunk in square_patterns:
			return True
	
	# otherwise is not a terminal state
	return False

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
	print "And the winner is..."
	initial_state = BitArray('0b001000010000110000010010010000001') # i think..
	#initial_state = BitArray('0b001010101000000000010000010001010') #(player 2 win)
	#initial_state = BitArray('0b001101001100000101000100101101000') #(player 1 win)
	tree = Tree(initial_state, 100000)

	# def init_dictionaries(self):

	# 	for i in range(self.dict_num):
	# 		cur_dict = {}
	# 		start_num = i * self.interval

	# 		for j in range(self.interval):
	# 			cur_num = start_num + j
	# 			cur_state = BitArray('0b' + str(bin(cur_num)))
	# 			cur_board = cur_state[1:]

	# 			if is_legal_board(cur_board):
	# 				visual_board(cur_board)
	# 				if is_terminal_board(cur_board):
	# 					if cur_state[0]: #(player 2's turn)
	# 						cur_dict[j] = [BitArray('0b10')] + get_children(cur_state)#player 1 wins
	# 					else:
	# 						cur_dict[j] = [BitArray('0b01')] + get_children(cur_state)#player 2 wins
	# 				else:
	# 					cur_dict[j] = [BitArray('0b00')] + get_children(cur_state)#undecided
					
			
	# 		pickleloc = os.path.join(self.dict_dir, str(i) + ".p")
	# 		pickle.dump(cur_dict, open(pickleloc, "wb"))