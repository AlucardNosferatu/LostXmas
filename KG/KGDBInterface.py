# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:34:47 2019

@author: 16413
"""
import os
import sys
from py2neo import Graph, Node, Relationship, walk
import jieba
from tqdm import tqdm
import time
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
import seq2seq.word.test_model_word as test_model_word
import seq2seq.word.data_word as data_word
import seq2seq.word.train_word as train_word


def load_data(filename='data.txt', amount=500):
    count = 0
    lines_dict = []
    name = ''
    with open(filename, encoding='utf-8') as f:
        while count < amount:
            line = f.readline()
            if not line:
                break
            else:
                line = line.split('	')
                if len(line) != 3:
                    pass
                else:
                    if line[0] == name:
                        attr_name = line[1]
                        attr_value = line[2]
                        lines_dict[count - 1][attr_name] = attr_value
                    else:
                        count += 1
                        name = line[0]
                        attr_name = line[1]
                        attr_value = line[2]
                        line_dict = {'name': name, attr_name: attr_value}
                        lines_dict.append(line_dict)
    f.close()
    return lines_dict


def create_nodes(lines_dict, gi, node_type='常识数据库'):
    f = open('KG\\dict.txt', 'w', encoding='utf-8')
    print("开始建立节点...")
    for i in tqdm(range(0, len(lines_dict))):
        new_node = Node(node_type, name='')
        for key in lines_dict[i]:
            if key == 'name':
                new_node['name'] = lines_dict[i][key].split("（")[0]
                f.write(new_node['name'] + '\n')
                f.flush()
            else:
                new_node[key] = lines_dict[i][key]
        gi.create(new_node)
    f.close()


def find_relationships(gi, match_result=None, node_type='常识数据库'):
    if match_result is None:
        match_result = gi.nodes.match(node_type)
    else:
        pass
    temp = ''
    namelist = []
    relationships = []
    length = len(match_result)
    # make namelist for all nodes matched
    print("\n开始建立关系目标清单...")
    for i in tqdm(range(0, length)):
        temp = match_result.skip(i).first()['name']
        # prevent matcher from mismatching short words
        if len(temp) < 2 or (len(temp) < 5 and temp.encode('UTF-8').isalpha()):
            pass
        else:
            namelist.append(temp)
    # match all properties of nodes with names of other nodes
    time.sleep(2)
    print("\n开始匹配关系目标...")
    for i in tqdm(range(0, length)):
        node_temp = dict(match_result.skip(i).first())
        values = node_temp.values()
        temp_rel = []
        for value in values:
            value = value.replace('\n', '')
            for j in range(0, len(namelist)):
                # limit the amount of relationships to a rational range
                if j < 100 and namelist[j] in value:
                    temp_rel.append(namelist[j])
                else:
                    pass
        relationships.append(temp_rel)
    # remove relationships between nodes and themselves
    time.sleep(2)
    print("\n开始关系去重...")
    for i in tqdm(range(0, len(relationships))):
        for j in range(0, len(relationships[i])):
            if match_result.skip(i).first()['name'] in relationships[i]:
                relationships[i].remove(match_result.skip(i).first()['name'])
            else:
                pass
        # remove repetition
        relationships[i] = list(set(relationships[i]))
    return [match_result, relationships]


def create_relationships(gi, relationships, match_result=None):
    if match_result is None:
        match_result = gi.nodes.match(type)
    else:
        pass
    time.sleep(2)
    print("\n开始建立关系...")
    for i in tqdm(range(0, len(relationships))):
        node_this = match_result.skip(i).first()
        for rel in relationships[i]:
            node_that = match_result.where(name=rel).first()
            rel_instance = Relationship(node_this, "REL", node_that)
            gi.create(rel_instance)
    return match_result


def init(gi, amount=500, filename="KG\\data.txt"):
    lines_dict = load_data(filename=filename, amount=amount)
    create_nodes(lines_dict=lines_dict, gi=gi)
    result = find_relationships(gi=gi)
    create_relationships(gi=gi, relationships=result[1], match_result=result[0])


def node_comment(input_node):
    str_temp = ''
    keys_temp = []
    for each_key in input_node:
        if each_key == 'name':
            pass
        else:
            keys_temp.append(each_key)
    for i in range(0, len(keys_temp)):
        if i == 0:
            str_temp += input_node['name']
            str_temp += '的'
        elif i % 2 == 1:
            str_temp += '其'
        else:
            str_temp += '它的'
        str_temp += keys_temp[i]
        str_temp += '是'
        str_temp += input_node[keys_temp[i]].strip('\n')
        if i == len(keys_temp) - 1:
            str_temp += '。'
        else:
            str_temp += '，'
    print(str_temp)


def switch_topic(gi, input_node):
    node_comment(input_node)
    print("相关词条：")
    f_null = open(os.devnull, "w")
    relationships1 = gi.match((input_node,), r_type=None)
    relationships2 = gi.match((None, input_node), r_type=None)
    temp = []
    for i in range(0, len(relationships1) + len(relationships2)):
        # print("====三元组分割线====")
        # print("####" + str(i) + "####")
        # print("====三元组分割线====")
        if i < len(relationships1):
            j = i
            relationships = relationships1
        else:
            j = i - len(relationships1)
            relationships = relationships2
        for each in walk(relationships.skip(j).first()):
            if type(each) is Node:
                if each != input_node:
                    print(each, file=f_null)
                    # print(dict(each))
                    print(each['name'])
                    # will be replaced by node_comment()
                    temp.append(each)
            else:
                # print("****关系类型****")
                # print(each)
                # print("****关系类型****")
                pass
    print("================")
    return temp


def auto_switch(gi, input_node):
    node_list = switch_topic(gi=gi, input_node=input_node)
    hint_str = input('')
    if '*' not in hint_str:
        return input_node, hint_str
    for each in node_list:
        if each["name"] in hint_str:
            return each, hint_str
    return input_node, hint_str


def topics_chain(gi, input_node):
    hint_str = '*'
    if input_node is not None:
        while '*' in hint_str:
            input_node, hint_str = auto_switch(gi=gi, input_node=input_node)
    return hint_str


def eval_relationship(relationship):
    f_null = open(os.devnull, "w")
    if relationship is not None and len(relationship) > 0:
        for each_rel in relationship:
            print("=====================")
            for each in walk(each_rel):
                print(each, file=f_null)
                if type(each) is Node:
                    for each_key in each:
                        print(each_key + " : " + each[each_key].replace('\n', ''))
                else:
                    print('关系类型：' + type(each).__name__)


def search(gi, name='Carol', node_type='Tulpa', rel_type='LOVES', from_node=False):
    nodes = gi.nodes.match(node_type).where(name=name)
    node_matched = nodes.first()
    relationship_matched = []
    if rel_type is not None and node_matched is not None:
        if from_node:
            relationships = gi.match((node_matched,), r_type=rel_type)
        else:
            relationships = gi.match((None, node_matched), r_type=rel_type)
        for i in range(0, len(relationships)):
            relationship_matched.append(relationships.skip(i).first())
        return node_matched, relationship_matched
    return node_matched, None


def key_in_dialog(gi, dialog_str, node_type='常识数据库', rel_type='REL', seg=True):
    if seg:
        seg_list = jieba.lcut(dialog_str, cut_all=True)
    else:
        seg_list = [dialog_str.strip("？")]
    node_searched = None
    relationship_searched = None
    for word in seg_list:
        node_searched, relationship_searched = search(gi, name=word, node_type=node_type, rel_type=rel_type)
        if node_searched is not None:
            break
    return node_searched, relationship_searched


def reply(gi, input_str=None, node_type="常识数据库", seg=True, rel_type="REL", eval_rel=False):
    next_str = None
    if input_str is None:
        input_str = input()
    if "?" in input_str or "？" in input_str:
        node_matched, relationship = key_in_dialog(dialog_str=input_str, gi=gi, seg=seg, rel_type=rel_type)
        if node_matched is not None:
            if eval_rel:
                eval_relationship(relationship=relationship)
            else:
                next_str = topics_chain(gi=gi, input_node=node_matched)
        else:
            print("我不知道耶。。。")
    elif "*你知道么*" in input_str:
        str_test = input_str.strip("*你知道么*")
        str_test = str_test.split("是")
        str_a = str_test[0]
        str_test = str_test[1].split("的")
        str_b = str_test[0]
        str_rel = str_test[1]
        node_a = gi.nodes.match(node_type).where(name=str_a).first()
        if node_a is None:
            node_a = Node(node_type, name=str_a)
        node_b = gi.nodes.match(node_type).where(name=str_b).first()
        if node_b is None:
            node_b = Node(node_type, name=str_b)
        rel = Relationship.type(str_rel)
        gi.merge(rel(node_a, node_b), node_type, "name")
        print("是这样吗？")
        reply(gi=gi, input_str=str_b + "？", seg=False, rel_type=str_rel, eval_rel=True)
    else:
        print(test_model_word.TulpaAvatar(input_str))
        # seq2seq
    return next_str


def loop_talking(gi):
    jieba.load_userdict("KG\\dict.txt")
    next_str = None
    while True:
        next_str = reply(gi=gi, input_str=next_str)


rootPath = os.path.dirname(sys.path[0])
os.chdir(rootPath)
# graph_instance = Graph('http://localhost:7474', auth=('neo4j', '20160712'))
# loop_talking(gi=graph_instance)
train_word.train_start()
# init(gi=graph_instance, amount=2000)