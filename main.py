
import time
import requests
import json
import telegram
from decimal import Decimal
from binance.client import Client
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, BINANCE_API_KEY, BINANCE_API_SECRET

bot = telegram.Bot(token=TELEGRAM_TOKEN)
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

meta_objetivo_brl = Decimal("500000")
ultimo_saldo_total = Decimal("0.00")
saldo_anterior = {}

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}BRL"
    response = requests.get(url)
    data = response.json()
    return Decimal(data["price"])

def obter_saldos():
    contas = client.get_account()
    saldos = {}
    for ativo in contas["balances"]:
        asset = ativo["asset"]
        free = Decimal(ativo["free"])
        locked = Decimal(ativo["locked"])
        total = free + locked
        if total > 0:
            saldos[asset] = total
    return saldos

def calcular_total_e_lucro(saldos):
    total_brl = Decimal("0.00")
    variacoes = []
    for moeda, quantidade in saldos.items():
        if moeda == "BRL":
            preco = Decimal("1.00")
        else:
            try:
                preco = get_price(moeda)
            except:
                continue
        valor_brl = quantidade * preco
        total_brl += valor_brl

        variacao = Decimal("0.00")
        if moeda in saldo_anterior:
            variacao = valor_brl - saldo_anterior[moeda]

        saldo_anterior[moeda] = valor_brl
        variacoes.append((moeda, valor_brl, variacao))

    return total_brl, variacoes

def enviar_alerta(saldo_total, variacoes):
    progresso = (saldo_total / meta_objetivo_brl) * 100
    lucro = saldo_total - ultimo_saldo_total
    msg = "📊 *Saldo Atualizado*
"
    for moeda, valor, variacao in variacoes:
        emoji = "🟢" if variacao > 0 else "🔴" if variacao < 0 else "⚪️"
        sinal = "+" if variacao > 0 else ""
        msg += f"{emoji} {moeda}: R$ {valor:.2f} ({sinal}R$ {variacao:.2f})
"
    msg += f"
🧾 Total: R$ {saldo_total:.2f}
💰 Lucro: R$ {lucro:.2f}
🎯 Meta: R$ {meta_objetivo_brl:,} ({progresso:.2f}%)"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    global ultimo_saldo_total
    while True:
        try:
            saldos = obter_saldos()
            saldo_total, variacoes = calcular_total_e_lucro(saldos)
            if saldo_total != ultimo_saldo_total:
                enviar_alerta(saldo_total, variacoes)
                ultimo_saldo_total = saldo_total
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
