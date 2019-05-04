from graphics import *
# using graphics.py library found from
# https://mcsp.wartburg.edu//zelle/python/graphics.py
# using documentation from:
# https://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf
from screen import *
from shape import *
import time
import random
import os
def main():
	doki = False
	playthru = 0
	try:
		import winsound
	except ImportError:
		print('If you want some awesome tetris music, play this on Windows')
		os.remove('sayori.chr')
		os.remove('monika.chr') # ominous, isn't it
	else:
		try:
			file = open('sayori.chr', 'rb')
		except OSError:
			try:
				file = open('monika.chr', 'rb')
			except OSError:
				playthru = 3 # all other times
			else:
				playthru = 2 # second time
				file.close()
		else:
			playthru = 1 # first time
			file.close()
		if playthru == 1:
			sound = 'tetris.wav'
		elif playthru == 2:
			sound = 'doki.wav'
			doki = True
		else:
			r = random.random()
			if r < .25:
				sound = 'doki.wav'
				doki = True
			else:
				sound = 'tetris.wav'

		winsound.PlaySound(sound,  winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
	# opens graphics window with graphics.py
	win = GraphWin("Tetris", 360, 600)
	screen = Screen(win)
	Shape.screen = screen
	screen.drawGrid()
	win.setBackground('dark slate gray')
	shapes = ['T', 'L', 'bL', 'jack', 'jill', 'stick', 'square']
	interval = 1.0 # interval between when shapes move down
	intervalCounter = time.perf_counter() # keeps track of 
	lastTime = time.perf_counter()		  # time between 'cycles' or move-downs
	linesCleared = 0
	dialogue = 1
	heldPiece = random.choice(shapes) # initialized first held piece to a random piece
	holdUsed = False
	keepIncrementing = True # turns off when the pieces go too fast
	stickoMode = False # cheat mode with all sticks
	stickoText = Text(Point(280, 15), "sticko mode activated")
	stickoText.setFill('floral white')
	while True:
		lines = screen.checkLines() # sees if 1+ lines have been cleared
		if len(lines) > 0: # if they have...
			linesCleared += len(lines)
			screen.clearLines(lines) # actually clears the lines
			if dialogue == 1 and (doki or playthru < 3): # fun stuff
				txt = Text(Point(50, 15), "import os...")
				txt.setFill('white')
				txt.draw(win)
				dialogue = 2
			elif dialogue == 2:
				txt = Text(Point(85, 45), "")
				txt.setFill('white')
				if playthru == 1:
					txt.setText("os.remove('sayori.chr')")
					os.remove('sayori.chr') #bet you didn't see that coming
					txt.draw(win)
				elif playthru == 2:
					txt.setText("os.remove('monika.chr')")
					os.remove('monika.chr')
					txt.draw(win)
				dialogue = 3
		if holdUsed: # if hold is activated by typing 'c'
			temp = shapeName
			shapeName = heldPiece
			heldPiece = temp
		elif stickoMode: # elif stick mode is being used via typing 's'
			shapeName = 'stick'
		else: #else pick a random shape
			shapeName = random.choice(shapes)
		shape = Shape(shapeName, 8, 0)
		shape.draw()
		if not shape.move(0,1): # game over
			break
		placed = False
		almostPlaced = False # for when the piece is right on top of a surface
		holdUsed = False
		while not placed:
			#check line clear
			currTime = time.perf_counter()
			# increases the speed at which the piece drops every 5 seconds
			# until it hits a speed of .06 seconds per drop
			if keepIncrementing and currTime - intervalCounter > 5:
				if(interval < .06):
					keepIncrementing = False
				intervalCounter = time.perf_counter()
				interval *= .95
			# moves the piece down every 'interval' seconds
			# if the piece cannot be moved, it enters the 'almost placed' mode
			# after a second of being in this mode, it is finally placed
			if currTime - lastTime > interval:
				lastTime = currTime
				if not shape.move(0,1):
					if not almostPlaced:
						almostPlaced = True
						almostPlacedCounter = time.perf_counter()
					else:
						if currTime - almostPlacedCounter > 1:
							placed = True
				elif almostPlaced:
					almostPlaced = False
			# takes in keyboard commands
			keyStroke = win.checkKey()
			if keyStroke == 'Up':
				shape.rotate()
			elif keyStroke == 'Left':
				shape.move(-1,0)
			elif keyStroke == 'Right':
				shape.move(1,0)
			elif keyStroke == 'Down':
				shape.move(0,1)
			elif keyStroke == 'space':
				shape.place()
				placed = True
			# holds the current piece for later use
			elif keyStroke == 'c':
				if not holdUsed:
					placed = True
					shape.remove()
					if heldPiece:
						holdUsed = True
			# makes all future pieces sticks / can be toggled off with the same button
			elif keyStroke == 's':
				if stickoMode:
					stickoMode = False
					stickoText.undraw()
				else:
					stickoMode = True
					stickoText.draw(win)
	if doki:
		winsound.PlaySound('sayonara.wav',  winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
	screen.showScores(linesCleared, doki)
	win.getMouse() # closes on mouse click
	win.close()
main()