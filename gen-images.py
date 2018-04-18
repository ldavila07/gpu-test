import os
import sys
from bs4 import BeautifulSoup
from shutil import copyfile
import pandas as pd
from PIL import Image


if not os.path.exists("train"):
    os.makedirs("train")
if not os.path.exists("test"):
    os.makedirs("test")
output_path = "./"
image_dir_path = sys.argv[1]
annotation_dir_path = sys.argv[2]
print("image_dir_path: ", image_dir_path)
print("annotation_dir_path: ", annotation_dir_path)


def get_num_pixels(filepath):

    img = Image.open(filepath)
    width, height = img.size

    return width, height

def convert(size, box):
    dw = 1/int(size[0])
    dh = 1/int(size[1])
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def save_image(data_path, output_path, orig_dirname, orig_filename, new_dirname, train_file_counter, label_id):
    if not os.path.exists(output_path + new_dirname):
        os.makedirs(output_path + new_dirname)
    new_filename = str(train_file_counter) + "_" + label_id + '.jpg'
    orig_file_path = data_path + orig_dirname + "/" + orig_filename
    new_file_path = output_path + new_dirname + "/" + new_filename
    copyfile(orig_file_path, new_file_path)

def save_annotation(file_path,output_path,dir, test_file_counter,label_id):
    with open(file_path, 'r') as myfile:
        text = myfile.read()
    soup = BeautifulSoup(text, 'xml')
    width = soup.find('width').string
    height = soup.find('height').string
    xmin = soup.find('xmin').string
    xmax = soup.find('xmax').string
    ymax = soup.find('ymax').string
    ymin = soup.find('ymin').string

    b = (float(xmin), float(xmax), float(ymin), float(ymax))
    bb = convert((width, height), b)
    path = output_path + dir + "/" + str(test_file_counter) + "_" + label_id + '.txt'
    f = open(path, "w+")
    f.write(str(label_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    f.close()


output_train_dirname = 'train'
output_test_dirname = 'test'
label_id = []
label_name = []

labels_file = open(output_path + 'labels.txt', 'w')
labels_mapping_file = open(output_path + 'name.txt', 'w')
train_list = open(output_path + 'train.txt', 'w')
test_list = open(output_path + 'test.txt', 'w')

dir_list = os.listdir(image_dir_path)

train_file_counter = 0
test_file_counter = 0

for dir in dir_list:
    if not dir.startswith('.'):
        files_list = os.listdir(image_dir_path + dir)
        print("directory", dir, len(files_list))
        label_id = dir[0:9]
        label_name = dir[10:]
        labels_mapping_file.write(label_name + '\n')
        labels_file.write(label_id + '\n')
        files_list.sort()
        #split training and test data
        train_files = files_list[int(len(files_list) * .20): int(len(files_list) * .80)]
        test_files = files_list[len(train_files):]
        for file in train_files:
            train_file_counter += 1
            save_annotation(annotation_dir_path + dir + "/" + file.replace(".jpg", ""), output_path, output_train_dirname, train_file_counter, label_id)
            save_image(image_dir_path, output_path, dir, file, output_train_dirname, train_file_counter, label_id )
            train_list.write("./" + output_train_dirname + "/" + str(train_file_counter) + "_" + label_id + '.jpg' + '\n')

        file_counter = 0
        for file in test_files:
            test_file_counter += 1
            save_annotation(annotation_dir_path + dir + "/" + file.replace(".jpg", ""), output_path, output_test_dirname, test_file_counter, label_id)
            save_image(image_dir_path, output_path, dir, file, output_test_dirname, test_file_counter, label_id)
            test_list.write("./" + output_test_dirname + "/" + str(test_file_counter) + "_" + label_id + '.jpg' + '\n')
train_list.close()
test_list.close()

print("training files: ", str(train_file_counter))
print("test files: ", str(test_file_counter))

labels_mapping_file.close()
labels_file.close()


