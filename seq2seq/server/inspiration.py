from cloudmusic.api import Api


def search(api_instance, para_dict):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    param = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + \
            para_dict["string"] + '","type":"1006","offset":"0","total":"true","limit":"' + \
            para_dict["number"] + '","csrf_token":""}'
    return api_instance.send(url, param)


if __name__ == '__main__':
    A = Api()
    para = {"string": "平安夜", "number": "10"}
    r = search(A, para)
    print(r)
