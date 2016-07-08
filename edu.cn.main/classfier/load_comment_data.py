__author__ = 'zhuhongmei'
###load评价数据,输出数组，第一列评论内容，第二列是评价标识
def load_comment_data(filename):
    comment_data = []
    # ##load否定词词典，权重-1
    myfile = open(filename,'r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
        ##评论内容
          cotent = line.split('|')
          comment_data.append(cotent)
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return comment_data