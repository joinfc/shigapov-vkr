"""Telegram-бот «Помощник арендатора»"""

from tomllib import load

from telebot import TeleBot

with open("config.ini", mode="rb") as f:
    config = load(f)

bot = TeleBot(config["TOKEN"])
