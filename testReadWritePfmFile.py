import numpy as np
import sys
from readWritePfmFile import readPfm, writePfm,readPfm1, writePfm1
from showImageTools import showImage, waitMoment

def main():
	fpath="/home/zhaosl/python_project/tools/dest/0-020808-916-0000001.pfm"
	img1 = readPfm(fpath)
	showImage(fpath, img1)
	waitMoment(0)
#	writePfm(img1, '0008_2.pfm')

if __name__ == "__main__":
    main()

