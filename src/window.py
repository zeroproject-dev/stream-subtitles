from tkinter import *
from tkinter import colorchooser
from server import init_web_server, close, update_settings
from settings import settings, save_config, load_config
from threading import Thread
import json


class App:
  def __init__(self, master):
    self.frame = Frame(master=master)

    self.frame.grid_rowconfigure(0, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)

    self.web_server = Thread(target=init_web_server)
    self.web_server.daemon = True
    self.web_server.start()

    self.load_config()
    self.create_widgets()
    self.pack_widgets()

    self.frame.grid(row=0, column=0, sticky='nsew')

  def create_widgets(self):
    vcmd = (self.frame.register(self.validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    self.lbl_text_color = Label(self.frame, text='Text Color: ')
    self.lbl_color = Label(self.frame, text="     ", bg=self.color)
    self.btn_text_color = Button(
        self.frame, text='Choose Color', command=self.choose_color)

    self.lbl_background_opacity = Label(
        self.frame, text='Background Opacity: ')
    self.scl_background_opacity = Scale(
        self.frame, from_=0, to=100, orient=HORIZONTAL)
    self.scl_background_opacity.set(self.background_opacity * 100)
    self.lbl_font_size = Label(self.frame, text='Font Size: ')
    self.entry_font_size = Entry(
        self.frame, validate='key', validatecommand=vcmd)
    self.entry_font_size.insert(0, self.font_size)
    self.lbl_port = Label(self.frame, text='Port (need restart): ')
    self.entry_port = Entry(self.frame, validate='key', validatecommand=vcmd)
    self.entry_port.insert(0, self.port)

    self.lbl_ip = Label(
        self.frame, text=f'http://localhost:{settings["port"]}')

    self.btn_save_settings = Button(
        self.frame, text='Save Settings', command=self.save_settings)

  def on_close(self):
    close()
    self.frame.destroy()

  def pack_widgets(self):
    self.lbl_text_color.pack()
    self.lbl_color.pack()
    self.btn_text_color.pack()
    self.lbl_background_opacity.pack()
    self.scl_background_opacity.pack()
    self.lbl_font_size.pack()
    self.entry_font_size.pack()
    self.lbl_port.pack()
    self.entry_port.pack()
    self.lbl_ip.pack()
    self.btn_save_settings.pack()

  def save_settings(self):
    settings['color'] = self.color
    settings['background_opacity'] = self.scl_background_opacity.get() / 100
    settings['font_size'] = self.entry_font_size.get()
    settings['port'] = self.entry_port.get()
    save_config()
    self.load_config()
    update_settings(settings=json.dumps(settings))

  def choose_color(self):
    color = colorchooser.askcolor()
    self.color = color[1]
    self.lbl_color.config(bg=self.color)

  def load_config(self):
    load_config()
    self.color = settings['color']
    self.background_opacity = settings['background_opacity']
    self.font_size = settings['font_size']
    self.port = settings['port']

  def validate(self, action, index, value_if_allowed,
               prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
      try:
        int(value_if_allowed)
        return True and text != " "
      except ValueError:
        return False
    else:
      return False
