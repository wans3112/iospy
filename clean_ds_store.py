#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 批量删除.DS_Store文件
#

import os

allfiles = []

targetPath = os.getcwd() + "/"


# 移除所有 .DS_Store 文件
def remove_ds_store_files():
    for filename in allfiles:
        if filename.endswith(".DS_Store") and os.path.isfile(filename):
            print filename
            # 移除git版本库
            os.system("cd %s;git rm --cached %s" % (targetPath, filename))
            # 移除文件
            os.system("cd %s;rm %s" % (targetPath, filename))

    # 创建.gitignore文件
    fo = open(targetPath + ".gitignore", 'w')
    fo.write(".DS_Store")
    fo.flush()

    # 提交.gitignore文件
    os.system("cd %s;git add .gitignore;git commit -a -m \"ignore .DS_Store file\";git push origin master" % targetPath)

# 返回指定目录所有文件
def find_files_list(target_dir):
    global allfiles
    files = os.listdir(target_dir)
    for filename in files:
        subdir = os.path.join(target_dir, filename)
        if os.path.isfile(subdir):
            allfiles.append(subdir)
        else:
            find_files_list(subdir)

def main():
    find_files_list(targetPath)

    remove_ds_store_files()

if __name__ == '__main__':
    main()
