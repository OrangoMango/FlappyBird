from tkinter import *
from tkinter import messagebox
import FeedbackInterface
import time, os

class ErrorManager():
	def __init__(self, error="A None-Type Error"):
		self.err = error
		self.tk = Tk()
		self.tk.title("Oooops! An error occured - {time}".format(time=time.asctime()))
		self.feedbacktext = "When i was playing, i got this error:\n {error};\n" \
												" Can you fix it?\n Thanks".format(error=self.err)
	def showgui(self):
		l_title = Label(self.tk, text="Oooooops! An error occured", font=("Purisa", 20))
		l_title.pack()
		texts = [("See error", self.showerror), ("Send feedback", self.feedback), ("Quit", self.quit)]
		self.buttons = []
		for text, command in texts:
			b = Button(self.tk, text=text, command=command)
			b.pack()
			self.buttons.append(b)
	def showerror(self):
		messagebox.showerror("Error", self.err)
	def quit(self):
		try:
			self.tk.destroy()
		except:
			pass
	def mainloop(self):
		self.tk.mainloop()
	def feedback(self):
		f = FeedbackInterface.Feedback(pathinit=os.getcwd()+"/", users=os.listdir("C:/Users"), \
						initialfeedback=self.feedbacktext)
		f.start()

'''try:
	x = sewfgy
except Exception as e:
	error = ErrorManager(e)
	error.showgui()
	error.mainloop()'''
