#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 批量更新子模块代码
#
import os
import re

# profile文件目录
ROOT_PATH = os.getcwd()
# ROOT_PATH = "/Users/wans/Documents/lark_iOS/BigFan"

# 业务模块名
MODULES_NAMES = ['Crust', 'Match', 'TalentC', 'Stadium', 'Club']
# 本地路径名
MODULES_PATHS = ['../../Crust', '../../Match', '../../TalentC', '../../Stadium', '../../Club']
# 项目远程地址
MODULES_URLS = ['http://192.168.30.6/platform/Crust.git', 'http://192.168.30.6/match/Match.git', 'http://192.168.30.6/talent/TalentC.git', 'http://192.168.30.6/stadium/Stadium.git', 'http://192.168.30.6/club/Club.git']
# 最新的分支（与模块名列表对应）
MODULES_BRANCHS = ['release/3.0', 'release/3.0', 'release/3.0', 'release/3.0', 'release/3.0']

def update_project():

    # 关闭Xcode
    os.system("killall Xcode")

    # 批量更新业务模块
    for path in MODULES_PATHS:
        index = MODULES_PATHS.index(path)
        sub_moudle_dir = os.path.join(ROOT_PATH, path)
        if os.path.exists(sub_moudle_dir):
            print "start update >> %s" % MODULES_NAMES[index]
            os.system("cd %s;git -C %s pull" % (ROOT_PATH, path))
        else:
            print "start clone >> %s" % MODULES_NAMES[index]
            os.system("cd %s;git clone %s %s;cd %s;git checkout -b %s origin/%s" % (ROOT_PATH, MODULES_URLS[index], path, path, MODULES_BRANCHS[index], MODULES_BRANCHS[index]))

    print "start update >> lark_ios"
    # 更新主目录(注意：此处主项目有修改请先提交，不然后果自负)
    os.system("cd %s;git reset --hard;git clean -d -fx"";git pull;git status" % ROOT_PATH)

    # 更新podfile，替换为本地路径
    update_podfile()

    # pod install
    os.system("cd %s;pod install" % ROOT_PATH)

    # 打开Xcode,(Xcode与应用里当前xcode名相同)
    os.system("cd %s;open -a Xcode BigFan.xcworkspace/" % ROOT_PATH)

# 更新Podfile文件
def update_podfile():
    podfile_path = ROOT_PATH + "/Podfile"

    fo = open(podfile_path,'r+')
    content = fo.read()
    for eachline in open(podfile_path,'r+'):
        pattern = re.compile(r'\'(\w+)\', :(\w+) => (.+)')
        match = pattern.search(eachline)
        if match:
            module_name = match.group(1)
            if module_name in MODULES_NAMES:
                index = MODULES_NAMES.index(module_name);
                type_name = match.group(2)
                if not (type_name == 'path'):
                    eachline_new = "  pod '%s', :path => '%s'\n" % (module_name, MODULES_PATHS[index])
                    content = content.replace(eachline, eachline_new)

    # 清空原字文件，写入替换后的内容
    fo = open(podfile_path, 'w')
    fo.write(content)
    fo.flush()

def main():
    update_project()

if __name__ == '__main__':
    main()