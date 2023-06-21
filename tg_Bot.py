from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import  Text
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold,hlink
from main import collect_data
import json
import time




storage=MemoryStorage()
API_TOKEN='6056634354:AAHggnftQx9m9NkgAQ3lAa1K_zvtyAF8FCM'
bot= Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp=Dispatcher(bot=bot,storage=storage)


class ClientStatesGroup(StatesGroup):
    min_price=State()
    max_price=State()
    discount=State()




@dp.message_handler(commands='start')
async def start(message:types.Message):
    await ClientStatesGroup.min_price.set()
    await message.answer('Введите минимальную цену')

@dp.message_handler(state=ClientStatesGroup.min_price)
async def min_price(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['min_price']=message.text
    await ClientStatesGroup.next()
    await message.answer('Введите максимальную цену')

@dp.message_handler(state=ClientStatesGroup.max_price)
async def min_price(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['max_price']=message.text
    await ClientStatesGroup.next()
    await message.answer('Введите желаемую скидку')

@dp.message_handler(state=ClientStatesGroup.discount)
async def min_price(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['discount']=message.text
        await message.answer('Please waiting...')
        await bot.send_chat_action(message.chat.id, 'typing')

        collect_data(data['min_price'],data['max_price'],int(data['discount']))

        with open('result.json') as file:
            result=json.load(file)

        for index,item in enumerate(result):
            card = f"{hlink(item.get('full_name'),item.get('3d'))}\n" \
                f"{hbold('Скидка:')}{int(item.get('discount'))}%\n" \
                f"{hbold('Цена:')}${int(item.get('price'))}\n" \
                f"_____________________________________________________"

            if index%20==0:
                time.sleep(5)

            await message.answer(card)
            await state.reset_state()


executor.start_polling(dp,skip_updates=True)

