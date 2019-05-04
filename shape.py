import copy

class Shape(object): 
	# class dictionary variable mapping all the shapes to their colors
	colors = shapes = {'T':'fuchsia', 'L':'orange', 'bL':'blue', 'jack':'green', 
		'jill':'red', 'stick':'cyan', 'square':'yellow'}
	# class variable of all of the different shapes
	shapes = \
	{
		'T':
		[ 
		[0,0,0,0],
		[0,0,1,0],
		[0,1,1,1],
		[0,0,0,0]
		],
		'L':[ 
		[0,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,0,0]
		],
		'bL':[ # bL
		[0,0,1,0],
		[0,0,1,0],
		[0,1,1,0],
		[0,0,0,0]
		],
		'jack':[ # Jack
		[0,0,0,0],
		[0,0,1,1],
		[0,1,1,0],
		[0,0,0,0]
		],
		'jill':[ # Jill
		[0,0,0,0],
		[1,1,0,0],
		[0,1,1,0],
		[0,0,0,0]
		],
		'stick':[ # stick
		[0,0,1,0],
		[0,0,1,0],
		[0,0,1,0],
		[0,0,1,0]
		],
		'square':[ # square
		[0,0,0,0],
		[0,1,1,0],
		[0,1,1,0],
		[0,0,0,0]
		]	
	}

	screen = None
	# function init()
	# typeOf is a string of the name of the new piece
	# x and y are the starting location of the piece on the grid
	def __init__(self, typeOf, x, y):
		self.typeOf = typeOf
		self.arr = copy.deepcopy(self.shapes[typeOf])
		self.x = x
		self.y = y
		self.color = self.colors[typeOf] # sets proper color

	# function draw()
	# draws self on the board at (self.x, self.y)
	def draw(self): #x and y are top left corner
		for y in range(4):
			for x in range(4):
				if(self.arr[y][x] == 1):
					currCell = self.screen.arr[self.y + y][self.x + x]
					currCell.fill(self.color)
					currCell.draw()

	# function remove()
	# erases the shape from the screen at (self.x, self.y)
	def remove(self):
		for y in range(4):
			for x in range(4):
				if(self.arr[y][x] == 1):
					currCell = self.screen.arr[self.y + y][self.x + x]
					currCell.unfill()
					currCell.erase()

	# function checkCollision() 
	# checks if a move is valid
	# parameter tempArr is the shape of the piece after it has been moved
	# parameters ox and oy specify which direction the piece would be moved
	# if the piece does not collide with any other or a wall, returns True
	# works for both move() and rotate()
	def checkCollision(self, tempArr, ox, oy):
		for y in range(4):
			for x in range(4):
				if(self.arr[y][x] == 1):
					currCell = self.screen.arr[self.y + y][self.x + x]
					currCell.unfill()
		collision = False
		for y in range(4):
			for x in range(4):
				if(tempArr[y][x]):
					if(self.screen.arr[oy + y][ox + x].getFill()):
						collision = True
		for y in range(4):
			for x in range(4):
				if(self.arr[y][x] == 1):
					currCell = self.screen.arr[self.y + y][self.x + x]
					currCell.fill(self.color)
		return collision

	# function move()
	# moves the piece in the direction specified by dx and dy
	# moves the piece both in the underlying array as well as on the screen
	# does nothing if the piece cannot be moved (if there is a collision)
	def move(self, dx, dy, redraw=True):
		if self.checkCollision(self.arr, self.x + dx, self.y + dy):
			return False
		self.remove()
		self.x += dx
		self.y += dy
		if redraw:
			self.draw()
		return True

	# function rotate()
	# rotates the piece by 90 degrees if possible
	# does not shift the piece, so rotates are not always possible
	# when against a wall or other piece
	def rotate(self):
		tempArr = copy.deepcopy(self.arr)
		for y in range(4):
			for x in range(4):
				tempArr[y][x] = self.arr[3-x][y]
		move = 0
		if self.checkCollision(tempArr, self.x, self.y):
			return False
		self.remove()
		self.arr = tempArr
		if move:
			self.move(move, 0)
		self.draw()
		return True
	# function place()
	# places the piece as low as possible by calling the move() function until
	# a collion is found
	def place(self):
		placed = True
		while placed:
			placed = self.move(0, 1)