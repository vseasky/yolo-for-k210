# Yolo-for-k210

[vseasky/yolo-for-k210](https://github.com/vseasky/yolo-for-k210)

## 环境配置

1. 常规版本

- windows
- python3.7
- tensorflow-gpu1.15
- cuda10.0
- cudnn7.4.2
- 其它扩展你可以使用 `pip3 install -r requirements.txt` 命令添加。

2. 30显卡系列

- windows-wsl-ubuntu20.04
- python3.8.16
- tensorflow-gpu1.15.5
	- `nvidia-pyindex`
	- `nvidia-tensorflow[horovod]`
	- `nvidia-tensorboard==1.15`
- cuda11.1
- cudnn8.6
- 其它扩展你可以使用 `pip3 install -r requirements.txt` 命令添加。
- nvidia 为兼容最新的显卡驱动舍弃了对lite的支持，因此要想使用toco工具，可尝试安装tf2版本提供模型转换工具。

## 准备数据集

1. 推荐使用**Vott**工具对数据集进行标注，导出为**PascalVoc**格式。
2. 案例 **VOC** 数据集存储于 `/train-image/VOCdevkit`，你可以修改为自定义数据集路径为 `/train-image/your_img`。 

	[数据集结构](/train-image/readme.md)

![readme.png](./readme-image/63ec954ed5aba.png)

3. 运行`make-train.py`脚本，会按照7:2:1的比例，分配为训练集、验证集、测试集文件(pscalvoc.txt、train.txt、val.txt、test.txt)，同时会自动检测并删除不成对的多余文件。

- Win平台手动下载并合并数据集。
- Linux平台下载数据集。

```bash
cd ./train-image
wget https://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar
wget https://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar
wget https://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar
# 解压文件
tar xf VOCtrainval_11-May-2012.tar
tar xf VOCtrainval_06-Nov-2007.tar
tar xf VOCtest_06-Nov-2007.tar
# 合并数据集
cd VOCdevkit/
mv ./VOC2007/* ./
cp -r ./VOC2012/* ./
rm -rf VOC2007
rm -rf VOC2012
```

- 分配数据集。

```
# 使用VOC数据集
python make-train.py ./VOCdevkit
```

```bash
# 使用自定义数据集
python make-train.py ./your_img
```

4. 数据集预处理 `voc_label.py`。

- 修改 `voc_label.py`。

![image.png](./readme-image/63ec984640c4d.png)

```bash
# 使用VOC数据集
python voc_label.py
cat  VOCdevkit_train.txt VOCdevkit_val.txt> train.txt   #Linux使用此命令
# type VOCdevkit_train.txt VOCdevkit_val.txt> train.txt	#windowns使用此命令
```

```bash
# 使用自定义数据集
python voc_label.py
cat  your_img_train.txt your_img_val.txt> train.txt     #Linux使用此命令
# type your_img_train.txt your_img_val.txt> train.txt	#windowns使用此命令
```

6. 检查 txt 文件内容是否正确，文件内容为图片路径。

7. 将 **JPEGImages** 路径和 **Annotations** 合并到一个NPY 文件中。

```bash
python make_voc_list.py train.txt data/voc_img_ann.npy
```

![image.png](./readme-image/63ecf92e580ec.png)

## 修改配置文件

你可以直接在 **Makefile** 编辑默认配置，又或者在 make 操作时传入参数。

![image.png](./readme-image/63ecbfc2c866c.png)

## 生成 **Anchors**

加载**Annotations**生成 **Anchors** (LOW 和 HIGH 视数据集的分布而定)：

```bash
# make anchors # 使用默认参数
make anchors DATASET=voc ANCNUM=3 LOW="0.0 0.0" HIGH="1.0 1.0" # 更改自定义参数
```

当你成功的时候，你会看到这样以下内容：

![Figure_2.png](./readme-image/63ecc18bda042.png)

![image.png](./readme-image/63ecf9b31ba7a.png)

注：结果是随机的。当你有错误时，就重新运行它。

如果要使用自定义数据集，只需修改脚本并生成 `data/{your_img}_img_ann.npy`，然后使用 `make anchors DATASET=your_img`。更多选项请参见 `python ./make_anchor_list.py -h`

如果要更改输出层的数目，则应修改 OUTSIZE 在 Makefile

## 下载预训练模型

你必须下载您想要训练的模型权重，因为默认情况下会加载训练前的权重。把文件放进./data 目录。


| `MODEL`       | `DEPTHMUL` | Url                                                                                | Url                                        |
| ------------- | ---------- | ---------------------------------------------------------------------------------- | ------------------------------------------ |
| yolo_mobilev1 | 0.5        | [google drive](https://drive.google.com/open?id=1SmuqIU1uCLRgaePve9HgCj-SvXJB7U-I) | [weiyun](https://share.weiyun.com/59nnvtW) |
| yolo_mobilev1 | 0.75       | [google drive](https://drive.google.com/open?id=1BlH6va_plAEUnWBER6vij_Q_Gp8TFFaP) | [weiyun](https://share.weiyun.com/5FgNE0b) |
| yolo_mobilev1 | 1.0        | [google drive](https://drive.google.com/open?id=1vIuylSVshJ47aJV3gmoYyqxQ5Rz9FAkA) | [weiyun](https://share.weiyun.com/516LqR7) |
| yolo_mobilev2 | 0.5        | [google drive](https://drive.google.com/open?id=1qjpexl4dZLMtd0dX3QtoIHxXtidj993N) | [weiyun](https://share.weiyun.com/5BwaRTu) |
| yolo_mobilev2 | 0.75       | [google drive](https://drive.google.com/open?id=1qSM5iQDicscSg0MYfZfiIEFGkc3Xtlt1) | [weiyun](https://share.weiyun.com/5RRMwob) |
| yolo_mobilev2 | 1.0        | [google drive](https://drive.google.com/open?id=1Qms1BMVtT8DcXvBUFBTgTBtVxQc9r4BQ) | [weiyun](https://share.weiyun.com/5dUelqn) |
| tiny_yolo     |            | [google drive](https://drive.google.com/open?id=1M1ZUAFJ93WzDaHOtaa8MX015HdoE85LM) | [weiyun](https://share.weiyun.com/5413QWx) |
| yolo          |            | [google drive](https://drive.google.com/open?id=17eGV6DCaFQhVoxOuTUiwi7-v22DAwbXf) | [weiyun](https://share.weiyun.com/55g6zHl) |

## 训练

使用 Mobileenet 时，需要指定 DEPTHMUL 参数。 使用 tiny yolo 或 yolo 你不需要设定 DEPTHMUL.

1.  设置并开始训练：MODE-LDEPTHMUL

```bash
make train MODEL=yolo_mobilev1 DEPTHMUL=0.75 MAXEP=10 ILR=0.001 DATASET=voc CLSNUM=20 IAA=False BATCH=16
```

![image.png](./readme-image/63ecfa0b97ee4.png)

	使用 Ctrl+C 停止训练，它将自动在日志目录中保存权重和模型。

2.  设置为继续训练：CKPT

```bash
make train MODEL=yolo_mobilev1 DEPTHMUL=0.75 MAXEP=10 ILR=0.0005 DATASET=voc CLSNUM=20 IAA=False BATCH=16 CKPT=log/xxxxxxxxx/yolo_model.h5
```


3.  设置为启用数据增强：IAA

```bash
make train MODEL=xxxx DEPTHMUL=xx MAXEP=10 ILR=0.0001 DATASET=voc CLSNUM=20 IAA=True BATCH=16 CKPT=log/xxxxxxxxx/yolo_model.h5
```

4.  使用 tensorboard:

```bash
tensorboard --logdir log
```

注意：更多选项请参阅与`python ./keras_train.py -h`

## 推理

1. 使用自己训练的模型

```bash
make inference MODEL=yolo_mobilev1 DEPTHMUL=0.75 CLSNUM=20 CKPT=log/xxxxxx/yolo_model.h5 IMG=data/input/people.jpg
```

2. 你可以尝试我的模型：

```bash
make inference MODEL=yolo_mobilev1 DEPTHMUL=0.75 CKPT=asset/yolo_model.h5 IMG=data/input/people.jpg
```

![people.png](./readme-image/63ef49b2dc633.png)


```bash
make inference MODEL=yolo_mobilev1 DEPTHMUL=0.75 CKPT=asset/yolo_model.h5 IMG=data/input/dog.jpg
```

![dog_res.jpg](./readme-image/63ef49ea40b66.jpg)


注：由于 anchors 是随机生成的，如果您的结果与上面的图像不同，你只需要加载这个模型并继续训练一段时间。

更多选项请参见`python ./keras_inference.py -h`

## 修剪模型

```bash
make train MODEL=xxxx MAXEP=1 ILR=0.001 DATASET=voc CLSNUM=20 BATCH=16 PRUNE=True CKPT=log/xxxxxx/yolo_model.h5 END_EPOCH=1
```

训练结束时，将模型保存为 log/xxxxxx/yolo_prune_model.h5.

## Freeze

```bash
toco --output_file data/tflite/mobile_yolo.tflite --keras_model_file log/xxxxxx/yolo_model.h5
```

现在你有了 mobile_yolo.tflite

## 转换 Kmodel

请参考  <a href="https://github.com/kendryte/nncase/releases/tag/v0.1.0-rc5">`nncase v0.1.0-RC5 example`</a>

1. [NNCase Converter v0.1.0 RC5](https://github.com/kendryte/nncase/releases/tag/v0.1.0-rc5)

```bash
./nncase/0.1.0/ncc --version
./nncase/0.1.0/ncc data/tflite/mobile_yolo.tflite mobile_yolo_v3.kmodel -i tflite -o k210model --dataset nncase-images
```

## 将 Kmodel 部署到 K210

这是一个完整的解决方案，底层的硬件和软件部署请参考 [vseasky/riscv-k210](https://github.com/vseasky/riscv-k210) 

![IMG_8355.JPG](./readme-image/63e66d1f9e630.png)

![IMG_8355.JPG](./readme-image/63ef79b776fdf.jpg)

![IMG_8351.JPG](./readme-image/63ef79d395798.jpg)

## 常见问题&FAQ

- 默认参数**Makefile**
- **OBJWEIGHT**，， 用于平衡精度和召回率 **NOOBJWEIGHT**,**WHWEIGH**
- 默认输出两层，如果需要更多输出层可以修改 **OUTSIZE**
- 如果要使用完整的 yolo，则需要将 和 在 **Makefile** 中修改为原始 yolo 参数 **IMGSIZE**,**OUTSIZE**

## 参考

[zhen8838/K210_Yolo_framework](https://github.com/zhen8838/K210_Yolo_framework)

**2020/7/5 21:04:35**
