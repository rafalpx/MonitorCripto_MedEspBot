import json
import time
import requests
from binance.client import Client
from telegram import Bot

with open('config.json') as f:
    config = json.load(f)

bot_token = config["bot_token"]
chat_id = config["chat_id"]
api_key = config["binance_api_key"]
api_secret = config["binance_api_secret"]
meta_reais = config["meta_reais"]

bot = Bot(token=bot_token)
client = Client(api_key, api_secret)

last_balances = {}

def get_balance():
    account = client.get_account()
    balances = {b['asset']: float(b['free']) + float(b['locked']) for b in account['balances'] if float(b['free']) > 0 or float(b['locked']) > 0}
    return balances

def get_prices():
    tickers = client.get_all_tickers()
    return {t['symbol']: float(t['price']) for t in tickers}

def calcular_valor_total(balances, prices):
    total = 0.0
    for asset, amount in balances.items():
        symbol = asset + "BRL" if asset != "BRL" else "BRL"
        price = prices.get(symbol, 0)
        total += amount * price
    return round(total, 2)

while True:
    try:
        balances = get_balance()
        prices = get_prices()
        total = calcular_valor_total(balances, prices)

        if total != last_balances.get("total"):
            progresso = (total / meta_reais) * 100
            message = f"📊 *Saldo Atualizado:*

💰 Total: R$ {total:.2f}
🎯 Meta: R$ {meta_reais:.2f} ({progresso:.2f}%)"
            bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
            last_balances["total"] = total

        time.sleep(30)
    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
