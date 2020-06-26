import itchat
import _thread
import time
wechat_login=False

def start():
    global wechat_login
    if(wechat_login):
        pass
    else:
        itchat.auto_login(hotReload=True)
        _thread.start_new_thread(itchat.run, ())
        time.sleep(0.5)#保证run已经开始运行
        wechat_login=True

def send(str):
    if(wechat_login):
        pass
    else:
        start()
    mps = itchat.get_mps()
    for each in mps:
        if each.NickName=="小冰":
            xiaoice=each
            break;
    xiaoice.send(str)
    