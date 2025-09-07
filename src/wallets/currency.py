from dataclasses import dataclass

@dataclass(frozen=True)
class Currency:
    code: str  # Код валюты (ISO)
    name: str  # Название валюты

# Предварительно определим основные валюты
rub = Currency(code='RUB', name='Российский рубль')
usd = Currency(code='USD', name='Американский доллар')
