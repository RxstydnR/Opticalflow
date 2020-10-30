# Opticalflow for Aurora image

These codes are written for calculating and visualizing the movement of the aurora, but can be used for other purpose as well.

# Usage
## image_preprocess.py

**In : images** <br>
**Out : processed images**

This code is for formatting images that are unevenly shaped or have unwanted parts.
In addition, augmentation and removing noise are supported.

Included process are below, but **more will be added in the future**.
- Masking
- Resize
- Mediun Blur
- Cropping
- Random rotation and flipping


Run `"image_preprocess.py"`

```bash
python image_preprocess.py --data_path [Image folder] --save_path [Save folder]
```
---

## make_movie.py

**In : images** <br>
**Out : a movie**

This code is for create a video from multiple image data using "opencv2".

Run `"make_movie.py"`

Note that image names should be consistent.(ex. 00001.jpg,00002.jpg) <br>
Unless the images in the video may not line up in the correct order.

```bash
python make_movie.py --data_path [Image folder] --save_path [Save folder] --fps 20.0
```

---

## opticalflow_image.py

**In : images** <br>
**Out : opticalflow images**

This code calculates the optical flow of image sequence and outputs it to image sequence.
**Optical flow parameters have to be adjusted by your hand.**


Run `"opticalflow_image.py"`

Note that image names should be consistent.(ex. 00001.jpg,00002.jpg) <br>
Unless the images in the video may not line up in the correct order.

```bash
python opticalflow_image.py --data_path [Image folder] --save_path [Save folder]
```

---

## opticalflow_movie.py

**In : movie** <br>
**Out : opticalflow movie**

This code calculates the optical flow of the video and outputs it to the video.
**Optical flow parameters have to be adjusted by your hand.**


Run `"opticalflow_movie.py"`

```bash
python opticalflow_movie.py --data_path [Movie path] --save_path [Save folder] --fps 20.0
```


## Note

MP4 video sometimes fails to be save.<br>
**.avi** format is used in these codes.

**I test environments under Mac, not Windows.**
