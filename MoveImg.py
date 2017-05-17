# -*- coding:utf-8 -*-
import os
import shutil

fileDir = "/Users/guchengfeng/Desktop/other/taomm1"
finalPath = "/Users/guchengfeng/Desktop/other/taommAll"

class Move:

    def __init__(self):
        self.fileDir = fileDir
        self.finalPath = finalPath

    def GetFileNameAndExt(self, filename):
        (filepath, tempfilename) = os.path.split(filename);
        (shotname, extension) = os.path.splitext(tempfilename);
        return [shotname, extension]

    def test(self, dir):
        count = 0
        for dirPath, dirNames, fileNames in os.walk(dir):
            print (dirPath)
            for aFile in fileNames:
                filePath = os.path.join(dirPath, aFile)
                if os.path.exists(finalPath) == False:
                    os.makedirs(finalPath)
                if os.path.isfile(filePath):
                    fn = self.GetFileNameAndExt(filePath)
                    if fn[1] == '.jpg':
                        try:
                            count += 1
                            shutil.move(filePath, finalPath)
                        finally:
                            print '移动文件完成'
                        print filePath
        print '共有' + str(count) + '照片'


    def enumDir(self, dir):
        for dir in os.listdir(dir):
            print os.path.abspath(dir)
            # for file in dir:
            #     print (os.path.abspath(file))


mover = Move()
mover.test(fileDir)
# mover.enumDir(fileDir)