from tkinter import *
from tkinter import messagebox, colorchooser
import sqlite3, os
import tkinter.ttk as t

class Preference():
	def __init__(self, pathinit="", pt=""):
		self.path = pathinit

		fc = ["F"+str(x+1) for x in range(12)]
		ap = "0123456789abcdefghijklmnopqrstuvwxyz"
		self.pos_keys = tuple(fc + list(ap))
	def initialization(self):
		self.data = [None] * 6
		self.tk = Tk()
		self.tk.title("Preferences")

		self.key = StringVar(master=self.tk)
		self.key.set("<space>")
		self.ingmi = IntVar(master=self.tk)
		self.devmode = BooleanVar(master=self.tk)
		self.color = "#00ff00"

		self.txts = {"binds":["SpaceBar", "Left-Button"], \
								"intro":["Kick-Bindings", "InitialAttemp-GamingIntro", "Binding-Keys", \
													"Development Mode", "Scrollbars"], \
								"binds-key":["<space>", "<Button-1>"], \
								"types-type":["Kick-Key", "GamingIntro-Init", "Bindings", "DevMode", "Scales", "Color"], \
								"checkbuttons":["Activate GamingIntro at any attemp", "Activate Development " \
																"Mode on game start"]}

		#=========Key-Kick=============
		lb = LabelFrame(self.tk, text=self.txts["intro"][0], font=("bold"))
		lb.pack()
		for x in range(2):
			r = Radiobutton(lb, text=self.txts["binds"][x], \
											value=self.txts["binds-key"][x], \
											variable=self.key)
			r.grid(row=0, column=x)

		#==============================

		#=========Initial-GamingIntro=========
		lb2 = LabelFrame(self.tk, text=self.txts["intro"][1], font=("bold"))
		lb2.pack()
		ck = Checkbutton(lb2, text=self.txts["checkbuttons"][0], variable=self.ingmi)
		ck.grid()
		def changecolor():
			color = colorchooser.askcolor(master=self.tk)
			self.color = color[1]
			lc["bg"] = self.color
		bc = Button(lb2, text="Change GamingIntro background color", command=changecolor)
		bc.grid(row=1, column=0)
		lc = Label(lb2, bg="#00ff00", text="     ")
		lc.grid(row=1, column=1)
		#=====================================

		#==========Development Mode===========
		lb4 = LabelFrame(self.tk, text=self.txts["intro"][3], font=("bold"))
		lb4.pack()
		ck = Checkbutton(lb4, text=self.txts["checkbuttons"][1], variable=self.devmode)
		ck.pack()
		#=====================================

		#=========Binding-Keys==========
		lb3 = LabelFrame(self.tk, text=self.txts["intro"][2], font=("bold"))
		lb3.pack()
		testi = ["Pause", "Dev. Mode", "Screenshot"]
		self.comboxes = []
		currents = [self.pos_keys.index('p'), self.pos_keys.index("F3"), self.pos_keys.index('s')]
		for x in range(3):
			l = Label(lb3, text=testi[x])
			cbx = t.Combobox(lb3, values=self.pos_keys)
			l.grid(column=0, row=x)
			cbx.grid(column=1, row=x)
			cbx.current(currents[x])
			self.comboxes.append(cbx)
		#===============================

		#=======SPACES SCALES========
		lb4 = LabelFrame(self.tk, text=self.txts["intro"][4], font=("bond"))
		lb4.pack()
		testi = ["Spaces between bars", "Px space for kick bird"]
		spaces = [[160, 200], [10, 20]]
		self.scales = []
		for x in range(2):
			scb = Scale(lb4, orient="vertical", from_=spaces[x][0], to=spaces[x][1], label=testi[x])
			scb.grid(row=0, column=x)
			scb.set(180 if x == 0 else 14)
			self.scales.append(scb)
		#============================

		okb = Button(self.tk, text="OK", command=self.ok)
		okb.pack()
	def mainloop(self):
		self.tk.mainloop()
	def ok(self):
		self.data[0], self.data[1], self.data[3], self.data[5] = self.key.get(), \
								self.ingmi.get(), self.devmode.get(), self.color
		cb1, cb2, cb3 = self.comboxes[0].get(), self.comboxes[1].get(), self.comboxes[2].get()
		s1, s2 = self.scales[0].get(), self.scales[1].get()
		templist = [cb1, cb2, cb3]
		for item in templist:
			if templist.count(item) > 1 or item == "":
				messagebox.showerror("Error", "You can\'t use the same binding in two things or use a null event")
				del templist
				return
		self.data[2] = cb1+";"+cb2+";"+cb3
		self.data[4] = str(s1)+";"+str(s2)
		#print("self.data:", self.data) #Non necessario
		self.save()
		#print("After self.save, self.getData():", self.getData())
		self.tk.destroy()
		#print("self.getData 2:", self.getData())
	def save(self):
		if os.path.exists(self.path+".FlappyBird/preferences_save.db"):
			os.remove(self.path+".FlappyBird/preferences_save.db")
		conn = sqlite3.connect(self.path+".FlappyBird/preferences_save.db")
		cursor = conn.cursor()
		sql = "CREATE TABLE data(type TEXT, attribute TEXT)"
		cursor.execute(sql)
		for x in range(len(self.data)):
			sql = "INSERT INTO data VALUES(?, ?)"
			cursor.execute(sql, (self.txts["types-type"][x], str(self.data[x])))
			conn.commit()
		conn.close()
	def getData(self):
		conn = sqlite3.connect(self.path+".FlappyBird/preferences_save.db")
		cursor = conn.cursor()
		sql = "SELECT * FROM data"
		try:
			cursor.execute(sql)
		except:
			return {}
		tempdic = {}
		for dt in cursor:
			tempdic[dt[0]] = dt[1]
		return tempdic

if False:
        '''print("Senza funzione")
        p = Preference()
        #print(p.getData())
        p.initialization()
        #print(p.getData()) 
        #p.data = ['<space>', '0', 'p;F3;s', 'False', '180;14']
        #p.getData() = {'Kick-Key':'<space>', 'GamingIntro-Init':'0', 'Bindings':'p;F3;s', 'DevMode':'False', 'Scales':'180;14', 'Color':'#00ff00'}
        p.mainloop()'''
#================================================
        def cicco():
                global a
                p = Preference()
                #print(p.getData())
                p.initialization()
                #print(p.getData()) 
                #p.data = ['<space>', '0', 'p;F3;s', 'False', '180;14']
                #p.getData() = {'Kick-Key':'<space>', 'GamingIntro-Init':'0', 'Bindings':'p;F3;s', 'DevMode':'False', 'Scales':'180;14', 'Color':'#00ff00'}
                p.mainloop()
                a = p.getData()
        print("Con funzione")
        cicco()
        print(a)
