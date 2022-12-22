import json

settings = {
    'color': '#ffffff',
    'background_opacity': 0.3,
    'font_size': 3,
    'port': 9090,
}


def load_config():
  try:
    with open('config.json', 'r') as f:
      config = json.load(f)
      settings['color'] = config['color']
      settings['background_opacity'] = config['background_opacity']
      settings['font_size'] = config['font_size']
      settings['port'] = config['port']
  except FileNotFoundError:
    save_config()


def save_config():
  with open('config.json', 'w') as f:
    json.dump(settings, f)
