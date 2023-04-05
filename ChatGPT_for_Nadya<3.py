##import os
##import sys
##import requests
##import telegram
##from telegram.ext import Updater, MessageHandler, Filters
##import multiprocessing
##
##key = "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"
##TOKEN = "6168635183:AAFXZe7OmGV268-Ll8V2R45549ryI6jIXqE"
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text, escape_md

API_TOKEN = '6168635183:AAFXZe7OmGV268-Ll8V2R45549ryI6jIXqE'
OPENAI_API_KEY = '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'

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_messages_history = {}

async def chat_gpt_generate_answer(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        message = response.choices[0].text.strip()
        return message
    except openai.error.RateLimitError:
        return "К сожалению, я превысил квоту доступа к API OpenAI. Пожалуйста, попробуйте позже."

@dp.message_handler()
async def process_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_messages_history:
        user_messages_history[user_id] = []
    user_messages_history[user_id].append(message.text)

    prompt = " ".join(user_messages_history[user_id])

    response = await chat_gpt_generate_answer(prompt)
    await message.reply(response, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
