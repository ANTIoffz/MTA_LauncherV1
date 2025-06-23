from abc import ABC
from typing import Final

class Config(ABC):
    APP_TITLE: Final = "SpotlightRP"
    APP_WIDTH: Final = 450
    APP_HEIGHT: Final = 500
    APP_THEME = "dark"
    APP_COLOR_THEME = "blue"

    MAX_PATH_LENGTH = 25
    
    FOLDER_NAME = 'SpotlightRP'
    GAME_NAME = 'SpotlightRP'
    EXE_NAME = 'Spotlight RP/Multi Theft Auto.exe'
    UPDATER_NAME = 'SpotlightRPLauncherUpdate.exe'

    CREATE_SHORTCUT = False

    LAUNCHER_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRP.exe'
    GAME_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRP.zip'
    UPDATE_SCRIPT_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRPLauncherUpdate.exe'
    LAUNCHER_VERSION_CHECK_URL = 'http://download.spotlightrp.ru/version/launcher'
    GAME_VERSION_CHECK_URL = 'http://download.spotlightrp.ru/version/game'
    BACKGROUND_URL = 'http://download.spotlightrp.ru/download/background.png'
    ICON_IMAGE = ''
