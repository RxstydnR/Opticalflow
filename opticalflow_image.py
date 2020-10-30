import glob
import os
import cv2
import argparse

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm, trange

# For GPU
# os.environ["CUDA_VISIBLE_DEVICES"] = "4"


def DenceOpticalFlow(img1, img2, params):
    """ Compute and visualize the dense optical flow between two images. (2つの画像間における密なオプティカルフローを計算し可視化する)

    Args:
        img1 (arr): Before frame (前フレーム)
        img2 (arr): After Frame (後フレーム)
        params (list): Opticalflow parameters (オプティカルフローのパラメータ)

    Returns:
        rgb (arr): Opticalflow visualization image (オプティカルフローの可視化画像)
    """
    
    frame1 = img1
    frame2 = img2

    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    
    prev = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    
    # Menian Blur
    # frame1 = cv2.medianBlur(frame1, ksize=11)
    # frame2 = cv2.medianBlur(frame2, ksize=11)


    ''' Example Parameter
        Parameter reference : http://bicycle.life.coocan.jp/takamints/index.php/doc/opencv/function/calcOpticalFlowFarneback
                            : https://code-graffiti.com/opencv-dense-optical-flow-in-python/

        calcOpticalFlowFarneback( prevImg, nextImg, flow, pyrScale, levels, winsize, iterations, polyN, polySigma, flags ）                                
        calcOpticalFlowFarneback( prev,    next,    None,  0.5,       1,     10,      1,         10,    5.0,       256   ) 
    '''            
    flow = cv2.calcOpticalFlowFarneback( prev=prev, next=next,  flow=None,  pyr_scale=params[0],  levels=params[1],  winsize=params[2],  iterations=params[3],  poly_n=params[4],   poly_sigma=params[5], flags=params[6])
    
    # Opticalflow visualization
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)

    return rgb



parser = argparse.ArgumentParser(prog='opticalflow_image.py')
parser.add_argument('--data_path', type=str, required=True, help='The path of image data.')
parser.add_argument('--save_path', type=str, required=True, help='The path of save folder.')
opt = parser.parse_args()
    
if __name__=="__main__":
    """ Calculate the optical flow and make visualization images. (オプティカルフローを計算し、その可視化画像を出力する)
    """
    data_path = opt.data_path
    save_path = opt.save_path
    os.makedirs(save_path, exist_ok=True)

    prams = [
        0.2, # pyrScale
        2,   # levels
        4,   # winsize
        2,   # iterations
        3,   # polyN
        30,  # polySigma
        256  # flags
    ]
    print(f"pyrScale={prams[0]}, levels={prams[1]}, winsize={prams[2]}, iterations={prams[3]}, polyN={prams[4]}, polySigma={prams[5]}, flags={prams[6]}")
 

    # Get image data
    X = []
    imgs_path = sorted(glob.glob(data_path+"/*.jpg"))
    for img in tqdm(imgs_path):
        x = cv2.imread(img)
        X.append(x)
    X = np.array(X)

 
    # Calculate opticalflow (オプティカルフローを計算)
    cnt = 0
    prev = X[0]
    for x in X[1:]:
        next = x
        flow = DenceOpticalFlow(prev, next, prams)
        cv2.imwrite(save_path+'/flow_{}.jpg'.format(cnt), flow)
        prev = next.copy()
        cnt+=1

