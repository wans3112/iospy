#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 清除项目中由于git冲突生成的临时文件
#
import math
import os
import re

print "hello world!";

def printinfo(arg1,*wans):
	pass
	print arg1
	for x in range(len(wans)):
		print wans[x] , x
		pass
	print dir()
	print globals()
	return;

def inputstring():
	str = raw_input("请输入：");
	print str
	pass

def createfile(filename,content):
	file = open(filename,"w+")
	file.write(content)

	file.close();
	pass

#寻找git合并冲突文件 wans1
def findMergeFiles(dir):
    allfiles =  os.listdir(dir);
    global filecount;
    for filename in allfiles:
    	subDir = os.path.join(dir,filename);
    	if os.path.isfile(subDir):
    		result = re.search("[\._][A-Z]+[\._]\d+\.",filename)
    		if result:
    			print filename
    			filecount +=1
    			#os.remove(subDir) 删除冲突文件
    		else:
    			pass
        else :
            findMergeFiles(subDir)
            #print subDir

#printinfo(10,1,2,3,4,"wans");
#inputstring();
#createfile("help.txt","wans");

filecount = 0
try:
	findMergeFiles("/Users/wans/Documents/lark_iOS/BigFan")
	pass
except Exception, e:
	raise e
else:
	pass
finally:
	print "找到 %d 个文件" % (filecount)
	pass
