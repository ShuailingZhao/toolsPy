import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import os
import seaborn as sns
from matplotlib import cm
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D

def getDepthErrors(pred, gt):
	"""Computation of error metrics between predicted and ground truth depths
	"""
	thresh = np.maximum((gt / pred), (pred / gt))
	a1 = (thresh < 1.25     ).mean()
	a2 = (thresh < 1.25 ** 2).mean()
	a3 = (thresh < 1.25 ** 3).mean()

	rmse = (gt - pred) ** 2
	rmse = np.sqrt(rmse.mean())

	rmse_log = (np.log(gt) - np.log(pred)) ** 2
	rmse_log = np.sqrt(rmse_log.mean())

	abs_rel = np.mean(np.abs(gt - pred) / gt)

	sq_rel = np.mean(((gt - pred) ** 2) / gt)

	return abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3



def garyMapToColor(grayPix):
	LC = [[0.0,1.0,49,54,149],
	[1.0,2.0,116,173,209],
	[2.0,3.0,171,217,233],
	[3.0,6.0,254,224,144],
	[6.0,1000000000.0,165,0,38]]
	
	for i in range(0,5):
		if grayPix>=LC[i][0] and grayPix<LC[i][1]:
			red   = np.uint8(LC[i][2]);
			green = np.uint8(LC[i][3]);
			blue  = np.uint8(LC[i][4]);
	return  red, green, blue

def garyToColor(grayPix):
	LC = [[0,0.0625,49,54,149],
	[0.0625,0.125,69,117,180],
	[0.125,0.25,116,173,209],
	[0.25,0.5,171,217,233],
	[0.5,1,224,243,248],
	[1,2,254,224,144],
	[2,4,253,174,97],
	[4,8,244,109,67],
	[8,16,215,48,39],
	[16,1000000000.0,165,0,38]]
	
	for i in range(0,10):
		if grayPix>=LC[i][0] and grayPix<LC[i][1]:
			red   = np.uint8(LC[i][2]);
			green = np.uint8(LC[i][3]);
			blue  = np.uint8(LC[i][4]);
	return  red, green, blue

def setColorErrrorImagePixel3X3(errColorImg, h,w,red,green,blue):
	for H in range(h-1,h+2):
		for W in range(w-1,w+2):
			errColorImg[H,W] = red,green,blue

def setColorErrrorImagePixel(errColorImg, h,w,red,green,blue):
	errColorImg[h,w] = red,green,blue
	
def getErrorImage(imgsPredict, imgsGroundtruth):

	errImage = abs(imgsPredict.astype(np.int64) -imgsGroundtruth.astype(np.int64))
	errImage = errImage.astype(np.uint8)
	errImage[imgsGroundtruth==0]=0
	grayErrImg = errImage
	H,W = errImage.shape
	errColorImg = np.zeros((H,W,3),np.uint8)
	
	for h in range(0,H):
		for w in range(0,W):
			if 0 == imgsGroundtruth[h,w]:#0 == grayErrImg[h,w]
				continue
#			d_err = grayErrImg[h,w]
#			d_mag = imgsGroundtruth[h,w]
#			n_err = min(d_err/3.0,20.0*d_err/d_mag)
#			red,green,blue = garyToColor(n_err)
			red,green,blue = garyMapToColor(grayErrImg[h,w])
			setColorErrrorImagePixel3X3(errColorImg,h,w,red,green,blue)
			
	return errImage, errColorImg		
	
def reShapeList(x,y):
	x = np.array(x)
	y = np.array(y)
	xx1, yy1 = np.meshgrid(x,y)
	newshape = (xx1.shape[0])*(xx1.shape[0])
	y_input = xx1.reshape(newshape)
	x_input = yy1.reshape(newshape)
	return x_input.tolist(), y_input.tolist()

def show3DCurveTrisurf(fig,x_input,y_input,z_input):
	sns.set(style='white')
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_trisurf(x_input,y_input,z_input,cmap=cm.viridis)#cmap cm.coolwarm, cm.viridis, cm.plasma, cm.inferno, cm.magma, cm.cividis
	
	
def interp2dXYZ(x,y,z,xInter=-1,yInter=-1):
	if xInter<0.0:
		x_input = np.array(x)
		y_input = np.array(y)
		z_input = np.array(z)
	
	if xInter>0.0:
		f = interpolate.interp2d(x, y, z, kind='cubic')
		xmin = np.min(x)
		xmax = np.max(x)
		ymin = np.min(y)
		ymax = np.max(y)
		xnew = np.arange(xmin, xmax, xInter)
		ynew = np.arange(ymin, ymax, yInter)
		znew = f(xnew, ynew)


		xx1, yy1 = np.meshgrid(xnew, ynew)
		newshape = (xx1.shape[0])*(xx1.shape[0])
		y_input = xx1.reshape(newshape)
		x_input = yy1.reshape(newshape)
		z_input = znew.reshape(newshape)
	return x_input,y_input,z_input
	
def show3DSurface(fig,x,y,z,xInter=-1,yInter=-1):

	xnew, ynew, znew = interp2dXYZ(x,y,z,xInter,yInter)
	show3DCurveTrisurf(fig,xnew,ynew,znew)

def showOnePoint(fig,x,y,z):
	ax = fig.axes[0]
	ax.scatter3D(np.array(x),np.array(y),np.array(z), c='r', marker='*',s=100)#'Greens'

def show3Dcurve(fig,x,y,z, xInter=0.2):
	
	if xInter<0:
		x_knots = np.array(x)
		y_knots = np.array(y)
		z_knots = np.array(z)
	
	if xInter>=0:
		xInter = int(1.0/xInter)
		tck,u = interpolate.splprep([x,y,z],s=2)
		u_fine = np.linspace(0,1,xInter)
		x_knots, y_knots, z_knots = interpolate.splev(u_fine, tck)
	
	ax = fig.axes[0]
	ax.plot3D(x_knots,y_knots,z_knots,color='gray',linewidth=1)#cmap=cm.coolwarm)#cmap cm.coolwarm, cm.viridis, cm.plasma
	ax.scatter3D(np.array(x),np.array(y),np.array(z), c=np.array(z), cmap='Reds')#'Greens'
#	ax.scatter3D(np.array(x[len(x)-1]),np.array(y[len(x)-1]),np.array(z[len(x)-1]), c='r', marker='*',s=100)#'Greens'
	showOnePoint(fig,x[len(x)-1],y[len(x)-1],z[len(x)-1])

def getFile_name(root_dir, ext='.pfm'):
	L = []
	for dirpath, dirnames, filenames in os.walk(root_dir):
		for file in filenames:
			if -1 == dirpath.find('.png') and os.path.splitext(file)[1] == ext:# only using the left disparity
				L.append(os.path.join(dirpath, file))
	return sorted(L)
    
def drawPairPos(event,fig, disp):
	
	ax = event.inaxes
	currentAxesIndex = getAxesIndex(ax,fig.axes)
	if 0 == currentAxesIndex:
		drawPointOnAxes(fig.axes[0], event.xdata, event.ydata)
		drawPointOnAxes(fig.axes[1], event.xdata-disp[int(round(event.ydata)), int(round(event.xdata))], event.ydata)
	

def getAxesIndex(ax,axes):
	currentAxesIndex=-1
	if type(ax) != type(axes[0]):
		return currentAxesIndex
	
	for i in range(len(axes)):
		if isSameAxes(ax,axes[i]):
			currentAxesIndex=i
			break
	return currentAxesIndex
	


def isSameAxes(axesFirst,axesSecond):
	if abs(axesFirst.get_position().x0-axesSecond.get_position().x0)<0.0001 and abs(axesFirst.get_position().y0-axesSecond.get_position().y0)<0.0001:
		return True
	return False

def drawPointOnAxes(ax, x, y):
	circle = mpathes.Circle(np.array([x,y]),1.0,color='r')
	ax.add_patch(circle)
	
	
def showImage(fileName, img):
	cv2.namedWindow(fileName, cv2.WINDOW_NORMAL)
	cv2.imshow(fileName, img)
	
def waitMoment(miniseconds):
	cv2.waitKey(miniseconds)

def pause(seconds):
	if 0 == seconds:
		try:
			input('Enter to next')
		except:
			print('...')
	else:
		plt.pause(seconds)

def show2X2Pictures(imgs):
	imgsLeft = imgs[0]
	imgsRight = imgs[1]
	imgsPredict = imgs[2]
	imgsGrounth = imgs[3]
	imgsRight = cv2.resize(imgsRight,(imgsLeft.shape[1],imgsLeft.shape[0]))
	imgsPredict = cv2.resize(imgsPredict,(imgsLeft.shape[1],imgsLeft.shape[0]))
	imgsGroundtruth = cv2.resize(imgsGrounth,(imgsLeft.shape[1],imgsLeft.shape[0]))

	imgsTopRow = np.hstack([imgsLeft,imgsRight])
	imgsBottomRow = np.hstack([imgsPredict,imgsGroundtruth])
	#    imgs = np.vstack([imgsTopRow,imgsBottomRow]);
	showImage('left right image', imgsTopRow)
	showImage('predict groundtruth image', imgsBottomRow)

def showSubWindowPictures(imgs):
	
	imgNum = len(imgs)
	cols = 2
	rows = imgNum/cols
	plt.ion()
	imgInd=0
	subLeftTop = plt.subplot(rows, cols, imgInd+1)
	plt.imshow(imgs[imgInd].astype(np.uint8))
	imgInd+=1
	subRightTop = plt.subplot(rows, cols, imgInd+1)
	plt.imshow(imgs[imgInd].astype(np.uint8))
	imgInd+=1
	subLeftBottom = plt.subplot(rows, cols, imgInd+1)
	plt.imshow(imgs[imgInd],cmap='gray')
	imgInd+=1
	subRightBottom = plt.subplot(rows, cols, imgInd+1)
	plt.imshow(imgs[imgInd],cmap='gray')
	
#	imgInd+=1
#	subErrGray = plt.subplot(rows, cols, imgInd+1)
#	plt.imshow(imgs[imgInd],cmap='gray')
#	imgInd+=1
#	subErrColor = plt.subplot(rows, cols, imgInd+1)
#	plt.imshow(imgs[imgInd].astype(np.uint8))
	
#	plt.legend(handles=[subLeftTop, subRightTop, subLeftBottom, subRightBottom], labels=['left','right','prediction','groundtruth'], loc='upper right', ncol=len(imgs)/2)
	plt.show()
	
def showSubWindowPicturesWithEvent(fig, imgs, seconds):
	showSubWindowPictures(imgs)
	fig.canvas.mpl_connect('button_press_event', lambda event: drawPairPos(event,fig,imgs[2]))
	pause(seconds)
