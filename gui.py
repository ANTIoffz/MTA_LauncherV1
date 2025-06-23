from customtkinter import CTk, CTkButton, CTkLabel, set_appearance_mode, set_default_color_theme
from tkinter import Frame, Label, Text, filedialog
from config import Config
from os import path, startfile
from random import choice, randint
from PIL import Image, ImageTk
from requests import head
from psutil import disk_usage
from shutil import rmtree
from subprocess import Popen
from time import sleep
from installer import installer
from update import check_game_updates, update_game
from urllib.request import urlopen
from io import BytesIO
from ctypes import windll
import webbrowser


class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode(Config.APP_THEME)
        set_default_color_theme(Config.APP_COLOR_THEME)
        self.has_game_updates = check_game_updates()

        installer.log = self.log
        self.create_widgets()
        self.installed_game_path = installer.read_game_config()['path_to_game']
        if self.installed_game_path:
            self.log(f'Installed game path: "{self.installed_game_path}"')
            self._change_install_path(self.installed_game_path)
        self.check_state()

    def create_widgets(self):
        self.create_control_frame()
        self.create_log_frame()
        try:
            self.create_background()
        except Exception as exc:
            self.log(f"Error getting background: {exc}")
        self.create_buttons()
        self.create_path_label()
        self.create_warnings()

    def create_control_frame(self):
        self.control_frame = Frame(self, height=100, bg="#040014")
        self.control_frame.pack(fill='x', side="bottom")

    def create_log_frame(self):
        self.log_frame = Frame(self, height=10, bg="gray")
        self.log_frame.pack(fill='x', side="bottom")

        self.log_text_block = Text(
            self.log_frame,
            width=0,
            height=1,
            wrap='none',
            state='disabled'
        )
        self.log_text_block.pack(fill='x', side="bottom")

    def create_background(self):
        with urlopen(Config.BACKGROUND_URL) as background:
            raw_data = background.read()
        im = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)
        self.background = Label(self, image=photo)
        self.background.image = photo
        self.background.pack(side="top", fill="both")
        self.background.lower()

    def create_buttons(self):
        self.install_btn = CTkButton(
            self.control_frame,
            text="",
            font=('Helvetica', 18),
            width=200, height=60,
            command=self.start_install
        )
        self.install_btn.pack(side='right', anchor='se', pady=10, padx=10)

        self.change_install_path_btn = CTkButton(
            self.control_frame,
            text="Изменить",
            width=30, height=20,
            command=self.change_install_path
        )
        self.change_install_path_btn.pack(side='left', anchor='sw', pady=10, padx=10)

        self.delete_btn = CTkButton(
            self.control_frame,
            text="Удалить",
            width=30, height=20,
            command=self.start_delete
        )
        self.delete_btn.pack(side='left', anchor='sw', pady=10, padx=5)

        self.rickroll_btn = CTkButton(
            self,
            text='',
            fg_color='transparent',
            width=10,
            height=10,
            command=self.rickroll
        )
        self.rickroll_btn.place(x=0, y=0)

    def create_path_label(self):
        current_installing_path = installer.current_installing_path
        self.log(f'Install path: "{current_installing_path}"')
        self.path_to_install_lbl = CTkLabel(
            self.control_frame,
            text=f"Путь установки:\n{current_installing_path if len(current_installing_path) <= Config.MAX_PATH_LENGTH else current_installing_path[:Config.MAX_PATH_LENGTH] + '...'}",
            font=('Helvetica', 14),
            padx=10,
            pady=10,
            justify='left'
        )
        self.path_to_install_lbl.place(x=0, y=0)
        self.path_to_install_lbl.lower()

    def create_warnings(self):
        if not windll.shell32.IsUserAnAdmin():
            self.start_on_admin_lbl = CTkLabel(
                self,
                text=f"ЗАПУСТИТЕ УСТАНОВЩИК ОТ ИМЕНИ АДМИНИСТРАТОРА",
                font=('Helvetica', 14),
                padx=10,
                pady=10,
                bg_color='red'
            )
            self.start_on_admin_lbl.place(
                x=0,
                y=0
            )

    def _change_install_path(self, new_path):
        installer.current_installing_path = new_path
        self.log(f'Install path: "{installer.current_installing_path}"')
        self.path_to_install_lbl.configure(text=f"Путь установки:\n{new_path if len(new_path) <= Config.MAX_PATH_LENGTH else new_path[:Config.MAX_PATH_LENGTH] + '...'}")

    def change_install_path(self, add_folder=True):
        new_path = filedialog.askdirectory()
        if new_path:
            if (not new_path.endswith(Config.FOLDER_NAME)) and add_folder:
                new_path += f'{"/" if not new_path.endswith("/") else ""}{Config.FOLDER_NAME}'
            self._change_install_path(new_path)
        self.check_state()

    def _start_install(self):
        if path.exists(installer.current_installing_path):
            self._start_delete()
        installer.start()
        self.check_state()

    def start_install(self):
        self.install_btn.configure(
            text=choice(
                [
                    'Колдую', 'Пицца', 'rm -rf /*', 'Fire in the hole',
                    'Never gonna give you up', 'Автор - ANTI', '🍕',
                    'Это полная пицца', 'Пудж 😍', 'Что это сверху слева?',
                    'Тут нет пасхалок', 'Это 11 элемент в массиве'
                ]
            ) if randint(1, 6) == 1 else 'Работаю'
        )
        self.install_btn.configure(state="disabled")
        self.change_install_path_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.after(1000, self._start_install)

    def _start_game(self):
        self.install_btn.configure(state="disabled")
        self.update()
        game_path = self.get_game_path()
        self.log(f'Launching "{game_path}"')
        startfile(game_path)
        # Popen(f'"{self.get_game_path()}"', start_new_session=True)
        sleep(1)
        self.install_btn.configure(state="normal")

    def start_game(self):
        self._start_game()

    def _start_delete(self):
        installer.delete_game_config()
        self.log(f'Removing "{installer.current_installing_path}"')
        self.log(f"Wait!")
        rmtree(installer.current_installing_path)
        self.log(f"Done")
        
    def start_delete(self):
        self.log("Start deleting")
        self._start_delete()
        self.check_state()

    def check_state(self):
        not_enough_space = self.check_enough_space()
        self.installed_game_path = installer.read_game_config()['path_to_game']
        self.log(f'{not_enough_space=}')
        self.log(f'{self.has_game_updates=}')
        self.log(f'{self.installed_game_path=}')
        self.log(f'Install path: "{installer.current_installing_path}"')
        
        self.delete_btn.configure(state="disabled")
        self.change_install_path_btn.configure(state="disabled")

        if self.installed_game_path:
            if self.has_game_updates:
                self.log(f'Update available')
                if not_enough_space > 0:
                    self.log(f'Not enough {not_enough_space}')
                    self.install_btn.configure(
                        state="disabled",
                        text=f'Недостаточно {"маны" if randint(1, 6) == 1 else "места для обновления"}\nНужно ещё {not_enough_space:.0f} мб'
                    )
                    return

                self.install_btn.configure(
                    state="normal",
                    text=f'Обновить',
                    command=update_game
                )
                self.delete_btn.configure(state="normal")
                return

            if path.exists(self.get_game_path()):
                self.install_btn.configure(
                    state="normal",
                    text=f'Запустить',
                    command=self.start_game
                )
                self.delete_btn.configure(state="normal")
                return

        if not_enough_space > 0:
            self.log(f'Not enough {not_enough_space}')
            self.install_btn.configure(
                state="disabled",
                text=f'Недостаточно {"маны" if randint(1, 6) == 1 else "места"}\nНужно ещё {not_enough_space:.0f} мб'
            )
            self.change_install_path_btn.configure(state="normal")
            return

        self.install_btn.configure(
            state="normal",
            text=f'Скачать',
            command=self.start_install
        )
        self.change_install_path_btn.configure(state="normal")

    def get_available_disk_space(self):
        drive_letter = installer.current_installing_path[0]
        drive_path = f"{drive_letter.upper()}:\\"
        disk_info = disk_usage(drive_path)
        available_space = disk_info.free
        self.log(f'Available space in "{drive_path}": {available_space}')
        return available_space

    def check_enough_space(self):
        file_size = self.get_file_size(Config.GAME_DOWNLOAD_URL)
        disk_free = self.get_available_disk_space()
        not_enough = (file_size - disk_free) / (1024 ** 2)
        return not_enough

    def get_game_path(self):
        game_path = path.join(self.installed_game_path, Config.EXE_NAME)
        self.log(f'Game path: {game_path}')
        return game_path

    def get_file_size(self, url):
        response = head(url, allow_redirects=True)
        if response.status_code == 200:
            file_size = int(response.headers.get('Content-Length', 0))
            self.log(f'File size of "{url}" = {file_size}')
            return file_size

    def rickroll(self):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def log(self, text):
        print(text)
        self.log_text_block.config(state='normal')
        self.log_text_block.insert('1.0', f"{text}\n")
        self.log_text_block.config(state='disabled')
        self.update()


app = App()
