__author__ = 'zhuhongmei'
###load��������,������飬��һ���������ݣ��ڶ��������۱�ʶ
def load_comment_data(filename):
    comment_data = []
    # ##load�񶨴ʴʵ䣬Ȩ��-1
    myfile = open(filename,'r',encoding= 'utf-8')
    line = myfile.readline().strip('\n').strip()
    while line != '':
        ##��������
          cotent = line.split('|')
          comment_data.append(cotent)
          line = myfile.readline().strip('\n').strip()
    myfile.close()
    return comment_data