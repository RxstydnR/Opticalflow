# coding: UTF-8
import sys
import os
import glob
import argparse

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image,ImageOps, ImageDraw, ImageFilter


def image_processing(img_path):
    """ Processing Images to suit the purpose of the experiment.（画像の前処理.）
        - Mask processing (masking the logs in the lower left corner). マスク処理（左下の撮影ログをマスク処理）
        - Resize (画像サイズの変更)
        - Median Blur (ぼかし効果)
        - Croping center (中央切り抜き)
        - Random rotation and flip (ランダムに回転 & 左右反転)

    Args:
        img_path (str): Image path (画像パス)

    Returns:
        img: Processed image (加工済み画像)
    """

    img = Image.open(img_path)
    
    # Resize
    img = img.resize((640,480), Image.LANCZOS)

    # Crop -> (480,480)
    img = img.crop((90, 0, 570, 480))

    # Smoothing
    # img = cv2.medianBlur(np.array(img), ksize=5) # ksize=3 (Auroral Image Classification with Deep Neural Networks,A. Kvammen,2020)

    # Rotate at 45 degrees each rotation angle (45度ずつの回転角度で回転を行う）
    # ANGLE = random.randint(0, 7)
    # img = img.rotate(45*ANGLE)

    # Flipping an image left to right
    # if random.choice([True, False]):
    #     img = ImageOps.mirror(img)

    # Mask processing
    mask_height = 480
    mask_width = 480
    black_mask = Image.open("black.jpg").resize((mask_width,mask_height))
    # img.paste(black_mask, (0, 480-mask_height))
    
    # Adjusting the center camera space. (中央の全点カメラ領域の調整)
    circle_margin = 30

    # Drawing a circle in another panel. (円を別パネルに描画)
    circle_mask = Image.new("L", (480,480), 255)
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse(((circle_margin,circle_margin),(480-circle_margin,480-circle_margin)), fill=0)
    
    # Paste mask (black_maskをペースト)
    img.paste(black_mask, (0, 0), circle_mask)

    return img



parser = argparse.ArgumentParser(prog='image_processing.py')
parser.add_argument('--data_path', type=str, required=True, help='The path of image data.')
parser.add_argument('--save_path', type=str, required=True, help='The path of save folder.')
opt = parser.parse_args()

if __name__ == "__main__":
    
    data_path = opt.data_path
    save_path = opt.save_path

    for filename in tqdm(glob.glob(data_path+"/*.jpg")):
        img = image_processing(filename)
        img.save(os.path.join(save_path, filename.split("/")[-1]))

        