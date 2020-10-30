# Opticalflow for Aurora image

These codes are written for calculating and visualizing the movement of the aurora, but can be used for other purpose as well.

## Usage

### image_preprocess.py
This code is for formatting images that are unevenly shaped or have unwanted parts.
In addition, augmentation and removing noise are supported.

Included process are below, but **more will be added in the future**.
- Masking
- Resize
- Mediun Blur
- Cropping
- Random rotation and flipping

**Run "image_preprocess.py"**

```bash
python image_preprocess.py --data_path [Image folder] --save_path [Save folder]
```

## Note

I test environments under Mac, not Windows.
