# -*- coding: utf-8 -*-
import os
import os.path
import re
import codecs
import PinyinTest

'''
扫描项目目录并记录module java代码路径
'''
def scan2dfiremanager(dfireprojectpath):
    for entry in os.scandir(dfireprojectpath):
        if entry.is_dir():
            rootNames.append(entry.name)
            # print("文件夹路径: " + entry.path)
            #entry.path 是各个仓库的根路径
            scanmodulemanager(entry.path, False)
        elif entry.is_file():
            # print("文件路径: " + entry.path)
            continue

def scanmodulemanager(path, isSecond):
    for module in os.scandir(path):
        if module.is_dir():
            if module.name == ("src"):
                # print("一层module路径" + module.path)
                modulePaths.append(module.path + '/main/java')
                name = os.path.basename(os.path.dirname(module.path)) #取 module 名
                moduleNames.append(name)
            else:
                # print("非一层module路径" + module.path)
                if isSecond:
                    continue;
                else:
                    # print("开始二层扫描 当前path = " + module.path)
                    scanmodulemanager(module.path, True)


def openFileStream(moduleDir):
    global generatedStringFileOpen
    #翻译转换后的路径
    generatedRootDir = diskPath + translateRootName
    generatedStringDir = generatedRootDir + moduleDir + "/src/main/res/values"

    if not os.path.exists(generatedStringDir):
        os.makedirs(generatedStringDir)

    # stringPath = generatedStringDir + "/string.xml"    #by:hongshen
    stringPath = translatePath + "/string.xml"
    generatedStringFileOpen = codecs.open(stringPath, 'a', 'utf-8')
'''*****************************************************************2018.05.28***********************************************************************'''
def traverseFile(dir):
    '''
    遍历所有的目录
    :param dir:
    :return:
    '''
    i = 0
    for parent,dirNames,filenames in os.walk(dir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # 当前文件夹下文件内容
        #输出文件信息
        i = i + 1
        for filename in filenames:
            # 文件内容
            # print ("parent:" + parent + "\n" + "filename is:" + filename)
            if filename.startswith("."):
                continue
            filePath = parent + "/" + filename
            transFilePath = filePath.replace(rootName,translateRootName)
            transParent = parent.replace(rootName,translateRootName)
            translate(transParent,filePath,transFilePath)

def translate(transParent,oldFilePath,transFilePath):
    '''
    匹配 "" 中的文字，然后进行过滤，最后写入文件
    :param transParent:
    :param oldFilePath:
    :param transFilePath:
    :return:
    '''
    global replaceCount
    global ifWriteImportLine
    oldFileOpen = codecs.open(oldFilePath,'r','utf-8')
    if not os.path.exists(transParent):
        os.makedirs(transParent)
    transFileOpen = codecs.open(transFilePath,'w','utf-8')
    lines = oldFileOpen.readlines()
    for line in lines:
        # newLine = line.encode('utf-8')
        newLine = line
        line.strip('\n')
        strList = pattern.findall(line)
        if not (strList == None or strList.__len__() == 0):
            # 匹配到了，修改line，然后写入文件
            # 过滤 Log comments 返还是 true 表示 需要过滤
            if not filterPattern(line):
                newLine = translateLine(strList,newLine)
                ifWriteImportLine = True
                # print transFilePath
                replaceCount = replaceCount + 1
        transFileOpen.write(str(newLine))

    transFileOpen.close()
    if ifWriteImportLine:
        writeImportLine(transFilePath)
        ifWriteImportLine = False
    oldFileOpen.close()

def writeImportLine(fileName):
    '''
    写入 import 内容
    :param fileName:
    :return:
    '''
    # f = open(fileName,'r', encoding = 'utf-8')
    f = codecs.open(fileName, 'r', 'utf-8')

    tempLines = f.readlines()
    f.close()

    # f = open(fileName,'w')
    f = codecs.open(fileName,'w','utf-8')

    flag = True
    for line in tempLines:
        f.write(str(line))
        if flag:
            f.write(str(importLine))
            flag = False
    f.close()

def filterPattern(line):
    '''
    过滤掉 log 和 注释
    此处也可以加入其他 pattern 进行过滤
    :param line:
    :return: boolean true 需要过滤，false 不过滤
    '''
    logList = patternLog.findall(line)
    if logList != None and logList.__len__() > 0:
        return True
    # 当前行必然有 string ，正则只需要匹配是 注释类型，
    # 如果是，那么直接返回 true 过滤
    # 否则 返回 false 不过滤
    commentList = patternComments.findall(line)
    if commentList != None and commentList.__len__() > 0:
        return True
    return False

def translateLine(strList,newLine):
    '''
    把字符串变化成 R.string.字符串
    写入 string.xml 文件中
    :param strList:
    :param newLine:
    :return:
    '''
    for str in strList:
        stringName = stringNamePattern.search(str)

        # strId = str.encode('utf-8')                                                                          by:hs
        strId = str

        stringValue = strId.split('\"')[1]
        # 替换 java 文件中的中文字符成 R.string.{中文字符}
        newLine = writeToStringFile(stringValue,stringName,newLine,strId)
        # newLine = newLine.replace(strId,'QuickApplication.getStringFromR(R.string.'+ stringValue + ")")
    return newLine

def writeToStringFile(stringValue, stringName, oldLine, oldStrKey):
    '''

    :param stringValue: 中文字符
    :param stringName: 切出来的中文内容，变换后可以得到新的 key
    :param oldLine: 整行内容
    :param oldStrKey: 原来的 id 值
    :return:
    '''
    global stringCount

    same = False

    '''
        值去重
    '''
    # rStringKey = ''.join(stringName.group()).encode('utf-8')                                                  by:hs
    rStringKey = ''.join(stringName.group())
    # oldLine = oldLine.decode('utf-8')

    #中文转拼音
    rStringKey = test.hanzi2pinyin_split(string=rStringKey, split="_")

    newLine = oldLine.replace(oldStrKey, functionName + '(R.string.' + rStringKey + ")")

    if listString.__len__() == 0:
        listString[rStringKey] = stringValue
        listStringKey.append(rStringKey)
        rStringValue = '<string name="' + rStringKey + '">' + stringValue +  '</string>\n'
        generatedStringFileOpen.write(str(rStringValue))
        stringCount = stringCount + 1
        return newLine

    # 遍历所有的值 如果有相同的，直接替换掉
    for key in listString.keys():
        if listString[key] == stringValue:
            newLine = oldLine.replace(oldStrKey, functionName + '(R.string.' + key + ")")
            same = True
            break

    # 有相同的
    # 无需写入 string 文件，直接返回整行
    if same:
        # rStringValue = '<string name="' + rStringKey + '">' + stringValue +  '</string>\n'
        # generatedStringFileOpen.write(unicode(rStringValue,"utf-8"))
        return newLine
    else:
        # 需要遍历所有的 key，变换出新的 key
        # 看新切出来的 key 和老的 key 是否会相同
        # 相同就变换新的 key，放入 dic 中
        # 不同的 不用管
        i = 0
        for stringKey in listStringKey:

            if stringKey == rStringKey:
                # 切出来的新 key 和老 key 相同
                if i == 0:
                    i = i + 1
                    rStringKey = rStringKey + '_' + str(i)
                else:
                    rStringKey = rStringKey.replace(str(i),str(i + 1))
                    i = i + 1

    listString[rStringKey] = stringValue
    listStringKey.append(rStringKey)

    rStringValue = '<string name="' + rStringKey + '">' + stringValue +  '</string>\n'
    generatedStringFileOpen.write(str(rStringValue))
    newLine = oldLine.replace(oldStrKey, functionName + '(R.string.' + rStringKey + ")")
    stringCount = stringCount + 1
    return newLine

'''
整体运行部分
该部分需要自定义文件目录
自定义生成的目录
还有修改获取字符串的方法
需要导入的 R 文件以及 AppContextWrapper 之类的获取字符串方法的类
'''
#代码硬盘路径   :可修改
diskPath = "D:/AndroidStudio/AndroidProject/Checkout3/"

translatePath = "D:/translateTemp/replace2018.05.28/Atranslate/"

# 替换获取字符串的方法
functionName = "AppContextWrapper.getString"
#  import 的内容
importLine = "\nimport com.zmsoft.AppContextWrapper;\n"
#  是否需要插入 import
ifWriteImportLine = False

#加载拼音类
test = PinyinTest.PinYin()
test.load_word()

listStringValue = []
listStringKey = []
listString = {}

# 匹配当前行中是否有字符串
pattern = re.compile(r'(\"[^\"]*[\u4e00-\u9fa5]+[^\"]*\")')
replaceCount = 0
stringCount = 0
# 过滤 log 信息
patternLog = re.compile(r'Logger|LogUtils|JLog|Log\.+')
# 过滤 comments 信息
patternComments = re.compile(r'\ *(.)*(\/\/)+|[\*]+|(\/\*)+')
# 字符串的 key
stringNamePattern = re.compile(r'[\u4e00-\u9fa5]+')

'''*****************************************************'''
modulePaths = [] #记录 diskPath 目录下 所有module的src/main/java 目录path
moduleNames = [] #记录 所有module 名字
rootNames = [] #记录 所有 仓库名
rootName = "1"
scan2dfiremanager(diskPath)
for idx,true_dir in enumerate(modulePaths):
    print('第' + str(idx) + '个module开始扫描 module path is：' + true_dir)
    for name in rootNames:
        if true_dir.find(name)>=0:
            rootName = name
            print("rootName: " + rootName)
    translateRootName = rootName + "_translate"
    openFileStream('/' + moduleNames[idx])
    traverseFile(true_dir)   #by:0528
    generatedStringFileOpen.close()
    print(replaceCount)
    print(stringCount)


