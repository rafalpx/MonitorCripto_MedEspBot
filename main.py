# -*- coding: utf-8 -*-
import time
from binance.client import Client
from telegram import Bot
import os

# API Binance
api_key = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
api_secret = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"

client = Client(api_key, api_secret)

# Telegram
bot_token = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
chat_id = "251321771"
bot = Bot(token=bot_token)

# Saldo anterior
saldo_anterior = None

def obter_saldo_total_reais():
    info = client.get_account()
    total_brl = 0.0
    for asset in info["balances"]:
        moeda = asset["asset"]
        saldo = float(asset["free"])
        if saldo > 0:
            if moeda == "BRL":
                total_brl += saldo
            elif moeda != "USDT":
                try:
                    preco = client.get_symbol_ticker(symbol=f"{moeda}BRL")["price"]
                    total_brl += saldo * float(preco)
                except:
                    continue
    return round(total_brl, 2)

while True:
    try:
        total = obter_saldo_total_reais()
        if total != saldo_anterior:
            saldo_anterior = total
            mensagem = f"📊 *Saldo Atualizado*"
💰 Total: R$ {total:.2f}"
            bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")
        time.sleep(60)
    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
