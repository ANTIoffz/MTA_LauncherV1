from abc import ABC
from typing import Final

# Это первая версия лаунчера Spotlight RP
# Это конфиг файл лаунчера, тут нужно всё настроить, да
# Я не стал убирать старые конфиги с прокта Spotlight RP для примера, на них можно ориентироваться
# Сама структура лаунчера довольно своеобразная, так что есть схема


class Config(ABC):
    APP_TITLE: Final = "SpotlightRP" # Имя приложения
    APP_WIDTH: Final = 450 # Ширина окна
    APP_HEIGHT: Final = 500 # Высота окна
    APP_THEME = "dark" # Тема
    APP_COLOR_THEME = "blue" # Цвет темы

    MAX_PATH_LENGTH = 25 # Длина пути, после которой продолжеие будет отображаться как три точки
    
    FOLDER_NAME = 'SpotlightRP' # Имя папки для установки
    GAME_NAME = 'SpotlightRP' # Имя проекта (желательно как FOLDER_NAME)
    EXE_NAME = 'Spotlight RP/Multi Theft Auto.exe' # EXE файл игры
    UPDATER_NAME = 'SpotlightRPLauncherUpdate.exe' # Имя файла обновления

    CREATE_SHORTCUT = False # Создавать ли ярлык на рабочем столе

    LAUNCHER_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRP.exe' # Ссылка на загрузку лаунчера
    GAME_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRP.zip' # Ссылка на загрузку игры
    UPDATE_SCRIPT_DOWNLOAD_URL = 'http://download.spotlightrp.ru/download/SpotlightRPLauncherUpdate.exe' # Ссылка на загрузку скрипта обновления
    LAUNCHER_VERSION_CHECK_URL = 'http://download.spotlightrp.ru/version/launcher' # Ссылка на файл с текущей версией лаунчера
    GAME_VERSION_CHECK_URL = 'http://download.spotlightrp.ru/version/game' # Ссылка на файл с текущей версией игры
    BACKGROUND_URL = 'https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDI0LTAzL3Jhd3BpeGVsX29mZmljZV81MV9waG90b19vZl9ibGFja19kYXJrX3NreV9iYWNrZ3JvdW5kX21pbmltYWxpc19iYjA3Njk5OS1hMWNhLTRhZTUtOTgxMy1hYWI4ZTQ1NWU0MGNfMS5qcGc.jpg' # Ссылка на задний фон
    ICON_IMAGE = '' # Иконка
