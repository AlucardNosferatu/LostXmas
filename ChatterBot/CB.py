from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
from tqdm import tqdm
import os
import sys
import jieba

bot = ChatBot("Proto",
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              logic_adapters=['chatterbot.logic.BestMatch'],
              database_uri='sqlite:///database.sqlite3')
rootPath = os.path.dirname(sys.path[0])
os.chdir(rootPath)

FILENAME = 'seq2seq\\word\\data\\conv_zh.txt'

# c_trainer = ChatterBotCorpusTrainer(bot)
# trainer = ListTrainer(bot)
# c_trainer.train("chatterbot.corpus.chinese")
#
# conversation_list = open(FILENAME, encoding='UTF-8').read().split('\n')
# for i in tqdm(range(0, len(conversation_list)//2)):
#     conversation = [conversation_list[i], conversation_list[i+1]]
#     trainer.train(conversation)

raw_str = "我感觉饥饿"
cut_str = jieba.lcut(raw_str)
temp_str = ''
for each in cut_str:
    temp_str += each
    temp_str += ' '

response = bot.get_response(temp_str)
print(response)
print(response.confidence)
