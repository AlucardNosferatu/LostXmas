from cloudmusic.api import Api
from advanced_quotes import topics, misc, quotes
import bdtrans
import cloudmusic


def search_lyrics(api_instance, para_dict):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    param = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + \
            para_dict["string"] + '","type":"1006","offset":"0","total":"true","limit":"' + \
            para_dict["number"] + '","csrf_token":""}'
    return api_instance.send(url, param)[0]


def test_lyrics():
    A = Api()
    keyword = '平安夜'
    para = {"string": keyword, "number": "10"}
    r = search_lyrics(A, para)
    music = cloudmusic.getMusic(r)
    r = music.getLyrics()
    r = r[0].split('\n')
    for each in r:
        if keyword in each:
            r = each[11:]
            break
    print(r)


def search_quotes(keyword):
    t = topics.Topic(misc.toUUID(keyword))
    try:
        q = t.quotes(1)['elements']
        q = q[0]
    except ValueError as e:
        print(repr(e))
        q = quotes.random()
    q = q.snippet()
    q = q['body']
    return q


def test_quotes():
    keyword = bdtrans.trans('爱', 'zh', 'en')
    quote = search_quotes(keyword)
    quote = bdtrans.trans(quote, 'en', 'zh')
    print(quote)


if __name__ == '__main__':
    print('start')
    test_lyrics()