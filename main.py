
import requests
import time
import hmac
import hashlib
import base64
import json
from datetime import datetime
import pytz
from telegram import Bot

# Credenciais da Binance
API_KEY = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
API_SECRET = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"

# Telegram
bot_token = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
chat_id = "251321771"
bot = Bot(token=bot_token)

# Meta em reais
META = 500000

def get_binance_balances():
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/account"
    timestamp = int(time.time() * 1000)
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    return {item["symbol"]: float(item["price"]) for item in response.json()}

def monitor():
    prices = get_prices()
    data = get_binance_balances()
    balances = data.get("balances", [])
    total_brl = 0
    report = []

    symbols_map = {
        "BTC": "BTCBRL",
        "ETH": "ETHBRL",
        "XRP": "XRPBRL",
        "W": "WBRL",
        "ERA": "ERABRL"
    }

    for item in balances:
        asset = item["asset"]
        free = float(item["free"])
        if free > 0 and asset in symbols_map:
            pair = symbols_map[asset]
            price = prices.get(pair, 0)
            value_brl = free * price
            total_brl += value_brl
            report.append(f"• {asset}: R$ {value_brl:.2f}")

    lucro = total_brl - 91.75
    percentual = (total_brl / META) * 100

    mensagem = f"📊 Saldo Atualizado
" + "
".join(report)
    mensagem += f"\n\n💰 Total: R$ {total_brl:.2f}\n📈 Lucro: R$ {lucro:.2f}\n🎯 Meta: R$ {META} ({percentual:.2f}%)"

    bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='Markdown')

if __name__ == "__main__":
    while True:
        try:
            monitor()
            time.sleep(30)  # Ajustável conforme desejado
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=f"❌ Erro: {str(e)}")
            time.sleep(60)
