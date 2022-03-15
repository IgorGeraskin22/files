# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
from collections import defaultdict
from pathlib import Path


class Journal:
    """Класс парсинга файла ТЗ и посчета значений 'NOK по минутам"""
    file_result = 'log_minutes.txt'  # файл с конечным результатом согласно ТЗ
    slice_value = 17  # диапазон среза строки до нужного параметра(минута,час,месяц и т.д)
    # символы оформления строки
    message = 'Statistics by minutes'  # сообщение о собраной статистики

    def __init__(self, original_file):
        self.original_file = original_file  # файл предоставленный в ТЗ
        self.stat = defaultdict(int)  # словарь статистики подсчета совпадающих значений.
        self.formatted_list = []  # список строк с полученным конечным результатом в формате ТЗ.
        self.strings_nok = []  # список строк включающие только "NOK"
        self.key_string = None  # вывод строки в нужный формат
        self.time_value = None  # значение времени
        self.character_format = '] - '

    def data_retrieval(self):
        """Метод открытия файла и получение  нужной нам строки('NOK') обрезанной до минут  и получение статистики """
        with open(self.original_file, mode='r', encoding='cp1251') as file:
            for line in file:
                if 'NOK' in line:
                    self.time_value = line[:self.slice_value]
                    self.stat[self.time_value] += 1

    def data_output(self):
        """Метод вывода подсчитанных строк в нужный формат согласно ТЗ"""
        for item in self.stat:
            self.key_string = str(item)  # взять ключ как строку
            self.key_string += self.character_format  # добавить символы в конец строки
            self.key_string += str(self.stat.get(item))  # добавить значение value по его ключу
            self.key_string += '\n'  # добавить символ новой строки
            self.formatted_list.append(self.key_string)  # добавить в список

    def write_to_file(self):
        """Метод открытия или создания текстового файла и запись в него полученной информации"""
        with open(self.file_result, mode='w', encoding='cp1251') as file:
            file.write(self.message)  # сообщение о собраной статистики
            file.write('\n')
            file.write('*' * len(self.message))  # разделитель
            file.write('\n')
            for self.string_record in self.formatted_list:
                file.write(str(self.string_record))

    def start(self):
        """Метод старта проекта"""
        self.stat.clear()  # очищаем словарь
        self.data_retrieval()
        # self.statistics()
        self.data_output()
        self.write_to_file()


class LogClock(Journal):
    """Класс статистики значений 'NOK по часам"""
    file_result = 'log_clock.txt'
    slice_value = 14
    character_format = ' hours ]'
    message = 'Hourly statistics'


class LodMonth(Journal):
    """Класс статистики значений 'NOK по месяцу"""
    file_result = 'log_month.txt'
    slice_value = 8
    character_format = ' month ] '
    message = 'Statistics by month'


class LodYear(Journal):
    """Класс статистики значений 'NOK по году"""
    file_result = 'log_god.txt'
    slice_value = 5
    character_format = ' God ] '
    message = 'Statistics by year'


my_path = str(Path("events.txt"))  # events.txt
journal = Journal(original_file=my_path)
journal.start()

log_clock = LogClock(original_file=my_path)
log_clock.start()

lod_month = LodMonth(original_file=my_path)
lod_month.start()

lod_year = LodYear(original_file=my_path)
lod_year.start()

# Зачёт!
