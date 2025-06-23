from os import path, getlogin, makedirs, listdir, remove
from zipfile import ZipFile
from subprocess import run
from shutil import move, rmtree
from tempfile import mkdtemp, TemporaryDirectory
import urllib.request
from config import Config
import json
from requests import get


class Installer:
    def __init__(
            self,
            install_path: str,
            download_url: str,
            filename: str,
            exe_name: str,
            create_shortcut: bool = True,
            start_on_finish: bool = True,
    ):
        self.path_to_game = None
        self.temp_path = None
        self.current_installing_path = install_path
        self.download_url = download_url
        self.filename = filename
        self.create_shortcut = create_shortcut
        self.start_on_finish = start_on_finish
        self.exe_name = exe_name

    @staticmethod
    def log(text):
        print(text)

    def _get_username(self):
        username = getlogin()
        self.log(f'Username: "{username}"')
        return username

    def _create_desktop_shortcut(self, executable):
        shortcut_path = path.join(path.expanduser("~"), "Desktop", f"{self.filename}.lnk")
        run([
            "powershell",
            "-Command",
            f"$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{shortcut_path}'); $Shortcut.TargetPath = '{executable}'; $Shortcut.Save()"
        ])
        self.log(f'Desktop shortcut created: "{shortcut_path}"')

    def _run_exe(self, executable):
        self.log(f'Starting: "{executable}"')
        run(f"{executable}", shell=True)

    def _set_integrity_level(self, executable):
        run(f'icacls {executable} /setintegritylevel high', shell=True)
        self.log(f'Set integrity level to high: "{executable}"')

    def _dl_progress(self, count, block_size, total_size):
        percent = count * block_size * 100 / total_size
        downloaded_gb = (count * block_size) / (1024 ** 3)
        total_gb = total_size / (1024 ** 3)
        self.log(f"Downloading: {percent:.2f}%\t\t\t{downloaded_gb:.2f}GB / {total_gb:.2f} GB")

    def _download_and_extract(self):
        try:
            zip_path = path.join(self.temp_path, f"{self.filename}.zip")
            urllib.request.urlretrieve(self.download_url, zip_path, reporthook=self._dl_progress)
            with ZipFile(zip_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                for file in files:
                    self.log(f'Extracting "{file}": {self.temp_path}')
                    zip_ref.extract(file, self.temp_path)
            remove(zip_path)
        except Exception as e:
            self.log(f"Error during download and extraction: {e}")

    def _move_files(self):
        try:
            for item in listdir(self.temp_path):
                source_path = path.join(self.temp_path, item)
                destination_path = path.join(self.current_installing_path, item)
                self.log(f'Moving "{source_path}": {destination_path}')
                move(source_path, destination_path)
        except Exception as e:
            self.log(f"Error during file movement: {e}")
    
    def get_game_version(self):
        try:
            version = get(Config.GAME_VERSION_CHECK_URL).text
            self.log(f'Last game version: {version}')
            return version
        except ConnectionError:
            messagebox.showerror("Connection error", "No connection to server.\nCheck your internet connection")
            sys.exit(1)
        
    def save_game_config(self):
        config_file = path.expanduser(f'~/.{Config.GAME_NAME}.config.json')
        with open(config_file, 'w') as file:
            json.dump({"path_to_game": self.current_installing_path, "game_version": self.get_game_version()}, file)
        self.log(f'Game config saved to "{config_file}"')

    def read_game_config(self):
        config_file = path.expanduser(f'~/.{Config.GAME_NAME}.config.json')
        self.log(f'Reading config from "{config_file}"')
        if path.exists(config_file):
            with open(config_file, 'r') as file:
                config = json.load(file)
            self.log(f'Config readed from "{config_file}": {config}')
            return config
        self.log(f'Config "{config_file}" not exist')
        return {"path_to_game": "", "game_version": ""}

    def delete_game_config(self):
        config_file = path.expanduser(f'~/.{Config.GAME_NAME}.config.json')
        self.log(f'Removing "{config_file}"')
        if path.exists(config_file):
            remove(config_file)

    def start(self):
        self.log(f'Starting install')
        makedirs(self.current_installing_path, exist_ok=True)
        #self.temp_path = mkdtemp(dir=f"{self.current_installing_path[0].upper()}:\\temp")
        with TemporaryDirectory(dir=f"{self.current_installing_path}", prefix="spotlightrptmp_") as temp_file:
            self.temp_path = temp_file
            self._download_and_extract()
            self._move_files()
            
        if self.create_shortcut:
            self._create_desktop_shortcut(path.join(f'"{self.current_installing_path}', f'{self.exe_name}"'))
        self.path_to_game = path.join(f'"{self.current_installing_path}', f'{self.exe_name}"')
        self._set_integrity_level(self.path_to_game)
        self.save_game_config()
        if self.start_on_finish:
            self._run_exe(self.path_to_game)


installer = Installer(
    install_path=path.join("C:\\", "Users", getlogin(), "games", Config.FOLDER_NAME),
    download_url=Config.GAME_DOWNLOAD_URL,
    filename=Config.GAME_NAME,
    exe_name=Config.EXE_NAME,
    create_shortcut=Config.CREATE_SHORTCUT
)
