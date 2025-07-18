
import time
import requests
from binance.client import Client
from telegram import Bot

# Configurações
api_key = 'SUA_BINANCE_API_KEY'
api_secret = 'SUA_BINANCE_API_SECRET'
bot_token = '8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4'
chat_id = '251321771'

client = Client(api_key, api_secret)
bot = Bot(token=bot_token)

def obter_saldo():
    info = client.get_account()
    balances = info['balances']
    moedas = {b['asset']: float(b['free']) for b in balances if float(b['free']) > 0}
    return moedas

def enviar_mensagem(mensagem):
    bot.send_message(chat_id=chat_id, text=mensagem)

def main():
    saldo_anterior = {}
    while True:
        saldo_atual = obter_saldo()
        if saldo_atual != saldo_anterior:
            total = 0
            msg = "💰 Saldo Atualizado:\n"
            for moeda, quantidade in saldo_atual.items():
                preco = obter_preco_moeda(moeda)
                valor = quantidade * preco
                total += valor
                msg += f"{moeda}: {quantidade} ≈ R$ {valor:.2f}\n"
            msg += f"Total: R$ {total:.2f}"
            enviar_mensagem(msg)
            saldo_anterior = saldo_atual
        time.sleep(60)

def obter_preco_moeda(moeda):
    if moeda == "BRL":
        return 1.0
    try:
        ticker = client.get_symbol_ticker(symbol=f"{moeda}BRL")
        return float(ticker['price'])
    except:
        return 0.0

if __name__ == "__main__":
    main()
