import socket
import threading
from random import randint
import string
import sys


#Colors and styles for text output on the screen
class bcolors:
	PINK = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


#Board Class: Corresponds to the game itself, the board with its boats
class Board(object):

	#We enter number of rows (r), columns (c) and boats in board (q)
	def __init__(self, r, c, q):
		#game board
		self.board = []
		#Boats on the board
		self.boats = []

		#We started the necessary methods
		self.loadBoard(r, c)
		self.fillBoats(q)

	# Add rows and columns to the board
	def loadBoard(self, r, c):
		# Filled my board with r: rows and c: columns
		circle = u"\u25CB" 
		circle = circle.encode('utf-8')
		for x in range(r):
			self.board.append([circle] * c)

	# Show the board
	def printBoard(self):
		#Add numbers for each column
		headBoard =  "  "
		for x in range(len(self.board[0])):
			headBoard =  headBoard + str(x + 1) + " "

		#Get alphabet for board side
		abc = list(string.uppercase)
		count = 0;
		outp = ""
		#We store the complete board
		for row in self.board:
		#Delete commas and commas, concatenate only string with "" .join
		#We also add one letter per row
			outp = outp + bcolors.OKGREEN + abc[count] + bcolors.PINK + " " + " ".join(row) + bcolors.ENDC + "\n"
			count = count + 1
		#We return the board
		return headBoard + "\n" + outp

	# We load each of the boats (with random) on the board
	# Parameters: number of boats to load on board
	def fillBoats(self, quan):
		# I get number of rows and columns of the board
		nrow = len(self.board)
		ncol = len(self.board[0])
		# I create my board of boats of the same size as the board
		for x in range(nrow):
			self.boats.append(["0"] * ncol)
		# We generate random positions
		# The number of times required
		count = 0
		while (count < quan):
			ship_row = randint(0, nrow - 1)
			ship_col = randint(0, ncol - 1)
			# If there is no boat in this position, it is created
			if self.boats[ship_row][ship_col] != "1":
				# The boats are represented with a "1"
				self.boats[ship_row][ship_col] = "1"
				count = count + 1

	# Shows boats on the board
	def printBoats(self):
		for row in self.boats:
		# Remove quotation marks and commas, concatenate only string
			print " ".join(row)

	# Method that allows to play a turn
	def play(self, r, col):
		#Convert row letter to number (to play)
		di = dict(zip(string.letters,[ord(c)%32 for c in string.letters]))
		r = di[str(r)] - 1
		col = col - 1 
		# If it is off the board
		if ( r < 0 or r >= len(self.board) ) or ( col < 0 or col >= len(self.board[0]) ):
			return "You've given the ocean"
		# If you gave in the same space above
		elif (self.boats[r][col] == "2"):
			return "You already hit this place"
		# If he gave a boat
		elif (self.boats[r][col] == "1"):
			self.boats[r][col] = "2"
			tick = u"\u2713"
			tick = tick.encode('utf-8')
			self.board[r][col] = tick
			win = True
			# Check if there are "ones" (boats on the board)
			# If they do not exist I mean kill them all
			for row in self.boats:
				for x in range(len(row)):
					if row[x] == "1":
						win = False
			# Yes, win returns win
			if win:
				return "win"
			return "Very well :)"
		# si no le dio a nada
		else:
			self.boats[r][col] = "2"
			self.board[r][col] = "x"
			return ":("

#Class carrying the game between the two users
# This is done in a game thread that joins two players
class Game(threading.Thread):  #Inherits from threading
	# Receives both players (users)
	def __init__(self, p1, p2):
		threading.Thread.__init__(self)
		self.p1 = p1
		self.p2 = p2
		self.turn = 1

	# Game start
	def run(self):

		print "\nThere are two users, a game has been created"
		# We tell player one who has entered the game
		self.p1.sendMsg("yes")
		self.p1.setName(self.p1.getMsg())
		print "The player 1 entered the name of: " + self.p1.getName()
		# We tell the player two who has entered the game
		self.p2.sendMsg("yes")
		self.p2.setName(self.p2.getMsg())
		print "The player 2 entered the name of: " + self.p2.getName()
		# We advise both players that the game has started
		self.p1.sendMsg(bcolors.OKGREEN + "STARTS THE GAME!!!" + bcolors.ENDC)
		self.p2.sendMsg(bcolors.OKGREEN + "STARTS THE GAME!!!" + bcolors.ENDC)
		print "Both names have been entered, game starts"
		#Starts the game in turns
		while True:
			# Player plays one (has his turn)
			if self.turn == 1:
				self.p1.sendMsg("turn")
				self.p2.sendMsg("noturn")
				nombre = self.p1.getName()
				# We show game boards to both players
				# Also if it's your turn to play or not
				self.p1.sendMsg(bcolors.BOLD + "+++++++++++\nIt's your turn\n+++++++++++\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard())
				self.p2.sendMsg(bcolors.BOLD + "++++++++++++\nOpponent turn\n++++++++++++\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard())
				# We get row and column entered by player 1
				row = self.p1.getMsg()
				col = int(self.p1.getMsg())
				# The game is played on the board of the contricante (player 2)
				result = self.p2.board.play(row, col)
				if result == "win":
					self.p1.sendMsg(" You Won!!")
					self.p2.sendMsg("You lost!!")
					# If he has won he leaves the cycle or game
					break
				else:
					#The result of the game is sent to the player
					self.p1.sendMsg(result)
				# Change the turn
				self.turn = 2
			# Play second player (has his turn)
			elif self.turn == 2:
				self.p1.sendMsg("noturn")
				self.p2.sendMsg("turn")
				# We show game boards to both players
				# Also if it's your turn to play or not
				self.p2.sendMsg(bcolors.BOLD + "+++++++++++\nIt's your turn\n+++++++++++\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard())
				self.p1.sendMsg(bcolors.BOLD + "++++++++++++\nOpponent turn\n++++++++++++\n-----------\n" + self.p1.getName() + "\n-----------\n" + bcolors.ENDC + self.p1.board.printBoard() + bcolors.BOLD + "\n-----------\n" + self.p2.getName() + "\n-----------\n" + bcolors.ENDC + self.p2.board.printBoard())
				# We get row and column entered by player 2
				row = self.p2.getMsg()
				col = int(self.p2.getMsg())
				# The game is played on the board of the contricant (player 1)
				result = self.p1.board.play(row, col)
				if result == "win":
					self.p2.sendMsg(" You Won!!")
					self.p1.sendMsg("You lost!!")
					# If he has won he leaves the cycle or game
					break
				else:
					# The result of the game is sent to the player
					self.p2.sendMsg(result)
				# Change the turn
				self.turn = 1
		# When I finish the game, I close the games socket.
		self.p1.closeSocket()
		self.p2.closeSocket()
		print "Game finished"
	
#class server
class Server():

	def __init__(self):
		#Variables needed to create socket
		#And to indicate the port and max queue
		self.host = "127.0.0.1"
		self.port = 9991
		self.maxcon = 1
		self.clients = []
		
	def start(self):
		# We create socket
		self.s=socket.socket()
		#Reserve the port
		self.s.bind((self.host, self.port))
		#The socket is listening for connections
		self.s.listen(self.maxcon)
		#We create a cycle, so that every time a customer arrives,
		# Creates a client and derives it to its own socket
		while True:
			# If there are 2 clients connected to the server create a game
			# And clean the client list
			if len(self.clients) == 2:
				game = Game(self.clients[0], self.clients[1])
				game.start()
   				del self.clients[0]
   				del self.clients[0]
   			# If there are no two users, the server receives it, creates its socket and
   			# Adds it to the list of users (clients)
			else: 
				client = User(self.s.accept())
				self.clients.append(client)
				client.start()
			
# 3 4 8 - 2 2 2
#Class user that has thread inheritance, which comes from thereading
class User(threading.Thread): #Inherits from threading
	def __init__(self, (sc, addr)):
		#I call the Thread class constructor
		threading.Thread.__init__(self)
		# Small socket leaving released main socket
		self.sc = sc
		self.addr = addr
		self.name = ''
		self.board = Board(3,4,8)

	def run(self):
		print "Client started"

	# Add user name
	def setName(self, n):
		self.name = n

	# Get username
	def getName(self):
		return self.name

	# Get messages from users
	def getMsg(self):
		return self.sc.recv(1024)

	# Close user's socket
	def closeSocket(self):
		self.sc.close()

	# Send messages to user
	def sendMsg(self, msg):
		self.sc.send(msg)

if __name__ == "__main__":
	server = Server()
	server.start()