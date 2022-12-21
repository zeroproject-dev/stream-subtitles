from vosk import Model, KaldiRecognizer

from queue import Queue
import sounddevice as sd
import os
import sys


class SpeechRecognition:
  def __init__(self):
    self.q = Queue()

    self.device_info = sd.query_devices(sd.default.device, "input")
    self.samplerate = int(self.device_info["default_samplerate"])

    self.model_path = os.path.join(os.path.dirname(__file__), "model")

    try:
      self.model = Model(model_path=self.model_path)
    except:
      self.model = None

  def callback(self, indata, _frames, _time, status):
    if status:
      print(status, file=sys.stderr)
    self.q.put(bytes(indata))

  def start(self, cb):
    self.q = Queue()

    is_on = True
    with sd.RawInputStream(
        samplerate=self.samplerate,
        blocksize=8000,
        device=sd.default.device,
        dtype="int16",
        channels=1,
        callback=self.callback
    ):
      rec = KaldiRecognizer(self.model, self.samplerate)
      while is_on:
        data = self.q.get()
        if rec.AcceptWaveform(data):
          print(rec.Result())
        else:
          text = rec.PartialResult()
          print(text)
          is_on = cb(text)
