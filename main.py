import os
import time
import requests
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_fake_balance():
    # Exemplo de função fictícia — substitua pela real integração com API da Binance
    return {"BTC": 0.0001, "ETH": 0.001, "R$": 91.75}

def format_message(balances):
    total_brl = balances.get("R$", 0.0)
    return f"📊 Saldo Atualizado:\nBTC: {balances['BTC']}\nETH: {balances['ETH']}\nTotal: R$ {total_brl:.2f}"

def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == "__main__":
    while True:
        try:
            saldo = get_fake_balance()
            msg = format_message(saldo)
            send_telegram_message(msg)
            time.sleep(600)  # espera 10 minutos
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)