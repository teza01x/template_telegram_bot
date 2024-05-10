import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from async_sql_scripts import *
from async_markdownv2 import *
from text_scripts import *
from config import *


bot = AsyncTeleBot(telegram_token)


@bot.message_handler(commands=['start', 'menu'])
async def start(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        if not await check_user_exists(user_id):
            try:
                await add_user_to_db(user_id, username)
            except Exception as error:
                print(f"Error adding user to db error:\n{error}")
        else:
            await update_username(user_id, username)

        text = await escape(dictionary['start_msg'], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("Button 1", callback_data="callback_1"),
            types.InlineKeyboardButton("Button 2", callback_data="callback_2"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])


        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

        await change_menu_status(user_id, start_menu_status)

    except Exception as e:
        print(f"Error in start message: {e}")



async def run_services():
    try:
        bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=500))
        await asyncio.gather(bot_task)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_services())
    loop.run_forever()
