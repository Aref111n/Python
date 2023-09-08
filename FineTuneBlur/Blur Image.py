import cv2
import numpy as np
import matplotlib.pyplot as plt

def imgshow(img):
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def blur_img(path, depth):
    img = cv2.imread(path)
    mat = np.ones((depth,depth), dtype = 'uint32')/(depth*depth)
    blur_img = cv2.filter2D(img, -1, mat)
    imgshow(blur_img)

print('Enter the path of the Image:')
path = input()
print('Enter depth[0-100]:')
depth = int(input())
blur_img(path, depth)
