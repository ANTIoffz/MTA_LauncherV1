from customtkinter import CTk, CTkButton, CTkLabel, set_appearance_mode, set_default_color_theme
from config import Config
from os import path, getlogin
from gui import app
from update import check_launcher_updates, update_launcher

def main():
    if check_launcher_updates():
        update_launcher()

    set_appearance_mode(Config.APP_THEME)
    set_default_color_theme(Config.APP_COLOR_THEME)
    app.resizable(width=False, height=False)
    app.title(Config.APP_TITLE)
    if Config.ICON_IMAGE:
        app.iconbitmap(Config.ICON_IMAGE)
    app.geometry(f"{Config.APP_WIDTH}x{Config.APP_HEIGHT}")
    app.mainloop()


if __name__ == "__main__":
    main()
