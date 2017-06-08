class bcolors:
	PINK = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class Bombfield:
	def __init__(self):
		self.field = {}
		cellNumber = 4
		for code in range(ord('A'), ord('E')):
			self.field[chr(code)] = {}
			for j in range(1, cellNumber + 1):
				 k = {j:False}
				 self.field[chr(code)][j] = ""