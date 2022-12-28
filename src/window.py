from tkinter import *
from tkinter import colorchooser
from server import init_web_server, close, update_settings, get_num_connections
from settings import settings, save_config, load_config
from threading import Thread
import json


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
    vcmd = (self.frame.register(self.validate),
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
        self.frame_subtitles, validate='key', validatecommand=vcmd)
    self.entry_font_size.insert(0, settings['font_size'])

    self.lbl_port = Label(self.frame_network, text='Port: ')
    self.entry_port = Entry(
        self.frame_network, validate='key', validatecommand=vcmd)
    self.entry_port.insert(0, settings['port'])

    self.expose = IntVar(value=settings['expose'])
    self.cb_expose = Checkbutton(
        self.frame_network, text='Expose to network?', variable=self.expose)

    ip_text = f'http://localhost:{settings["port"]}'
    ip_text += f"\nor\nhttp://{str(self.host_ip)}:{settings['port']}" if settings["expose"] else ""

    self.txt_ip = Text(
        self.frame, height=3 if settings['expose'] else 1, borderwidth=0)
    self.txt_ip.insert(1.0, ip_text)
    self.txt_ip.configure(bg=self.frame.cget('bg'), state=DISABLED)

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
    self.cb_expose.pack()
    self.txt_ip.grid(row=2, column=0)
    self.btn_save_settings.grid(row=3, column=0)

  def save_settings(self):
    settings['background_opacity'] = self.scl_background_opacity.get() / 100
    settings['font_size'] = self.entry_font_size.get()
    settings['port'] = self.entry_port.get()
    settings['expose'] = self.expose.get() == 1
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
