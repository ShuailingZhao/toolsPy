# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 实现视频和图像的互相转换
# Reference：https://blog.csdn.net/r1141207831/article/details/107403222
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import cv2
import time
from PIL import Image
from tqdm import tqdm
import multiprocessing as mp


# 图片转视频
def Pic2Video(imgPath, videoPath):
    """
    imgPath: 读取图片路径，文件夹
    videoPath: 保存视频路径，带文件名
    """
    images = os.listdir(imgPath)
    fps = 25  # 每秒25帧数

    # VideoWriter_fourcc为视频编解码器 ('I', '4', '2', '0') —>(.avi) 、
    # ('P', 'I', 'M', 'I')—>(.avi)、('X', 'V', 'I', 'D')—>(.avi)、
    # ('T', 'H', 'E', 'O')—>.ogv、('F', 'L', 'V', '1')—>.flv、('m', 'p', '4', 'v')—>.mp4
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    image = Image.open(os.path.join(imgPath, images[0]))
    videoWriter = cv2.VideoWriter(videoPath, fourcc, fps, image.size)
    for im_name in tqdm(range(len(images))):
        frame = cv2.imread(os.path.join(imgPath, images[im_name]))  # 这里的路径只能是英文路径
        # frame = cv2.imdecode(np.fromfile((imgPath + images[im_name]), dtype=np.uint8), 1)  # 此句话的路径可以为中文路径
        print(im_name)
        videoWriter.write(frame)
    print("图片转视频结束！")
    videoWriter.release()
    cv2.destroyAllWindows()


def saveimg(img, imgpath):
    cv2.imwrite(imgpath, img)

# 视频转图片
def Video2Pic(imgPath, videoPath):
    """
    videoPath: 读取视频路径，带文件名
    imgPath: 保存图片路径，文件夹
    """
    cap = cv2.VideoCapture(videoPath)
    # fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取高度
    suc = cap.isOpened()  # 是否成功打开
    frame_count = 1000000  # 保存的图像的起始编号
    p = mp.Pool(mp.cpu_count())
    while suc:
        suc, frame = cap.read()
        # 多进程保存图像，快
        p.apply_async(saveimg, args=(frame, os.path.join(imgPath, "{}.jpg".format(frame_count))))
        # 单进程保存图像，慢
        # cv2.imwrite(os.path.join(imgPath, "{}.jpg".format(frame_count)), frame)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(timestamp, frame_count)
        frame_count += 1

        cv2.waitKey(1)
    cap.release()
    p.close()
    p.join()
    print("视频转图片结束！")


if __name__ == '__main__':
    videopath = "../data/undistort20210118_143813.mp4"
    imgpath = "../data/undistort20210118_143813_imgs/"
    if not os.path.exists(imgpath):
        os.mkdir(imgpath)

    Video2Pic(imgpath, videopath)
    print("+++++ end +++++")
