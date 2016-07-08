# encoding=utf-8
#!/usr/bin/python3
import sys
sys.path.append("../")
import os
# ##结巴分词模块
import jieba
jieba.load_userdict("dict/userdict.txt")


# ##自定义其他
import load_dict as ld

neg_dic = ld.load_neg_dic()
pos_dic = ld.load_pos_dic()
print(neg_dic)
print(pos_dic)

sent = [ [1, "他面目可憎"], [2, "确保万无一失"], [3, "马云独具慧眼,万无一失"]]
sent_has_sentiment = []
cut_words = []
for every_sent in sent :
    words = jieba.cut(every_sent[1])
    cut_words.append(words)
    has_sentiment_flag = 0
    pos_weight = 0
    neg_weight = 0
    sent_after_cut = ""
    for w in words:
        sent_after_cut = sent_after_cut + " "+w
        if w in pos_dic :
            has_sentiment_flag = 1
            pos_weight = pos_weight + pos_dic[w]
        elif w in neg_dic :
            has_sentiment_flag = 1
            neg_weight = neg_weight + neg_dic[w]
        else :
            None
    if has_sentiment_flag == 1:
        every_sent.append(sent_after_cut)
        every_sent.append(pos_weight)
        every_sent.append(neg_weight)
        sent_has_sentiment.append(every_sent)
        
for every_sentiment in sent_has_sentiment :
    print(every_sentiment)


