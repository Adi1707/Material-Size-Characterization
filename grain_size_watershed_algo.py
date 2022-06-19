import marshal
import cv2 as cv
import numpy as np
import sklearn as sk
from matplotlib import pyplot as plt
from skimage import io , color , measure
from scipy import ndimage
from sklearn.preprocessing import KernelCenterer

img = cv.imread("pellet.jpg")
cv.imshow("Raw Image",img)
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
cv.imshow("Original Image",img)
cv.imshow("Segmented Image" , img1)

regions = measure.regionprops(markers , intensity_image=image)

propList = ['Area',
            'equivalent_diameter', 
            'orientation',
            'MajorAxisLength',
            'MinorAxisLength',
            'Perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']    
    

output_file = open('image_measurements_watershed.csv', 'w')
output_file.write(',' + ",".join(propList) + '\n') #join strings in array by commas, leave first cell blank
#First cell blank to leave room for header (column names)

for cluster_props in regions:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]*pix_um_ratio**2   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
            to_print = cluster_props[prop]*pix_um_ratio
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')
output_file.close()   #Closes the file, otherwise it would be read only. 



cv.waitKey(0)



