from telegram import Bot
import filetype
import os

# Dados do seu bot
TOKEN = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
CHAT_ID = "251321771"

# Inicializa o bot
bot = Bot(token=TOKEN)

# Função para detectar tipo do arquivo
def detect_image_type(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        bot.send_message(chat_id=CHAT_ID, text=f"Erro: Arquivo '{file_path}' não encontrado.")
        return None
    kind = filetype.guess(file_path)
    return kind.mime if kind else "desconhecido"

# Envia uma imagem para o chat do Telegram
def send_photo(file_path):
    if not os.path.exists(file_path):
        print(f"Imagem não encontrada: {file_path}")
        bot.send_message(chat_id=CHAT_ID, text=f"Erro: Imagem '{file_path}' não encontrada.")
        return
    with open(file_path, "rb") as f:
        bot.send_photo(chat_id=CHAT_ID, photo=f)

# Uso principal
if __name__ == "__main__":
    path = "imagem_teste.jpg"
    tipo = detect_image_type(path)
    if tipo:
        print("Tipo detectado:", tipo)
        bot.send_message(chat_id=CHAT_ID, text=f"Tipo de imagem detectado: {tipo}")
        send_photo(path)
