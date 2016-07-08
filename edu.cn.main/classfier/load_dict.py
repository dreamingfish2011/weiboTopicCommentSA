# encoding=utf-8
# filename:load_dic.py
import sys
sys.path.append("../")
import os
import json
#ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\', '/')
#print ROOT('dict/userdict.txt') 

###load程度副词词典
def load_adv_dic():
    adv_dic = {}
    # ##load程度副词词典，权重分级别
    myfile = open('dict/adv_1.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    
    myfile = open('dict/adv_2.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 2
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    
    myfile = open('dict/adv_3.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 3
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    
    myfile = open('dict/adv_4.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 4
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    
    myfile = open('dict/adv_5.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 5
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    
    myfile = open('dict/adv_6.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          adv_dic[line] = 6
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return adv_dic

###load否定词词典
def load_deny_dic():
    deny_dic = {}
    # ##load否定词词典，权重-1
    myfile = open('dict/deny_1.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          deny_dic[line] = -1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return deny_dic

###load负面评价词典
def load_neg_dic():
    neg_dic = {}
    # ##load负面评价词词典，权重-1
    myfile = open('dict/neg_1.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
          neg_dic[line] = -1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return neg_dic

###load正面评价词典
def load_pos_dic():
    pos_dic = {}
    # ##load正面评价词词典，权重-1
    myfile = open('dict/pos_1.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '' :
          pos_dic[line] = 1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    myfile = open('dict/pos_2.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '' :
          pos_dic[line] = 1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    myfile = open('dict/pos_3.txt','r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '' :
          pos_dic[line] = 1
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return pos_dic
