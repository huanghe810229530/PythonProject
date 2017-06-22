# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
#oooo
#一定要对齐
#字典对应的key不能写错


# 糗事百科
class QSBK():
    """docstring for QSBK"""

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False
        # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            print pageCode
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败，错误原因", e.reason
            return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None

        pattern = re.compile('<div class="author clearfix">.*?href.*?<img src=.*?(.*?)alt=.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageCode)
        # print len(items)
        pageStories = []
        for item in items:
            # print item[0],item[1],item[2]
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[2])
            pageStories.append([item[0].strip(), item[1].strip(), text.strip(), item[3].strip()])
            return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1


    def getOneStory(self,pageStories,page):
                for story in pageStories:
                    input = raw_input()
                    self.loadPage()
                    if input == "q":
                        self.enable = False
                        return
                    print u"头像地址：-- %s\n发布人:-- %s\t\n发布内容:-- %s\t\n评论数:-- %s" %(story[0],story[1],story[2],story[3])

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStroies = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStroies,nowPage)
            else:
                print "not load"

spider = QSBK()
spider.start()





