"""Главный файл"""

from telebot import types

import commands
from bot import bot


def register_handlers() -> None:
    bot.register_message_handler(commands.start_cmd, commands=["start"])
    bot.register_message_handler(commands.payment_cmd, commands=["payment"])
    bot.register_callback_query_handler(commands.payer_call, func=lambda _: True)
    bot.set_my_commands([
        types.BotCommand("start", "Начать общение"),
        types.BotCommand("payment", "Добавить оплату"),
    ])


def lambda_handler(event: dict, _context: dict) -> dict:
    """Точка входа в Yandex Cloud Functions (AWS Lambda)"""
    register_handlers()
    update = types.Update.de_json(event["body"])
    if update:
        bot.process_new_updates([update])
    return {"statusCode": 200}


def main() -> None:
    """Точка входа для разработки"""
    register_handlers()
    bot.infinity_polling()


if __name__ == "__main__":
    main()
