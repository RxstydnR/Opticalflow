import os
import glob
import argparse

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def imgs_to_movie(Imgs, save_path, fps=20.0):

    ref_img = Image.open(Imgs[0])
    video_size = (ref_img.size[1],ref_img.size[0])

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video = cv2.VideoWriter(save_path+'/movie.avi', fourcc, fps, video_size)

    for img_name in Imgs:
        img = np.array(Image.open(img_name))
        video.write(img)
    video.release()

    return video


parser = argparse.ArgumentParser(prog='make_movie.py')
parser.add_argument('--data_path', type=str, required=True, help='The path of image data.')
parser.add_argument('--save_path', type=str, required=True, help='The path of save folder.')
parser.add_argument('--fps', type=float, default=20, help='Frame Per Second.')
opt = parser.parse_args()


if __name__ == "__main__":

    data_path = opt.data_path 
    save_path = opt.save_path
    os.makedirs(save_path)

    Imgs = sorted(glob.glob(data_path+"/*.jpg"))
    
    imgs_to_movie(Imgs, save_path, opt.fps)


