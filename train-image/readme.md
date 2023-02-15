```
train-image
  ->  VOCdevkit
      --> Annotations
        --  000001.xml
        --  000002.xml
        --  000003.xml
        --  ...
      --> ImageSets
        --> Main
          --  pscalvoc.txt
          --  test.txt
          --  train.txt
          --  val.txt
      --> JPEGImages
        --  000001.jpg
        --  000002.jpg
        --  000003.jpg
        --  ...
  ->  images
      -->
```

```shell
# 使用VOC数据集
python3 make-train.py ./VOCdevkit
# 使用自定义数据集
# python3 make-train.py ./your_img
```