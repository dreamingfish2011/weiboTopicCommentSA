__author__ = 'zhuhongmei'
# encoding=utf-8
#!/usr/bin/python3
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import jieba
import load_comment_data as ld
import load_dict as ld_dic
import collections
from nltk.metrics import scores


def word_feats(words):
  return dict([(word, True) for word in words])

neg_dic = ld_dic.load_neg_dic()
pos_dic = ld_dic.load_pos_dic()
print(neg_dic)
print(pos_dic)

filename ='data/comment_data.txt'
comment_data = ld.load_comment_data(filename)
negfeats = []
posfeats = []
for every_sent in comment_data :
    words = jieba.cut(every_sent[1])
    words_has_sentiment = []
    for w in words :
        if w in pos_dic :
            words_has_sentiment.append(w)
        elif w in neg_dic :
            words_has_sentiment.append(w)
        else :
            None
    if 'pool' == every_sent[2]:
        neg = [word_feats(words_has_sentiment), 'neg']
        negfeats.append(neg)
    else :
        pos = [word_feats(words_has_sentiment), 'pos']
        posfeats.append(pos)

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4

trainfeats = negfeats[:int(negcutoff)] + posfeats[:int(poscutoff)]
testfeats = negfeats[int(negcutoff):] + posfeats[int(poscutoff):]
print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
classifier = NaiveBayesClassifier.train(trainfeats)
print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
print(classifier.classify({'厌恶':True, '恶心': True, '差劲': True}) )
classifier.show_most_informative_features()

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testfeats):
  refsets[label].add(i)
  observed = classifier.classify(feats)
  testsets[observed].add(i)
print('pos precision:', scores.precision(refsets['pos'], testsets['pos']))
print('pos recall:', scores.recall(refsets['pos'], testsets['pos']))
print('pos F-measure:', scores.f_measure(refsets['pos'], testsets['pos']))
print('neg precision:', scores.precision(refsets['neg'], testsets['neg']))
print('neg recall:', scores.recall(refsets['neg'], testsets['neg']))
print('neg F-measure:', scores.f_measure(refsets['neg'], testsets['neg']))