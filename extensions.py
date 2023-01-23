import requests
import json
from config import keys, keys_base, access_key


class ConvertionException(Exception):
    pass

class CriptoConverter:
    @staticmethod
    def get_price(base, symbols, amount):
        if symbols == base:
            raise ConvertionException(f'Невозможно перевести  одинаковые валюты {base}')
        try:
            base_keys = keys_base[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base},\n базовая валюта - доллар')
        try:
            symbols_keys = keys[symbols]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {symbols}\n валюта не найдена. Базовая валюта - доллар, доступных валюты {keys}')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}!')

        url = (f'https://openexchangerates.org/api/latest.json?app_id={access_key}&base={base_keys}&symbols={symbols_keys}')
        response = requests.get(url)
        r = json.loads(response.content)

        #zena_o = (r["rates"][symbols])

        total_base = (r["rates"][symbols_keys] * amount)

        return round(total_base)

