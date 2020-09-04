# Telegram spamer by Oleg Sazonov
# Здесь идет ипморт необходимых функций для работы спамера
from telethon import TelegramClient, connection
from telethon.tl.functions.messages import ImportChatInviteRequest, SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import UserAlreadyParticipantError, FloodWaitError, ChatWriteForbiddenError, InviteHashExpiredError, ChannelInvalidError, ChannelPrivateError, ChannelsTooMuchError, InviteHashInvalidError, ChatAdminRequiredError, UsernameInvalidError, ChatRestrictedError, UsernameNotOccupiedError
from telethon.tl.types import InputPeerChannel, InputPeerChat
from asyncio import sleep
from glob import glob
from string import ascii_lowercase
from random import choice
# Открытие файлов с данными
chats = open("chats", "r")
id = open("id", "r")
text = open("text_of_message", "r")
# Инициализация переменных (выведены в начало, чтобы выделить память только в начале работы)
hash = []
spam_api_id = []
spam_api_hash = []
user_type = []
user_link = []
counter = 0
acc_count = 0

def randomString(stringLength=10):
    """Сгенерировать случайную строку определенной длины"""
    letters = ascii_lowercase
    return ''.join(choice(letters) for i in range(stringLength))

def build_data():
    # Здесь происходит сборка таблицы чатов и их идентификаторов
    for line in chats:
        if line.find("#", 0) != -1:
            continue
        if line.find("@") != -1:
            user_type.append(line.lstrip("@"))
            continue
        if line.find("joinchat") == -1:
            user_link.append(line.lstrip("https://t.me/"))
            continue
        tmp = line.lstrip('https://t.me/joinchat/')
        hash.append(tmp)
    for line in id:
        if line.find("#") != -1:
            continue
        tmp = line.split()
        spam_api_id.append(tmp[0])
        spam_api_hash.append(tmp[1])
    txt = ''
    for line in text:
        if line.find("#") == 0:
            continue
        txt += line
        txt += '\n'
    return txt
    



def login_as_user(api_id, api_hash, count, session='0'):
    # Функция для входа под видом пользователя (НЕ бота) в Telegram
    if session != '0':
        client = TelegramClient(session, spam_api_id[count], spam_api_hash[count])
        return client
    client = TelegramClient(randomString(3), spam_api_id[count], spam_api_hash[count], connection=connection.ConnectionTcpMTProxyRandomizedIntermediate, proxy=(host, port, sec))
    return client



async def main(client, session, acc_count, reklama, counter, user_type, user_link):
    # Главная функция рассылки
    me = await client.get_me()
    print("You are", me.first_name, me.last_name)
    for i in range(hash.__len__()):
        tmp = hash[i]
        tmp = tmp.rstrip()
        print("Sending to", tmp)
        try:
            # Здесь происходит рассылка и отлов ошибок
            await client(ImportChatInviteRequest(tmp))
        except UserAlreadyParticipantError:
            print("User already on channel")
        except InviteHashExpiredError:
            print("Ссылка на чат протухла, смотрите", i, "позицию")
            continue
        except InviteHashInvalidError:
            print("Битая ссылка на позиции", i)
            continue
        entity = await client.get_entity("https://t.me/joinchat/" + tmp)
        await client(SendMessageRequest(peer=InputPeerChannel(entity.id, entity.access_hash), message=reklama))
        await sleep(client.flood_sleep_threshold-10)
    for j in range(0, user_type.__len__()):
        tmp1 = user_type[j]
        print("Sending to ", tmp1)
        try:
            entity = await client.get_input_entity(tmp1)
        except UsernameInvalidError:
            print("Неправильное имя пользователя:", j)
            continue
        try:
            await client(JoinChannelRequest(entity))
        except ChannelsTooMuchError:
            print("Вы должны подчистить каналы на акке", me.username)
            return
        except ChannelInvalidError:
            print("Неправильный канал на позиции", j)
            continue
        except ChannelPrivateError:
            print("Канал закрыт на позиции", j)
            continue
        except ChatAdminRequiredError:
            print("На канал под номером", j, "мы не можем писать")
            continue
        try:
            await client(SendMessageRequest(peer=InputPeerChannel(entity.channel_id, entity.access_hash), message=reklama))
        except ChatWriteForbiddenError:
            print("Мы не можем писать туда:", j)
            continue
        except ChatAdminRequiredError:
            print("Мы не можем писать туда:", j)
            continue
        except ChatRestrictedError:
            print("Мы не можем писать туда:", j)
            continue
        await sleep(client.flood_sleep_threshold-10)
    for a in range(0, user_link.__len__()):
        tmp1 = user_link[a]
        print("Sending to:", tmp1)
        try:
            entity = await client.get_input_entity(tmp1)
        except UsernameInvalidError:
            print("Неправильное имя пользователя:", a)
            continue
        except ValueError:
            print("Нет такого пользователя", user_link[a])
            continue
        try:
            await client(JoinChannelRequest(entity))
        except ChannelsTooMuchError:
            print("Вы должны подчистить каналы на акке", me.username)
            return
        except ChannelInvalidError:
            print("Неправильный канал на позиции", a)
            continue
        except ChannelPrivateError:
            print("Канал закрыт на позиции", a)
            continue
        except ChatAdminRequiredError:
            print("На канал под номером", a, "мы не можем писать")
            continue
        try:
            await client(SendMessageRequest(peer=InputPeerChannel(entity.channel_id, entity.access_hash), message=reklama))
        except ChatWriteForbiddenError:
            print("Мы не можем писать туда:", a)
            continue
        except ChatAdminRequiredError:
            print("Мы не можем писать туда:", a)
            continue
        except ChatRestrictedError:
            print("Мы не можем писать туда:", a)
            continue
        await sleep(client.flood_sleep_threshold-10)

    return





reklama = build_data()

def launch():
    # Лаунчер главной функции (необходим для запуска в асинхронном режиме)
    session = glob("*.session")
    print("Добавляем новые сессии?(1 или 0):")
    if int(input()) == 1:
        print("Сколько(число):")
        i = int(input())
        for j in range(0, i):
            client = login_as_user(spam_api_id, spam_api_hash, counter)
            client.start()
            client.disconnect()
        with client:
            client.loop.run_until_complete(main(client, session, acc_count, reklama, counter, user_type, user_link))
            return
    client = login_as_user(spam_api_id, spam_api_hash, counter, session=session[0])
    with client:
        client.loop.run_until_complete(main(client, session, acc_count, reklama, counter, user_type, user_link))
        return

if __name__ == "__main__":
    # Входная точка
    launch()


