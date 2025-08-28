import os
from pathlib import Path

from dotenv import load_dotenv
from vyper import v

load_dotenv()

config = Path(__file__).parent.joinpath("../../").joinpath("config")
v.set_config_name("dev")
v.add_config_path(config)
v.read_in_config()

from telebot import TeleBot


def send_file() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    _telegram_bot = TeleBot(token)

    file_path = Path(__file__).resolve().parents[2] / "swagger-coverage-dm-api-account.html"
    exists = file_path.exists()
    size = file_path.stat().st_size if exists else -1

    if not exists:
        _telegram_bot.send_message(chat_id, "❌ Файл не найден. Проверь путь выше.")
        return
    if size == 0:
        _telegram_bot.send_message(chat_id, "❌ Файл нулевого размера (0 bytes).")
        return
    if size > 50 * 1024 * 1024:
        _telegram_bot.send_message(chat_id, f"❌ Файл слишком большой: {size} bytes (>50MB).")
        return

    with open(file_path, "rb") as f:
        _telegram_bot.send_document(chat_id=chat_id, document=f, caption="coverage")


if __name__ == '__main__':
    send_file()
