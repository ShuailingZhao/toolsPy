import cv2
import numpy as np
import sys
from readWritePfmFile import readPfm, writePfm,readPfm1, writePfm1,readPfm3, writePfm3
from showImageTools import showImage, waitMoment

def main():
	fpath="./test/0008_2.pfm"
	img1 = readPfm1(fpath)
	print("------------- ", img1[214,872])
	showImg = img1.astype(np.uint8);

	showImage(fpath, showImg)
	waitMoment(3000)
	writePfm3(img1, '0008_2.pfm')



if __name__ == "__main__":
    main()

