from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List


# Класс заказа с необходимыми данными
@dataclass
class Order:
    total: float
    is_loyal_customer: bool = False
    applicable_discounts: List[str] = None


# Абстрактный класс скидки
class Discount(ABC):
    @abstractmethod
    def apply(self, order: Order) -> float:
        pass


class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        return min(self.amount, order.total)


class PercentageDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, order: Order) -> float:
        return order.total * self.percent / 100


class LoyaltyDiscount(Discount):
    def apply(self, order: Order) -> float:
        return order.total * 0.05 if order.is_loyal_customer else 0.0


# Фабрика для создания скидок
class DiscountFactory:
    @staticmethod
    def create(discount_type: str, *args) -> Discount:
        match discount_type:
            case "fixed":
                return FixedDiscount(*args)
            case "percentage":
                return PercentageDiscount(*args)
            case "loyalty":
                return LoyaltyDiscount()
            case _:
                raise ValueError(f"Unknown discount type: {discount_type}")


# Механизм применения скидок
class DiscountEngine:
    def __init__(self, order: Order):
        self.order = order
        self.discounts: List[Discount] = []

        # Автоматические скидки
        if order.total > 5000:
            self.discounts.append(FixedDiscount(300))
        if order.is_loyal_customer:
            self.discounts.append(LoyaltyDiscount())

        # Пользовательские скидки
        if order.applicable_discounts:
            for d in order.applicable_discounts:
                dtype, *params = d.split('_')
                self.discounts.append(
                    DiscountFactory.create(dtype, *map(float, params))
                )

    def calculate_total_discount(self) -> float:
        total = sum(d.apply(self.order) for d in self.discounts)
        return max(0, min(total, self.order.total))


# Пример использования
if __name__ == "__main__":
    order = Order(
        total=8000.0,
        is_loyal_customer=True,
        applicable_discounts=["percentage_10", "fixed_500"]
    )

    engine = DiscountEngine(order)
    discount = engine.calculate_total_discount()

    print(f"Исходная сумма: {order.total} руб.")
    print(f"Общая скидка: {discount:.2f} руб.")
    print(f"Итоговая сумма: {order.total - discount:.2f} руб.")
