import ctypes
import inspect
import os
import sys
import json
import random
import threading
import tensorflow as tf
from tqdm import tqdm
from urllib import parse
from snownlp import SnowNLP

from data.data_tool import get_file_list
from train.train_seq2seq import build_seq2seq, train_seq2seq, load_seq2seq
from train.utils import load_resource, get_vocab_size
from server.inspiration import Inspiration
from infer.infer_seq2seq import build_qa_model
from http.server import SimpleHTTPRequestHandler
from infer.utils import input_question, decode_greedy
from data.obsolete.grammar4fluency import mark_invalid
from data.data_packer import read_conversation, add_padding
from data.augmentation.similarity import similarity_complex, Keywords_IoU


class Seq2seq:
    info_log = []
    qa_lines = []
    a_lines_list = []
    similar_answers_from_data = []
    BaseDir = ""
    currentQ = ""
    currentA = ""
    f_r = None
    f_q = None
    f_a = None
    q_model = None
    a_model = None
    word_to_index = None
    index_to_word = None
    # all_composed = None
    # syn = None
    UseKeywords = False

    def __init__(self, use_keywords=False, base_dir='../', weight_name="W -140-0.0120-.h5"):
        self.UseKeywords = use_keywords
        self.BaseDir = base_dir
        self.f_r = open(self.BaseDir + "data/resource/raw/all_corpus.tsv", 'r+', encoding='utf-8-sig')
        self.qa_lines = self.f_r.readlines()
        lines = self.qa_lines.copy()
        for i in tqdm(range(len(lines))):
            lines[i] = lines[i].split('\t')[1].replace('\n', '').strip()
            self.a_lines_list = [lines]
        self.q_model, self.a_model = build_qa_model(
            BaseDir=self.BaseDir,
            wp=base_dir + "train/check_points/" + weight_name
        )
        _, _, _, _, self.word_to_index, self.index_to_word = load_resource(base_dir=self.BaseDir)
        self.f_q = open(self.BaseDir + "infer/Online_Q.txt", 'a', encoding='utf-8-sig')
        self.f_a = open(self.BaseDir + "infer/Online_A.txt", 'a', encoding='utf-8-sig')
        # with open(BaseDir + 'data/resource/composable.pkl', 'rb') as f:
        #     self.all_composed = pickle.load(f)
        # with open(BaseDir + 'data/resource/syn_dict.pkl', 'rb') as f:
        #     self.syn = pickle.load(f)
        print(self.interact(new_question="你好"))

    def interact(self, new_question):
        self.currentQ = new_question
        if new_question == 'x':
            self.currentA = "DEBUG:那不打扰你了，回聊~"
            return self.currentA
        new_question, sentence = input_question(
            seq=new_question,
            word_to_index=self.word_to_index,
            all_composed=None,
            syn_dict=None
        )
        if sentence is None:
            self.currentA = "DEBUG:" + new_question
            return self.currentA

        with tf.device("/gpu:0"):
            self.currentA = decode_greedy(
                seq=new_question,
                sentence=sentence,
                question_model=self.q_model,
                answer_model=self.a_model,
                word_to_index=self.word_to_index,
                index_to_word=self.index_to_word
            )
        return self.currentA

    def education(self, new_answer):
        if new_answer == "cancel":
            return "取消添加新语料："
        else:
            self.f_q.write(self.currentQ + "\n")
            self.f_a.write(new_answer + "\n")
            self.f_q.flush()
            self.f_a.flush()
            self.currentA = new_answer
            return "新语料添加成功："

    def orientation(self, include, exclude):
        self.info_log = []
        if self.UseKeywords:
            include = ""
            exclude = ""
        for j in range(len(self.a_lines_list)):
            self.similar_answers_from_data = []
            for i in range(len(self.a_lines_list[j])):
                line = self.a_lines_list[j][i]
                line = line.replace(' ', '')
                if "【禁用】" in self.qa_lines[i]:
                    continue

                # region use Similarity
                if not self.UseKeywords:
                    if len(exclude) >= 2 and exclude in line:
                        continue
                    if include in line:
                        scores = similarity_complex(line, self.currentA)
                        scores, mean_score, max_score, std_score = scores
                        if max_score > 0.5:
                            self.similar_answers_from_data.append(i)
                            self.info_log.append(
                                " 行号：" + str(i + 1) + " 内容：" + self.qa_lines[i].replace(
                                    "\t",
                                    "<-------"
                                ) + " 最高分：" + str(max_score))
                # endregion

                # region Use Keywords
                else:
                    i_o_u, matched = Keywords_IoU(line, self.currentA)
                    if i_o_u >= 0.25 and matched >= 2:
                        self.similar_answers_from_data.append(i)
                        self.info_log.append(
                            " 行号：" + str(i + 1) + " 内容：" + self.qa_lines[i].replace(
                                "\t",
                                "<-------"
                            ) + " IoU：" + str(i_o_u) + " 相同：" + str(matched))

                # endregion

        return self.similar_answers_from_data, self.info_log

    def correction(self):
        if len(self.similar_answers_from_data) >= 1:
            self.qa_lines = mark_invalid(self.similar_answers_from_data, self.qa_lines)
            self.f_r.truncate(0)
            self.f_r.seek(0)
            self.f_r.writelines(self.qa_lines)
            self.f_r.flush()
            return "被选中的语料禁用成功。"
        else:
            return "相似回答搜索结果为空。"


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class TrainThread(threading.Thread):
    model = None

    def run(self):
        train_seq2seq(input_model=self.model, base_dir="")

    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
        vocab_size = get_vocab_size(base_dir="")
        build_seq2seq(vocab_size=vocab_size, base_dir="")
        self.model = load_seq2seq(file_path="models/seq2seq_raw.h5")


# noinspection PyPep8Naming
class MyRequestHandler(SimpleHTTPRequestHandler):
    weight_name = ""
    protocol_version = "HTTP/1.0"
    server_version = "PSHS/0.1"
    sys_version = "Python/3.7.x"
    seq2seq = None
    ins = Inspiration(base_dir='', limit=3)
    train_thread = None

    @staticmethod
    def load_weight(input_weight_name):
        MyRequestHandler.seq2seq = Seq2seq(base_dir='', weight_name=input_weight_name)
        print("weight name: ", input_weight_name)
        return MyRequestHandler.seq2seq

    def do_GET(self):
        if self.seq2seq is None:
            print("Haven't load weight yet.")
            self.seq2seq = MyRequestHandler.load_weight(self.weight_name)
        if self.path == "/":
            print(self.path)
            content = self.seq2seq.currentQ + "<br>" + self.seq2seq.currentA + "<br>"
            content += "<br>"
            for each in self.seq2seq.info_log:
                content += each + "<br>"
            content += "<br>"
            content += self.ins.q + "<br>"
            content += self.ins.a + "<br>"
            content += "<br>"
            for each in self.ins.a_list:
                content += each + "<br>"
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            content = content.encode("utf-8")
            self.wfile.write(content)
        else:
            print("get path error")

    def do_POST(self):
        if self.seq2seq is None:
            print("Haven't load weight yet.")
            self.seq2seq = MyRequestHandler.load_weight(self.weight_name)
        if self.path == "/":
            response = ""
            print("postmsg recv, path right")
            data = self.rfile.read(int(self.headers["content-length"]))
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                data = parse.parse_qs(data.decode('utf-8'))
            if data.__contains__('content'):
                response = self.seq2seq.interact(data['content'])
                self.send_response(200)
            elif data.__contains__('sync'):
                if len(data['sync']) != 0:
                    self.seq2seq.currentA = data['sync']
                response = [self.seq2seq.currentQ, self.seq2seq.currentA]
                response = [self.seq2seq.education(new_answer=self.seq2seq.currentA)] + response
                self.send_response(200)
            elif data.__contains__('include') or data.__contains__('exclude'):
                include = data.get('include', '')
                exclude = data.get('exclude', '')
                _, response = self.seq2seq.orientation(include, exclude)
                self.send_response(200)
            elif data.__contains__('purge'):
                response = self.seq2seq.correction()
                self.send_response(200)
            elif data.__contains__('hint'):
                self.seq2seq.currentQ = data['hint']
                try:
                    s = SnowNLP(self.seq2seq.currentQ)
                    tags = list(s.tags)
                    i = 0
                    while i < len(tags):
                        if len(tags[i][0]) < 2:
                            del tags[i]
                        elif not tags[i][1][0] in ['v', 'a', 't', 'n', 'i']:
                            del tags[i]
                        else:
                            i += 1
                    keyword = random.choice(tags)[0]
                except ZeroDivisionError:
                    keyword = ""
                except UnboundLocalError:
                    keyword = " "
                response = self.ins.search_keyword(keyword=keyword)
                self.send_response(200)
            elif data.__contains__('keyword'):
                response = self.ins.search_keyword(keyword=data['keyword'])
                self.send_response(200)
            elif data.__contains__('hers'):
                self.ins.select_reply(int(data['hers']))
                q_index = data.get('mine', None)
                response = self.ins.get_qa(q_index=q_index)
                if q_index == "use_current":
                    _, self.seq2seq.currentA = response
                    response = [self.seq2seq.currentQ, self.seq2seq.currentA]
                else:
                    self.seq2seq.currentQ, self.seq2seq.currentA = response
                self.send_response(200)
            elif data.__contains__('h') or data.__contains__('t'):
                self.seq2seq.currentQ = data.get('h', '')
                self.seq2seq.currentA = data.get('t', '')
                response = data
                self.send_response(200)
            elif data.__contains__('data'):
                read_conversation(base_dir="")
                response = add_padding(base_dir="")
                self.send_response(200)
            elif data.__contains__('train'):
                if data['train'] == 'stop':
                    if MyRequestHandler.train_thread is not None and MyRequestHandler.train_thread.is_alive():
                        stop_thread(MyRequestHandler.train_thread)
                        response = "DEBUG:训练已终止"
                    else:
                        response = "DEBUG:训练未开始"
                else:
                    if data['train'] == 'continue':
                        pass
                    else:
                        dir_path = "train/check_points"
                        for e, i in enumerate(os.listdir(dir_path)):
                            if i.endswith('h5'):
                                file_path = os.path.join(dir_path, i)
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                    if MyRequestHandler.train_thread is None or not MyRequestHandler.train_thread.is_alive():
                        MyRequestHandler.train_thread = TrainThread()
                    MyRequestHandler.train_thread.start()
                    response = "DEBUG:训练已开始"
                self.send_response(200)
            elif data.__contains__('weights'):
                file_list = os.listdir('train/check_points/')
                weight_changed = False
                if len(file_list) > 0:
                    response = get_file_list('train/check_points/')
                    if str(data['weights']).isnumeric():
                        load_index = int(data['weights'])
                        if 0 <= load_index < len(response):
                            self.weight_name = response[load_index]
                            weight_changed = True
                    elif data['weights'] == "newest":
                        self.weight_name = response[-1]
                        weight_changed = True
                    elif data['weights'].startswith("E") and data['weights'][1:].isnumeric():
                        for each in response:
                            if data['weights'][1:] == each.split('-')[1].strip():
                                self.weight_name = each
                                weight_changed = True
                                break
                    if weight_changed:
                        self.seq2seq = MyRequestHandler.load_weight(self.weight_name)
                        response = "Use weight: " + self.weight_name
                else:
                    response = "train/check_points is empty."
                self.send_response(200)
            else:
                self.send_response(400)

            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            res = {'reply': response}
            response_str = json.dumps(res, ensure_ascii=False)
            self.wfile.write(response_str.encode("utf-8"))
            if response == "DEBUG:那不打扰你了，回聊~":
                sys.exit()
        else:
            print("postmsg recv, path error")
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
