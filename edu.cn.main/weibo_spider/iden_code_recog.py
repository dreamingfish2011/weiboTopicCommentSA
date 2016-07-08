__author__ = 'zhuhongmei'
#############
#文件名：iden_code_recog.py
#说明：识别二维码图片
#日期：2016-07-07
#####################
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps
import sys
class IdenCodeRecog:
####使用img处理工具将图片进行清晰化处理：灰度化，灰度反转和二值处理等
    def cleanImage(self,imagePath):
        image = Image.open(imagePath)
        image = image.convert('RGBA')
        image = self.binarize_img(image)
        image.save(imagePath)
        #image = image.point(lambda x :0 if x<143 else 255)
        borderImage = ImageOps.expand(image,border=0,fill ='white')
        borderImage.save(imagePath)

    def binarize_img(self,img):
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x,y][0] < 100 or pixdata[x,y][1] < 100 or pixdata[x,y][2] < 100 :
                    pixdata[x,y] = (0,0,0,255)
                else :
                    pixdata[x,y] = (255,255,255,255)
        return img

    def recog_iden_code_image(self,imageLocation,imagename):
        #html = urlopen("http://pythonscraping.com/humans-only")
        #bsObj = BeautifulSoup(html,"html.parser")
        #imageLocation = bsObj.find("img",{"title":"Image CAPTCHA"})["src"]
        #formBuildId = bsObj.find("input",{"name":"form_build_id"})["value"]
        #captchaSid = bsObj.find("input",{"name":"captcha_sid"})["value"]
        #captchaToken = bsObj.find("input",{"name":"captcha_token"})["value"]
        #captchaUrl = "http://pythonscraping.com" + imageLocation
        jpgname = imagename+".jpg"
        txtname = imagename+".txt"
        urlretrieve(imageLocation,jpgname)
        self.cleanImage(jpgname)
        p = subprocess.Popen(["tesseract",jpgname,imagename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.wait()
        f=open(txtname,"r",encoding='utf-8')
        captchaResponse = f.read().replace(" ","").replace("\n","")
        print("captcha=========="+captchaResponse)
        return captchaResponse
