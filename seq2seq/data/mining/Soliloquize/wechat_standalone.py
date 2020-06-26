# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 21:50:38 2018

@author: Scrooge
"""

import itchat
import talk
import time
import datetime

now_time = datetime.datetime.now()

now_str = datetime.datetime.strftime(now_time,'%Y-%m-%d-%H-%M-%S')

filename = now_str+".txt"

rounds = 0


@itchat.msg_register(itchat.content.TEXT,isMpChat=True)
def simple_reply(msg):
    if len(msg['FromUserName'])<49:
                f = open(filename,'a')
                print(msg['Text'])
                f.writelines(msg['Text']+'\n')
                fromTL=talk.talk(msg['Text'])
                print(fromTL)
                f.writelines(fromTL+'\n')
                f.close()
                time.sleep(5)
                itchat.send(fromTL,toUserName=msg['FromUserName'])

                
itchat.auto_login()
itchat.run()
#xiaoice=itchat.search_mps(name='小冰')



#itchat.send(talk.talk("今天开心吗"),toUserName='@6b3fb613fa6481e46c36b8ce7d86e1ab')
