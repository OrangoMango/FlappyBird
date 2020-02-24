import os, sqlite3

class Highscore:
	def __init__(self, users=[], pathinit=""): #__init__ method for Highscore
		self.users = users
		self.path = pathinit
		self.hs = {}
	def getTable(self): #Load all the highscores in a dictionary
		for user in self.users:
			if os.path.exists("/home/%s/.FlappyBird/highscore.txt" % user):
				f = open("/home/%s/.FlappyBird/highscore.txt" % user, "r")
				h = f.read()
				f.close()
				self.hs[user] = h.rstrip('\n')
		return self.hs
	def getSortedTable(self, tb): #Using SQLite for sort the dictionary
		if os.path.exists(self.path+".FlappyBird/highscores.db"):
			os.remove(self.path+".FlappyBird/highscores.db")
		conn = sqlite3.connect(self.path+".FlappyBird/highscores.db")
		cursor = conn.cursor()
		sql = "CREATE TABLE highscores(name TEXT, highscore INTEGER)"
		cursor.execute(sql)
		hsdic = self.getTable()
		for k, v in hsdic.items():
			sql = "INSERT INTO highscores VALUES(?, ?)"
			cursor.execute(sql, (k,v))
			conn.commit()
		sql = "SELECT * FROM highscores ORDER BY highscore DESC"
		cursor.execute(sql)
		sdic = {}
		for item in cursor:
			sdic[item[0]] = item[1]
		conn.close()
		return sdic
