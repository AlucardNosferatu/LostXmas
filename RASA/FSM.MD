# FSM
### 基本原理：

利用slot来存储状态标记（名为state）

对话意图识别（通过主体抽取，目前未实现，暂以特定字符串匹配代替）决定当前状态输出和下一刻状态：

1.保持状态：状态不变，输入→当前状态的响应函数→输出

2.切换状态：状态根据输入进行切换，输入→先切换→下一状态的响应函数→输出

之所以采用状态切换是为了对付RASA中特定story不能覆盖所有可能回答的问题

可能当前在进行storyA，但是用户不想等该轮对话结束想要直接进入storyB

如果用原本的方法可能要写一个storyA和storyA-B还有一个storyB

我希望这个FSM能够利用有限种stories进行组合给用户造成连续对话的体验

如果不能实现有限个stories通过组合形成多轮对话，那么这个想法也将宣告失败

### 具体实现

1.首先我写了一个叫做state的slot √

2.我写了个叫做action_state_change的自定义action √

这个action的作用是把用户最后发来的内容作为条件，通过SlotSet变更不同条件下state的下一状态

4.给n个已有stories的条件和回答中间加入各自不同的checkpoints，结尾统一加一个相同的checkpoint（以下称做CP）

3.写另外n个stories，开头都写上CP，中间运行一次action_listen，然后action_state_change

最后各自用不同slot做条件指向其它stories各自内含的不同checkpoints

### 思考

由于对RASA这个框架还不是很熟悉，可能绕了弯路

比如说写到这里我才发现似乎不用slot只用checkpoint就可以完成状态切换的功能。。。

若有一天发现RASA本身就可以完成指定目标，那么也会把这个repo删掉吧

也欢迎各位大佬多多指教

### 参考：

https://rasa.com/docs/rasa/core/stories/#checkpoints

https://rasa.com/docs/rasa/core/slots/#slots-set-by-actions
