# -*- coding: utf-8 -*-
import operator
import zipfile
from pathlib import Path

from prettytable import PrettyTable


# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

class Statistics:
    stat = {}
    statistics_table = PrettyTable()
    reverse = False
    key = None

    def __init__(self, file_name):
        self.res_items = None
        self.delete_symbol = None
        self.total = None
        self.quantity = 0
        self.file_name = file_name
        self.statistics_table.field_names = ["Буквы", "Частота"]
        self.cell_line = [f'+{"-" * 10}+', f'+{"-" * 10}+']
        self.res = []

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():  # получаем информацию о файлах и директориях
            zfile.extract(filename)  # извлекаем отдельный файл из корня архива
            self.file_name = filename

    def collect(self):
        if self.file_name.endswith('.zip'):  # если заканчивается на .zip. Проверяем является ли файл архивом
            self.unzip()  # если это zip архив то запускаем функцию  unzip()
        with open(self.file_name, mode='r', encoding='cp1251') as file:
            for self.line in file:
                self.delete_symbol = (''.join(filter(str.isalpha, self.line)))
                self.res += self.delete_symbol

    def statistic(self):

        for self.ch in self.res:
            if self.ch in self.stat:

                self.stat[self.ch] += 1

            else:
                self.stat[self.ch] = 1

    def sum_values(self):
        self.quantity = sum(self.stat.values())  # сумма количества букв

    def add_table(self):

        self.statistics_table.add_row(self.cell_line)
        self.total = ['Итого', self.quantity]
        self.statistics_table.add_row(self.total)  # добавили в таблицу self.total

    def sorted(self):
        """Метод сортировки  убывания по  алфавиту"""
        for self.res_items in sorted(self.stat.items(), reverse=self.reverse, key=self.key):
            self.statistics_table.add_row(self.res_items)

    def start_script(self):
        self.collect()
        self.statistic()
        self.sum_values()
        self.sorted()
        self.add_table()
        print(self.statistics_table)


class AlphabetAscending(Statistics):
    """Класс сортировки по возрастанию алфавита"""
    reverse = True
    key = None


class FrequencyDecay(Statistics):
    """Класс сортировки  убывания значений по частоте"""
    reverse = True
    key = operator.itemgetter(1)


class IncreaseFrequency(Statistics):
    """Класс сортировки  возрастание значений по частоте"""
    reverse = False
    key = operator.itemgetter(-1)


my_path = str(Path("python_snippets", "voyna-i-mir.txt.zip"))
statistics = Statistics(my_path)
statistics.start_script()  # сортировка по убыванию алфавита

alphabet_ascending = AlphabetAscending(my_path)
alphabet_ascending.start_script()  # сортировка по возрастанию алфавита

frequency_decay = FrequencyDecay(my_path)
frequency_decay.start_script()  # сортировки  убывание по частоте

increase_frequency = IncreaseFrequency(my_path)
increase_frequency.start_script()  # сортировки  возрастание по частоте

# Зачёт!
