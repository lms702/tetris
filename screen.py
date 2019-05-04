from graphics import *
from scores import Scores
import time
# screen dimension constants so that the dimensions of the window can be changed in the future
WIDTH = 360
HEIGHT = 600
CS = 30 # Cell Size (in pixels)

# Cell class for each cell of the screen grid
class Cell(object):
	# function init()
	# initializes location from parameters x, y, as well as fill and color
	# uses a Rectangle object from graphics.py
	def __init__(self, x, y):
		point1 = Point(CS * x, CS * y)
		point2 = Point(CS * (x + 1), CS * (y + 1) )
		self.rect = Rectangle(point1, point2)
		self.filled = False
		self.color = 'white'
		self.outline = 'light gray'

	# function draw()
	# draws a cell at its specified color on the scren
	def draw(self):
		self.rect.undraw()
		self.rect.setFill(self.color)
		self.rect.setOutline(self.outline)
		self.rect.draw(self.win)

	# function fill()
	# sets the fill status to true and sets the color from the parameter
	def fill(self, color):
		self.filled = True
		self.color = color
		self.outline = 'black'

	# function unfill()
	# sets the fill variable to false in the underlying array of the grid
	def unfill(self):
		self.filled = False

	# function getFill()
	# returns the fill status of the cell
	def getFill(self):
		return self.filled

	# function erase()
	# erases the cell from the screen
	def erase(self):
		self.rect.undraw()

	# function copyCell()
	# performs a deep copy of the given cell to self, except for the location
	# used for the place() function in shape.py
	def copyCell(self, otherCell):
		self.filled = otherCell.getFill()
		self.color = otherCell.color
		self.outline = otherCell.outline
		if self.filled:
			self.draw()
		else:
			self.erase()
	def __str__(self):
		return str(self.filled)

# Screen class for the grid on the screen
class Screen(object):

	# function init()
	# Initializes the grid on the screen
	# Implemented through a 2d array of Cell objects
	# Adds borders around the visible screen so that 
	# shapes cannot move outside of them
	def __init__(self, window, w=12, h=20):
		WIDTH = CS * w
		HEIGHT = CS * h
		Cell.win = window
		self.win = window
		self.width = w
		self.height = h
		self.arr = []
		for y in range(h + 4):
			row = []
			for x in range(w + 8):
				row.append(Cell(x - 4, y - 2))
			self.arr.append(row)
		for y in range(h + 4): 
			for x in range(4):
				self.arr[y][x].fill('black') # left border
			for x in range(w + 4, w + 8):
				self.arr[y][x].fill('black') # right border
		for x in range(4, w + 4): # bottom border
			for y in range(h + 2, h + 4):
				self.arr[y][x].fill('black')
		self.activePiece = None
		self.activeX = None
		self.activeY = None

	# function drawGrid()
	# draws lines on the screen to show where each cell is for ease of visibility
	def drawGrid(self):
		for y in range(0, HEIGHT, CS):
			p1 = Point(0, y)
			p2 = Point(WIDTH, y)
			line = Line(p1, p2)
			line.setFill('light gray')
			line.draw(self.win)
		for x in range(0, WIDTH, CS):
			p1 = Point(x, 0)
			p2 = Point(x, HEIGHT)
			line = Line(p1, p2)
			line.setFill('light gray')
			line.draw(self.win)

	# function checkLines()
	# checks to see if a line has been filled and should be cleared
	# returns a list of lines cleared, which can be empty
	def checkLines(self):
		y = -1
		lines = []
		for y in range(2, self.height + 2):
			lineFull = True
			for x in range(4, self.width + 4):
				if not self.arr[y][x].getFill():
					lineFull = False
					break
			if lineFull:
				lines.append(y)
		return lines

	# function clearLines()
	# takes the list of lines from checkLines() and clears each line
	def clearLines(self, lines):
		# blinks the lines twice before clearing them
		for i in range(4):
			for y in lines:
				for x in range(4, self.width + 4):
					if i % 2:
						self.arr[y][x].erase()
					else:
						self.arr[y][x].draw()
			time.sleep(.1)
		# clears a line by moving everything above it down once
		for line in lines:
			for y in range(line, 4, -1):
				for x in range(4, self.width + 4):
					self.arr[y][x].copyCell(self.arr[y - 1][x])

	# function showScores()
	# shows player scores and high scores after the game has ended
	# if the player's score places within the top 10 scores, they are prompted
	# to input their name so they can be displayed in later games
	def showScores(self, newScore, doki):
		outerRect = Rectangle(Point(CS, CS), Point(WIDTH - CS, HEIGHT - CS))
		outerRect.setFill('purple')
		outerRect.draw(self.win)
		innerRect = Rectangle(Point(CS + 5, CS + 5), \
			Point(WIDTH - CS - 5, HEIGHT - CS - 5)) 
		innerRect.setFill('floral white')
		innerRect.draw(self.win)

		text = Text(Point(WIDTH / 2, 2 * CS), "Game Over!")
		text.setTextColor('black')
		text.setSize(36)
		text.draw(self.win)

		text = Text(Point(WIDTH/2, CS * 3.5), "You cleared " + str(newScore) + ' lines!')
		text.setSize(18)
		text.setTextColor('black')
		text.draw(self.win)

		text = Text(Point(WIDTH/2, CS * 4.5), "High Scores:")
		text.setSize(18)
		text.setTextColor('black')
		text.draw(self.win)

		for i in range(1, 11):
			text = Text(Point(CS*1.65, CS * (4.4 + i)), str(i) + '.')
			text.draw(self.win)

		sc = Scores()
		newIdx = sc.addScore('', newScore)
		highScore = False
		if newIdx < 10:
			highScore = True
		scoreList = sc.getScores()
		vals = [5.5, 10]
		currScore = None
		for val in range(2):
			for i,scoreArr in enumerate(scoreList):
				if doki and not val: # :)
					text = Text(Point(CS*vals[val], CS * (5.4 + i)), 'Monika')
				else:
					text = Text(Point(CS*vals[val], CS * (5.4 + i)), str(scoreArr[val]))
				text.draw(self.win)
				if val == 0 and i == newIdx:
					currScore = text
		if not highScore:
			return
		newEntry = Entry(Point(CS*5.5, CS*(5.4 + newIdx)), 10)
		newEntry.draw(self.win)
		submitted = False
		newName = ''
		while self.win.getKey() != 'Return':
			newName = newEntry.getText()
		newEntry.undraw()
		currScore.undraw()
		if doki:
			currScore.setText('Just Monika') # :')
		else:
			currScore.setText(newName)
		currScore.draw(self.win)
		sc.addName(newIdx, newName)