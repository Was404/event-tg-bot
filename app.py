from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN_API, ALLOWED_USER_IDS, ADMIN_ID
from strings import HELP_COMMAND, START_TEXT, DESCRIPTION, COUNT_ERROR
#from backend.main import result
#from backend.main import handle_variable
#from backend.additional_functions import find_all_names, ManufacorChoice, handle_variable2
import logging
from datetime import datetime
#from os import getenv

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

#logging.basicConfig(level=logging.INFO)
#Всякие переменные 
count = 0
number_of_inputs = 0
previous_message = '' # Переменная для хранения предыдущего сообщения
#list_manufacors = None
# Конец всяких переменных

""" КЛАВИАТУРА """
kb = ReplyKeyboardMarkup(resize_keyboard=True) # parameter one_time_keyboard def=False
btn1 = KeyboardButton('Описание')
btn2 = KeyboardButton('Помощь')
kb.add(btn1).add(btn2) # insert(кнопка) - для нов столбика 

ikb = InlineKeyboardMarkup()
ibtn_back = InlineKeyboardButton(text="Назад", callback_data="back_button") #Назад только один раз
ibtn_events = InlineKeyboardButton(text="Мероприятия", callback_data="events")
ikb.add(ibtn_events)

ikb_back_only = InlineKeyboardMarkup()
ill_come_back = InlineKeyboardButton(text= "Вернуться назад", callback_data="fuckgoback")
ikb_back_only.add(ill_come_back)
""" КОНЕЦ КЛАВИАТУРА """

async def on_startup(_):
    print("Стартуем!")


async def check_user_id(message: types.Message, ALLOWED_USER_IDS: list):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER_IDS:
        await message.answer("Привет, ты в списке! Вот список мероприятий...",reply_markup = types.ReplyKeyboardRemove()) #или другое сообщение
    else:
        await message.answer("Извини, тебя нет в списке.",reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global previous_message
    await message.answer(text= START_TEXT, parse_mode="HTML", reply_markup = ikb) # написать
    previous_message = message.text
    #await message.delete() # удоли сообщение пользователя
        
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    global previous_message
    await message.answer(HELP_COMMAND) # ответить
    previous_message = message.text
    
@dp.message_handler(text = 'Помощь')
async def help_command(message: types.Message):
    global previous_message
    await message.answer(HELP_COMMAND, reply_markup=ikb_back_only) # ответить
    previous_message = message.text
    await message.delete()
        
@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    global previous_message 
    await message.answer(DESCRIPTION)
    previous_message = message.text
    
@dp.message_handler(text = 'Описание')
async def help_command(message: types.Message):
    await message.answer(DESCRIPTION, reply_markup=ikb_back_only) # ответить
    await message.delete()     

@dp.message_handler(text = 'Пенис')
async def sticker_giver(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJ9exk0oa87s2dqdLDTO0j6_g3tyYDbgAC1AsAAg74eUlJg1T3YVm93jAE")
   

@dp.message_handler(commands=['photo'])
async def send_penis(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo="https://cdn-icons-png.flaticon.com/512/6147/6147668.png")
    

@dp.message_handler()
async def interception(message: types.Message):
    global number_of_inputs
    global previous_message
    if message.text.count(' ') >= 1:
        previous_message = message.text
        await message.answer(message.text, reply_markup=ikb_back_only)
    else:
        await message.answer(text = COUNT_ERROR, parse_mode="HTML", reply_markup=kb)
        number_of_inputs +=1
        if number_of_inputs > 2:
            await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJ9exk0oa87s2dqdLDTO0j6_g3tyYDbgAC1AsAAg74eUlJg1T3YVm93jAE")
            number_of_inputs = 0
    

@dp.callback_query_handler(text='back_button')
async def back_button_handler(query: types.CallbackQuery):
    global previous_message

    # Отправляем предыдущее сообщение
    if previous_message:
        await query.message.bot.send_message(query.from_user.id, previous_message)
        previous_message = ''

    # Удаляем кнопку
    await query.message.delete()  

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'fuckgoback')
async def back_back_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text= START_TEXT, parse_mode="HTML", reply_markup = ikb)      


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'events')
async def process_events_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await check_user_id(callback_query.message, ALLOWED_USER_IDS)


current_time = datetime.now()
formatted_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(),
        ],
    )
logging.debug('Старт программы')

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
