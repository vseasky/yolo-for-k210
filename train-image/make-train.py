import random
import os
import argparse
import sys
import _thread
import time

# 按照7:2:1的比例，生成训练集、验证集、测试集文件(pscalvoc.txt、train.txt、val.txt、test.txt)
def main(train_file_input: str):
   # path = os.path.dirname(__file__) + train_file_input
   path = train_file_input.replace('\\','/')
   
   print(path)
   img_path = os.path.join(path+'/JPEGImages')
   xml_path = os.path.join(path+'/Annotations')
   write_path = open(path+'/ImageSets/Main/pscalvoc.txt','w')
   
   jpg_list = []
   xml_list = []

   for root, dirs, files in os.walk(img_path):
      for file in files:
         jpg_list.append(os.path.splitext(file)[0])

   for root, dirs, files in os.walk(xml_path):
      for file in files:
         xml_list.append(os.path.splitext(file)[0])

   diff1 = set(xml_list).difference(set(jpg_list))  
   for name in diff1:
      os.remove(xml_path +"/"+name +'.xml')
      print("diff1 not have %s.jpg,remove %s.xml"%(name,name))

   diff2 = set(jpg_list).difference(set(xml_list)) 
   for name in diff2:
      os.remove(img_path + "/"+name +'.jpg')
      print("diff2 not have %s.xml,remove %s.jpg"%(name,name))

   train_list = []
   for root, dirs, files in os.walk(xml_path):
      for file in files:
         write_path.write(os.path.splitext(file)[0]+'\n')
         train_list.append(os.path.splitext(file)[0])

   write_path.close()

   annotation_path = path+u"/ImageSets/Main/pscalvoc.txt"
   train_path = path+u"/ImageSets/Main/train.txt"
   val_path = path+u"/ImageSets/Main/val.txt"
   test_path = path+u"/ImageSets/Main/test.txt"

   train_file = open(train_path, "w")
   val_file = open(val_path, "w")
   test_file = open(test_path, "w")
   anno = open(annotation_path, 'r')
   
   print(len(train_list))

   total_num = len(train_list)
   train_num = int(total_num * 0.7)
   val_num = int(total_num * 0.2)
   test_num = total_num-train_num-val_num

   test_set = set()
   val_set = set()
   train_set = set()

   while (len(test_set) < test_num):
      x = random.randint(0, total_num)
      if x not in test_set:
         test_set.add(x)

   while (len(val_set) < val_num):
      x = random.randint(0, total_num)
      if (x in test_set):
         continue
      if (x not in val_set):
         val_set.add(x)

   for x in range(total_num):
      if (x in test_set) or (x in val_set):
         continue
      else:
         train_set.add(x)

   for i in range(total_num):
      strs = train_list[i]
      if i in train_set:
         train_file.write(strs+"\n")
         print("train :"+strs)
      elif i in val_set:
         val_file.write(strs+"\n")
         print("val   :"+strs)
      else:
         test_file.write(strs+"\n")
         print("test  :"+strs)

   train_file.close
   val_file.close
   test_file.close


def parse_arguments(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument('train_file_input', type=str,
                        help='voc datasets file path')
   return parser.parse_args(argv)

if __name__ == "__main__":
   args = parse_arguments(sys.argv[1:])
   main(args.train_file_input)
