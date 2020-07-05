from cloudmusic.api import Api
from advanced_quotes import topics, misc, quotes
import bdtrans
import cloudmusic
import random
import time

from data.data_tool import remove_brackets


def search_lyrics(api_instance, para_dict):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    param = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + \
            para_dict["string"] + '","type":"1006","offset":"0","total":"true","limit":"' + \
            para_dict["number"] + '","csrf_token":""}'
    return api_instance.send(url, param)


def test_lyrics(keyword):
    a = Api()
    para = {"string": keyword, "number": "100"}
    r = search_lyrics(a, para)
    lyrics_list = []
    while len(lyrics_list) < 2:
        choice = random.choice(range(len(r)))
        music = cloudmusic.getMusic(r[choice])
        lyrics = music.getLyrics()
        lyrics = lyrics[0].split('\n')
        for each in lyrics:
            if keyword in each and len(each.replace(keyword, '')) > 4:
                lyrics_list.append(each)
                break
    lyrics_list = remove_brackets(lyrics_list)
    lyrics_list = [item.strip() for item in lyrics_list]
    return lyrics_list


def search_quotes(keyword):
    t = topics.Topic(misc.toUUID(keyword))
    q = []
    q_list = t.quotes(1)['elements']
    while len(q) < 2:
        try:
            choice = random.choice(range(len(q_list)))
            q_temp = q_list[choice]
            while q_temp.UUID.startswith("/"):
                choice = random.choice(range(len(q_list)))
                q_temp = q_list[choice]
            q_temp = q_temp.snippet()['body']
        except ValueError:
            continue
        if len(q_temp.split(' ')) < 20:
            q.append(q_temp)
    return q


def test_quotes(keyword):
    keyword = bdtrans.trans(keyword, 'zh', 'en')
    quote_list = search_quotes(keyword)
    for i in range(len(quote_list)):
        quote_list[i] = bdtrans.trans(quote_list[i], 'en', 'zh')
        time.sleep(1)
    return quote_list


if __name__ == '__main__':
    print('start')
    searched = "开始"
    ql = test_quotes(searched)
    ll = test_lyrics(searched)
    result = ql + ll
    print(result)
