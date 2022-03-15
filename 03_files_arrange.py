# -*- coding: utf-8 -*-

import sys
import time
import os
import shutil
from pathlib import Path
import pyglet


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# (время создания файла берется по разному в разых ОС - см https://clck.ru/PBCAX - поэтому берем время модификации).
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит, см .gitignore в папке ДЗ)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4


class Sort:
    path = ''
    new_path = ''
    month = {'1': 'январь', '2': 'февраль', '3': 'март', '4': 'апрель', '5': 'май', '6': 'июнь', '7': 'июль',
             '8': 'август', '9': 'сентябрь', '10': 'октябрь', '11': 'ноябрь', '12': 'декабрь'}

    def __init__(self):
        self.new_file_path = None
        self.year = None  # вычленяем год модификации файла
        self.secs = None
        self.file_time = None  # вернет тьюпл со временем
        self.full_file_path = None
        self.mon = None

    def walk_to_file(self):
        if os.path.exists(self.path):
            for dir_path, dir_names, filenames in os.walk(self.path):
                for file in filenames:
                    self.full_file_path = os.path.join(dir_path, file)  # Здесь путь до файла
                    self.secs = os.path.getmtime(self.full_file_path)
                    self.file_time = time.gmtime(self.secs)  # вернет тьюпл со временем
                    self.year = f'{self.file_time[0]}'  # вычленяем год модификации файла
                    self.mon = f'{self.file_time[1]}'  # вычленяем месяц модификации файла
                    # self.month = [self.mon]

                    self.new_file_path = os.path.join(
                        self.new_path, self.year, self.month[self.mon]
                    )  # формируем путь создания будущей директории из year,
                    # month
                    if self.new_file_path not in self.new_path:  # если такой папки нет, то создается
                        os.makedirs(self.new_file_path,
                                    exist_ok=True)  # exist_ok=True проверка на существования папки с таким именем
                        shutil.copy2(self.full_file_path, self.new_file_path)
            sound_end = str(Path('1.mp3'))
            song = pyglet.media.load(sound_end)
            song.play()
            pyglet.app.run()
            print('Готово')

        else:
            print('Вы ввели неправильный путь или такой директории не существует')
            print('Запустите программу заново')

    def new_directory(self):
        if not os.path.exists(self.new_path):
            os.mkdir(self.new_path)  # создал директорию Foto
        else:
            print('Директория с таким именем уже существует')
            sys.exit()

    def start(self):
        self.walk_to_file()
        self.new_directory()


class Input(Sort):
    path = str(Path(input('Введите путь до базовой директории с фото:\n')))
    new_path = str(Path(input('Введите путь до конечной директории:\n')))


inp = Input()
inp.start()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html

# Зачёт!
