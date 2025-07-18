
import time
import requests
import json
from binance.client import Client
from telegram import Bot

API_KEY = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
API_SECRET = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"
bot_token = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
chat_id = "251321771"
meta = 500000.0

client = Client(API_KEY, API_SECRET)
bot = Bot(token=bot_token)

def get_total_balance_brl():
    prices = {i["symbol"]: float(i["price"]) for i in client.get_all_tickers()}
    balances = client.get_account()["balances"]

    total_brl = 0.0
    for asset in balances:
        asset_name = asset["asset"]
        free = float(asset["free"])
        if free == 0.0:
            continue
        if asset_name == "BRL":
            total_brl += free
        elif asset_name + "BRL" in prices:
            total_brl += free * prices[asset_name + "BRL"]
        elif asset_name + "USDT" in prices:
            brl_usdt = prices.get("USDTBRL", 5.0)
            total_brl += free * prices[asset_name + "USDT"] * brl_usdt
    return total_brl

last_balance = None

while True:
    try:
        current_balance = get_total_balance_brl()
        if last_balance is None or abs(current_balance - last_balance) > 0.01:
            lucro = current_balance - 91.75
            progresso = (current_balance / meta) * 100
            mensagem = (
                f"📊 *Saldo Atualizado*
"
                f"💰 Total: R$ {current_balance:.2f}
"
                f"📈 Lucro: R$ {lucro:.2f}
"
                f"🎯 Meta: R$ {meta:.0f} ({progresso:.2f}%)"
            )
            bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")
            last_balance = current_balance
    except Exception as e:
        print("Erro:", e)
    time.sleep(60)
