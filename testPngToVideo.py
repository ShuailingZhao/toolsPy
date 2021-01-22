import glob as gb
import cv2
    
def main():
	img_path = gb.glob("./data/input/*.jpg")
	img_path.sort()
	imgsLeft = cv2.cvtColor(cv2.imread(img_path[0]),cv2.COLOR_BGR2RGB)
	h,w,c = imgsLeft.shape
	videoWriter = cv2.VideoWriter('./data/output/test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (w,h))
#	 videoWriter = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc(*'XVID'), 25, (640,480))
	for path in img_path:
		img  = cv2.imread(path)
		img = cv2.resize(img,(w,h))
		videoWriter.write(img)

if __name__ == '__main__':
	main()
