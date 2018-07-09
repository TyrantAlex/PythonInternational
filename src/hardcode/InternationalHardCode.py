# 2018.05.28
import os
#代码硬盘路径   :可修改
diskPath = "D:/AndroidStudio/AndroidProject/Checkout3/ManagerChargeModule/src/main/java" #文件夹目录
diskPathTest = "D:/translateTemp/replace2018.05.28"

# def listdir(path, list_name):
#     for file in os.listdir(path):
#         file_path = os.path.join(path, file)
#         if file_path.__contains__('/build'):
#         	continue
#         elif os.path.isdir(file_path):
#             listdir(file_path, list_name)
#         # elif os.path.splitext(file_path)[1]=='.jpeg':
#         #     list_name.append(file_path)
#         else:
#         	print ("filename is:" + file_path)

# listdir(diskPath,'1')

files = []

#扫描单个路径 并将所有文件列入files数组
# def scanDir(path):
#     for entry in os.scandir(path):
#         file_path = entry.path
#         if entry.is_dir():
#             scanDir(file_path)
#         elif entry.is_file():
#             files.append(entry.path)

# scanDir(diskPath)
# for filePath in files:
#     print(filePath)
#     print("")
# print(len(files))

'''
扫描项目目录并记录module java代码路径
'''
modulePaths = []

def scan2dfiremanager(dfireprojectpath):
    for entry in os.scandir(dfireprojectpath):
        if entry.is_dir():
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
                name = os.path.basename(os.path.dirname(module.path))
                print("取module名name " + name)
            else:
                # print("非一层module路径" + module.path)
                if isSecond:
                    continue;
                else:
                    # print("开始二层扫描 当前path = " + module.path)
                    scanmodulemanager(module.path, True)

scan2dfiremanager(diskPathTest)

# for path in modulePaths:
#     print(path)
#     print('')
print(len(modulePaths))