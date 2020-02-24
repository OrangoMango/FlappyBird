'''Module for intro to games'''

from tkinter import *
import tkinter.ttk as t
import time, random, os, playsound

class Intro:
	def __init__(self, backgroundcolor="lightgreen", firsttime=False, dir="", button=False):
		self.introfinished = False
		self.ft = firsttime
		self.w = Tk()
		self.w.tk.call('update')
		#imgicon = PhotoImage(file=os.path.join(dir,dir+'iconl.gif'))
		#self.w.tk.call('wm', 'iconphoto', self.tk._w, imgicon)
		self.w.title("OrangoMangoGames (OMGames)")
		self.introimage = PhotoImage(file=dir+"OrangoMango.gif", master=self.w)
		self.introimage2 = PhotoImage(file=dir+"CacoMacaco.gif", master=self.w)
		self.cv = Canvas(self.w, width=500, height=500, bg=backgroundcolor)
		self.cv.grid(column=0, row=0, columnspan=2)
		self.imgw, self.imgh = (self.introimage.width(), self.introimage.height())
		self.cv.create_image(250,250, image=self.introimage, anchor="center")
		self.cv.create_image(280, 250+self.imgh, image=self.introimage2, anchor="center")
		self.txtload = self.cv.create_text(250, self.imgh, text="Loading...", fill="red", anchor="center", font="Times 18")
		self.loading_texts = ["Loading...", "Loading sounds...", "Downloading images...", "Compressing sounds...", \
													"Loading images...", "Unpacking Archives...","Unpacking packages...","Loading Data...", \
													"Loading Launcher...","Loading Sprites...","Downloading Sprites...", "Ready to start"]
		l = Label(self.w, text="Launcher OMGames (C)2019 OrangoMango - PAUL KOCIAN")
		l.grid(column=0, row=1)
		time.sleep(0.2)
		pb = t.Progressbar(self.w, length=200, value=0)
		pb.grid(column=0, row=2)
		perc = 0
		while perc <= 125:
			if not self.ft:
				pb.config(value=perc)
				perc += random.randint(0,10)
				time.sleep(0.075)
				self.w.update_idletasks()
			else:
				pb.config(value=perc)
				r = random.randint(0,100)
				ind = 0
				if r <= 32:
					ind = 0
				elif r > 55 and r <= 100:
					ind = random.randint(0,len(self.loading_texts)-2)
				self.cv.itemconfig(self.txtload, text=self.loading_texts[ind])
				perc += random.randint(0,10)
				time.sleep(1.5)
				self.w.update_idletasks()
		time.sleep(1)
		self.cv.itemconfig(self.txtload, text=self.loading_texts[11])
		self.w.update()
		time.sleep(2)
		playsound.playsound(dir+"FlappyBird_Sounds/jingle.mp3")
		if button:
			bt = Button(self.w, text="Play", command=self.start_prg)
			bt.grid(column=1, row=2)
			self.w.update_idletasks()
			self.w.mainloop()
		self.introfinished = True
	def start_prg(self):
		self.introfinished = True
		self.w.destroy()
		time.sleep(0.5)

#i = Intro(dir="FlappyBird_Game/")
