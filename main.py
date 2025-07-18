from telegram import Bot
import filetype
import os
import asyncio

# Dados do seu bot
TOKEN = "8145852232:AAFB7J8vofCx9q2iW3nUuboiwl3K4uUPmI4"
CHAT_ID = "251321771"

# Inicializa o bot
bot = Bot(token=TOKEN)

# Detecta tipo de imagem
def detect_image_type(file_path):
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return None
    kind = filetype.guess(file_path)
    return kind.mime if kind else "desconhecido"

# Função principal assíncrona
async def main():
    path = "imagem_teste.jpg"
    tipo = detect_image_type(path)

    if tipo:
        print("Tipo detectado:", tipo)
        await bot.send_message(chat_id=CHAT_ID, text=f"Tipo de imagem detectado: {tipo}")

        if os.path.exists(path):
            with open(path, "rb") as f:
                await bot.send_photo(chat_id=CHAT_ID, photo=f)
        else:
            await bot.send_message(chat_id=CHAT_ID, text="Erro: Imagem não encontrada.")

if __name__ == "__main__":
    asyncio.run(main())
