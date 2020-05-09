# LostXmas
使用itchat库操作网页微信，调用图灵机器人API和微软小冰聊天

刷出来的数据存到txt文件里，然后利用该文件训练seq2seq模型（采用jieba中文分词）

建议：数据使用前请清洗

# 2019.05.20
结构及功能变化较大，说明待主体全部完成后更新

# 2019.11.23
ChatterBot：利用ChatterBot库做的简单对话程序和仿照ChatterBot原理自己写的对话框架（采用Neo4J存储语料数据）

KG：Neo4J数据库接口原型

seq2seq：改变网络结构（增加层数、编码长度），改用分字取代分词加大语料覆盖，增加数据清洗器筛出不良数据

answers：利用情绪识别和冷读法原理做的答案之书

# 2019.11.29
基于欧几里得距离的KMeans文本分类：终止

基于回答相似性的孪生seq2seq编码训练：终止

基于SeqGAN的ChatBot：等待参考repo消除issue（空词典）

# 2019.12.03
由于微软小冰的微信公众号不知道什么时候被封，itchat刷数据也用不了了

基于有限状态机和RASA框架的对话机器人：进行中

昨天是梦梦奈的生日，先祝她生日快乐吧

虽然挺喜欢梦梦奈，也有花钱在上面

但之前在兽耳科技的粉丝群被管理员不知道怎么回事给骂了一顿，对这个产品还是有些微妙的感觉

虽然那个狗管理最后离职了，但我还是觉得，不应该埋怨谁

毕竟在我看来，人类的品性和平均道德水准不如他们所创造的AI，就不用苛求别人都是善良的了

# 2019.12.04

昨天学习了一下FSM的原理，思考了一下使用情形

感觉FSM可能不适合对话这种状态切换比较频繁、切换方式都不相同的任务

如果有n个状态，则状态切换函数就有n*(n-1)个，这样代码量就实在太大了，不符合要求

而且还需要重新思考下RASA本身的特点和不足

也许对于RASA本身还不够了解，对于其所能够实现的模型的优缺点还认知不完全
