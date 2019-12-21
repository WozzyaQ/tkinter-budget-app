from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
import datetime
import copy
import json

class AbstractTask(ABC):

    @abstractmethod
    def attach_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass


class DepositTask(AbstractTask):
    def __init__(self):
        self._state = None
        self._observers = list()

        # self._deposits = list()
        self._deposits = self.retrieve_data()

    def attach_observer(self, observer: Observer):
        print("Observer has been added!")
        self._observers.append(observer)

    def detach_observer(self, observer: Observer) -> None:
        print("Observer has been removed")
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def put_on_deposit(self, *args):
        self._state = "deposit"
        self._deposits.append(dict(date=args[0],
                                   total=args[1],
                                   period=args[3],
                                   percent=args[4],
                                   purpose=args[5]))

        print(self._deposits)
        self.notify_observers()
        self._state = None

    @staticmethod
    def retrieve_data():
        try:
            with open("deposit.json", "r") as file:
                data = json.load(file)
                print(data)
                return data

        except json.JSONDecodeError:
            return list()

    def save_data(self):
        with open("deposit.json", "w") as file:
            json.dump(self._deposits, file, indent=4)


class CreditTask(AbstractTask):
    def __init__(self):
        self._state = None
        self._observers = list()

        self._credits = self.retrieve_data()

    def attach_observer(self, observer: Observer):
        print("Observer has been added!")
        self._observers.append(observer)

    def detach_observer(self, observer: Observer) -> None:
        print("Observer has been removed")
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def get_credit(self, *args):
        self._state = "credit"
        self._credits.append(dict(date=args[0],
                                  total=args[1],
                                  period=args[3],
                                  percent=args[4],
                                  purpose=args[5]))

        self.notify_observers()
        self._state = None

    @staticmethod
    def retrieve_data():
        try:
            with open("credit.json", "r") as file:
                data = json.load(file)
                print(data)
                return data

        except json.JSONDecodeError:
            return list()

    def save_data(self):
        with open("credit.json", "w") as file:
            json.dump(self._credits, file, indent=4)



class Observer(ABC):

    @abstractmethod
    def update(self, subject: AbstractTask) -> None:
        pass


class Expense(Observer):
    def __init__(self):
        self._expenses = self.retrieve_data()

    def add_expense(self, *args):
        self._expenses[args[0]].append(dict(total=args[1],
                                            is_periodic=args[2],
                                            period=args[3],
                                            percent=args[4],
                                            purpose=args[5]))

    def update(self, subject: AbstractTask) -> None:
        state = subject._state
        if state == "deposit":
            new_transaction = subject._deposits[-1]
            self._expenses[new_transaction["date"]].append(dict(total=new_transaction["total"],
                                                                is_periodic=False,
                                                                period=False,
                                                                percent=None,
                                                                purpose=new_transaction["purpose"]))

        elif state == "credit":
            new_transaction = subject._credits[-1]
            self._expenses[new_transaction["date"]].append(dict(total=new_transaction["total"],
                                                                is_periodic=True,
                                                                period=new_transaction["period"],
                                                                percent=new_transaction["percent"],
                                                                purpose=new_transaction["purpose"]))

    @staticmethod
    def retrieve_data():
        try:
            with open("expense.json", "r") as file:
                data = json.load(file)
                data = defaultdict(list, data)
                return data

        except json.JSONDecodeError:
            return defaultdict(list)

    def save_data(self):
        with open("expense.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    @property
    def expenses(self):
        return self._expenses


class Income(Observer):
    def __init__(self):
        self._incomes = self.retrieve_data()

    def add_income(self, *args):
        # date 0 / total 1 / is periodic  2/ period 3 / percent  4/ / purpose  5

        self._incomes[args[0]].append(dict(total=args[1],
                                           is_periodic=args[2],
                                           period=args[3],
                                           percent=args[4],
                                           purpose=args[5]))

    def update(self, subject: AbstractTask) -> None:
        state = subject._state
        if state == "deposit":
            new_transaction = subject._deposits[-1]
            self._incomes[new_transaction["date"]].append(dict(total=new_transaction["total"],
                                                               is_periodic=True,
                                                               period=new_transaction["period"],
                                                               percent=new_transaction["percent"],
                                                               purpose=new_transaction["purpose"]))
        elif state == "credit":
            new_transaction = subject._credits[-1]
            self._incomes[new_transaction["date"]].append(dict(total=new_transaction["total"],
                                                               is_periodic=False,
                                                               period=False,
                                                               percent=None,
                                                               purpose=new_transaction["purpose"]))

    @staticmethod
    def retrieve_data():
        try:
            with open("income.json", "r") as file:
                data = json.load(file)
                data = defaultdict(list, data)
                return data

        except json.JSONDecodeError:
            return defaultdict(list)

    def save_data(self):
        with open("income.json", "w") as file:
            json.dump(self.incomes, file, indent=4)

    @property
    def incomes(self):
        return self._incomes


class Terminal:
    def __init__(self):
        self._income = Income()
        self._expense = Expense()
        self._credit = CreditTask()
        self._deposit = DepositTask()

        # Attaching observers
        self._credit.attach_observer(self._income)
        self._credit.attach_observer(self._expense)

        self._deposit.attach_observer(self._income)
        self._deposit.attach_observer(self._expense)

        self._transaction_types = {
            'income': self._income.add_income,
            'expense': self._expense.add_expense,
            'credit': self._credit.get_credit,
            'deposit': self._deposit.put_on_deposit
        }

    def create_and_load_transaction(self, _transaction_type, _date, _total, _periodic=False,
                                    _period=False, _percent=None, _purpose=None):

        transaction = self._transaction_types[_transaction_type]

        transaction(_date, _total, _periodic, _period, _percent, _purpose)

    def get_total_expense(self):
        total = 0
        for list_of_transaction in self._expense.expenses.values():
            for transaction in list_of_transaction:
                if not transaction["period"]:
                    total += float(transaction["total"])
        return round(total, 2)

    def get_total_income(self):
        total = 0
        for list_of_transaction in self._income.incomes.values():
            for transaction in list_of_transaction:
                if not transaction["period"]:
                    total += float(transaction["total"])
        return round(total, 2)

    def get_total_overall(self):
        return round(self.get_total_income()-self.get_total_expense(), 2)

    def save_all(self):
        self.income.save_data()
        self.expense.save_data()
        self.deposit.save_data()
        self.credit.save_data()

    @property
    def expense(self):
        return self._expense

    @property
    def income(self):
        return self._income

    @property
    def credit(self):
        return self._credit

    @property
    def deposit(self):
        return self._deposit


class Filter:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal

    @staticmethod
    def sort_dates(_dates):
        return sorted(_dates, key=lambda date: datetime.datetime.strptime(date, '%d.%m.%Y'))

    def get_dates_in_range(self, start_date, end_date, data_list):
        begin = list(map(int, start_date.split(".")))
        end = list(map(int, end_date.split(".")))

        dates_to_sort = list()
        for key in data_list:
            dates_to_sort.append(key)

        sorted_dates = self.sort_dates(dates_to_sort)

        dates_in_range = list()
        for date in sorted_dates:
            current_date = list(map(int, date.split(".")))
            if begin[-1] < current_date[-1] < end[-1]:
                dates_in_range.append(date)

            elif current_date[-1] == begin[-1]:
                if current_date[-2] > begin[-2]:
                    dates_in_range.append(date)
                elif current_date[-2] == begin[-2]:
                    if current_date[-3] >= begin[-3]:
                        dates_in_range.append(date)

            elif current_date[-1] == end[-1]:
                if not current_date[-2] > end[-2]:
                    dates_in_range.append(date)
                elif current_date[-2] == begin[-2]:
                    if current_date[-3] <= begin[-3]:
                        dates_in_range.append(date)
        return dates_in_range

    def get_transactions_in_sum_range(self, lower_bound, upper_bound, date_list):
        transactions_in_sum_range = defaultdict(list)
        for key, values in date_list.items():
            for single_value in values:
                if lower_bound <= float(single_value["total"]) <= upper_bound:
                    transactions_in_sum_range[key].append(single_value)

        dates_to_sort = list()
        for key in transactions_in_sum_range:
            dates_to_sort.append(key)

        sorted_dates = self.sort_dates(dates_to_sort)

        return self.fetch_transactions_by_date(transactions_in_sum_range,sorted_dates)

    @staticmethod
    def fetch_transactions_by_date(data, date_range):
        payload = []

        for date, value in data.items():
            if date in date_range:
                payload.append((date, value))
        return payload

    # TODO  how to pass suitable dates to user
    def get_incomes_for_period(self, start_date, end_date):
        date_range = self.get_dates_in_range(start_date, end_date, self.terminal.income.incomes)
        return self.fetch_transactions_by_date(self.terminal.income.incomes, date_range)

    def get_expenses_for_period(self, start_date, end_date):
        date_range = self.get_dates_in_range(start_date, end_date, self.terminal.expense.expenses)
        return self.fetch_transactions_by_date(self.terminal.expense.expenses, date_range)

    def term_forecast(self, start_date, end_date):
        pass

    def get_all_transactions(self):
        pass

    def filter_by_sum_diapason(self, lower_bound: float, upper_bound):
        merged_transaction_list = copy.copy(self.terminal.expense.expenses)
        for key, value in merged_transaction_list.items():
            for single_value in value:
                single_value.update(type="E")

        for key, value in self.terminal.income.incomes.items():
            for single_value in value:
                single_value.update(type="I")
                merged_transaction_list[key].append(single_value)

        return self.get_transactions_in_sum_range(lower_bound, upper_bound, merged_transaction_list)


# terminal_ = Terminal()
# filter_ = Filter(terminal_)
# terminal_.create_and_load_transaction("expense", "12.10.2008", 1999)
#
# terminal_.create_and_load_transaction("expense", "12.10.2008", 1999)
# terminal_.create_and_load_transaction("income", "11.12.2000",250)
# terminal_.create_and_load_transaction("income", "12.10.1999", 300)
# terminal_.create_and_load_transaction("deposit", "12.10.1999", 300)
# terminal_.create_and_load_transaction("credit", "12.10.1999", 300)

#
#
# terminal_.save_all()