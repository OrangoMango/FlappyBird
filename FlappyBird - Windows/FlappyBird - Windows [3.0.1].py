'''
FlappyBird Version 2.9.3 on Ubuntu Linux

Game for python3.5 [Linux Version]
A similar game to FlappyBird on Android
For kick the bird you can use 'spacebar' or 'left mouse button'
By using 'p' you pause and resume the game and by using
'F3' you activate and deactivate development mode (you can not
die and there are rectangulars arround the sprites, so you can
see when the bird touches the sticks)

For feedback please write in the comments! or from menu
\BY PAUL KOCIAN OrangoMango (C)2019-2020
'''

#Program for python 3.5
try:
	from tkinter import *            #needed tkinter module
	from tkinter import messagebox, filedialog
	import tkinter.ttk as t
except ImportError:
	raise ImportError("You need to install tkinter module for python3.5")
from random import randint
import time, sys, os, threading
try:
	from playsound import *
except ImportError:
	raise ImportError("You need to install playsound module for python3.5")
try:                             #####IMPORT MODULES AND NOT CRASH PROGRAM WITH TRY-EXCEPT######
	import GamingIntro
except ImportError:
	raise ImportError("Missing file module for this program: \'GamingIntro.py\'")           #My module-file
try:
	import HighscoreManager
except ImportError:
	raise ImportError("Missing file module for this program: \'HighscoreManager.py\'")      #My module-file
try:
	import FeedbackInterface
except ImportError:
	raise ImportError("Missing file module for this program: \'FeedbackInterface.py\'")     #My module-file
try:
	import Preferences
except ImportError:
	raise ImportError("Missing file module for this program: \'Preferences.py\'")           #My module-file
try:
	from ErrorCase import ErrorManager
except ImportError:
	raise ImportError("Missing file module for this program: \'ErrorCase.py\'")           #My module-file

global home
#print(__file__.split("\ "[0])[2])
user = os.path.abspath("").split("\ "[0])[2]#input("Whats your current username directory on this computer?: ") #__file__.split("\ "[0])[2]#
home = "C:/Users/{0}".format(user) + "/"

#Sound
#directory, openfile, openfilename, openfilenames, openfiles, saveasfile, saveasfilename, commanddialog

highscore = 0

if os.path.isdir(home+".FlappyBird") == False:     #Create data directory
	os.mkdir(home+".FlappyBird")
	first_time = True
else:
	first_time = False
if os.path.exists(home+".FlappyBird/highscore.txt") == False:
	f = open(home+".FlappyBird/highscore.txt", "w")
	f.write(str(highscore))
	f.close()
else:
	f = open(home+".FlappyBird/highscore.txt", "r")
	dt = f.read()
	highscore = int(dt)
	f.close()

class CollisionZone(): #Collision zone class for development mode
	def __init__(self, game, x, y, x1, y1, color="blue"):
		self.game = game
		self.color = color
		self.id = self.game.canvas.create_rectangle(x, y, x1, y1, outline=self.color)
	def update(self, x, y, x1, y1):
		self.game.canvas.delete(self.id)
		self.id = self.game.canvas.create_rectangle(x, y, x1, y1, outline=self.color)
	def __del__(self):
		self.game.canvas.delete(self.id)

class Game():
	def __init__(self, dev=False, directory=""):
		self.dev = dev #development mode
		self.dir = directory #path location
		p = Preferences.Preference(pathinit=home, pt=self.dir)
		if p.getData() == {}:
			self.preferences_data = {'Kick-Key':'<space>', 'GamingIntro-Init':'0', \
						'Bindings':'p;F3;s', 'DevMode':'False', 'Scales':'180;14', "Color":"#00ff00"}
		else:
			self.preferences_data = p.getData()
		self.current_pref = [self.preferences_data['Kick-Key']] + \
				self.preferences_data['Bindings'].split(";")
		self.bars_space = int(self.preferences_data['Scales'].split(";")[0]) #space between bars (px)
		self.current_pref = [self.preferences_data['Kick-Key']] + self.preferences_data['Bindings'].split(";")
		self.tk = Tk()
		self.tk.bind("<Key>", self.keys)
		#self.tk.bind("<Destroy>", self.destroy)
		menu = Menu(self.tk) #Menu for user
		self.tk.config(menu=menu)
		def callback():
			self.gameover()
		def hsc():
			#init highscore from my HighscoreManager module
			h = HighscoreManager.Highscore(users=os.listdir("C:/Users"), pathinit=home)
			hs = h.getTable()
			shs = h.getSortedTable(hs) #get sorted highscores
			highscore = "Highscores: \n"
			for k, v in shs.items():
				highscore += str(k)+" "+str(v)+"; "
			messagebox.showinfo("OMGames", highscore)
		def w_fe():
			f = FeedbackInterface.Feedback(pathinit=home, users=os.listdir("C:/Users"))
			f.start()
		def s_fe():
			f = FeedbackInterface.Feedback(pathinit=home, users=os.listdir("C:/Users"))
			f.see_feedbacks()
		def pref():
			#messagebox.showinfo("Missing Option", "This option needs to be continued")
			p = Preferences.Preference(pathinit=home)
			p.initialization()
			#print(p.getData())
			self.preferences_data = p.getData()
			#print("preferences_data:", self.preferences_data)
			#print("\nQUIIIIIIIIIII\n")
			self.load_data_pref()
			p.mainloop()
		#pref()
		filemenu = Menu(menu, tearoff=0)
		feedmenu = Menu(menu, tearoff=0)
		prefmenu = Menu(menu, tearoff=0)
		menu.add_cascade(label="Game", menu=filemenu)
		menu.add_cascade(label="Feedback", menu=feedmenu)
		menu.add_cascade(label="Preferences", menu=prefmenu)
		feedmenu.add_command(label="Write feedback", command=w_fe)
		feedmenu.add_command(label="See feedbacks", command=s_fe)
		filemenu.add_command(label="See highscores", command=hsc)
		filemenu.add_separator()
		filemenu.add_command(label="Quit", command = callback)
		prefmenu.add_command(label="Change Settings", command=pref)
		imgicon = PhotoImage(file=os.path.join(self.dir,self.dir+'FlappyBird_Game/icon.gif'), master=self.tk) #Set icon of game
		self.tk.tk.call('wm', 'iconphoto', self.tk._w, imgicon)
		self.tk.title("Flappy Bird (OMGames) V3.0.1") #Game title
		self.canvas = Canvas(self.tk, width=600, height=500)
		self.canvas.pack()
		self.score = 0              #Default game values (score, highscore, attemps and if the game is Running)
		self.attemps = 1
		self.highscore = 0
		self.sound = True
		self.sound2 = True
		self.gameIsRunning = False
		self.score_text = self.canvas.create_text(290,20, fill="red", \
							font="Purisa 20 bold", \
							text="Score: %s Attemps: %s " \
																										"Highscore: %s" % (self.score, self.attemps, \
																																				self.highscore))
		self.canvas2 = Canvas(self.tk, width=600, height=100) #A second canvas for the bottom image
		self.canvas2.pack()
		self.pause = False #if game is paused
	def destroy(self, evt=None):
		try:
			self.save_highscore()
			self.tk.destroy()
		except:
			pass
	def load_data_pref(self):
		self.tk.unbind(self.current_pref[0])
		self.tk.bind("<Key-l>")#self.preferences_data['Kick-Key'], ball.kick)
		self.current_pref = [self.preferences_data['Kick-Key']] + self.preferences_data['Bindings'].split(";")
		#print("\n", self.current_pref, self.preferences_data, "\n")
		self.bars_space = int(self.preferences_data['Scales'].split(";")[0]) #space between bars (px)
	def keys(self, evt):
		if evt.keysym == self.current_pref[2] or evt.char == self.current_pref[2]: #For activating development mode
			self.dev = (not self.dev)
			if self.dev:
				print("Development mode activated")
			else:
				print("Development mode deactivated")
		if evt.char == self.current_pref[1] or evt.keysym == self.current_pref[1]: #for pause game
			self.pause = not (self.pause)
			if self.pause:
				self.gameIsRunning = False
				print("Game paused")
				messagebox.showinfo("OMGames", "Game paused, press p to resume")
			elif self.pause == False:
				print("Game resumed")
				messagebox.showinfo("OMGames", "Game resumed, after clicking the ok button the game will start")				
				self.gameIsRunning = True
				self.mainloop()
	def play_sound(self, path, bs=False, ks=False): #Playing sound effects using a thread so
		def pl(pt):               #that the game does not stop by playing the sound
			playsound(pt)
			if bs:
				self.sound = True
			'''if ks:
				self.sound2 = True'''
		if not bs:# or not ks:
			x = threading.Thread(target=pl, args=(path,))
			x.start()
		elif bs:
			if self.sound:
				x = threading.Thread(target=pl, args=(path,))
				self.sound = False
				x.start()
		'''elif ks:
			if self.sound2:
				x = threading.Thread(target=pl, args=(path,))
				self.sound2 = False
				x.start()'''
	def mainloop(self): #Game Mainloop
		try:
			while True:
				if self.gameIsRunning:
					ball.draw()              #Draw the bird
					pali[pli[0]].draw()      #Draw the sticks
					pali[pli[1]].draw()
					pali[pli[2]].draw()
					pali_r[pri[0]].draw()
					pali_r[pri[1]].draw()
					pali_r[pri[2]].draw()
					self.tk.update()
					self.canvas.tag_raise(self.score_text)
					time.sleep(0.01)
				else:
					self.tk.update()
		except:
			pass
	def gameover(self):
		self.gameIsRunning = False #Stop the game after gameover
		self.tk.update()
		self.play_sound(self.dir+"FlappyBird_Game/FlappyBird_Sounds/hit.mp3")
		self.play_sound(self.dir+"FlappyBird_Game/FlappyBird_Sounds/die.mp3")
		messagebox.showerror("Game over", "GAME OVER - Your Score is: %s Highscore: %s" % (self.score, \
																																												self.highscore))
		self.attemps += 1
		self.update_score()
		a = messagebox.askyesno("Game", "Do you want to continue playing?")
		if a:
			load = Tk()
			load.title("Attemp retry: %s" % self.attemps)
			ll = Label(load, text="Attemp retry: %s" % self.attemps)
			ll.pack()
			pr = t.Progressbar(load, length=150, value=0)
			pr.pack()
			vl = 0
			while vl <= 135:
				pr.config(value=vl)
				load.update()#_idletasks()
				time.sleep(0.7)
				vl += randint(0,35)
			l = Label(load, text="Done")
			l.pack()
			time.sleep(2)
			self.destroy()
			load.destroy()
			try:
				main(self.attemps, self.highscore, self.dir) #If the user wants to play another
									#time, it starts another time the main 
			except Exception as e:
				error = ErrorManager(e)
				error.showgui()
				error.mainloop()
		else:
			messagebox.showinfo("Game", "See you Player - Attemps: %s" % self.attemps)
			self.save_highscore()
	def save_highscore(self):
		f2 = open(home+".FlappyBird/highscore.txt", "w") #Save the current highscore
		f2.write(str(self.highscore))
		f2.close()
		try:
			self.tk.destroy()
		except:
			pass
	def update_score(self):
		self.canvas.itemconfig(self.score_text, text="Score: %s Attemps: %s " \
							"Highscore: %s" % (self.score, self.attemps, self.highscore))
		self.tk.update()
	def GetImageCoords(self, id, cc): #Get coordinates of something
		xy = self.canvas.coords(id) #2 items list of coords [x1, y1] because the function is for images
		xy.append(xy[0]+cc[0]) #add width to x coord
		xy.append(xy[1]+cc[1]) #add height to y coord
		return xy #get 4 items list
	def collision(self, ball_pos, pos_palo): #Fetch collision between two objects
		if ((ball_pos[0] >= pos_palo[0] and ball_pos[0] <= pos_palo[2]) and \
				(ball_pos[1] >= pos_palo[1] and ball_pos[1] <= pos_palo[3])) or \
				((ball_pos[2] >= pos_palo[0] and ball_pos[2] <= pos_palo[2]) and \
				(ball_pos[3] >= pos_palo[1] and ball_pos[3] <= pos_palo[3])):
			return True
		return False

class Ball():
	def __init__(self, game, x, y, image):
		self.game = game
		self.ih, self.iw = (image.height(), image.width()) #save img width and height
		self.xc, self.yc = (x, y)
		self.id = self.game.canvas.create_image(x,y, image=image, anchor="nw")
		self.y = 0.5
		self.game.tk.bind(g.preferences_data['Kick-Key'], self.kick)
		self.x = 0
		self.s = True
	def draw(self):
		if self.game.dev and self.s: #if development mode is activated and is the first time after deactivated
			self.collisionzone = CollisionZone(self.game, self.xc, self.yc, self.xc+self.iw, \
							self.yc+self.ih, color="red") #create collision zone
			self.s = False #it isn't more the first time
		self.game.canvas.move(self.id, self.x, int(self.y)) #vedi int
		self.y += 0.3 #the bird must go down
		self.game.play_sound(self.game.dir+"FlappyBird_Game/FlappyBird_Sounds/swoosh.mp3", bs=True)
		pos = self.game.GetImageCoords(self.id, [self.iw, self.ih])
		if self.game.dev:
			self.collisionzone.update(pos[0], pos[1], pos[2], pos[3]) #update collision zone
		elif not self.s:
			del self.collisionzone #delete collision zone
			self.s = True
		if pos[3] >= 500 or pos[1] <= 0: #if touching the borders
			self.game.gameover()
	def kick(self, evt):
		if self.game.gameIsRunning:
			#self.game.play_sound(self.game.dir+"FlappyBird_Game/FlappyBird_Sounds/wing.mp3", bs=True)
			self.y -= int(self.game.preferences_data['Scales'].split(";")[1]) #kick the bird 17 pixel upper

class Palo():
	def __init__(self, game, x, y, ball, image, image1):
		self.game = game
		self.ball = ball
		self.image = image   #top image
		self.image1 = image1 #bottom image
		self.xc, self.yc = (x, y)
		self.id = self.game.canvas.create_image(x,y, image=image1, anchor="nw")
		self.x = -1
		self.y = 0
		self.ih, self.iw = (image.height(), image.width())
		self.coord = [x, y, x+self.iw, y+self.ih]
		self.side = "bottom" #side of the stick
		if self.game.dev:
			self.collisionzone = CollisionZone(self.game, self.coord[0], self.coord[1], \
							self.coord[2], self.coord[3])
		self.s = True
	def draw(self):
		if self.game.dev and self.s:
			self.collisionzone = CollisionZone(self.game, self.xc, self.yc, self.xc+self.iw, \
							self.yc+self.ih)
			self.s = False
		self.game.canvas.move(self.id, int(self.x), self.y)
		pos_palo = self.game.GetImageCoords(self.id, [self.iw, self.ih])
		self.coord = pos_palo
		if self.game.dev:
			self.collisionzone.update(self.coord[0], self.coord[1], self.coord[2], self.coord[3])
		elif not self.s:
			del self.collisionzone
			self.s = True
		ball_pos = self.game.GetImageCoords(self.ball.id, [self.ball.iw, self.ball.ih])
		if self.game.collision(ball_pos, pos_palo): #if touching the ball:
			if self.game.dev: #with development mode you can not die!
				print("GameOver::Status")
				#time.sleep(0.4)
			else:
				self.game.gameover()
		if pos_palo[2] <= 0:
			self.game.canvas.delete(self.id)
			#choose if after the border the stick it will be with side bottom or side top
			if bool(randint(0,1)): #random choose     #top
				y = randint(-60, 0)
				self.id = self.game.canvas.create_image(600,y, image=self.image, anchor="nw")
				self.side = "top"
				return
			else: #bottom
				y = randint(350, 420)
				self.id = self.game.canvas.create_image(600,y, image=self.image1, anchor="nw")
				self.side = "bottom"
				return
		if pos_palo[2] == 220: #===SCORE MANIPULATION===
			self.game.play_sound(self.game.dir+"FlappyBird_Game/FlappyBird_Sounds/point.mp3")
			self.game.score += 1
			if self.game.score > self.game.highscore: #if you beat your highscore
				self.game.highscore = self.game.score
			self.game.update_score()

class Palo_Riserva():
	def __init__(self, game, palo, side, ball, image, image1):
		self.game = game
		self.palo = palo
		self.ball = ball
		self.image = image
		self.image1 = image1
		self.iw, self.ih = (image.width(), image.height())
		#create the stick with the opposite side of the other corrispondent stick
		if side == "bottom":
			self.id = self.game.canvas.create_image(self.palo.coord[0], \
								self.palo.coord[3]+self.game.bars_space, \
								image=self.image1, anchor="nw")
		elif side == "top":
			self.id = self.game.canvas.create_image(self.palo.coord[0], \
								(self.palo.coord[1]-self.game.bars_space)-self.ih, \
								image=self.image, anchor="nw")
		self.x = -1
		self.y = 0
		self.s = True
		tempos = self.game.GetImageCoords(self.id, [self.iw, self.ih]) #a temporary position of the stick
		self.s = True
		self.xc, self.yc = (tempos[0], tempos[1])
		if self.game.dev:
			self.collisionzone = CollisionZone(self.game, tempos[0], tempos[1], tempos[2], tempos[3])
	def draw(self):
		if self.game.dev and self.s:
			self.collisionzone = CollisionZone(self.game, self.xc, self.yc, self.xc+self.iw, self.yc+self.ih)
			self.s = False
		self.game.canvas.move(self.id, self.x, self.y)
		pos_palo_r = self.game.GetImageCoords(self.id, [self.iw, self.ih])
		ball_pos = self.game.GetImageCoords(self.ball.id, [self.ball.iw, self.ball.ih])
		if self.game.dev:
			self.collisionzone.update(pos_palo_r[0], pos_palo_r[1], pos_palo_r[2], pos_palo_r[3])
		elif not self.s:
			del self.collisionzone
			self.s = True
		if self.game.collision(ball_pos, pos_palo_r): #if touching ball:
			if self.game.dev:
				print("GameOver::Status")
				#time.sleep(0.4)
			else:
				self.game.gameover()
		if pos_palo_r[2] <= 0: #after touching border:
			self.game.canvas.delete(self.id)
			if self.palo.side == "bottom": #top #if the side of the corrispondent stick is bottom this stick has side top
				self.id = self.game.canvas.create_image(self.palo.coord[0], (self.palo.coord[1]-self.game.bars_space) \
									-self.ih, image=self.image, anchor="nw")
			elif self.palo.side == "top": #bottom
				self.id = self.game.canvas.create_image(self.palo.coord[0], self.palo.coord[3]+self.game.bars_space, \
									image=self.image1, anchor="nw")

def main(atmp, hs, path): #Main function for running game
	global pali, pali_r, pri, pli, ball, g
	g = Game(directory=path) #For development mode please write here 'g = Game(dev=True)'
	g.attemps = atmp #set game attemps
	g.highscore = hs #set game highscore
	g.update_score()

	if int(g.preferences_data['GamingIntro-Init']):
		i = GamingIntro.Intro(dir=path+"FlappyBird_Game/") #Normal Intro for game
		i.start_prg()
	g.dev = True if g.preferences_data['DevMode'] == 'True' else False

	backgroundimage = PhotoImage(file=g.dir+"FlappyBird_Game/background.gif", master=g.tk) #load background image
	btm = PhotoImage(file=g.dir+"FlappyBird_Game/bottom.gif", master=g.tk) #load bottom image

	bg = g.canvas.create_image(0,0, image=backgroundimage, anchor="nw")
	g.canvas2.create_image(0,0, image=btm, anchor="nw")

#===IMG===
	palo1 = PhotoImage(file=g.dir+"FlappyBird_Game/palo1.gif", master=g.tk)
	palo2 = PhotoImage(file=g.dir+"FlappyBird_Game/palo2.gif", master=g.tk)
	bird = PhotoImage(file=g.dir+"FlappyBird_Game/bird.gif", master=g.tk)
#=========

	ball = Ball(g, 120, 200, bird) #init the bird class
	pali = {} #a dictionary containing all the primary sticks
	pali_r = {} #a dictionary containing the secondary sticks
	pri = ["rpalo1", "rpalo2", "rpalo3"]
	pli = ["palo1", "palo2", "palo3"]
	c = 0
	for x in [610, 810, 1010]:
		y_value = randint(250,300)
		pali[pli[c]] = Palo(g, x, y_value, ball, palo1, palo2)                        #Update dictionaries
		pali_r[pri[c]] = Palo_Riserva(g, pali[pli[c]], "top", ball, palo1, palo2) 
		c += 1
	g.gameIsRunning = True #Start Game
	messagebox.showinfo("Game", "Game will start when you click the ok button, 'Return' or 'space' key")
	g.mainloop()           #Start Mainloop

if first_time and (not os.path.exists(home+".FlappyBird/directory.txt")):
	tk = Tk()
	fcd = open(home+".FlappyBird/directory.txt", "w")
	cd = filedialog.askdirectory(title="Select the FlappyBird directory", master=tk) + "/"
	fcd.write(cd)
	fcd.close()
	tk.destroy()

#==========================|PATH AREA|===================================
fcd = open(home+".FlappyBird/directory.txt")
cd = fcd.read().rstrip('\n')
fcd.close()
#========================================================================

if first_time:
	fi = GamingIntro.Intro(dir=cd+"FlappyBird_Game/", firsttime=True, button=True) #Intro for first time using the game
#==================|Introduction|======================<
	intk = Tk()
	intk.title("Introduction OMGames")
	messagebox.showinfo("OMGames", "Current files directory: %sFlappyBird_Game/" % cd)
	pl = Label(intk, text="INTRODUCTION", font=("bold")).pack()
	v1 = "Warning: If there is an \'No such file or directory\' error, please " \
				"change the directory file with your \'path\'"
	v2 = "Warning: This program creates files: dir: \'.FlappyBird/\'"
	v3 = "Warning: Program uses modules: tkinter, random, time, sqlite3, sys, os, " \
			"playsound, webbrowser, ErrorCase, HighscoreManager, FeedbackInterface, Preferences and GamingIntro"
	v4 = "Warning: This game is for 7+ and is not for videodipendent people (Blocked by waiting) - :-)"
	v5 = "All related images are copyright by .GEARS 2013, Program copyright by " \
				"OrangoMangoGames 2019-2020 (Paul Kocian)"
	v6 = "Keys: Spacebar or left button to kick the bird, p to pause and to resume, F3 for " \
					"turning on and off development mode, you can change them"
	v7 = "Privacy Therms: Your highscore will be accessible by all the players and you can" \
				" see their highscore"
	v8 = "Remember that if you close this window, you will in any case accept the Privacy Terms"
	labels = []
	texts = [v1, v2, v3, v4, v5, v6, v7, v8]
	for text in texts:
		l = Label(intk, text=text)
		l.pack()
		labels.append(l)
	def com():
		messagebox.showinfo("OMGames", "Have fun! And beat your highscores!")
		intk.destroy()
		return
	b = Button(intk, text="Accept Privacy and Continue", command=com)
	b.pack()
	intk.mainloop()
#======================================================<

if __name__ == '__main__':
	try:
		i = GamingIntro.Intro(dir=cd+"FlappyBird_Game/") #Normal Intro for game
		i.start_prg()
		main(1, highscore, cd)
	except Exception as e: #Fetch errors
		error = ErrorManager(e)
		error.showgui()
		error.mainloop()
