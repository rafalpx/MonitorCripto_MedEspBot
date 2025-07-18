from telegram import Bot
from telegram.constants import ParseMode
import os
from decimal import Decimal
from dotenv import load_dotenv
from binance.client import Client
import ccxt

# Carregar variáveis de ambiente (se estiver usando .env)
load_dotenv()

# Configurações do Telegram e Binance
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_AQUI")
API_KEY = os.getenv("BINANCE_API_KEY", "SUA_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET", "SUA_API_SECRET")

bot = Bot(token=TELEGRAM_TOKEN)
client = Client(API_KEY, API_SECRET)

def obter_saldo_total():
    info = client.get_account()
    total = 0.0
    for asset in info['balances']:
        quantidade = float(asset['free']) + float(asset['locked'])
        if quantidade > 0:
            total += quantidade  # Simulação, o ideal é multiplicar pela cotação
    return total

def enviar_mensagem_saldo():
    total = obter_saldo_total()
    mensagem = f"📊 Saldo Atualizado:"
💰 Total: R$ {total:.2f}"
    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    enviar_mensagem_saldo()
