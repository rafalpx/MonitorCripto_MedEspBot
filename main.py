import asyncio
from report_utils import gerar_relatorio, gerar_grafico
from telegram import Bot
import ccxt

# Configurações reais
TOKEN = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
CHAT_ID = "251321771"
META_R = 500_000.0

API_KEY = "SgiViR6JUUJjwkLpLUXkt5S1i43YIzNphg2QVfpsD34uVCpPn77JDNGR1lInL6xvM"
API_SECRET = "NJyWvy1MLOUHWemLbaCHDZMoJLuuA8iLGXZd2Bua23FNDVmSvKMo1td9eq7TXW0"

async def main():
    bot = Bot(token=TOKEN)

    exchange = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True
    })

    balances = exchange.fetch_balance()['total']
    moedas = {k: v for k, v in balances.items() if v > 0}

    # Obter preços em USDT e converter para BRL
    tickers = exchange.fetch_tickers()
    cotacoes = {}
    for moeda in moedas:
        par = f"{moeda}/USDT"
        if par in tickers:
            cotacoes[moeda] = tickers[par]['last']

    total_brl = 0
    moedas_brl = {}
    btc_brl = exchange.fetch_ticker("BTC/BRL")['last']
    for moeda, quantidade in moedas.items():
        if moeda in cotacoes:
            valor_usdt = cotacoes[moeda] * quantidade
            valor_brl = valor_usdt * btc_brl / tickers["BTC/USDT"]['last']
            moedas_brl[moeda] = round(valor_brl, 2)
            total_brl += valor_brl

    progresso = total_brl / META_R * 100
    msg = gerar_relatorio(total_brl, moedas_brl, META_R)
    img_path = gerar_grafico(total_brl, moedas_brl, progresso)

    await bot.send_message(chat_id=CHAT_ID, text=msg)
    with open(img_path, "rb") as img:
        await bot.send_photo(chat_id=CHAT_ID, photo=img)

if __name__ == "__main__":
    asyncio.run(main())
