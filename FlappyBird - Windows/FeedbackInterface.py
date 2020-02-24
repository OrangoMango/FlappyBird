from tkinter import *
import os, time, sqlite3, webbrowser
from tkinter import scrolledtext, messagebox

class Feedback:
	def __init__(self, interface="Linux", pathinit="", users=[None], initialfeedback="feedback;stars"):
		self.initfeed = initialfeedback
		self.assvar = StringVar()
		self.assvar.set(self.initfeed)
		self.path = pathinit
		self.interface = interface
		if self.interface == "Windows":
			self.slash = "\ "[0]
		elif self.interface == "Linux":
			self.slash = "/"
		else:
			self.interface = "Linux"
			self.slash = "/"
		self.middle = -1
		#for x in users:
		conn = sqlite3.connect(self.path+".FlappyBird"+self.slash+"Feedbacks.db")
		cursor = conn.cursor()
		sql = "SELECT stars FROM feedbacks"
		try:
			cursor.execute(sql)
			self.sm = [item[0] for item in cursor]
			self.middle = sum(self.sm) / len(self.sm)
		except:
			pass
	def start(self):
		self.tk = Tk()
		self.tk.title("OrangoMango Feedback [{0:.2f}stars]".format(self.middle))
		self.titlelabel = Label(self.tk, text="Send Feedback")
		self.titlelabel.grid()
		self.t_EnterName = Label(self.tk, text="Enter name: ")
		self.t_EnterName.grid(row=1)
		self.t_EnterFeedback = Label(self.tk, text="Enter \'Feedback;stars\': ")
		self.t_EnterFeedback.grid(row=2)
		self.e_EnterName = Entry(self.tk)
		self.e_EnterName.grid(row=1, column=1)
		self.e_EnterFeedback = scrolledtext.ScrolledText(self.tk, width=40, height=7)
		self.e_EnterFeedback.grid(row=2, column=1)
		self.e_EnterFeedback.insert("end", self.assvar.get())
		self.b_Cancel = Button(self.tk, text="Cancel", command=self.cancel)
		self.b_Cancel.grid(row=3, column=2, sticky="w")
		self.b_Submit = Button(self.tk, text="Submit", command=self.submit)
		self.b_Submit.grid(row=3, column=2, sticky="e")
		self.tk.mainloop()
	def cancel(self):
		self.tk.destroy()
	def submit(self):
		a = messagebox.askyesno("GitHub", "Do you want to post the feedback online? (YES-github.com; NO-locally)")
		if a:
			webbrowser.open("http://www.github.com/OrangoMango/FlappyBird/issues/new")
			self.tk.destroy()
			return
		self.name = self.e_EnterName.get()
		#print(self.e_EnterFeedback.get("1.0", "end-1c").split(";"))
		try:
			self.feedback, self.stars = self.e_EnterFeedback.get("1.0", "end-1c").split(";") #Try tuple()			
			self.stars = float(self.stars)
			if self.stars < 1 and stars > 5:
				raise
		except:
			messagebox.showerror("Error", "Invalid star input, please write: \'Feedback;stars_number\'.")
			return
		now = time.asctime()
		con = sqlite3.connect(self.path+".FlappyBird"+self.slash+"Feedbacks.db")
		cursor = con.cursor()
		sql = "CREATE TABLE IF NOT EXISTS feedbacks(name TEXT, date TEXT, feedback TEXT, stars INTEGER)"
		cursor.execute(sql)
		sql = "INSERT INTO feedbacks VALUES(?, ?, ?, ?)"
		cursor.execute(sql, (self.name, now, self.feedback, self.stars))
		con.commit()	
	
		sql = "SELECT * FROM feedbacks WHERE name = ?"
		cursor.execute(sql, (self.name,))
		data = [item for item in cursor]
		con.close()
		messagebox.showinfo("ClientInfo", "Feedback from {user} in {date} [{feedback}] {stars}:".format(user=data[-1][0], \
																													date=data[-1][1], feedback=data[-1][2], stars=data[-1][3]))
		self.tk.destroy()

	def see_feedbacks(self):
		messagebox.showinfo("AdminInfo", "Feedbacks Access Is only for admin")
