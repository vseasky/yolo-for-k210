import random
import os
 
path = "E:/github_ide/Yolo-for-k210/Yolo-for-k210/Train_Image/MyImage"


rootdir=os.path.join(path+'/Annotations')
# rootdir=os.path.join(path+'/JPEGImages')
write_path = open(path+'/ImageSets/Main/pscalvoc.txt','w')
for (dirpath,dirnames,filenames) in os.walk(rootdir):
    for filename in filenames:    
        if os.path.splitext(filename)[1]=='.xml':
            write_path.write(os.path.splitext(filename)[0]+'\n')
write_path.close()

annotation_path = path+u"/ImageSets/Main/pscalvoc.txt"
train_path = path+u"/ImageSets/Main/train.txt"
val_path = path+u"/ImageSets/Main/val.txt"
test_path = path+u"/ImageSets/Main/test.txt"

train_file = open(train_path,"w")
val_file = open(val_path,"w")
test_file = open(test_path,"w")
anno = open(annotation_path, 'r')
result = []
my_dict = {}
cnt = 0
for line in anno:
   my_dict[cnt]=line
   cnt+=1
totalnum = cnt
train_num = int(totalnum * 0.7)
val_num = int(totalnum * 0.2)
test_num = totalnum-train_num-val_num
 
test_set = set()
val_set = set()
train_set = set()
 
while(len(test_set) < test_num):
     x = random.randint(0,totalnum)
     if x not in test_set :
        test_set.add(x)
 
while(len(val_set) < val_num):
     x = random.randint(0,totalnum)
     if x in test_set :
        continue
     if x not in val_set :
        val_set.add(x)
		
for x in range(totalnum):
     if x in test_set or x in val_set:
        continue
     else:
        train_set.add(x)
 
index = 0		
for i in range(cnt):
     strs = my_dict[i]
     if i in train_set:
        train_file.write(strs)
     elif i in val_set:
        val_file.write(strs)
     else:
        test_file.write(strs)
     index+=1

train_file.close
val_file.close
test_file.close