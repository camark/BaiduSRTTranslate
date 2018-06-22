import re
import urllib.request
import random
import hashlib
import http.client
import json
from tkinter import *
import tkinter.filedialog



class ZimuObj:
    def __init__(self,index,start_time,end_time,title):
        self.index=index
        self.start_time=start_time
        self.end_time=end_time
        self.title=title

    def writetofile(self,f):
        f.write(self.index)
        f.write('\n')
        f.write('%s --> %s' % (self.start_time,self.end_time))
        f.write('\n')
        f.write(self.title)
        f.write('\n')
        f.write('\n')

class BaiduTranslate:
    def __init__(self,appid,appKey):
        self.appid=appid
        self.secretKey=appKey
        self.url='http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.salt = random.randint(32768, 65536)  
                

    def translate(self,content,fromLang,toLang):
        q=content
        self.sign = self.appid + q + str(self.salt) + self.secretKey
        self.sign = hashlib.md5(self.sign.encode()).hexdigest()
        myurl=self.url
        myurl = myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(self.salt) + '&sign=' + self.sign
        try:  
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')  
            httpClient.request('GET', myurl)  
            # response是HTTPResponse对象  
            response = httpClient.getresponse()  
            jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式
            #print(jsonResponse)
            js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构  
            dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
            s=''
            for s1 in js['trans_result']:
                s=s+s1['dst']
            #print(s) # 打印结果
            return s
        except Exception as e:  
            print(e)  
        finally:  
            if httpClient:  
                httpClient.close()  

def convert():
    srcfile=lb.cget("text")
    #print(srcfile)
    #return
    if len(srcfile)==0:
        return
    
    with open(srcfile,'r',encoding='UTF-8') as f:
            text=f.read()
    splits = [s.strip() for s in re.split(r'\n\s*\n', text) if s.strip()]
    regex = re.compile(r'''(?P<index>\d+).*?(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})\s*.*?\s*(?P<text>.*)''', re.DOTALL)
    bt=BaiduTranslate('Your appid','Your key')
    fromLang='en'
    toLang='zh'

    zs=[]
    for s in splits:
     r = regex.search(s)
     #print r.groups()
     rg=r.groups()
     subt = rg[-1]
     subt_chn=bt.translate(subt,fromLang,toLang)

     z1=ZimuObj(rg[0],rg[1],rg[2],subt_chn)
     zs.append(z1)
     #print(subt_chn)

    with open('dest.srt','w') as fd:
        for b in zs:
            b.writetofile(fd)


def xz():
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:            
        lb.config(text = filenames[0])
    else:
        lb.config(text = "");
root=Tk()
root.title("英文字幕百度转换")
root.geometry('300x200')                 #是x 不是*
#root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True

lb = Label(root,text = '')
lb.pack()
btn = Button(root,text="选择文件",command=xz)
btn.pack(side=LEFT)
btnConvert = Button(root,text="转换",command=convert)
btnConvert.pack(side=RIGHT)
root.mainloop()
