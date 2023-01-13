import eel
import os
import json
import socket
from speech_recognition import SpeechRecognition
from settings import settings, save_config

speech_thread = None
is_up = True

speech = SpeechRecognition()


def get_num_connections():
  return len(eel._websockets)


@eel.expose
def start_voice_recognition():
  global speech_thread
  if speech_thread is not None:
    print("Killing voice recognition")
    speech_thread.kill()

  speech_thread = eel.spawn(speech.start, send_text)


def send_text(text):
  global is_up
  eel.putText(text)()
  return is_up


@eel.expose
def get_settings():
  return json.dumps(settings)


def update_settings(settings):
  eel.updateSettings(settings)()


def verify_port():
  port = int(settings['port'])
  if port > 1024 and port < 65535:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while sock.connect_ex(("localhost", port)) == 0:

      port += 1
      if port > 65534:
        port = 1024

    sock.close()

    settings['port'] = port
    save_config()


def init_web_server():
  static_path = os.path.join(os.path.dirname(__file__), "static")
  eel.init(path=static_path)

  verify_port()

  host = "0.0.0.0" if settings["expose"] else "localhost"

  eel.start("index.html", mode=None, host=host, port=int(settings['port']),
            close_callback=lambda a, b: print("Closing"))


def close():
  global is_up
  is_up = False
