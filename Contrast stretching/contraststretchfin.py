import cv2
import numpy as np
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input image")
args = vars(ap.parse_args())
 
# load the input image from disk
img = cv2.imread(args["input"])

img = cv2.resize(img,(img.shape[1]/2,img.shape[0]/2))

# convert the image to grayscale, blur it, and threshold it
image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow('original',img)

#input image pixel values in a list 'k'
k=[]
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		k.append(image[i][j])

c1=len(k)

#finding max number in the list of values
maxk = 0
for j in range(c1):
	if k[j]>maxk:
		maxk = k[j]
mink=maxk

for j in range(c1):
	if k[j]<mink:
		mink=k[j]


v=maxk-mink

for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		image[i][j]=(image[i][j]-mink)*255/(v)
		#print image[i][j]

#forming a histogram
#img=image
#import histofin
cv2.imshow('new',image)
#cv2.imwrite('contrasted.jpg',image)

cv2.waitKey(0)
cv2.destroyAllWindows()
