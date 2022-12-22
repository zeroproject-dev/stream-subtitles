from window import App
from tkinter import *
import sys


def close():
  sys.exit()


def create_window():
  root = Tk()
  root.geometry('300x300')
  root.resizable(False, False)
  root.title('Stream Subtitles')

  Grid.rowconfigure(root, 0, weight=1)
  Grid.columnconfigure(root, 0, weight=1)

  app = App(root)

  root.protocol("WM_DELETE_WINDOW", close)

  root.mainloop()


if __name__ == '__main__':
  create_window()
