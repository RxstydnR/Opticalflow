import os
import cv2
import glob
import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# os.environ["CUDA_VISIBLE_DEVICES"] = "4"


def Movie_OpticalFlow(movie_path, save_path, params, fps):
    """ Create and save opticalflow videos.

    Args:
        movie_path (str): Path to movie.
        save_path (str): Path to save folder.
        params (list): Opticalflow parameters. (オプティカルフローのパラメータ)

    https://github.com/ContinuumIO/anaconda-issues/issues/223
    """
    
    cap = cv2.VideoCapture(movie_path)
    ret, frame1 = cap.read()
    prev = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[...,1] = 255
    
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Width of movie
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Height of movie
    
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    # Get the total number of frames. (総フレーム数を取得)
    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Frame rate (a frame is measured in milliseconds) (フレームレート(1フレームの時間単位はミリ秒)の取得)
    if fps <= 0:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Opticalflow movie
    writer_OPF = cv2.VideoWriter(save_path+"/Opticalflow.avi", fourcc, fps, (width,height))#, isColor=False)
    # Orignal movie corresponding to Opticalflow movie
    writer_ORG = cv2.VideoWriter(save_path+"/Original.avi", fourcc, fps, (width,height))#, isColor=False)

    while(True):
        ret, frame2 = cap.read()

        # check next frame exists.
        if not ret: break

        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        ''' Example Parameter
            Parameter reference : http://bicycle.life.coocan.jp/takamints/index.php/doc/opencv/function/calcOpticalFlowFarneback
                                : https://code-graffiti.com/opencv-dense-optical-flow-in-python/

            calcOpticalFlowFarneback( prevImg, nextImg, flow, pyrScale, levels, winsize, iterations, polyN, polySigma, flags ）                                
            calcOpticalFlowFarneback( prev,    next,    None,  0.5,       1,     10,      1,         10,    5.0,       256   ) 
        '''            
        flow = cv2.calcOpticalFlowFarneback(prev=prev, next=next,  flow=None,  pyr_scale=params[0],  levels=params[1],  winsize=params[2],  iterations=params[3],  poly_n=params[4],   poly_sigma=params[5], flags=params[6])
    
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)

        writer_OPF.write(rgb)
        writer_ORG.write(frame2)

        prev = next.copy()

    writer_OPF.release() 
    writer_ORG.release() 
    cap.release()
    cv2.destroyAllWindows()

    return 



if __name__=="__main__":

    parser = argparse.ArgumentParser(prog='opticalflow_movie.py')
    parser.add_argument('--data_path', type=str, required=True, help='The path of video.')
    parser.add_argument('--save_path', type=str, required=True, help='The path of save folder.')
    parser.add_argument('--fps', type=float, default=0, help='Frame Per Second. If you dont set, the same fps as your video will be used.')
    opt = parser.parse_args()

    os.makedirs(opt.save_path, exist_ok=False)

    params = [
        0.2, # pyrScale
        2,   # levels
        4,   # winsize
        2,   # iterations
        3,   # polyN
        30,  # polySigma
        256  # flags
    ]
    print(f"pyrScale={params[0]}, levels={params[1]}, winsize={params[2]}, iterations={params[3]}, polyN={params[4]}, polySigma={params[5]}, flags={params[6]}")

    Movie_OpticalFlow(opt.data_path, opt.save_path, params, opt.fps)




            
