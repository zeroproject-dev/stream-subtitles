import eel
import os
import json
from speech_recognition import SpeechRecognition
from settings import settings

speech_thread = None
is_up = True

speech = SpeechRecognition()


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


def init_web_server():
  static_path = os.path.join(os.path.dirname(__file__), "static")
  eel.init(path=static_path)

  eel.start("index.html", mode=None, port=int(settings['port']),
            close_callback=lambda a, b: print("Closing"))


def close():
  global is_up
  is_up = False
