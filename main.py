import requests
import time
from binance.client import Client
from telegram import Bot

# Chaves fornecidas
API_KEY = 'SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM'
API_SECRET = 'NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0'
bot_token = '8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4'
chat_id = '251321771'

# Inicializa clientes
client = Client(API_KEY, API_SECRET)
bot = Bot(token=bot_token)

# Saldo anterior
last_total = 0

def get_balance():
    prices = client.get_all_tickers()
    balances = client.get_account()['balances']
    total_brl = 0
    for asset in balances:
        asset_name = asset['asset']
        free_amount = float(asset['free'])
        if free_amount > 0:
            for price in prices:
                if price['symbol'] == asset_name + 'USDT':
                    brl_price = float(price['price']) * 5  # Aproximando 1 USDT ≈ 5 BRL
                    total_brl += free_amount * brl_price
    return total_brl

def main_loop():
    global last_total
    while True:
        try:
            total = get_balance()
            if abs(total - last_total) > 0.01:
                last_total = total
                mensagem = f"*📊 Saldo Atualizado:*
💰 Total: R$ {total:.2f}"
                bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='Markdown')
        except Exception as e:
            print("Erro:", e)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
