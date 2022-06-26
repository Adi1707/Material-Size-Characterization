import marshal
import cv2 as cv
import numpy as np
import pandas as pd
import sklearn as sk
from matplotlib import pyplot as plt
from skimage import io , color , measure
from scipy import ndimage
from sklearn.preprocessing import KernelCenterer

class Image_Pr:
    def __init__(self):
        pass

    def obtain_data(self):
        img = cv.imread("pellet.jpg")
        image = cv.imread("pellet.jpg" , 0)
        pix_um_ratio = 0.5

        ret , thresh = cv.threshold(image , 0 , 255 , cv.THRESH_BINARY+cv.THRESH_OTSU)

        kernel = np.ones((3,3),np.uint8)
        opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel,iterations=2)


        sure_bg = cv.dilate(opening , kernel , iterations=2)

        dist_transform = cv.distanceTransform(opening , cv.DIST_L2 , 3)
        ret2 , sure_fg = cv.threshold(dist_transform , 0.2*dist_transform.max() , 255 , 0)

        sure_fg = np.uint8(sure_fg)
        unknown_area = cv.subtract(sure_bg,sure_fg)


        ret3 , markers = cv.connectedComponents(sure_fg)
        markers = markers+10

        markers[unknown_area==255] = 0

        markers = cv.watershed(img,markers)
        img[markers == -1] = [255,0,255]

        img1 = color.label2rgb(markers,bg_label=0)
        propList = ['Area',
                    'equivalent_diameter', 
                    'orientation',
                    'MajorAxisLength',
                    'MinorAxisLength',
                    'Perimeter',
                    'MinIntensity',
                    'MeanIntensity',
                    'MaxIntensity']

        regions = measure.regionprops_table(markers , intensity_image=image , properties=propList)
        df = pd.DataFrame(regions)
        return df
        #print(df.head())

ipr = Image_Pr()
