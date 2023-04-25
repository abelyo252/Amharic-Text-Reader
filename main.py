import cv2
import numpy as np
import util



heightImg = 640
widthImg  = 480



if __name__ == '__main__':
    image = cv2.imread("img/paper8.jpg")
    text = imageReader(image)
    print(text)

