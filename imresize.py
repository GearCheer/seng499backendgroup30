import cv2
import glob
import os

TARGET_DIR = 'resized-images'

os.mkdir(TARGET_DIR)

image_files = glob.glob("*.jpg")

for file in image_files:
    image = cv2.imread(file)
    new_image = cv2.resize(image, (512, 384))
    cv2.imwrite(TARGET_DIR + '/' + file, new_image)