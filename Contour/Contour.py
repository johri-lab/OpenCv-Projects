import cv2
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

# BGR to gray color conversion
gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)

# apply blur filter to remove noise
blur = cv2.GaussianBlur(gray,(11,11),29)

# apply thrasholding
ret, thresh = cv2.threshold(blur,235,255,cv2.THRESH_BINARY_INV)

# display thresholded image
cv2.imshow("THRESHOLD", thresh)

# find all contours in the processed image
contours,heirarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print "There are %d shapes in the image"%len(contours)

# draw all contours( outlining ) 
for i in contours: 
	cv2.drawContours(img,[i],-1,(0,0,255),3)

# display the contoured image
cv2.imshow("Contoured Image",img)
cv2.waitKey(0)
