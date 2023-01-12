import pathlib
import sys
import json

settings = {
    'color': '#ffffff',
    'background_opacity': 0.3,
    'font_size': "42",
    'port': 9090,
    'expose': False
}


def get_datadir() -> pathlib.Path:
  home = pathlib.Path.home()

  if sys.platform == "win32":
    return home / "AppData/Roaming"
  elif sys.platform == "linux":
    return home / ".local/share"
  elif sys.platform == "darwin":
    return home / "Library/Application Support"


config_path = get_datadir() / "zeroproject/stream-subtitles"

print("Config path: " + str(config_path))

try:
  if not config_path.exists():
    config_path.mkdir(parents=True)
except FileExistsError:
  pass


def load_config():
  try:
    with open(config_path / 'config.json', 'r') as f:
      config = json.load(f)
      settings['color'] = config['color']
      settings['background_opacity'] = config['background_opacity']
      settings['font_size'] = config['font_size']
      settings['port'] = config['port']
      settings['expose'] = config['expose']
  except Exception:
    save_config()


def save_config():
  with open(config_path / 'config.json', 'w') as f:
    json.dump(settings, f)
