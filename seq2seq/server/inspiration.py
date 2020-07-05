import time
import random
import bdtrans
import cloudmusic
from ltp import LTP
from cloudmusic.api import Api
from advanced_quotes import topics, misc
from data.data_tool import remove_brackets
from data.augmentation.frequency import getFreqDist

pos = LTP()


def search_lyrics(api_instance, para_dict):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    param = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + \
            para_dict["string"] + '","type":"1006","offset":"0","total":"true","limit":"' + \
            para_dict["number"] + '","csrf_token":""}'
    return api_instance.send(url, param)


def test_lyrics(keyword, a=None):
    if a is None:
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


def gen_random_keywords():
    with open('../infer/Online_A.txt', encoding='utf-8-sig', mode='r') as f:
        lines = f.readlines()
        words_with_dup = []
        for line in lines:
            words, hidden = pos.seg([line.replace('\n', '')])
            words_pos = pos.pos(hidden)
            words = words[0]
            words_pos = words_pos[0]
            for i in range(len(words)):
                if len(words[i]) >= 2 and words_pos[i] in ['v', 'n']:
                    words_with_dup.append(words[i])
        freq_dist = getFreqDist(words_with_dup)
    return freq_dist


class Inspiration:
    random_keywords = []
    q_list = [
        "在想啥呢？",
        "有啥想法。。。？",
        "想说些什么吗？",
        "什么事？",
        "怎么了？",
        "不妨说说看？"
    ]
    a_list = []
    q = ""
    a = ""
    keyword = ""
    api = None

    def __init__(self):
        self.api = Api()
        self.a_list = []
        self.q_list = [
            "在想啥呢？",
            "有啥想法。。。？",
            "想说些什么吗？",
            "什么事？",
            "怎么了？",
            "不妨说说看？"
        ]
        self.a = ""
        self.q = random.choice(self.q_list)
        self.keyword = ""
        self.random_keywords = gen_random_keywords()

    def search_keyword(self, keyword=None):
        self.q = random.choice(self.q_list)
        if keyword is None:
            keyword = self.keyword
        assert len(keyword) > 0
        quotes_list = test_quotes(keyword)
        lyrics_list = test_lyrics(keyword, self.api)
        self.a_list = quotes_list + lyrics_list

    def select_reply(self, selected_index):
        self.q = random.choice(self.q_list)
        if len(self.a_list) > 0 and 0 <= selected_index < len(self.a_list):
            self.a = self.a_list[selected_index]
        else:
            self.a = ""

    def get_qa(self):
        self.q = random.choice(self.q_list)
        if len(self.a) == 0:
            if len(self.a_list) == 0:
                if len(self.random_keywords) == 0:
                    self.random_keywords = gen_random_keywords()
                self.search_keyword(random.choice(self.random_keywords))
            self.a = random.choice(self.a_list)
        return [self.q, self.a]


if __name__ == '__main__':
    print('start')
    Ins = Inspiration()
    print(Ins.get_qa())
