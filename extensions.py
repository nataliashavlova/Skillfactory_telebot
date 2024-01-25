import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Вы ввели две одинаковые валюты: {base}. Для конвертации необходимо ввести разные валюты.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена. Проверить список доступных валют можно по команде /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена. Проверить список доступных валют можно по команде /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Пожалуйста, убедитесь, что вы написали число.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]*amount

        return total_base
