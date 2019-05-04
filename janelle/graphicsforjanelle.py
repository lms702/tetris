import time
from graphics import *
# just means import everything from graphics.py
myWindow = GraphWin("Tetris", 500, 500)
# this is your screen ~ the two numbers are the size in pixels
rect = Rectangle(Point(100, 100), Point(400, 400))
# make a rectangle where one corner is at 100,100 and the other is at 400,400
rect.setFill('green')
# set color of rectangle to green
rect.draw(myWindow)
# draw the rectangle in myWindow

# same thing for a circle
circle = Circle(Point(250, 250), 100)
circle.setFill('lime green')
circle.draw(myWindow)

# wait 1 second
time.sleep(1)

# this time a picture
pic = Image(Point(250, 250), 'troy.gif')
pic.draw(myWindow)

time.sleep(1)

# now erase everything
rect.undraw()
time.sleep(1)
circle.undraw()
time.sleep(1)
pic.undraw()
time.sleep(1)

# some text
text = Text(Point(250, 250), "Click the screen to exit!")
text.draw(myWindow)

# wait for a click
myWindow.getMouse()