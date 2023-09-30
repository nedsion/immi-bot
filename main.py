import os
import logging
import sqlite3

from dotenv import dotenv_values, load_dotenv
from telegram.ext import ApplicationBuilder

from handlers import handlers

load_dotenv()  # take environment variables from .env

env = dotenv_values(".env")
TOKEN = env.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handlers(handlers=handlers)

    app.run_polling()