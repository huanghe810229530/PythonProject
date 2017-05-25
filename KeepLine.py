# -*- coding:utf-8 -*-

from threading import Timer
import urllib2
import time

class KeepLine:

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def getPage(self, pageIndex):
        try:
            url = 'http://www.jianshu.com'
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            print '连线成功,可以继续冲浪!'
            # pageCode = response.read().decode('utf-8')
            # print pageCode
            # return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接简书失败，错误原因", e.reason
            return None

    def delayRun(self):
        while True:
            self.getPage(2)
            time.sleep(60*1)



line = KeepLine()
line.delayRun()

# timeInterval = 5
#
# def delayrun():
#     print 'running'
#
# timer = Timer(timeInterval, delayrun)
# timer.start()
#
# while True:
#     delayrun()
#     time.sleep(5)
#
# delayrun()

