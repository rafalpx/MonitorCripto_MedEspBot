import time
import requests
import json
from binance.client import Client
from telegram import Bot

# Credenciais
API_KEY = "SgiViR6JUJUjwkLpLUXkVt5S1i43YIzNphg2QVfpsD34uVcPn77JDNGRlInL6xvM"
API_SECRET = "NJyWvylMLOUUHwemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"
bot_token = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
chat_id = "251321771"

client = Client(API_KEY, API_SECRET)
bot = Bot(token=bot_token)

meta = 500000  # Meta em R$

def obter_saldos():
    infos = client.get_account()
    cotacoes = {
        "BTC": float(client.get_symbol_ticker(symbol="BTCBRL")["price"]),
        "ETH": float(client.get_symbol_ticker(symbol="ETHBRL")["price"]),
        "XRP": float(client.get_symbol_ticker(symbol="XRPBRL")["price"]),
        "CALDERA": 0.01,
        "WORMHOLE": 0.02
    }
    total = 0
    detalhes = []
    for item in infos["balances"]:
        moeda = item["asset"]
        saldo = float(item["free"])
        if moeda in cotacoes and saldo > 0:
            valor_em_reais = saldo * cotacoes[moeda]
            total += valor_em_reais
            detalhes.append((moeda, valor_em_reais))
    return total, detalhes

total_anterior = 0

while True:
    try:
        total, detalhes = obter_saldos()
        if total != total_anterior:
            lucro = total - 91.75
            percentual = (total / meta) * 100
            mensagem = "📊 *Saldo Atualizado*\n"
            for moeda, valor in detalhes:
                mensagem += f"• {moeda}: R$ {valor:.2f}\n"
            mensagem += f"\n💰 Total: R$ {total:.2f}\n"
            mensagem += f"📈 Lucro: R$ {lucro:.2f}\n"
            mensagem += f"🎯 Meta: R$ {meta:,.0f} ({percentual:.2f}%)"

            bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")
            total_anterior = total
        time.sleep(30)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Erro detectado:\n{str(e)}")
        time.sleep(60)
