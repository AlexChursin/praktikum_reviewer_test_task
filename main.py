import datetime as dt


class Record:
    def __init__(self, amount, comment,
                 date=''):  # Можно лучше: Можно использовать аннотацию типов, это даст ряд преимуществ, о которых можно почитать здесь: https://semakin.dev/2020/06/type_hints/
        self.amount = amount  # Можно лучше: На заметку: если переменная не должна быть видна из вне класса (быть публичной), то ее лучше скрыть. Подробнее: https://tirinox.ru/encapsulation-python/
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())  # Можно лучше: параметр date можно инициализировать как None, а не строкой, это будет выглядеть нагляднее: ... if date is not None else... А также, записать все в одну строчку
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:  # Надо исправить: переменная 'Record' должна называться с маленькой буквы, и тем более не именем класса
            if Record.date == dt.datetime.now().date():  # Можно лучше: функцию dt.datetime.now().date() лучше вынести в отдельную переменную перед циклом, так как она вызывается каждый раз, это не эффективно
                today_stats = today_stats + Record.amount  # Можно лучше: сокращенно today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                    (today - record.date).days < 7 and  # Можно лучше: такие условия лучше всего писать сокращенно 7 > (today - record.date).days >= 0. Это упрощает чтение кода
                    (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):  # Надо исправить: согласно требованиям, комментарии к функциям должны быть оформлены в виде Docstrings. https://www.python.org/dev/peps/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()  # Можно лучше: переменную x можно либо назвать, например diff, либо вообще обойтись без нее
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return ('Хватит есть!')  # Можно лучше: круглые скобки (...) лучше убрать


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  # Надо исправить: названия параметров должны быть маленькими буквами, и тем более не должны совпадать с аргументами класса
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # Надо исправить: синтаксическая ошибка в '=='. Или может эта сточка лишняя?
            currency_type = 'руб'
        if cash_remained > 0:
            return (  # Можно лучше: весь результат в скобках можно взять в тройные кавычки: f""" ... """ это избавит от лишних кавычек
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return f'Денег нет, держись:' \
                   f' твой долг - {cash_remained:.2f} {currency_type}'

    def get_week_stats(self):  # Надо исправить: не обязательно переопределять метод без необходимости. Если удалить тут этот метод, то при вызове его из CashCalculator, он все равно вызовется из класса Calculator
        super().get_week_stats()
