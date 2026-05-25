import requests

url = 'https://coinmarketcap.com/'

html = requests.get(url).text

price_list = []

for tag in html.split('<span>'):
    if tag.startswith('$'):
        for tag_value in tag.split('</span>'):
            if tag_value.startswith("$"):
                price_list.append(tag_value)


def price_to_float(price: str):
    return float(price[1:].replace(',', ''))


bit_coin = price_list[1]
bitcoin_price_usd = price_to_float(bit_coin)

try:
    nbu_url = 'https://bank.gov.ua/NBUStatService/v1/statistiki/exchange?valcode=USD&json'
    usd_to_uah = requests.get(nbu_url).json()[0]['rate']
except:
    usd_to_uah = 41.5

user_input = input("Скільки у вас біткоїнів? ")

try:
    my_bitcoins = float(user_input)

    total_usd = my_bitcoins * bitcoin_price_usd
    total_uah = total_usd * usd_to_uah

    print(f"Курс Bitcoin: {bit_coin}")
    print(f"Ваші {my_bitcoins} BTC коштують:")
    print(f"-> ${total_usd:,.2f} USD")
    print(f"-> {total_uah:,.2f} UAH")
except ValueError:
    print("Будь ласка, введіть коректне число.")