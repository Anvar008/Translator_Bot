import asyncio

from googletrans import Translator
from aiogram import Dispatcher, Bot, filters, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


translator1 = Translator()
bot = Bot(token="7020661438:AAEerWTPx-X78-idfXXvCeEvKl3E2wEvY94")
dp = Dispatcher(bot=bot)

keyboard1 = [
    [KeyboardButton(text="uz"), KeyboardButton(text="en")],
    [KeyboardButton(text="Ввести другое слово")]
]
main_button = ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)


class Text_for(StatesGroup):
    text1 = State()
    lang1 = State()


@dp.message(filters.Command("start"))
async def start_function(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать")
    await state.set_state(Text_for.text1)
    await message.answer("Введите текст чтоб я перевел: ")


@dp.message(Text_for.text1)
async def translate_text(message: types.Message, state: FSMContext):
    await state.update_data(text1=message.text)
    await state.set_state(Text_for.lang1)
    await message.answer("Выберите язык для перевода: ", reply_markup=main_button)


@dp.message(Text_for.lang1)
async def translate_text(message: types.Message, state: FSMContext):
    await state.update_data(lang1=message.text)
    data = await state.get_data()
    text1 = data.get("text1")
    lang1 = data.get("lang1")
    if text1 and lang1:
        text2 = translator1.translate(text=text1, dest=lang1)
    await message.answer(text2.text)


@dp.message(F.text == "Ввести другое слово")
async def yengi_soz(message: types.Message, state: FSMContext):
    await state.update_data(text1=message.text)
    await message.answer("Выберите язык", reply_markup=main_button)


@dp.message(F.text == "Выберите язык")
async def boshqa_til(message: types.Message, state: FSMContext):
    await state.update_data(lang1=message.text)
    data = await state.get_data()
    text1 = data.get("text1")
    lang1 = data.get("lang1")
    if text1 and lang1:
        text2 = translator1.translate(text=text1, dest=lang1)
    await message.answer(text2.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
