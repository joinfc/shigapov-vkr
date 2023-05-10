import gspread
from telebot import types
from telebot.util import quick_markup

from bot import bot, config


def start_cmd(message: types.Message) -> None:
    """Начинаем работу с пользователем"""
    bot.reply_to(message, "Hello")


def payment_cmd(message: types.Message) -> None:
    """Добавление оплаты"""
    client = gspread.service_account(config["SERVICE_ACCOUNT_KEY"])
    sheet = client.open_by_key(config["SHEET"])
    worksheet = sheet.worksheet("Аренда")
    payers = {}
    for i in range(2, worksheet.row_count + 1):
        car = worksheet.cell(i, 1).value
        tenant = worksheet.cell(i, 2).value
        if not car and not tenant:
            break
        payers[f"{tenant} - {car}"] = {
            "callback_data": f"{tenant} - {car}",
        }
    payers = quick_markup(payers)
    bot.send_message(message.chat.id, "Выберите плательщика:", reply_markup=payers)


def payer_call(query: types.CallbackQuery) -> None:
    """Выбор плательщика"""
    bot.answer_callback_query(query.id)
    msg = query.message
    print("DEBUG", query.data)
    bot.edit_message_text(
        f"Выберите плательщика: {query.data}",
        msg.chat.id, msg.id,
        reply_markup=None
    )
    bot.send_message(msg.chat.id, "Введите дату оплаты (ДД-ММ-ГГ):")
    bot.register_next_step_handler(msg, payment_date_cmd)


def payment_date_cmd(message: types.Message) -> None:
    """"""
    print("DEBUG", message.text)
