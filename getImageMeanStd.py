import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2

def getMeanStd(filepath, imageList):
	img = cv2.cvtColor(cv2.imread(os.path.join(filepath, imageList[0])),cv2.COLOR_BGR2RGB)
	h,w,c = img.shape
	print(w,h,c)
	R_channel = 0
	G_channel = 0
	B_channel = 0
	for idx in range(len(imageList)):
		filename = imageList[idx]
		img = cv2.cvtColor(cv2.imread(os.path.join(filepath, filename)),cv2.COLOR_BGR2RGB).astype(np.float64)
		R_channel = R_channel + np.sum(img[:, :, 0])
		G_channel = G_channel + np.sum(img[:, :, 1])
		B_channel = B_channel + np.sum(img[:, :, 2])
	 
	num = len(imageList) * w * h  # 这里（512,512）是每幅图片的大小，所有图片尺寸都一样
	R_mean = R_channel / num
	G_mean = G_channel / num
	B_mean = B_channel / num
	 
	R_channel = 0
	G_channel = 0
	B_channel = 0
	for idx in range(len(imageList)):
		filename = imageList[idx]
		img = cv2.cvtColor(cv2.imread(os.path.join(filepath, filename)),cv2.COLOR_BGR2RGB).astype(np.float64)
		R_channel = R_channel + np.sum((img[:, :, 0] - R_mean) ** 2)
		G_channel = G_channel + np.sum((img[:, :, 1] - G_mean) ** 2)
		B_channel = B_channel + np.sum((img[:, :, 2] - B_mean) ** 2)
	 
	R_var = np.sqrt(R_channel / num)
	G_var = np.sqrt(G_channel / num)
	B_var = np.sqrt(B_channel / num)

	return R_mean, G_mean, B_mean, R_var, G_var, B_var


filepath = '/home/zhaosl/python_project/toolsPy/test'  # 数据集目录

R_mean, G_mean, B_mean, R_var, G_var, B_var = getMeanStd(filepath, os.listdir(filepath))

print("R G B mean is %f, %f, %f" % (R_mean, G_mean, B_mean))
print("R G B var is %f, %f, %f" % (R_var, G_var, B_var))
