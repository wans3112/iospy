#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# ios自动打包ipa上传
#
import thread
import re
import httplib
import os
import urllib2
import time
import json
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

#打包文档:http://192.168.30.6/ios/AppstoreUploadHelp/blob/master/README.md
'''H5资源部地址'''
__H5ZIPURL__ = "http://192.168.30.223/packages/h5/2.7/test/lark.zip"

'''
 环境变量

 @param 1 开发
 @param 2 测试
 @param 3 预发布
 @param 4 生产

 @return 环境
'''
__BF_ENVIRONMENT__ = 4

# 微信生产环境的key
__KEY_WEIXIN__ = "wxec7a94ebfb021991"
# 新浪生产环境的key
__KEY_SINA__   = "sina.55b1c39f67e58e1208006a3f"
# info.plist中需要替换的建值对集合
__PLISTINFO__ = {'weixin': __KEY_WEIXIN__, 'sina': __KEY_SINA__}

# 项目的根目录，(workspace文件目录)
mainPath = os.getcwd() + "/BigFan"
# 项目target名
targetName = "BigFan"
# 项目scheme名
schemeName = "BigFan"

# 生产证书
certificateName = "iPhone Distribution: Beijing Quanyan Network Technology Co., Ltd. (LB5FL2PR9E)"
# 描述文件
profileName = "53e94426-6139-4eeb-8af6-57a82fb653a2"

# 是否是WorkSpace
isWorkSpace = True

# 蒲公英应用上传地址
url = 'http://www.pgyer.com/apiv1/app/upload'
# 蒲公英提供的 用户Key
uKey = 'eac22a676a92964d9ad6708341ea2752'
# 蒲公英提供的 API Key
_api_key = 'bf682e15bec70a02f47ae23077687273'
# 应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装。默认为1公开(选填)
installType = '2'
# 设置App安装密码，如果不想设置密码，请传空字符串，或不传(选填)
installPassword = '123456'
#打包生成的ipa包的地址
ipa_file_path = mainPath + "/" + targetName + ".ipa"


# 上传成功后ipa下载地址（暂无）
ipa_file_tomcat_http_url = "www.baidu.com"
# 邮件接受者
mail_receiver = ['346783916@qq.com']
# 邮箱主机地址 公司邮箱host：smtp.mxhichina.com
mail_host = 'smtp.qq.com'
# 发送者邮箱地址
mail_user = 'wans.wang@quncaotech.com'
# 发送者邮箱密码
mail_pwd = 'WANGbin3112382'

mail_content = '''

更新内容：无

'''

# 生产环境，Bugly的脚本
__SHELLSCRIPT__ = "#!/bin/sh\n#\n# Copyright 2016 Bugly, Tencent. All rights reserved.\n#\n# V1.4.0\n#\n# 2016.08.03\n#\n#\n\n##Debug模式下直接退出\nif [ \"${CONFIGURATION=}\" == \"Debug\" ]; then\nexit\nfi\n\n#\n######################################################\n# 1. 脚本集成到Xcode工程的Target\n######################################################\n#\n# --- Copy the SCRIPT to the Run Script of Build Phases in the Xcode project ---\n#\n# #\nBUGLY_APP_ID=\"f159ca409a\"\n# #\nBUGLY_APP_KEY=\"13f8cb76-e513-4b6d-afc4-62b42cc4de53\"\n# #\nBUNDLE_IDENTIFIER=\"com.quncaotech.lark.participator\"\n# #\nUPLOAD_DSYM_ONLY=1\n#\n# # 脚本默认配置的版本格式为CFBundleShortVersionString(CFBundleVersion),  如果你修改默认的版本格式, 请设置此变量, 如果不想修改, 请忽略此设置\n# CUSTOMIZED_APP_VERSION=\"\"\n#\n# # Debug模式编译是否上传，1＝上传 0＝不上传，默认不上传\n# UPLOAD_DEBUG_SYMBOLS=0\n#\n# # 模拟器编译是否上传，1=上传 0=不上传，默认不上传\n# UPLOAD_SIMULATOR_SYMBOLS=0\n#\n# #只有Archive操作时上传, 1=支持Archive上传 0=所有Release模式编译都上传\n# UPLOAD_ARCHIVE_ONLY=0\n#\n# #\n# source dSYMUpload.sh\n#\n# --- END OF SCRIPT ---\n#\n#\n#\n#\n#######################################################\n# 2. 脚本根据输入参数处理\n#######################################################\n#\n# #命令行下输入应用基本信息, .dSYM文件的父目录路径, 输出文件目录即可\n#\n# sh dSYMUpload.sh <bugly_app_id> <bugly_app_key> <app_bundle_identifier> <app_version> <dSYM_src_dir> <bSYMBOL_dest_dir>\n#\n# #\n#\n# #注意:\n# # 1. dSYMUpload.sh会调用buglySymboliOS.jar进行.dSYM解析，所以依赖Java运行时环境\n# # 2. dSYMUpload.sh和buglySymboliOS.jar的文件路径需一致\n#\n#\n\n#\n# --- CONTENT OF SCRIPT ---\n#\n\n# Bugly服务域名\nBUGLY_DSYM_UPLOAD_DOMAIN=\"api.bugly.qq.com\"\n\n# 注意jar工具的路径跟dSYMUpload.sh脚本路径一致, 请务必保证jar路径的正确性\nBUGLY_SYMBOL_JAR_PATH=\"dsymtool/buglySymboliOS.jar\"\n# 查找添加到系统目录的jar工具\nif [ ! -f \"${BUGLY_SYMBOL_JAR_PATH}\" ]; then\nBUGLY_SYMBOL_JAR_PATH=\"$HOME/bin/buglySymboliOS.jar\"\nfi\n\n# 打印错误信息\nfunction exitWithMessage(){\n    echo \"--------------------------------\"\n    echo \"${1}\"\n    echo \"--------------------------------\"\n    exit ${2}\n}\n\n# 上传bSYMBOL文件\nfunction dSYMUpload() {\n    P_APP_ID=\"$1\"\n    P_APP_KEY=\"$2\"\n    P_APP_BUNDLE_ID=\"$3\"\n    P_APP_VERSION=\"$4\"\n    P_BSYMBOL_ZIP_FILE=\"$5\"\n\n    #\n    P_BSYMBOL_ZIP_FILE_NAME=${P_BSYMBOL_ZIP_FILE##*/}\n        P_BSYMBOL_ZIP_FILE_NAME=${P_BSYMBOL_ZIP_FILE_NAME//&/_}\n            P_BSYMBOL_ZIP_FILE_NAME=\"${P_BSYMBOL_ZIP_FILE_NAME// /_}\"\n\n            DSYM_UPLOAD_URL=\"https://${BUGLY_DSYM_UPLOAD_DOMAIN}/openapi/file/upload/symbol?app_id=${P_APP_ID}&app_key=${P_APP_KEY}\"\n            echo \"dSYM upload url: ${DSYM_UPLOAD_URL}\"\n\n            echo \"-----------------------------\"\n            STATUS=$(/usr/bin/curl -k \"${DSYM_UPLOAD_URL}\" --form \"api_version=1\" --form \"app_id=${P_APP_ID}\" --form \"app_key=${P_APP_KEY}\" --form \"symbolType=2\"  --form \"bundleId=${BUNDLE_IDENTIFIER}\" --form \"productVersion=${BUGLY_APP_VERSION}\" --form \"fileName=${P_BSYMBOL_ZIP_FILE_NAME}\" --form \"file=@${P_BSYMBOL_ZIP_FILE}\" --verbose)\n            echo \"-----------------------------\"\n\n            UPLOAD_RESULT=\"FAILTURE\"\n            echo \"Bugly server response: ${STATUS}\"\n            if [ ! \"${STATUS}\" ]; then\n            echo \"Error: Failed to upload the zip archive file.\"\n            elif [[ \"${STATUS}\" == *\"{\"reponseCode\":\"0\"}\"* ]]; then\n            echo \"Success to upload the dSYM for the app [${BUNDLE_IDENTIFIER} ${BUGLY_APP_VERSION}]\"\n            UPLOAD_RESULT=\"SUCCESS\"\n            else\n            echo \"Error: Failed to upload the zip archive file to Bugly.\"\n            fi\n\n            #Remove temp dSYM archive\n            #echo \"Remove temporary zip archive: ${DSYM_ZIP_FPATH}\"\n            #/bin/rm -f \"${DSYM_ZIP_FPATH}\"\n\n            if [ \"$?\" -ne 0 ]; then\n            exitWithMessage \"Error: Failed to remove temporary zip archive.\" 0\n            fi\n\n            echo \"--------------------------------\"\n            echo \"${UPLOAD_RESULT} - dSYM upload complete.\"\n\n            if [[ \"${UPLOAD_RESULT}\" == \"FAILTURE\" ]]; then\n            echo \"--------------------------------\"\n            echo \"Failed to upload the dSYM\"\n            echo \"Please check the script and try it again.\"\n            fi\n        }\n\n        # .dSYM解析为bSYMBOL文件\n        function dSYMParse() {\n            DSYM_FILE=\"$1\"\n            DSYM_SYMBOL_FILE=\"$2\"\n\n            echo \"--------------------------------\"\n            echo \"Extract symbol info from .dSYM file. to ${DSYM_SYMBOL_FILE}\"\n            (/usr/bin/java -Xms512m -Xmx1024m -Dfile.encoding=UTF8 -jar \"${BUGLY_SYMBOL_JAR_PATH}\" -i \"${DSYM_FILE}\" -o \"${DSYM_SYMBOL_FILE}\" ) || exitWithMessage \"Error: Failed to extract symbols.\" 1\n            echo \"--------------------------------\"\n\n        }\n\n        # 执行\n        function run() {\n\n            CONFIG_BUGLY_APP_ID=\"$1\"\n            CONFIG_BUGLY_APP_KEY=\"$2\"\n\n            CONFIG_BUGLY_APP_BUNDLE_IDENTIFIER=\"$3\"\n            CONFIG_BUGLY_APP_VERSION=\"$4\"\n            CONFIG_DSYM_SOURCE_DIR=\"$5\"\n            CONFIG_DSYM_DEST_DIR=\"$6\"\n            CONFIG_UPLOAD_DSYM_ONLY=\"$7\"\n\n            # 检查必须参数是否设置\n            if [ ! \"${CONFIG_BUGLY_APP_ID}\" ]; then\n            exitWithMessage \"Error: Bugly App ID not defined. Please set 'BUGLY_APP_ID' \" 0\n            fi\n\n            if [[ \"${CONFIG_BUGLY_APP_ID}\" == *\"App ID\"* ]]; then\n            exitWithMessage \"Error: Bugly App ID not defined.\" 0\n            fi\n\n            if [ ! \"${CONFIG_BUGLY_APP_KEY}\" ]; then\n            exitWithMessage \"Error: Bugly App Key not defined.\" 0\n            fi\n\n            if [ ! \"${CONFIG_BUGLY_APP_BUNDLE_IDENTIFIER}\" ]; then\n            exitWithMessage \"Error: Bundle Identifier not defined.\" 0\n            fi\n\n            if [ ! \"${CONFIG_BUGLY_APP_VERSION}\" ]; then\n            exitWithMessage \"Error: App Version not defined.\" 0\n            fi\n\n            if [ ! -e \"${CONFIG_DSYM_SOURCE_DIR}\" ]; then\n            exitWithMessage \"Error: Invalid dir ${CONFIG_DSYM_SOURCE_DIR}\" 0\n            fi\n\n            if [ ! \"${CONFIG_DSYM_DEST_DIR}\" ]; then\n            exitWithMessage \"Error: Invalid dir ${CONFIG_DSYM_DEST_DIR}\" 0\n            fi\n\n            if [ ! -e \"${CONFIG_DSYM_DEST_DIR}\" ]; then\n            mkdir ${CONFIG_DSYM_DEST_DIR}\n            fi\n\n            DSYM_FOLDER=\"${CONFIG_DSYM_SOURCE_DIR}\"\n            IFS=$'\n'\n\n            echo \"Scaning dSYM FOLDER: ${DSYM_FOLDER} ...\"\n            RET=\"F\"\n\n            #\n            for dsymFile in $(find \"$DSYM_FOLDER\" -name '*.dSYM'); do\n            RET=\"T\"\n            echo \"Found dSYM file: $dsymFile\"\n\n            DSYM_FILE_NAME=${dsymFile##*/}\n                DSYM_SYMBOL_ZIP_FILE_NAME=\"${DSYM_FILE_NAME}.zip\"\n                DSYM_SYMBOL_ZIP_FILE_NAME=\"${DSYM_SYMBOL_ZIP_FILE_NAME// /_}\"\n                DSYM_SYMBOL_ZIP_FILE=${CONFIG_DSYM_DEST_DIR}/${DSYM_SYMBOL_ZIP_FILE_NAME}\n\n                if [ $CONFIG_UPLOAD_DSYM_ONLY -eq 1 ]; then\n                if [ -e $DSYM_SYMBOL_ZIP_FILE ]; then\n                rm -f $DSYM_SYMBOL_ZIP_FILE\n                fi\n                # 如果只上传dSYM，直接压缩dSYM目录\n                zip -r -j $DSYM_SYMBOL_ZIP_FILE $dsymFile -x *.plist\n                else\n                # 使用符号表工具来生成Symbol文件\n                dSYMParse $dsymFile $DSYM_SYMBOL_ZIP_FILE\n                fi\n\n                # 上传\n                dSYMUpload $CONFIG_BUGLY_APP_ID $CONFIG_BUGLY_APP_KEY $CONFIG_BUGLY_APP_BUNDLE_IDENTIFIER $CONFIG_BUGLY_APP_VERSION $DSYM_SYMBOL_ZIP_FILE\n                done\n\n                if [ $RET = \"F\" ]; then\n                exitWithMessage \"No .dSYM found in ${DSYM_FOLDER}\" 0\n                fi\n            }\n\n            # 在Xcode工程中执行\n            function runInXcode(){\n                echo \"Uploading dSYM to Bugly in Xcode ...\"\n\n                echo \"Info.Plist : ${INFOPLIST_FILE}\"\n\n                BUNDLE_VERSION=$(/usr/libexec/PlistBuddy -c 'Print CFBundleVersion' \"${INFOPLIST_FILE}\")\n                BUNDLE_SHORT_VERSION=$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' \"${INFOPLIST_FILE}\")\n\n                # 组装Bugly默认识别的版本信息(格式为CFBundleShortVersionString(CFBundleVersion), 例如: 1.0(1))\n                if [ ! \"${CUSTOMIZED_APP_VERSION}\" ]; then\n                BUGLY_APP_VERSION=\"${BUNDLE_SHORT_VERSION}(${BUNDLE_VERSION})\"\n                else\n                BUGLY_APP_VERSION=\"${CUSTOMIZED_APP_VERSION}\"\n                fi\n\n                echo \"--------------------------------\"\n                echo \"Prepare application information.\"\n                echo \"--------------------------------\"\n\n                echo \"Product Name: ${PRODUCT_NAME}\"\n                echo \"Bundle Identifier: ${BUNDLE_IDENTIFIER}\"\n                echo \"Version: ${BUNDLE_SHORT_VERSION}\"\n                echo \"Build: ${BUNDLE_VERSION}\"\n\n                echo \"Bugly App ID: ${BUGLY_APP_ID}\"\n                echo \"Bugly App key: ${BUGLY_APP_KEY}\"\n                echo \"Bugly App Version: ${BUGLY_APP_VERSION}\"\n\n                echo \"--------------------------------\"\n                echo \"Check the arguments ...\"\n\n                ##检查模拟器编译是否允许上传符号\n                if [ \"$EFFECTIVE_PLATFORM_NAME\" == \"-iphonesimulator\" ]; then\n                if [ $UPLOAD_SIMULATOR_SYMBOLS -eq 0 ]; then\n                exitWithMessage \"Warning: Build for simulator and skipping to upload. \nYou can modify 'UPLOAD_SIMULATOR_SYMBOLS' to 1 in the script.\" 0\n                fi\n                fi\n\n                ##检查是否是Release模式编译\n                if [ \"${CONFIGURATION=}\" == \"Debug\" ]; then\n                if [ $UPLOAD_DEBUG_SYMBOLS -eq 0 ]; then\n                exitWithMessage \"Warning: Build for debug mode and skipping to upload. \nYou can modify 'UPLOAD_DEBUG_SYMBOLS' to 1 in the script.\" 0\n                fi\n                fi\n\n                ##检查是否Archive操作\n                if [ $UPLOAD_ARCHIVE_ONLY -eq 1 ]; then\n                if [[ \"$TARGET_BUILD_DIR\" == *\"/Archive\"* ]]; then\n                echo \"Archive the package\"\n                else\n                exitWithMessage \"Warning: Build for NOT Archive mode and skipping to upload. \nYou can modify 'UPLOAD_ARCHIVE_ONLY' to 0 in the script.\" 0\n                fi\n                fi\n\n                #\n                run ${BUGLY_APP_ID} ${BUGLY_APP_KEY} ${BUNDLE_IDENTIFIER} ${BUGLY_APP_VERSION} ${DWARF_DSYM_FOLDER_PATH} ${BUILD_DIR}/BuglySymbolTemp ${UPLOAD_DSYM_ONLY}\n            }\n\n            # 根据Xcode的环境变量判断是否处于Xcode环境\n            INFO_PLIST_FILE=\"${INFOPLIST_FILE}\"\n\n            BuildInXcode=\"F\"\n            if [ -f \"${INFO_PLIST_FILE}\" ]; then\n            BuildInXcode=\"T\"\n            fi\n\n            if [ $BuildInXcode = \"T\" ]; then\n            runInXcode\n            else\n            echo \"\nUsage: dSYMUpload.sh <bugly_app_id> <bugly_app_key> <app_bundle_identifier> <app_version> <dSYM_src_dir> <bSYMBOL_dest_dir> [upload_dsym_only]\n\"\n            # 你可以在此处直接设置BuglyAppID和BuglyAppKey，排除不常变参数的输入\n            BUGLY_APP_ID=\"$1\"\n            BUGLY_APP_KEY=\"$2\"\n            BUNDLE_IDENTIFIER=\"$3\"\n            BUGLY_APP_VERSION=\"$4\"\n            DWARF_DSYM_FOLDER_PATH=\"$5\"\n            SYMBOL_OUTPUT_PATH=\"$6\"\n            UPLOAD_DSYM_ONLY=$7\n            run ${BUGLY_APP_ID} ${BUGLY_APP_KEY} ${BUNDLE_IDENTIFIER} ${BUGLY_APP_VERSION} ${DWARF_DSYM_FOLDER_PATH} ${SYMBOL_OUTPUT_PATH} ${UPLOAD_DSYM_ONLY}\n            fi"

# 下载h5资源包并替换
def downloadZipForH5():
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection("192.168.30.223")
        httpClient.request("GET",__H5ZIPURL__)

        response = httpClient.getresponse()
        total_length = int(response.getheader("Content-Length"))
        print total_length

        if response.status == 200:
            result = response.read()
            fo = open(mainPath + "/BigFan/H5zipfile/venue.zip","wb")
            with fo as code:
                code.write(result)
            print "H5资源包更新成功"

    except Exception,e:
        print "error: %s" % e
    finally:
        if httpClient:
            httpClient.close()

# 替换配置文件
def replaceConfig():
    configPath = os.getcwd() + "/BigFan/Crust/Classes/Main/BFConfigServer.m"
    fo = open(configPath, 'r+')
    fo.seek(0, 0)
    try:
        content = fo.read()
        pattern = re.compile(r'BF_ENVIRONMENT\s+\(\d+\)\n#endif')
        match = pattern.search(content)
        if match:
            result = match.group()
            pattern = re.compile(r'\d+')
            newresult = pattern.sub(str(__BF_ENVIRONMENT__), result)
            content = content.replace(result, newresult)

            # 清空原字文件，写入替换后的内容
            fo = open(configPath, 'w')
            fo.write(content)
            fo.flush()
            print "BFConfigServer配置文件更新成功"
    except Exception, e:
        print "error1: %s" % e

    finally:
        if fo:
            fo.close()

# 替换微信微博key
def replaceInfoPlist():
    configPath = os.getcwd() + "/BigFan/BigFan/Info.plist"
    fo = open(configPath, 'r+')
    fo.seek(0, 0)
    try:
        content = fo.read()
        for key in __PLISTINFO__:
            pattern = re.compile(r"<(string)>%s</\1>((?!\1)[\s\S])*<\1>([^<]+)" % key)
            match = pattern.search(content)
            if match:
                resultcell = match.group(3)
                content = content.replace(resultcell, __PLISTINFO__[key])

        # 清空原字文件，写入替换后的内容
        fo = open(configPath, 'w')
        fo.write(content)
        fo.flush()
        print "Info.Plist配置文件更新成功"

    except Exception, e:
        print "error: %s" % e

    finally:
        if fo:
            fo.close()

# 替换bugly脚本
def replaceShellScript():
    configPath = os.getcwd() + "/BigFan/BigFan.xcodeproj/project.pbxproj"
    fo = open(configPath, 'r+')
    fo.seek(0, 0)
    try:
        content = fo.read()
        for eachline in open(configPath, 'r+'):
            match = re.search("(\s+shellScript = \")(.*)(\")",eachline)
            if match:
                oldshellScript = match.group(2)
                if oldshellScript.startswith("#!/bin/"):
                    pattern = re.compile(r'\\')
                    #/转义还原成//
                    tranString = pattern.sub("\\\\\\\\", __SHELLSCRIPT__)
                    #换行转义还原成/n
                    tranString = tranString.replace("\n", "\\n")
                    #"转义还原成/"
                    tranString = tranString.replace("\"", "\\\"")
                    #生产脚本替换原有脚本代码
                    content = content.replace(oldshellScript, tranString)
                    break

        # 清空原字文件，写入替换后的内容
        fo = open(configPath, 'w')
        fo.write(content)
        fo.flush()
        print "ShellScript配置文件替换成功"
    except Exception, e:
        print "error2: %s" % e

    finally:
        if fo:
            fo.close()

# 编译
def buildapp():
    global mainPath
    global targetName
    global certificateName

    # os.system("cd %s;xcodebuild clean"%mainPath)
    if isWorkSpace:
        os.system("cd %s;xcodebuild -workspace %s.xcworkspace -scheme %s -configuration Release -sdk iphoneos build CODE_SIGN_IDENTITY='%s' PROVISIONING_PROFILE='%s'"%(mainPath,schemeName,targetName,certificateName,profileName))
    else:
        os.system("cd %s;xcodebuild -target %s CODE_SIGN_IDENTITY='%s' PROVISIONING_PROFILE='%s'" % (mainPath, targetName, certificateName,profileName))

# 签名生成ipa
def createipa():
    global mainPath
    global targetName
    global certificateName

    if not os.path.exists(mainPath + '/build/Build/Products/Release-iphoneos/%s.app' % targetName):
        return

    os.system("cd %s;rm -r -f %s.ipa" % (mainPath, targetName))
    os.system("cd %s;xcrun -sdk iphoneos PackageApplication -v %s/build/Build/Products/Release-iphoneos/%s.app -o %s/%s.ipa CODE_SIGN_IDENTITY='%s'"
              % (mainPath, mainPath, targetName, mainPath, targetName, certificateName))

# 设置httpheader
def _encode_multipart(params_dict):
    print "开始上传ipa至蒲公英！"
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in params_dict.items():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            content = v.read()
            decoded_content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="kangda.ipa"' % k)
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(decoded_content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

# 处理 蒲公英 上传结果
def handle_resule(result):
    json_result = json.loads(result)
    if json_result['code'] is 0:
        print "上传成功！开始发送邮件"
        send_email(json_result)
    else:
        print "上传失败"

# 上传ipa
def uploadipa():
    if not os.path.exists(ipa_file_path):
        return
    # 请求参数字典
    params = {
        'uKey': uKey,
        '_api_key': _api_key,
        'file': open(ipa_file_path, 'rb'),
        'installType': '2',
        'password': installPassword
    }

    coded_params, boundary = _encode_multipart(params)
    req = urllib2.Request(url, coded_params.encode('ISO-8859-1'))
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    try:
        resp = urllib2.urlopen(req)
        body = resp.read().decode('utf-8')
        handle_resule(body)

    except urllib2.HTTPError as e:
        print(e.fp.read())


# 发送邮件
def send_email(json_result):
    appName = json_result['data']['appName']
    appKey = json_result['data']['appKey']
    appVersion = json_result['data']['appVersion']
    appBuildVersion = json_result['data']['appBuildVersion']
    appShortcutUrl = json_result['data']['appShortcutUrl']

    mail_to = ','.join(mail_receiver)
    msg = MIMEMultipart()

    environsString = '<h3>本次打包相关信息</h3><p>'
    environsString += '<p>ipa 包下载地址 : ' + ipa_file_tomcat_http_url + '<p>'
    environsString += '<p>你也可从蒲公英网站在线安装 : ' + 'http://www.pgyer.com/' + str(
        appShortcutUrl) + '   密码 : ' + installPassword + '<p>'
    environsString += '<li><a href="itms-services://?action=download-manifest&url=https://ssl.pgyer.com/app/plist/' + str(
        appKey) + '">点我直接安装</a></li>'
    environsString += mail_content;
    message = environsString
    body = MIMEText(message, _subtype='html', _charset='utf-8')
    msg.attach(body)
    msg['To'] = mail_to
    msg['from'] = mail_user
    msg['subject'] = '最新打包文件'

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pwd)

        s.sendmail(mail_user, mail_receiver, msg.as_string())
        s.close()

        print '邮件发送成功'
    except Exception, e:
        print "邮件发送失败，error：%s" % e

def main():

    downloadZipForH5()

    replaceConfig()

    replaceInfoPlist()

    replaceShellScript()

    buildapp()

    createipa()

    uploadipa()

if __name__ == '__main__':
    main()
