from currency_converter import CurrencyConverter
def convert_currency(amount, from_currency, to_currency):
    c = CurrencyConverter()
    converted_amount = c.convert(amount, from_currency, to_currency)
    return converted_amount