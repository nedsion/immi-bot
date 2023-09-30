import os
import json
import asyncio
import traceback

from decimal import Decimal
from time import sleep

from constants import constants, texts
# from utils import utils
from config import CONFIG
from helper import IMMI

from dotenv import dotenv_values, load_dotenv
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


load_dotenv()  # take environment variables from .env
env = dotenv_values(".env")
ADMIN_IDS = env.get("ADMIN_IDS")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def private_only(func):
    async def wrapper(update: Update, context, *args, **kwargs):
        if update.message.chat.type == "private":
            return await func(update, context, *args, **kwargs)
        else:
            msg = await update.message.reply_text(
                text=texts.IS_NOT_PRIVATE_MESSAGE, parse_mode="HTML"
            )
            # await asyncio.sleep(5)
            # await update.message.delete()
            # await msg.delete()

    return wrapper


def admin_only(func):
    async def wrapper(update: Update, context, *args, **kwargs):
        if str(update.effective_user.id) in ADMIN_IDS:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text(text=texts.IS_NOT_ADMIN, parse_mode="HTML")

    return wrapper

async def start(update: Update, context):
    await update.message.reply_text(
        text="Hello, I'm a bot!",
    )

@private_only
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=texts.HELP_MESSAGE, parse_mode="HTML")

async def clone_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(CONFIG.CLONE_LIST, 'r', encoding='utf-8') as f:
            clone_list = f.read().split('\n')

        clone_list = [clone for clone in clone_list if clone != '']

        if len(clone_list) > 0:
            # show clone list with <code> tag
            for i in range(len(clone_list)):
                clone_list[i] = f'<code>{clone_list[i]}</code>'
            clone_list = '\n'.join(clone_list)

            msg = texts.HAVE_CLONE_LIST.format(clone_list)

        else:
            msg = texts.HAVE_NO_CLONE_LIST

        await update.message.reply_text(text=msg, parse_mode="HTML")
    except:
        traceback.print_exc()
        await update.message.reply_text(text='Error not found clone list!')


async def create_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        immi = IMMI()
        email_address, email_password = immi.create_account()

        if email_address == False:
            await update.message.reply_text(text=texts.CREATE_CLONE_FAILED, parse_mode="HTML")
        else:
            await update.message.reply_text(text=texts.CREATE_CLONE_SUCCESS.format(email_address, email_password), parse_mode="HTML")

            
    except:
        traceback.print_exc()
        await update.message.reply_text(text=texts.CREATE_CLONE_FAILED, parse_mode="HTML")



strategyPatterns = {
    "start": start,
    "help": help,
    "clone_list": clone_list,
    "create_clone": create_clone,
}

handlers = []

for key, value in strategyPatterns.items():
    handlers.append(CommandHandler(key, value))


unknownHandler = MessageHandler(filters.COMMAND, unknown)

handlers.append(unknownHandler)