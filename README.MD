# Stream Subtitles

This project is developed with python for show subtitles in real time on a live stream, this program run a web server for show the subtitles in a web page.

## Installation

### Windows

If you just want to use the program, you can download the exe file and copy whatever you want in your computer.

> Note: the program will create a files named "settings.json" in the same folder where the exe file is.

### Build

For compile the project I recommend create a virtual environment with "virtualenv" or "venv", in this case I'll use "virtualenv". (Only tested in a Windows machine)

```bash
pip install virtualenv
git clone https://github.com/zeroproject-0/stream-subtitles.git
cd stream-subtitles
python -m virtualenv env
source env/Scripts/activate
pip install -r requirements.txt
```

With the virtual environment activated, you can run the program with the command:

```bash
python src/main.py
```

For build you can use auto-py-to-exe, or just pyinstaller, in this case I'll use pyinstaller.

> Important! You'll need to change one line in the file "env/Lib/site-packages/bottle.py", in the line 74 change the exception to "except Exception:".

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "env/Lib/site-packages/vosk;vosk/" --add-data "src/model;model/" --add-data "src/static;static/" --distpath "output" --clean src/main.py
```

This command will create a exe file in the folder "output", you can copy this file to your computer and run it.

## Usage

To use the program you just start it, and go to a web browser and type the link "http://localhost:9090" (or the port that you set in the program), you'll see a page with a black square in the middle, and when you talk the program will show the transcription in the square.

> Importan! The program use "rem" for the font size

For include the subtitles in OBS you can put the same link on a browser source and refresh the scene.

### OBS recommended settings

- Width: 1280
- Height: 300
- Remove the css of the browser source
- Activate "Refresh browser when scene becomes active"
