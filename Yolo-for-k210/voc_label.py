import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
os_removepath = 'E:/github_ide/Yolo-for-k210/Yolo-for-k210'

sets=[('MyImage', 'train'), ('MyImage', 'val'), ('MyImage', 'test')]#使用自定义数据集
#sets=[('VOCdevkit', 'train'), ('VOCdevkit', 'val'), ('VOCdevkit', 'test')]#使用VOCdevkit数据集
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
#classes = ["car","watcher","base","ignore"]
difficulty_set = 1
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
def convert_annotation(year, image_id):
    in_file = open('Train_Image/%s/Annotations/%s.xml'%(year, image_id))
    out_file = open('Train_Image/%s/labels/%s.txt'%(year, image_id), 'w')
    is_empty = 0    #默认设置为0，表示文件标注为空
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if root.find('object')==None:           #
        print("删除以下错误xml文件，请重新生成train.txt val.txt test.txt")
        in_file.close()
        os.remove(os_removepath+'/Train_Image/%s/Annotations/%s.xml'%(year,image_id)) 
        print(os_removepath+'/Train_Image/%s/Annotations/%s.xml'%(year,image_id))
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:#如果不包含，直接退出
          continue
        if obj.find('difficult')!=None:#优化代码，增加容错性，直接排除不包含difficulty的成分      
          difficult = obj.find('difficult').text
          if int(difficult) == difficulty_set:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        if float(xmlbox.find('xmin').text)<0 or float(xmlbox.find('xmax').text)<0:
            continue
        is_empty = 1
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    if(is_empty==0):
        print("删除以下错误xml文件，请重新生成train.txt val.txt test.txt")
        in_file.close()
        os.remove(os_removepath+'/Train_Image/%s/Annotations/%s.xml'%(year,image_id)) 
        print(os_removepath+'/Train_Image/%s/Annotations/%s.xml'%(year,image_id))

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('Train_Image/%s/labels/'%(year)):
        os.makedirs('Train_Image/%s/labels/'%(year))
    #image_ids = open('Train_Image/%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    image_ids = open('Train_Image/%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()

    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/Train_Image/%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

