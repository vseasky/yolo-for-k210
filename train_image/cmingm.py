# -*- coding:utf-8 -*-
# 图像批量重命名
import string
import random
import os
import shutil
 
def rename(path , newname):   #对文件重命名
     
    filelist = os.listdir(path)  #获取文件下的所有文件名
    m = 0
    for files in filelist:
        Olddir = path + files  #原来的文件路径
        if os.path.isdir(Olddir):  #如果是文件夹则跳过
            continue
        filename = os.path.splitext(files)[0] #文件名
        filetype = os.path.splitext(files)[1] #后缀名,是一个列表
        Newdir = os.path.join(path , newname + filetype) % m  #这里由于filetype是一个列表，因此不能用Newdir=path+'face%05d'+filetype!
        m += 1
        os.rename(Olddir , Newdir)
#图片批量重命名
rename('E:/github_ide/Yolo-for-k210/train_image/JPEGImages/' ,'2020_'+'%06d')