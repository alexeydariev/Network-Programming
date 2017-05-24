import socket
import time

class bcolors:
	PINK = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

s = socket.socket()
s.connect(('127.0.0.1',9991))

#We ask the user to enter a data
print bcolors.YELLOW + "Waiting for an opponent to enter ..." + bcolors.ENDC
# Lets play
while True:
	if s.recv(1024) == "yes":
		print bcolors.OKGREEN + "Ready to play" + bcolors.ENDC
		msg = bcolors.OKGREEN + "Enter your name here > " + bcolors.ENDC
		name = raw_input(msg)
		# We send the data to the server
		s.send(name)
		print bcolors.YELLOW + "Waiting for opponent's name ..." + bcolors.ENDC
		break
#game
time.sleep(1)
print s.recv(1024)
while True:
	isturn = s.recv(1024)
	if  isturn == "turn":
		print s.recv(1024)
		guess_row = raw_input("Enter a letter: ")
		guess_col = raw_input("Enter a number: ")
		s.send(guess_row)
		s.send(guess_col)
		result = s.recv(1024)
		if result == "You Won!!":
			print bcolors.OKGREEN + result + bcolors.ENDC
			break
		else:
			print bcolors.PINK + result + bcolors.ENDC
	elif isturn == "You lost!!":
		print bcolors.RED + "You lost!!" + bcolors.ENDC
		break
	else:
		result = s.recv(1024)
		if result == "You lost!!":
			print bcolors.OKGREEN + result + bcolors.ENDC
			break
		else:
			print result 
s.close()

