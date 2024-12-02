from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton(text='Расчитать')
button_info = KeyboardButton(text='Информация')
kb.row(button_calculate, button_info)

kb_inl = InlineKeyboardMarkup(resize_keyboard=True)
button_inl_cul = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inl_info = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inl.row(button_inl_cul, button_inl_info)


@dp.message_handler(text=['Расчитать'])
async def main_menu(msg):
    await msg.answer('Выберите опцию:', reply_markup=kb_inl)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст : ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(msg, state):
    await state.update_data(age=msg.text)
    data = await state.get_data()
    await msg.answer('Введите свой рост : ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(msg, state):
    await state.update_data(growth=msg.text)
    data = await state.get_data()
    await msg.answer('Введите свой вес : ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(msg, state):
    await state.update_data(weight=msg.text)
    data = await state.get_data()
    caloris = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await msg.answer(f' Ваша норма калорий {caloris:.2f} ')
    await state.finish()


@dp.message_handler(text=['Привет', 'привет', 'Hi', 'hi', 'Хай', 'хай'])
async def urban_messsge(msg):
    await msg.answer('Рады вас видеть в нашем боте !')


@dp.message_handler(commands=['start'])
async def start_message(msg: types.Message):
    await msg.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(msg):
    await msg.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
