import struct
import cv2 as cv
import numpy as np 

from matplotlib import pyplot as plt
from skimage import io , color , measure
#Scikit Image is a collection of image processing algorithms
from scipy import ndimage
#ndimage -> This package contains various functions for multidimensional image processing.

#loading the image
img = cv.imread("pellet.jpg" , 0)
width = img.shape[0]
height = img.shape[1]
print(width)
print(height)

grain = img[:,:]                #no cropping is to be done
#cv.imshow("Sample" , grain)

pix_to_um_ratio = 0.5

#Thresholding
ret , thresh = cv.threshold(grain , 0 , 255 , cv.THRESH_BINARY+cv.THRESH_OTSU)
cv.imshow("Thresholded Image" , thresh)
#Eroded
kernel = np.ones((3,3),np.uint8)
erode = cv.erode(thresh,kernel,iterations=1)
cv.imshow("Eroded Image" , erode)
#Dilate Image
dilate = cv.dilate(thresh,kernel,iterations=1)
cv.imshow("Dilated Image" , erode)

#Masking the Image
#We need a binary image. The thresholded image is binary as it contains values which are either 0 or 255 but for the compiler, its datatype is unit8
#mask would create a binary image with datatype bool
mask = dilate==255


s = [[1,1,1],[1,1,1],[1,1,1]] 
label_mask , num_labels = ndimage.label(mask , structure=s)
img2 = color.label2rgb(label_mask , bg_label=0)
cv.imshow("colored",img2)

print()
clusters = measure.regionprops(label_mask , img)

propList = ['Area',
            'equivalent_diameter', 
            'orientation',
            'MajorAxisLength',
            'MinorAxisLength',
            'Perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']    
    

output_file = open('image_measurements.csv', 'w')
output_file.write(',' + ",".join(propList) + '\n') #join strings in array by commas, leave first cell blank
#First cell blank to leave room for header (column names)

for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]*pix_to_um_ratio**2   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
            to_print = cluster_props[prop]*pix_to_um_ratio
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')
output_file.close()   #Closes the file, otherwise it would be read only. 

cv.waitKey(0)
