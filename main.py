from telegram import Bot, InputFile
import filetype

# Dados do seu bot
TOKEN = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
CHAT_ID = "251321771"

# Inicializa o bot
bot = Bot(token=TOKEN)

# Função para detectar tipo do arquivo (substitui imghdr)
def detect_image_type(file_path):
    kind = filetype.guess(file_path)
    if kind is not None:
        return kind.mime
    return "unknown"

# Envia uma imagem para o chat do Telegram
def send_photo(file_path):
    with open(file_path, "rb") as f:
        bot.send_photo(chat_id=CHAT_ID, photo=f)

# Exemplo de uso
if __name__ == "__main__":
    path = "imagem_teste.jpg"
    print("Tipo detectado:", detect_image_type(path))
    send_photo(path)
