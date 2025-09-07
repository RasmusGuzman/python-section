class NegativeValueException(ValueError):
    """Возникает при попытке использовать отрицательную сумму."""
    pass

class NotComparisonException(ValueError):
    """Возникает при попытке сравнить разные валюты."""
    pass

class InsufficientFundsException(ValueError):
    """Возникает при попытке снять больше, чем есть на счету."""
    pass
