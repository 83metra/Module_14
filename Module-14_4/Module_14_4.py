from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb = ReplyKeyboardMarkup(resize_keyboard=True)
# button1 = KeyboardButton(text='Рассчитать')
# button2 = KeyboardButton(text='Информация')
# button3 = KeyboardButton(text='Купить')
# kb.row(button1, button2).add(button3)

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать'),
         KeyboardButton(text='Информация'),
         ],
        [KeyboardButton(text='Купить'),
         ]
    ], resize_keyboard=True
)

buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт №1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт №2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт №3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт №4', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт №5', callback_data="product_buying")]
    ]
)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_in_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.row(button_in_1, button_in_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью. Кстати, курение вредит оному!', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию', reply_markup=kb_in)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(crud_functions.count_products()):
        with open(f'{i+1}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {crud_functions.get_all_products()[i][0]} |'
                                            f'Описание: {crud_functions.get_all_products()[i][1]} |'
                                            f'Цена: {crud_functions.get_all_products()[i][2]}')
    await message.answer(text='Выберите продукт для покупки:', reply_markup=buy_menu)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


# @dp.message_handler(text='Рассчитать')
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await call.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Мужчины: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'Женщины: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(text='Информация')
async def get_information(message):
    await message.answer('Для расчёта нормы калорий нужно ввести свой возраст, рост, вес и пол.\n'
                         'Расчёт ведётся по формуле Миффлина-Сан Жеора, выведенной в 2005 году\n'
                         'Иными словами сказала Татьяна Пельтцер в фильме "Вам и не снилось":'
                         '\t— А я тебе смолоду говорила: не жри много!')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    date = await state.get_data()
    await message.answer('Введите свой рост.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    date = await state.get_data()
    # await message.answer('Ваш рост {}'.format(date['growth']))
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight=message.text)
    date = await state.get_data()
    await message.answer('Введите свой пол (мужчина/женщина)')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def send_calories(message, state):
    await state.update_data(sex=message.text)
    date = await state.get_data()
    if 'му' in str(date['sex']).lower():
        result = (int(date['weight']) * 10) + (6.25 * int(date['growth'])) - (int(date['age']) + 5)
        await message.answer('Ваша норма калорий: %s' % (result))
    elif 'же' in str(date['sex']).lower():
        result = (int(date['weight']) * 10) + (6.25 * int(date['growth'])) - (int(date['age']) - 161)
        await message.answer('Ваша норма калорий: %s' % (result))
    else:
        await message.answer('В нашей стране только два пола — мужчина и женщина! Начните всё с начала!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
