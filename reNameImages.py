# -*- coding: utf-8 -*-
#python3
import os
import sys


def rename():
    path = input("路径(例如D:\\\\picture)：")
    name = input("新文件开头名:")
    startNumber = input("起始数字:")
    fileType = input("文件类型（如 .jpg、.txt等等）:")   
    count = 0
    filelist = os.listdir(path)
    filelist.sort()
    for file in filelist:
        oldF = os.path.join(path, file)
        if os.path.isfile(oldF) and os.path.splitext(oldF)[1] == fileType:
            newF = os.path.join(
                path, name+str(count+int(startNumber)).zfill(10)+fileType)
            os.rename(oldF, newF)
        else:
            continue
        count += 1
    print("一共修改了"+str(count)+"个文件")


rename()
