import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as Image
import re
import os
from readWritePfmFile import readPfm, writePfm
from showImageTools import getFile_name, showSubWindowPicturesWithEvent
	
def main():


##################################################################################
	rootDir = '/data4/zhaosl/python_project/monodepth2Git/assets'
	sourceSubDir = 'ori'
	destiSubDir='pad'
	hPading=560

	depthImgs = getFile_name(os.path.join(rootDir,sourceSubDir), ext='.pfm')
	fig = plt.figure()
	ind = 0 
	for depthImageFile in depthImgs:
		print(' ', ind, '/', len(depthImgs),' ', depthImageFile)
		depthImage = readPfm(depthImageFile)
		padingDepthImage = np.lib.pad(depthImage, ((hPading, 0),(0, 0),(0, 0)), 'constant', constant_values=np.array(((255, 0),(0, 0),(0, 0))))
		destImageFile = depthImageFile.replace(sourceSubDir, destiSubDir)
		writePfm(padingDepthImage, destImageFile)
#		imgs=[leftImage, leftImage, leftImage[:,:,0], leftImage[:,:,1]]
#		showSubWindowPicturesWithEvent(fig, imgs, 0)
		ind+=1
	
	
	

if __name__ == "__main__":
    main()


