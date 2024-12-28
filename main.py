import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parser import ItemParser
from service import Database
from configparser import ConfigParser
from creds import headers, cookies
config = ConfigParser()
config.read('./config.ini')

BOT_TOKEN = config["Telegram"]["bot_token"]
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация парсера и базы данных
url = 'https://sc-tech-solutions.itsm.mos.ru'
params = {}  # Добавь параметры
parser = ItemParser(url+'/inbox', params, cookies, headers)
db = Database()

# Функция для проверки новых элементов или изменения статусов

async def notify_new_items():
    new_items = parser.get_unread_items()
    if new_items:
        subscribers = db.get_subscribers()  # Получаем всех подписчиков
        if subscribers:
            for item in new_items:
                message = f'Запрос обновлен или новый запрос: {item["subject"]}\nID: {item["id"]}\nЗапросил: {item["requester"]}\nСтатус: {item["status"]}\n\n <a href="{url+item["href"]}">Перейти</a>'
                for user_id in subscribers:
                    try:
                        await bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.HTML)
                    except Exception as e:
                        ...

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    user_id = message.from_user.id
    db.add_subscriber(user_id)
    await message.reply("Вы подписаны на уведомления о новых сообщениях.")

# Команда для отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user_id = message.from_user.id
    db.remove_subscriber(user_id)
    await message.reply("Вы отписались от уведомлений.")
    
@dp.message_handler(commands=['test'])
async def unsubscribe(message: types.Message):
    await message.reply("работает")

async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_new_items, 'interval', seconds=15)  # Проверяем каждые 30 секунд
    scheduler.start()

async def main():
    await start_scheduler()
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
