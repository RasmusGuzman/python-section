from dataclasses import dataclass
from .currency import Currency
from .exceptions import NegativeValueException, NotComparisonException, InsufficientFundsException


@dataclass
class Money:
    value: float
    currency: Currency

    def __post_init__(self):
        if self.value < 0:
            raise NegativeValueException("Сумма не может быть отрицательной")

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        if self.currency != other.currency:
            raise NotComparisonException("Нельзя сравнивать разные валюты")
        return abs(self.value - other.value) < 1e-6

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Можно складывать только с объектом Money")
        if self.currency != other.currency:
            raise NotComparisonException("Нельзя складывать разные валюты")
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Можно вычитать только объект Money")
        if self.currency != other.currency:
            raise NotComparisonException("Нельзя вычитать разные валюты")
        return Money(self.value - other.value, self.currency)


class Wallet:
    def __init__(self, initial_money=None):
        self.currencies = {}
        if initial_money:
            self.currencies[initial_money.currency] = initial_money

    def __getitem__(self, currency):
        return self.currencies.get(currency, Money(value=0, currency=currency))

    def __delitem__(self, currency):
        if currency in self.currencies:
            del self.currencies[currency]

    def __len__(self):
        return len(self.currencies)

    def __contains__(self, currency):
        return currency in self.currencies

    def add(self, money):
        if money.currency in self.currencies:
            self.currencies[money.currency] += money
        else:
            self.currencies[money.currency] = money
        return self

    def sub(self, money):
        if money.currency not in self.currencies:
            raise NotComparisonException(f"No {money.currency} in wallet")

        new_value = self.currencies[money.currency].value - money.value
        if new_value < 0:
            raise NegativeValueException("Cannot have negative balance")

        self.currencies[money.currency] = Money(value=new_value, currency=money.currency)
        return self
