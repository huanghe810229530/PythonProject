# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

#复制粘贴难以对齐，报语法错误
#建立处理页面标签的类
#匹配最后一个span标签：re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
#爬取内容写入到txt文件


#处理页面标签类
class ReplaceTool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = ReplaceTool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return  None

    #获取帖子标题
    def getTitle(self, page):
    	#<h3 class="core_title_txt pull-left text-overflow  " title="纯原创我心中的NBA2014-2015赛季现役50大" style="width: 396px">纯原创我心中的NBA2014-2015赛季现役50大</h3>
    	pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
    	result = re.search(pattern, page)
    	if result:
    		print result.group(1)

    #获取帖子一共有多少页
    def getPageNum(self, page):
    	#<li class="l_reply_num" style="margin-left:8px" ><span class="red" style="margin-right:3px">141</span>回复贴，共<span class="red">5</span>页</li>
    	pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
    	result = re.search(pattern,page)
    	if result:
        	# print result.group(1)  #测试输出
        	return result.group(1).strip()
    	else:
        	return None

    def getContent(self, page):
    	pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
    	items = re.findall(pattern,page)
    	contents = []
    	for item in items:
    		content = "\n" + self.tool.replace(item) + "\n"
    		contents.append(content.encode('utf-8'))
    	return contents
    		# print floor, u"楼------------------------------------------------------------------------------------------------------------------------------------\n"
    		# print self.tool.replace(item)
    		# floor += 1

    def setFileTitle(self, title):
    	if title is not None:
    		self.file = open(title + ".txt", "w+")
    	else:
    		self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
    	#向文件写入每一楼的信息
    	for item in contents:
    		if self.floorTag == '1':
    			#楼之间的分隔符
    			floorLine = "\n" + str(self.floor) + u"------------------------------------------------------------------------------------------------------------------------------------\n"
    			self.file.write(floorLine)
    		self.file.write(item)
    		self.floor += 1

    def start(self):
    	indexPage = self.getPage(1)
    	pageNum = self.getPageNum(indexPage)
    	title = self.getTitle(indexPage)
    	print title
    	self.setFileTitle(title)
    	if pageNum == None:
    		print "URL已失效，请重试"
    		return
    	try:
    		print "该帖子共有" + str(pageNum) + "页"
    		for i in range(1,int(pageNum)+1):
    			print "正在写入第" + str(i) + "页数据"
    			page = self.getPage(i)
    			contents = self.getContent(page)
    			self.writeData(contents)
    	except IOError, e:
    		print "写入异常，原因" + e.message
    	finally:
    		print "写入任务完成"




print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/3138733512'
seeLZ = raw_input("是否只获取楼主信息，是输入1，否则输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否则输入0\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()
# page = bdtb.getPage(1)
# bdtb.getContent(page)










