import cv2
import numpy as np 
import os
import random
import shutil
from tqdm import trange

images_path = '/data/zrx/DDRomote/images/'
labels_path = '/data/zrx/DDRomote/vocxmls/'

new_path = '/data/zrx/DDRomote/split/'

try:
    os.mkdir(new_path)
except:
    pass

try:
    os.mkdir(os.path.join(new_path, 'trainval/'))
except:
    pass

try:
    os.mkdir(os.path.join(new_path, 'test/'))
except:
    pass

trainval_images = os.path.join(new_path, 'trainval/images/')
trainval_labels = os.path.join(new_path, 'trainval/labels/')
test_images = os.path.join(new_path, 'test/images/')
test_labels = os.path.join(new_path, 'test/labels/')

try:
    os.mkdir(trainval_images)
except:
    pass
try:
    os.mkdir(trainval_labels)
except:
    pass
try:
    os.mkdir(test_images)
except:
    pass
try:
    os.mkdir(test_labels)
except:
    pass


label_list = os.listdir(labels_path)

train = open(os.path.join(new_path, "trainval.txt"), mode="w")
val = open(os.path.join(new_path, "test.txt"), mode="w")

# for idx, label_file in enumerate(label_list):
for idx in trange(len(label_list)):
    label_file = label_list[idx]
    file_name = label_file.split('.xml')[0]
    label_file_path = os.path.join(labels_path, label_file)
    image_file_path = os.path.join(images_path, '{}.png'.format(file_name))
    if random.random() < 0.8:
        train.write(file_name + '\n')
        shutil.copy(image_file_path, trainval_images)
        shutil.copy(label_file_path, trainval_labels)
    else:
        val.write(file_name + '\n')
        shutil.copy(image_file_path, test_images)
        shutil.copy(label_file_path, test_labels)

train.close()
val.close()