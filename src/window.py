from tkinter import *


class App:
  def __init__(self, master):
    self.frame = Frame(master=master)

    self.frame.grid_rowconfigure(0, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)
