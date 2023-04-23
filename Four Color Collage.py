import cv2
import numpy as np
import pandas as pd

def four_color_collage(path):
    img = cv2.imread(path)
    b, g, r = cv2.split(img)
    zero = np.zeros(img.shape[0:2], dtype='uint8')
    blue = cv2.merge([b, zero, zero])
    green = cv2.merge([zero, g, zero])
    red = cv2.merge([zero, zero, r])
    frow = np.hstack((red, green))
    srow = np.hstack((blue, img))
    grid = np.vstack((frow, srow))
    cv2.imshow('Image', grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

four_color_collage('C:\\Users\\user\\Downloads\\pic.jpg')
