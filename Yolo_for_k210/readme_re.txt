make train MODEL=yolo_mobilev1 DEPTHMUL=0.75 MAXEP=10 ILR=0.001 DATASET=voc CLSNUM=20 IAA=False BATCH=8

我们先检验模型
make inference MODEL=yolo_mobilev1 DEPTHMUL=0.75 CLSNUM=20 CKPT=log/20200703-214844/yolo_model.h5 IMG=data/people.jpg

ncc mobile_yolo.tflite mobile_yolo.kmodel -i tflite -o k210model --dataset  train_images