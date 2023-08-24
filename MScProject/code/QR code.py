# -*-coding:utf-8 -*-
# Programs for identifying QR code


import os
import cv2 as cv
from pyzbar import pyzbar

path = "C:/Users/ROG/Desktop/MSc Project/Data/test"
data = [];

file_list = os.listdir(path)
for file in file_list:

    if not file.endswith(".jpg"):
        continue

    cur_path = os.path.join(path, file)
    # print(cur_path)

    img = cv.imread(cur_path)
    barcodes = pyzbar.decode(img)
    for barcode in barcodes:
        # print(file + ":" + bytes.decode(barcode.data));
        data.append(bytes.decode(barcode.data))

with open(path + "\data2.txt", "w") as f:
    for item in data:
        # print(item)
        f.write(item + '\n')
