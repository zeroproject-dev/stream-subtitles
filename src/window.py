from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
from server import init_web_server, close, update_settings, get_num_connections
from settings import settings, save_config, load_config
from threading import Thread
import json
import webbrowser


class App:
  def __init__(self, master):
    self.frame = Frame(master=master)

    self.frame.grid_rowconfigure(0, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)

    self.frame.config(padx=10, pady=10)

    self.frame_subtitles = LabelFrame(self.frame, text="Subtitles")
    self.frame_subtitles.grid(row=0, column=0, sticky='nsew')
    self.frame_network = LabelFrame(
        self.frame, text="Network (A restart is required to apply this changes)")
    self.frame_network.grid(row=1, column=0, sticky='nsew')

    self.web_server = Thread(target=init_web_server)
    self.web_server.daemon = True
    self.web_server.start()

    self.load_config()

    self.host_ip = None

    if settings['expose']:
      import socket
      self.host_ip = socket.gethostbyname(socket.gethostname())

    self.create_widgets()
    self.pack_widgets()

    self.frame.grid(row=0, column=0, sticky='nsew')

  def create_widgets(self):
    vcmd_font_size = (self.frame.register(self.validate_font_size),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    vcmd_port = (self.frame.register(self.validate_port),
                 '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    self.lbl_text_color = Label(self.frame_subtitles, text='Text Color: ')
    self.lbl_color = Label(self.frame_subtitles,
                           text="     ", bg=settings['color'])
    self.btn_text_color = Button(
        self.frame_subtitles, text='Choose Color', command=self.choose_color)

    self.lbl_background_opacity = Label(
        self.frame_subtitles, text='Background Opacity: ')
    self.scl_background_opacity = Scale(
        self.frame_subtitles, from_=0, to=100, orient=HORIZONTAL)
    self.scl_background_opacity.set(settings['background_opacity'] * 100)

    self.lbl_font_size = Label(self.frame_subtitles, text='Font Size: ')
    self.entry_font_size = Entry(
        self.frame_subtitles, validate='key', validatecommand=vcmd_font_size)
    self.entry_font_size.insert(0, settings['font_size'])

    self.selected_family = StringVar(value=settings['font_family'])
    self.lbl_font_family = Label(self.frame_subtitles, text='Font Family: ')
    self.cbox_font_family = ttk.Combobox(
        self.frame_subtitles, textvariable=self.selected_family)

    self.lbl_webpage = Label(
        self.frame_subtitles, text='My website: https://zeroproject.dev/', fg='blue', cursor='hand2')

    self.populate_font_families()

    self.lbl_port = Label(self.frame_network, text='Port: ')
    self.entry_port = Entry(
        self.frame_network, validate='key', validatecommand=vcmd_port)
    self.entry_port.insert(0, settings['port'])

    self.expose = IntVar(value=settings['expose'])
    self.cb_expose = Checkbutton(
        self.frame_network, text='Expose to network?', variable=self.expose)

    self.lbl_localhost = Label(
        self.frame, text=f'http://localhost:{settings["port"]}', fg='blue', cursor='hand2')

    self.lbl_network = Label(
        self.frame, text=f'http://{str(self.host_ip)}:{settings["port"]}', fg='blue', cursor='hand2')

    self.btn_save_settings = Button(
        self.frame, text='Save Settings', command=self.save_settings)

  def on_close(self):
    close()
    self.frame.destroy()

  def populate_font_families(self):
    self.cbox_font_family['values'] = list(font.families())

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
    self.cb_expose.pack()
    self.lbl_font_family.pack()
    self.cbox_font_family.pack()
    self.lbl_webpage.pack()
    self.lbl_webpage.bind(
        "<Button-1>", lambda e: webbrowser.open_new("https://zeroproject.dev/"))
    self.cbox_font_family['state'] = 'readonly'
    self.lbl_localhost.grid(row=2, column=0)
    self.lbl_localhost.bind(
        "<Button-1>", lambda e: webbrowser.open_new(f'http://localhost:{settings["port"]}'))
    if settings['expose']:
      self.lbl_network.grid(row=3, column=0)
      self.lbl_network.bind(
          "<Button-1>", lambda e: webbrowser.open_new(f'http://{str(self.host_ip)}:{settings["port"]}'))
    self.btn_save_settings.grid(row=4, column=0)

  def save_settings(self):
    settings['background_opacity'] = self.scl_background_opacity.get() / 100
    settings['font_size'] = self.entry_font_size.get()
    settings['port'] = self.entry_port.get()
    settings['expose'] = self.expose.get() == 1
    settings['font_family'] = self.selected_family.get()
    save_config()
    self.load_config()

    if get_num_connections() > 0:
      update_settings(settings=json.dumps(settings))

  def choose_color(self):
    color = colorchooser.askcolor()
    settings['color'] = color[1]
    self.lbl_color.config(bg=settings['color'])

  def load_config(self):
    load_config()

  def validate_font_size(self, action, index, value_if_allowed,
                         prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
      try:
        r = int(value_if_allowed)
        if text == " ":
          return False
        if r < 0 or r > 128:
          return False
        return True
      except ValueError:
        return False
    else:
      return False

  def validate_port(self, action, index, value_if_allowed,
                    prior_value, text, validation_type, trigger_type, widget_name):
    if value_if_allowed:
      try:
        r = int(value_if_allowed)
        if text == " ":
          return False
        if r < 0 or r > 65535:
          return False
        return True
      except ValueError:
        return False
    else:
      return False
