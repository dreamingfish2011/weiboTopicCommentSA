__author__ = 'zhuhongmei'
# encoding=utf-8
#!/usr/bin/python3
#功能：爬取新浪微博移动端的话题评论数据
#网址：http://weibo.cn/ 数据量更小 相对http://weibo.com/
import time
#import re
import os
import sys
import codecs
#import shutil
#import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
#from selenium.webdriver.common.action_chains import ActionChains
import iden_code_recog as iden

#先调用无界面浏览器PhantomJS或Firefox
driver = webdriver.PhantomJS(executable_path="D:\\IDE\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
#driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,10)


#全局变量 文件操作读写信息
inforead = codecs.open("SinaWeibo_List_best_1.txt", 'r', 'utf-8')
infofile = codecs.open("SinaWeibo_Info_best_1.txt", 'w', 'utf-8')

#********************************************************************************
#                            第一步: 登陆weibo.cn
#        该方法针对weibo.cn有效(明文形式传输数据) weibo.com见学弟设置POST和Header方法
#                LoginWeibo(username, password) 参数用户名 密码
#********************************************************************************
def LoginWeibo(username, password):
    try:
        #输入用户名/密码登录
        print(u'准备登陆Weibo.cn网站...')
        driver.get("http://login.weibo.cn/login/")
        elem_user = driver.find_element_by_name("mobile")
        elem_user.send_keys(username) #用户名
        elem_pwd = driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
        elem_pwd.send_keys(password)  #密码 name=password_6785
        #elem_rem = driver.find_element_by_name("remember")
        #elem_rem.click()             #记住登录状态
        elem_iden_image = driver.find_element_by_xpath("/html/body/div[2]/form/div/img")
        iden_image_location = elem_iden_image.get_attribute("src")
        #重点:暂停时间输入验证码(http://login.weibo.cn/login/ 手机端需要)
        idencoderecog = iden.IdenCodeRecog()
        iden_code = idencoderecog.recog_iden_code_image(iden_image_location,"idencode")
        time.sleep(10)
        elem_iden = driver.find_element_by_xpath("/html/body/div[2]/form/div/input[2]")
        elem_iden.send_keys(iden_code)  #密码 name=password_6785
        #点击submit按钮登陆方式或输入回车键登陆方式
        elem_sub = driver.find_element_by_name("submit")
        elem_sub.click()
        #elem_pwd.send_keys(Keys.RETURN)
        time.sleep(2)

        #获取Coockie
        print(driver.current_url)
        print(driver.get_cookies())  #获得cookie信息 dict存储
        print(u'输出Cookie键值对信息:')
        for cookie in driver.get_cookies():
            #print cookie
            for key in cookie:
                print(key, cookie[key])

        #driver.get_cookies()类型list 仅包含一个元素cookie类型dict
        print(driver.page_source)
        print(u'登陆成功...')
    except Exception as e:
        print("Error: ",e)
    finally:
        print(u'End LoginWeibo!\n\n')

#**********************************************************************************************
#                  第二步: 访问个人页面http://weibo.cn/5824697471并获取信息
#                                VisitPersonPage()
#        编码常见错误 UnicodeEncodeError: 'ascii' codec can't encode characters文件utf-8编码
#**********************************************************************************************

def VisitPersonPage(user_id):

    try:
        global infofile       #全局文件变量
        url = "http://weibo.com/" + user_id
        driver.get(url)
        print(u'准备访问个人网站.....', url)
        print(u'个人详细信息')

        #用户id
        print(u'用户id: ' + user_id)

        #昵称 关注数 粉丝数 微博数 个人资料其它信息
        #URL http://weibo.cn/3473948932/follow
    except Exception as e:
        print("Error: ",e)
    finally:
        print(u'VisitPersonPage!\n\n')

#********************************************************************************
#                  第三步: 访问http://weibo.cn/search/ (手机端) 页面搜索热点信息
#                         爬取微博信息及评论，注意评论翻页的效果和微博的数量
#********************************************************************************

def GetComment(key):
    try:
        global infofile       #全局文件变量
        driver.get("http://weibo.cn/search/")
        print(u'搜索热点主题关键词：', key)

        #输入主题并点击搜索
        item_inp = driver.find_element_by_xpath("//div[@class='c']/form/div/input") #name=keyword
        item_inp.send_keys(key)
        print(item_inp.get_attribute("value"))
        item_inp.send_keys(Keys.RETURN)    #采用点击回车直接搜索
        print(driver.page_source)

        #内容
        #content = driver.find_elements_by_xpath("//div[@class='content clearfix']/div/p")
        comment = driver.find_elements_by_xpath("//a[@class='cc']")
        content = driver.find_elements_by_xpath("//div[@class='c']")
        print(content)
        all_comment_url = []               #存储所有文件URL
        i = 0
        j = 0
        infofile.write(u'开始:\r\n')
        print(u'长度', len(content))
        while i<len(content):
            #print content[i].text
            if (u'收藏' in content[i].text) and (u'评论' in content[i].text): #过滤其他标签
                print(content[i].text)
                infofile.write(u'微博信息:\r\n')
                infofile.write(content[i].text + '\r\n')
                div_id = content[i].get_attribute("id")
                print(div_id)
                while(1):  #存在其他包含class=cc 如“原文评论”
                    url_com = comment[j].get_attribute("href")
                    if ('comment' in url_com) and ('uid' in url_com):
                        print(url_com)
                        infofile.write(u'评论信息:\r\n')
                        infofile.write(url_com+'\r\n')
                        all_comment_url.append(url_com)    #保存到变量里
                        j = j + 1
                        break
                    else:
                        j = j + 1

            i = i + 1

        #http://weibo.cn/search/?pos=search
        print(driver.current_url)

        #python中文转换url编码 urllib.quote(key) urllib.unquote转回来
        #转码失败
        #http://weibo.cn/search/mblog?hideSearchFrame=&keyword=欢乐颂&page=2
        #url = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword="+ key_url + "&page=2"


        #获取10个下页
        N = 2
        while N<=10:
            #后面采用换页 第一次为方便给大家解决方法就采用获取搜索框id回车访问
            url_get = driver.find_element_by_xpath("//div[@id='pagelist']/form/div/a")
            url = url_get.get_attribute("href")
            print(url)#获取下页)
            driver.get(url)
            comment = driver.find_elements_by_xpath("//a[@class='cc']")
            content = driver.find_elements_by_xpath("//div[@class='c']")
            print(content)
            i = 0
            j = 0                        #第一个<a class='cc' href>是多余的
            print(u'长度', len(content))
            infofile.write(u'\r\n下页:\r\n')
            while i<len(content):
                #print content[i].text
                if (u'收藏' in content[i].text) and (u'评论' in content[i].text):
                    print(content[i].text)
                    infofile.write(u'微博信息:\r\n')
                    infofile.write(content[i].text + '\r\n')
                    #获取该信息id值 通过id获取评论超链接
                    #先获取:<div id="M_Du3npzqSd" class="c">
                    #再获取:<a class="cc" href="http://weibo.cn/comment/#cmtfrm"></a>
                    div_id = content[i].get_attribute("id")
                    print(div_id)
                    '''''
                    url = driver.find_elements_by_xpath("//div[@id=" + div_id + "]/a")
                    print url
                    for u in url:
                        print u.get_attribute("href")
                    '''
                    while(1):  #存在其他包含class=cc 如“原文评论”
                        url_com = comment[j].get_attribute("href")
                        if ('comment' in url_com) and ('uid' in url_com):
                            print(url_com)
                            infofile.write(u'评论信息:\r\n')
                            infofile.write(url_com + '\r\n')
                            all_comment_url.append(url_com)
                            j = j + 1
                            break
                        else:
                            j = j + 1

                i = i + 1
            N = N + 1
        else:
            print(u'结束爬取评论URL 对齐while循环')


        #方位评论URL并进行爬取
        print(u'\n\n评论')
        infocomment = codecs.open("SinaWeibo_Info_best_2.txt", 'w', 'utf-8')
        for url in all_comment_url:
            print(url)
            driver.get(url)
            #driver.refresh()
            time.sleep(2)
            infocomment.write(url+'\r\n')
            test = driver.find_elements_by_class_name('c')
            print(len(test))
            #Error:  Message: Element not found in the cache -
            #perhaps the page has changed since it was looked up
            #http://www.51testing.com/html/21/n-862721-2.html
            #异常的说明已经很明显了：在cache中找不到元素，在元素被找到之后页面变换了。
            #这就说明，当当前页面发生跳转之后，存在cache中的关于这个页面的元素也被清空了。
            k = 0
            while k<len(test):
                print(test[k].text)
                infocomment.write(test[k].text + '\r\n')
                k = k + 1
            infocomment.write('\r\n')
        infocomment.close()



    except Exception as e:
        print("Error: ",e)
    finally:
        print(u'VisitPersonPage!\n\n')
        print('**********************************************\n')

#*******************************************************************************
#                                程序入口 预先调用
#         注意: 因为sina微博增加了验证码,但是你用Firefox登陆输入验证码
#         直接跳转到明星微博那部分,即: http://weibo.cn/guangxianliuyan
#*******************************************************************************

if __name__ == '__main__':
    print("dasha")
    #定义变量
    username = 'jumay201210@gmail.com'             #输入你的用户名
    password = '*********'               #输入你的密码
    print('init:username=' +username+'  password=' +password)
    #操作函数
    LoginWeibo(username, password)       #登陆微博

    #在if __name__ == '__main__':引用全局变量不需要定义 global inforead 省略即可
    print('Read file:')
    user_id = inforead.readline()
    while user_id!="":
        user_id = user_id.rstrip('\r\n')
        print(user_id)
        VisitPersonPage(user_id)         #访问个人页面http://weibo.cn/guangxianliuyan
        user_id = inforead.readline()
        #break

    #搜索热点微博 爬取评论
    key = u'欢乐颂'
    GetComment(key)

    infofile.close()
    inforead.close()
