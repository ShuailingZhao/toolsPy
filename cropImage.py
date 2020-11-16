import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as Image
import re
from showImageTools import getFile_name, showSubWindowPicturesWithEvent

def wrapeImage(rImg, index):
	h,w,c = rImg.shape
	reArrangeImg = np.zeros((h,w,c))
    
	for i in range(h):
		for j in range(w):
			if int(j-index[i,j])>0:
				reArrangeImg[i,j,:]=rImg[i,int(j-index[i,j]),:]
    
	return reArrangeImg
	
def main():


##################################################################################
	rootDir = '/data4/zhaosl/python_project/monodepth2Git/assets/'
	sourceDir = rootDir + 'undistort'

	leftImgs = getFile_name(sourceDir, ext='.jpg')
	fig = plt.figure()
	imgIndex=0
	for leftImageFile in leftImgs:
		print(' ', imgIndex, '/', len(leftImgs),' ', leftImageFile)
		leftImage = cv2.imread(leftImageFile)
		cropedLeftImage = leftImage[560:1200,:,:]
		destImageFile = leftImageFile.replace('undistort', 'crop')
		cv2.imwrite(destImageFile, cropedLeftImage)
#		imgs=[leftImage, leftImage, leftImage[:,:,0], leftImage[:,:,1]]
#		showSubWindowPicturesWithEvent(fig, imgs, 0)
		imgIndex+=1
	
	
	

if __name__ == "__main__":
    main()


