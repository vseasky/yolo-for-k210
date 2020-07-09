数据集结构

    Train_Image
          ->  VOCdevkit
              --> Annotations
                --  000001.xml
                --  000002.xml
                --  000003.xml
                --  ...
              --> ImageSets
                --> Main
                  --  test.txt
                  --  train.txt
                  --  val.txt
              --> JPEGImages
                --  000001.jpg
                --  000002.jpg
                --  000003.jpg
                --  ...
          ->  MyImage
              -->

你可以将自己的数据集放在MyImage，但是需要保证不会缺少以上列出来的VOC数据集结构的文件，同时你最好检查一下test.txt、train.txt、val.txt中的文本格式是否和VOC数据集中的一致。
