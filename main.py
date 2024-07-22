import random
import time
import telebot
import threading
from youtubesearchpython import *



def masToken():
    f = open('token.txt', 'r+', encoding="utf8")
    mas_token = []
    for i in f:
        if ('\n' in i):
            i = i.replace('\n', '')
        mas_token.append(i)
    return mas_token


mas_tokens=masToken()
token = mas_tokens[0]
id_channel = mas_tokens[1]
bot = telebot.TeleBot(token)

channel_id_youtube = "UCt7sv-NKh44rHAEb-qCCxvA"
back_post_id = []
ids_videos=[]
name_youtube = mas_tokens[2]



channelsSearch = ChannelsSearch(str(name_youtube), limit=30)
for i in channelsSearch.result()['result']:
    if (i['subscribers'] == name_youtube):
        print(i['subscribers'])
        channel_id_youtube = i['id']



@bot.message_handler(commands=["change"])
def get_user_change(message):
    bot.send_message(message.chat.id,"Напиши id канала начиная c @")
    bot.register_next_step_handler(message,commands)



def commands(message):
    # bot.send_message(channel_id, "Hello")
    if(message.text[0]=='@'):
        bot.send_message(message.chat.id, "Сохранил Канал")
        global name_youtube
        name_youtube = message.text
        channelsSearch = ChannelsSearch(str(message.text), limit=30)
        global channel_id_youtube
        for i in channelsSearch.result()['result']:
            if (i['subscribers'] == message.text):
                print(i['subscribers'])
                channel_id_youtube = i['id']
        print(channel_id_youtube)
        bot.send_message(message.chat.id, "Начинаю отслеживать")

    else:
        bot.send_message(message.chat.id, "Возникла ошибка проверьте правильность id должен начинаться с @")


def cycle():
    while True:
        try:
            post_text = post()
            global back_post_id,ids_videos

            for i in post_text:
                back_post_id.append(i[1])
                bot.send_message(id_channel, i[0])
                #print(back_post_id)
            print(back_post_id)
            if (len(back_post_id) > 15):
                back_post_id = back_post_id[1:]
            if (len(ids_videos) > 15):
                ids_videos = ids_videos[1:]

        except:
            pass
        time.sleep(random.randint(10,30))


def S_in_lists(playlist):
    mas = []
    for i in playlist.videos:
        id = i['id']
        title = i['title']
        accessibility = i['accessibility']['title']
        time = i['duration']
        link = i['link']
        if time == None and not("No views" in accessibility):
            if(not(id in ids_videos) and not(id in back_post_id)):
                ids_videos.append(id)
                mas.append([f"Трансляция идёт\n{title}\n\n{link}", id])

    return mas


def post():
    playlist = Playlist(playlist_from_channel_id(channel_id_youtube))
    mas=[]
    try:
        mas = S_in_lists(playlist)
        while playlist.hasMoreVideos:
            playlist.getNextVideos()
            mas += S_in_lists(playlist)
    except:
        pass
    return mas

rT = threading.Thread(target=cycle)
try:
    rT.join()
except:
    pass
rT.start()


try:
    bot.polling()
except Exception as e:
    print(e)
    time.sleep(1000)
    try:
        bot.polling()
    except Exception as e:
        print(e)
