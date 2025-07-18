# -*- coding: utf-8 -*-
import time
import requests
import json
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
from pytz import timezone
import telegram

# CONFIGURAÇÕES
API_KEY = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
API_SECRET = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"
TELEGRAM_TOKEN = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
CHAT_ID = "251321771"

BASE_URL = "https://api.binance.com"
HEADERS = {"X-MBX-APIKEY": API_KEY}

def get_account_info():
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_prices():
    url = f"{BASE_URL}/api/v3/ticker/price"
    response = requests.get(url)
    return {item['symbol']: float(item['price']) for item in response.json()}

def get_portfolio_value(account_info, prices):
    total_brl = 0
    report = []
    for asset in account_info['balances']:
        symbol = asset['asset']
        free = float(asset['free'])
        if free > 0 and symbol + "USDT" in prices:
            value = free * prices[symbol + "USDT"]
            total_brl += value * 5.4  # conversão aproximada
            report.append(f"🔸 {symbol}: R$ {value * 5.4:.2f}")
    return total_brl, report

def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def main():
    last_total = 0
    while True:
        try:
            account_info = get_account_info()
            prices = get_prices()
            total, report = get_portfolio_value(account_info, prices)

            if abs(total - last_total) > 0.01:
                last_total = total
                message = "*📊 Saldo Atualizado*
"
                message += "
".join(report)
                message += f"

💰 *Total: R$ {total:.2f}*"
                send_telegram_message(message)

            time.sleep(30)
        except Exception as e:
            print("Erro:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()

