#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 清除项目中未引用的图片
#
import os
import re
import shutil

filecount = 0
fileList = []

targetPath = "/Users/wans/Documents/python/find/SpreadViews"
targetImagePath = "/Users/wans/Documents/python/find/Outdoor"

# targetPath = "/Users/wans/Documents/lark_iOS/BigFan"
# targetImagePath = "/Users/wans/Documents/lark_iOS/BigFan/BigFan/Assets.xcassets"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

#根据字符串在文件中查找
def findImageWithPath(imagename,filePath):
	fileObj = open(filePath, 'r')
	isexist = False

	packagePattern = imagename
	pattern = re.compile(r'\d+')
	if pattern.search(imagename):
		# 将数字替换替换乘正则表达式，组装成一个整体匹配的正则
		packagePattern = pattern.sub('\d*%\d*[@d]|\d+', imagename)
		# print packagePattern
	for eachLine in fileObj:
		if re.search(packagePattern, eachLine):
			isexist = True
			break
	fileObj.close()

	return isexist

#加载图片
def loadImageList(string):
	tempList = []

	imageList = findFilesList(string,True)
	for filename in imageList:
		if (filename.endswith("png")):
			tempList.append(filename);
		pass
	return tempList

# 返回指定目录所有文件
def findFilesList(dir,isAddPath):
	allfiles =  os.listdir(dir)
	global filecount
	global fileList
	for filename in allfiles:
		subDir = os.path.join(dir,filename);
		if os.path.isfile(subDir):
			if isAddPath:
				fileList.append(subDir)
			else :
				fileList.append(filename)
			#findString(subDir)
			# print filename
			filecount +=1
		else :
			findFilesList(subDir,isAddPath)
			pass
	return fileList

def main():
   global targetImagePath
   global targetPath

   needinput = raw_input("手动输入目录 y/n:")
   if needinput == "y":
		targetImagePath = raw_input("请输入图片目录：")
   imagelist = loadImageList(targetImagePath)
   for pngname in imagelist:
		print pngname
   print "找到图片 %d 个文件" % (len(imagelist))

   #清空列表
   del fileList[:]
   if needinput == "y":
		targetPath = raw_input("请输入文件查找目录：")

   findFilesList(targetPath,True)
   for filename in fileList:
		print filename
   print "找到文件 %d 个文件" % (len(fileList))

   print "--------------------------------扫描开始--------------------------------"

   notexistList = []
   for pngname in imagelist:
	   isexist = False
	   # 图片全称
	   fullImagename = pngname[pngname.rindex("/") + 1:len(pngname)]
	   # 图片名（不包含后缀）
	   imagename = ""
	   try:
		   if ("@" in fullImagename):
			   imagename = fullImagename[0:fullImagename.index("@")]
		   else:
			   imagename = fullImagename[0:fullImagename.index(".")]
	   except Exception as e:
		   print "发现错误 %s" % fullImagename
		   raise e
	   finally:
		   pass

	   for filename in fileList:
		   # 如果是图片的json配置文件就忽略
		   if filename.endswith("Contents.json"):
			   continue
		   if (findImageWithPath(imagename, filename)):
			   print "存在图片：%s" % fullImagename
			   isexist = True
			   break
	   if not isexist:
		   notexistList.append(pngname)
		   print "\033[91m不存在图片：%s \033[0m" % fullImagename


   print "--------------------------------扫描结束--------------------------------"
   for path in notexistList:
		print "\033[91m%s\033[0m" % path
   print "---------------------总找到 \033[91m%d\033[0m 图片资源未被引用---------------------" % len(notexistList)
   state = raw_input("确定要删除所有未引用的图片吗 y/n:")
   if state == "y":
		for path in notexistList:
			#图片路径
			imagepath = path[0:path.rindex("/")]
			#删除冲突文件
			if os.path.exists(imagepath):
				shutil.rmtree(imagepath)
			print "\033[91m已删除%s\033[0m" % imagepath

if __name__ == '__main__':
	main()
