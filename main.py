import config
import asyncio
# Модуль для парсинга видео с канала
from youtube import Youtube
# Модуль для работы с TG Bot API
from aiogram import Bot, Dispatcher, types, executor
# Модуль для работы с базой данных
from database import DataBase
# Модуль для работы с файлами данных, где хранятся ссылки
import json
# Модуль для парсинга названия нового видео
import video

# Объявляем БД
db = DataBase('database.db')
# Объявляем бота
bot = Bot(config.TGtoken)
# Объявляем диспетчера, для обработки обновлений
disp = Dispatcher(bot)
# Доступные команды
commands_list = {'/help', '/start'}
# ID канала, в нашем случае MediaSoft
channel_id = 'UCWxQrOSmSwCp8MRAWe2pJ-g'


# Метод обработки команды /start, выводит привественное сообщение
@disp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id,
                           "Добро пожаловать, {0.first_name}!\n "
                           "Данный бот создан для рассылки новых видео с канала MediaSoft\n"
                           "Чтобы получить список доступных команд введите /help".format(
                               message.from_user, await bot.get_me()),
                           parse_mode='html')


# Метод обработки команды /help, выводит все доступные команды
@disp.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.chat.id,
                           'Доступные команды:\n'
                           '• /help — список доступных команд\n'
                           '• /subscribe — подписаться на рассылку \n'
                           '• /unsubscribe — отписаться от рассылки \n')


# Метод обработки /subscribe, подписывает на рассылку юзера
@disp.message_handler(commands=['subscribe'])
async def subscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)
    await bot.send_message(message.chat.id, 'Вы успешно подписались!')


# Метод обработки /unsubscribe, отписывает от рассылки юзера
@disp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        await bot.send_message(message.chat.id, 'Вы не подписаны!')
    else:
        db.update_subscription(message.from_user.id, False)
        await bot.send_message(message.chat.id, 'Вы успешно отписались от рассылки!')


# Метод обработки команды, которые не были заданы в боте, выводит соотвествующее сообщение о ошибке
@disp.message_handler(lambda message: message.text not in commands_list and message.text[0] == '/')
async def error_allert(message: types.Message):
    await message.answer("Вы ввели неверную команду.\n"
                         "Воспользуйтесь /help для получения списка доступных команд.")


# Метод для проверки нового видео на канале, срабатывает раз в 2 минуты
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        with open('data.json', 'r') as data_file:
            json_data = data_file.read()
        video_links = json.loads(json_data)

        video_links1 = Youtube.get_all_video_in_channel(channel_id)
        subscriptions = db.get_subscriptions()

        if video_links1[0] != video_links[0]:
            for s in subscriptions:
                vd = video.vid_info(video_links1[0])
                await bot.send_message(s[1], vd['title'] + "\n" + video_links1[0],
                                       disable_notification=True)
        video_links = video_links1


# Запуск лонгполинга
if __name__ == '__main__':
    disp.loop.create_task(scheduled(120))
    executor.start_polling(disp, skip_updates=True)
