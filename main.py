
import time
import requests
import hmac
import hashlib
import json
import telegram
from telegram import Bot

# Credenciais da Binance
API_KEY = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
API_SECRET = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"

# Telegram
bot = Bot(token="8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4")
chat_id = "251321771"

# Endpoint da Binance
BASE_URL = "https://api.binance.com"

# Armazena o último saldo conhecido
last_total = 0.0

def get_account_balance():
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

def calcular_total_brl(balances):
    # Para simplificação, valores fictícios de conversão
    cotacoes = {
        "BTC": 340000,
        "ETH": 18000,
        "XRP": 2.8,
        "SUI": 4.2,
        "SOL": 440,
        "USDT": 5.4,
        "WORM": 0.01,
        "CAL": 0.01
    }
    total = 0.0
    for asset in balances:
        symbol = asset["asset"]
        if symbol in cotacoes:
            total += float(asset["free"]) * cotacoes[symbol]
    return total

def main():
    global last_total
    while True:
        try:
            data = get_account_balance()
            if "balances" in data:
                total = calcular_total_brl(data["balances"])
                if abs(total - last_total) > 0.01:
                    last_total = total
                    mensagem = f"💹 Saldo Atualizado: R$ {total:.2f}"
                    bot.send_message(chat_id=chat_id, text=mensagem)
            time.sleep(30)
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=f"Erro: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
