# Общие замечания:
# 1) Используй аннотации типов для того, чтобы повысить информативность своего кода.
#    (https://habr.com/ru/company/lamoda/blog/432656/)
# 2) Используй Docstrings для комментирования объяснения логики своих классов и функций.
#    (https://dvmn.org/encyclopedia/qna/13/chto-takoe-docstring-s-chem-ego-edjat/)
# 3) Используй библиотеку pep8 для поиска нарушений PEP8 (https://pypi.org/project/pep8/)
# 4) Вместо datetime.now().date() Лучше использовать date.today(). Поправь во всем файле.
# 5) Бэкслеши для переносов является не очень хорошой практикой, Лучше прописывать
#    строку в тройные кавычки ('''). Поправь во всем файле.
#    (https://www.geeksforgeeks.org/triple-quotes-in-python) - взгляни на Example #2.

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Здесь вместо цикла можно использовать списковое включение (list comprehension). Такие выражения легко читать.
        # Далее можно вычислить сумму элементов списка при помощи встроенной функции sum.
        # (https://webdevblog.ru/kogda-ispolzovat-list-comprehension-v-python/)
        # имя Record уже зарезервировано другим классом + не очень
        # хорошо, что элемент итерирумого объекта будет называться с большой буквы.
        for Record in self.records:
            #  Вычислять текущую дату при каждой итерации цикла довольно затратно
            #  лучше объявить переменную с текущей датой вне цикла и использовать ее.
            if Record.date == dt.datetime.now().date():
                # Тут можно заменить оператором присваивания +=.
                # (https://letpy.com/handbook/Assignment-Operators/)
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # Этот цикл тоже можно заменить на list comprehension.
        for record in self.records:
            #  Подумай над тем как упростить это условие.
            #  (Подсказка: в Python можно использовать выражения вида a < b < c).
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    #  Для комментирования целой функции лучше использовать Docstrings
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        #  Называть переменные одной буквой не очень хорошо, переименуй в соотвествии с ее смыслом.
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        #  Это условие else является лишним, можно обойтись без него.
        else:
            # Круглые скобки окружающие условие избыточны. Необходимо убрать.
            # + пропустил пробел полсе return.
            return('Хватит есть!')


class CashCalculator(Calculator):
    #  При работе с деньгами лучше использовать тип decimal
    #  (https://asvetlov.blogspot.com/2012/08/numerics.html)
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    #  Лишнаяя передача переменных класса в его метод, ты можешь обратиться к ним через self.
    #  + по условиям тз, этот метод должен принимать только один параметр - currency.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        #  При проверке на 'usd' ты сравниваешь currency, во всех остальных случаях currency_type.
        #  + проверка этого значения повторяется слишком часто, подумай, как от этого можно избавиться.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            #  Эта строка не имеет никакого эффекта, ты просто сравнил значение с 1.00.
            cash_remained == 1.00
            currency_type = 'руб'
        #  Не определено поведение, при котором метод получает валюту, работать с которой
        #  он не умеет.
        if cash_remained > 0:
            return (
                #  В f-строках не принято вызывать функции, стоит вынести операцию
                #  округления в отдельную переменную и вызвтаь ее f-строке
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            #  Получить абсолютное значение числа можно с помощью функции abs.
            #  Подстановка переменных через функцию str.format() является устаревшей,
            #  Используй f-строки.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    #  Нет необходимости переопределения метода родительского класса, если ты
    #  не собираешься менять его логику.
    def get_week_stats(self):
        super().get_week_stats()
