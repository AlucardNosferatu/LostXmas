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


def test_lyrics(keyword, a=None, limit=2):
    if a is None:
        a = Api()
    if len(keyword.strip()) == 0:
        keyword = "你"
    para = {"string": keyword, "number": "100"}
    r = search_lyrics(a, para)
    lyrics_list = []
    while len(lyrics_list) < limit:
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


def search_quotes(keyword, limit=2):
    if " " in keyword or len(keyword) == 0:
        keywords = keyword.split(' ')
        i = 0
        while i < len(keywords):
            if len(keywords[i]) < 1:
                del keywords[i]
            else:
                i += 1
        keyword = max(keywords, key=len, default="you")
    t = topics.Topic(misc.toUUID(keyword))
    q = []
    try:
        q_list = t.quotes(1)['elements']
        print("Topic fetched")
    except Exception as e:
        print(repr(e))
        return q
    time.sleep(1)
    while len(q) < limit:
        print("Current length of q_list: ", len(q))
        choice = random.choice(range(len(q_list)))
        q_temp = q_list[choice]
        while q_temp.UUID.startswith("/"):
            choice = random.choice(range(len(q_list)))
            q_temp = q_list[choice]
        try:
            q_temp = q_temp.snippet()['body']
        except Exception as e:
            print(repr(e))
            continue
        if len(q_temp.split(' ')) < 20:
            q.append(q_temp)
    return q


def test_quotes(keyword, limit=2):
    keyword = bdtrans.trans(keyword, 'zh', 'en')
    print("Keyword translated")
    quote_list = search_quotes(keyword, limit=limit)
    print("Quotes fetched.")
    for i in range(len(quote_list)):
        quote_list[i] = bdtrans.trans(quote_list[i], 'en', 'zh')
        time.sleep(1)
    return quote_list


def gen_random_keywords(base_dir='../'):
    with open(base_dir + 'infer/Online_A.txt', encoding='utf-8-sig', mode='r') as f:
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
    base_dir = "../"
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
    limit = 0

    def __init__(self, limit=2, base_dir="../"):
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
        self.base_dir = base_dir
        self.random_keywords = gen_random_keywords(base_dir=base_dir)
        self.limit = limit

    def search_keyword(self, keyword=None):
        self.q = random.choice(self.q_list)
        if keyword is None:
            keyword = self.keyword
        try:
            assert len(keyword) > 0
        except AssertionError:
            keyword = " "
        quotes_list = test_quotes(keyword, limit=self.limit)
        print("Quotes searched.")
        lyrics_list = test_lyrics(keyword, self.api, limit=self.limit)
        print("Lyrics searched.")
        self.a_list = quotes_list + lyrics_list
        return self.a_list

    def select_reply(self, selected_index):
        self.q = random.choice(self.q_list)
        if len(self.a_list) > 0 and 0 <= selected_index < len(self.a_list):
            self.a = self.a_list[selected_index]
        else:
            self.a = ""
        return self.a

    def get_qa(self, q_index=None):
        if type(q_index) is int and q_index in range(len(self.q_list)):
            self.q = self.q_list[q_index]
        if len(self.q) == 0:
            self.q = random.choice(self.q_list)
        if len(self.a) == 0:
            if len(self.a_list) == 0:
                if len(self.random_keywords) == 0:
                    self.random_keywords = gen_random_keywords(base_dir=self.base_dir)
                self.search_keyword(random.choice(self.random_keywords))
            self.a = random.choice(self.a_list)
        return [self.q, self.a]


if __name__ == '__main__':
    print('start')
    Ins = Inspiration()
    print(Ins.get_qa())
