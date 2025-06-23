from requests import get
from requests.exceptions import ConnectionError
from config import Config
from installer import installer
import sys
from tkinter import messagebox
import webbrowser
from _version import __version__

log = installer.log


def get_game_version():
    try:
        version = get(Config.GAME_VERSION_CHECK_URL).text
        log(f'Last game version: {version}')
        return version
    except ConnectionError:
        messagebox.showerror("Connection error", "No connection to server.\nCheck your internet connection")
        sys.exit(1)


def get_launcher_version():
    try:
        version = get(Config.LAUNCHER_VERSION_CHECK_URL).text
        log(f'Last launcher version: {version}')
        return version
    except ConnectionError:
        messagebox.showerror("Connection error", "No connection to server.\nCheck your internet connection")
        sys.exit(1)

def check_game_updates():
    from installer import installer
    version = get_game_version()
    log(f'Current game version: {version}')
    if installer.read_game_config() and installer.read_game_config()['game_version'] != version:
        log(f'Game update available')
        return True
    return False


def check_launcher_updates():
    version = get_launcher_version()
    log(f'Current launcher version: {__version__}')
    if __version__ != version:
        log(f'Launcher update available')
        return True
    return False


def update_launcher():
    messagebox.showinfo("Обновление лаунчера", "Доступна новая версия лаунчера")
    webbrowser.open(Config.LAUNCHER_DOWNLOAD_URL)
    sys.exit(1)
    # log(f"ДОСТУПНО ОБНОВЛЕНИЕ ДЛЯ ЛАУНЧЕРА!")
    # exe_path = sys.executable
    # temp_path = mkdtemp(dir=f"{exe_path[0].upper()}:\\temp")
    # updater_path = os.path.join(temp_path, Config.UPDATER_NAME)
    #
    # urllib.request.urlretrieve(Config.LAUNCHER_DOWNLOAD_URL, updater_path)
    # log(f"Starting updating script")
    # subprocess.Popen(f'{updater_path} {Config.LAUNCHER_DOWNLOAD_URL} -p {exe_path}', shell=True)
    # sys.exit(1)


def update_game():
    log("Starting a game update")
    from gui import app
    app.start_install()
