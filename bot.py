import asyncio
import json
import logging

import requests


from aiogram import Bot, Dispatcher, types



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="")
# Диспетчер
dp = Dispatcher(bot)


def random_yes_or_no():
    url = "https://yesno.wtf/api"
    headers = {'content-type': 'application/json', "charset":"UTF-8"}
    rnd = requests.get(url=url, headers=headers)
    response_random = json.loads(rnd.content)
    return response_random
    print(response)


def forced_yes():
    url = "https://yesno.wtf/api"
    headers = {'content-type': 'application/json', "charset":"UTF-8"}
    body = {"forced":"yes"}
    rnd = requests.get(url=url, headers=headers, params={"force":"yes"})
    response_yes = json.loads(rnd.content)
    return response_yes
    print(response)


def forced_no():
    url = "https://yesno.wtf/api"
    headers = {'content-type': 'application/json', "charset":"UTF-8"}
    body = {"forced":"yes"}
    rnd = requests.get(url=url, headers=headers, params={"force":"no"})
    response_no = json.loads(rnd.content)
    return response_no
    print(response)

async def show_menu(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    YES_BUTTON = types.InlineKeyboardButton(text="Да", callback_data="yes")
    NO_BUTTON = types.InlineKeyboardButton(text="Нет", callback_data="no")
    RANDOM_BUTTON = types.InlineKeyboardButton(text="Рандом", callback_data="random")
    markup.add(YES_BUTTON, NO_BUTTON, RANDOM_BUTTON)
    await message.answer("Выбери свой ответ.", reply_markup=markup)

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, "Привет. Я помогу тебе ответить на вопрос: Да или Нет?")
    await show_menu(message)


async def ans_yes(message: types.Message):
    data = forced_yes()
    await bot.send_video(message.chat.id, f"{data['image']}", caption="Да")
    await bot.send_message(message.chat.id, "Каков твой следующий ответ?")



async def ans_no(message: types.Message):
    data = forced_no()
    if data["answer"] == "no":
        await bot.send_video(message.chat.id, f"{data['image']}", caption="Нет")
        await bot.send_message(message.chat.id, "Каков твой следующий ответ?")



async def ans_random(message: types.Message):
    data = random_yes_or_no()
    if data["answer"] == "yes":
        await bot.send_video(message.chat.id, f"{data['image']}", caption="Да")
        await bot.send_message(message.chat.id, "Каков твой следующий ответ?")
    elif data["answer"] == "no":
        await bot.send_video(message.chat.id, f"{data['image']}", caption="Нет")
        await bot.send_message(message.chat.id, "Каков твой следующий ответ?")
    else:
        await bot.send_video(message.chat.id, f"{data['image']}", caption="Может быть")
        await bot.send_message(message.chat.id, "Каков твой следующий ответ?")


@dp.callback_query_handler(lambda call: True)
async def callback_handler(call):
    if call.data == "yes":
        await ans_yes(call.message)
        await show_menu(call.message)
    elif call.data == "no":
        await ans_no(call.message)

        await show_menu(call.message)
    elif call.data == "random":
        await ans_random(call.message)
        await show_menu(call.message)




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
