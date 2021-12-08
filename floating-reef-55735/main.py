from spotify import Song
import telepot
import spotify
import requests
import threading

token = '5008674339:AAGEWlU0Qn5ZKFeu4P1SoEkOSEpUG7YTq4E'
bot = telepot.Bot(token)

sort = {}


def txtfinder(txt):
    a = txt.find("https://open.spotify.com")
    txt = txt[a:]
    return txt


def downloader(link, chat_id, type):
    if type == 'AL':
        ITEMS = spotify.album(link)
    elif type == 'AR':
        ITEMS = spotify.artist(link)
    elif type == 'PL':
        ITEMS = spotify.playlist(link)
    else:
        ITEMS = []

    MESSAGE = ""
    COUNT = 0
    for song in ITEMS:
        if type == 'PL':
            song = song['آهنگ']
        COUNT += 1
        MESSAGE += f"{COUNT}. {song['name']}\n"
    bot.sendMessage(chat_id, MESSAGE)

    for song in ITEMS:
        if type == 'PL':
            song = song['track']

        Song(song['href'], chat_id).Telegram()


def START(msg, chat_id):
    print(f"{chat_id}:{msg}")
    msglink = txtfinder(msg)
    if msglink[:30] == ('https://open.spotify.com/album'):
        downloader(msg, chat_id, 'AL')

    elif msglink[:30] == ('https://open.spotify.com/track'):
        Song(msg, chat_id).Telegram()

    elif msg[:33] == 'https://open.spotify.com/playlist':
        downloader(msg, chat_id, 'PL')

    elif msglink[:31] == ('https://open.spotify.com/artist'):
        downloader(msg, chat_id, 'AR')

    elif msg == "/start":
        bot.sendMessage(chat_id,
                        "سلام \nبمن لینک اهنگ اسپاتیفای را ارسال کن\nیا /single یا /album یا /artist")


    elif msg == "/album":
        sort[chat_id] = 'album'
        bot.sendMessage(chat_id,
                        'اسم خواننده هارا به این صورت ارسال کن ای مفت خور: \nName album\nor for better search use this:\nName album - Name artist')

    elif msg == '/single':
        sort[chat_id] = 'single'
        bot.sendMessage(chat_id,
                        'اسم خواننده هارا به این صورت ارسال کن ای مفت خور: \nName song\nor for better search use this:\nName song - Name artist')
    elif msg == '/artist':
        sort[chat_id] = 'artist'
        bot.sendMessage(chat_id, 'اسم خواننده هارا به این صورت ارسال کن ای مفت خور: \nName artist')

    else:
        if chat_id in sort:
            try:
                if sort[chat_id] == 'artist':
                    downloader(spotify.searchartist(msg), chat_id, 'AR')
                elif sort[chat_id] == 'album':
                    downloader(spotify.searchalbum(msg), chat_id, 'AL')
                elif sort[chat_id] == 'single':
                    Song(spotify.searchsingle(msg), chat_id).Telegram()

                del sort[chat_id]

            except:
                bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
                bot.sendMessage(chat_id, "نتواستیم دانلود کنیم")

        else:
            bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
            bot.sendMessage(chat_id, 'لینک بفرست یا یا use /single یا /album یا /artist')


print('بگوشین.....')

tokenurl = f'https://api.telegram.org/bot{token}'
Update = tokenurl + "/getUpdates"


def UPDATE():
    MESSAGES = requests.get(Update).json()
    return MESSAGES['result']


while 1:
    if threading.activeCount() - 1 < 15:
        try:
            for message in UPDATE():
                offset = message['update_id'] + 1
                offset = Update + f"?offset={offset}"
                offset = requests.post(offset)
                msg = message['message']['text']
                chat_id = message['message']['from']['id']
                thread = threading.Thread(target=START, args=(msg, chat_id))
                thread.start()
        except:
            pass
