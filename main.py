import config
import asyncio
from youtube import Youtube
from aiogram import Bot, Dispatcher, types, executor
from database import DataBase
import json
import video

db = DataBase('database.db')
bot = Bot(config.TGtoken)
disp = Dispatcher(bot)
commands_list = {'/help', '/start'}
channel_id = 'UCWxQrOSmSwCp8MRAWe2pJ-g'


@disp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id,
                           "Добро пожаловать, {0.first_name}!\n Чтобы получить список доступных команд введите /help".format(
                               message.from_user, await bot.get_me()),
                           parse_mode='html')


@disp.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.chat.id,
                           'Доступные команды:\n'
                           '• /help — список доступных команд\n'
                           '• /subscribe — подписаться на рассылку \n'
                           '• /unsubscribe — отписаться от рассылки \n')


@disp.message_handler(commands=['subscribe'])
async def subscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)
    await bot.send_message(message.chat.id, 'Вы успешно подписались!')


@disp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        await bot.send_message(message.chat.id, 'Вы не подписаны!')
    else:
        db.update_subscription(message.from_user.id, False)
        await bot.send_message(message.chat.id, 'Вы успешно отписались от рассылки!')


@disp.message_handler(lambda message: message.text not in commands_list and message.text[0] == '/')
async def error_allert(message: types.Message):
    await message.answer("Вы ввели неверную команду.\n"
                         "Воспользуйтесь /help для получения списка доступных команд.")


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


if __name__ == '__main__':
    disp.loop.create_task(scheduled(10))
    executor.start_polling(disp, skip_updates=True)
