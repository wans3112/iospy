#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 清除项目中未引用的.m文件
#

import os
import re
import shutil

allfiles = []

targetPath = "/Users/wans/Documents/lark_iOS/BigFan/Crust"
# targetPath = "/Users/wans/Documents/python/find/SpreadViews"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def fetch_filename_fromdir(dirname):
	pattern = re.compile(r'([^\\/:*?"<>|\r\n]+)\.m')
	match = pattern.search(dirname)
	if match:
		return match.group(1)

# 加载.m文件
def load_list_m():
	temp_m_list = []
	for filename in allfiles:
		if filename.endswith(".m"):
			truename = fetch_filename_fromdir(filename)

			fo = open(filename, 'r')
			content = fo.read()
			pattern = re.compile(r'IMPLEMENT_LOAD\((\S+)\)')
			match = pattern.search(content)
			if match:
				filename = match.group(1)
			else:
				filename = truename

			sub_file_exist = True
			# print filename
			for sub_file_name in allfiles:
				fo = open(sub_file_name, 'r')
				sub_file_content = fo.read()
				sub_truename = fetch_filename_fromdir(sub_file_name)

				if filename in sub_file_content:
					if truename == sub_truename:
						continue
					else:
						if truename.startswith("BF"):
							sub_file_exist = False
						break

			if not sub_file_exist:
				temp_m_list.append(filename)
				print "\033[91m不存在引用文件：%s\033[91m" % truename
			# else:
				# print "存在引用文件：%s" % truename

	return temp_m_list

# 返回指定目录所有文件
def find_files_list(target_dir):
	global allfiles
	files = os.listdir(target_dir)
	for filename in files:
		subdir = os.path.join(target_dir, filename)
		if os.path.isfile(subdir):
			allfiles.append(subdir)
			# print subdir
		else:
			find_files_list(subdir)

def main():
	find_files_list(targetPath)
	print "发现 %d 个文件" % len(allfiles)
	files_m = load_list_m()
	print "发现 %d 个.m文件" % len(files_m)



if __name__ == '__main__':
	main()
