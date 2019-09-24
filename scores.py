# Scores class used for keeping track of high scores
class Scores(object):

	# function init()
	# reads top 10 high scores from a csv file
	# stores them in a private local list variable
	def __init__(self):
		with open('scores.csv', 'r') as ifile:
			self.__scoreList__ = []
			for line in ifile: 
				lineArr = line.split(',')
				if len(lineArr) == 2:
					lineArr[1] = int(lineArr[1])
					self.__scoreList__.append(lineArr)

	# function getScores()
	# returns the list of scores
	def getScores(self):
		return self.__scoreList__

	# function addScore()
	# adds a new score and username to the list of scores if it 
	# ranks within the top 10 scores
	def addScore(self, newName, newScore):
		idx = self.getIdxForInsert(newScore, len(self.__scoreList__)-1)
		if idx < 10:
			self.__scoreList__.insert(idx, [newName, newScore])
		if len(self.__scoreList__) > 10:
			del self.__scoreList__[9]
		self.saveScores()
		return idx

	# function getIdxForInsert()
	# helper function for addScore()
	# returns the index for where the new score should be added
	def getIdxForInsert(self, newScore, end, start=0):
		numScores = len(self.__scoreList__)
		for i in range(numScores):
			if newScore >= self.__scoreList__[i][1]:
				return i
		return numScores

	# function addName()
	# changes the name of a high score
	def addName(self, idx, newName):
		self.__scoreList__[idx][0] = newName
		self.saveScores()

	# function saveScores()
	# saves the high scores to the file they were read from
	def saveScores(self):
		with open('scores.csv', 'w') as ofile:
			for highScore in self.__scoreList__:
				ofile.write(highScore[0] + ',' + str(highScore[1]) + '\n')