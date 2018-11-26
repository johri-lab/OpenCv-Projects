## Identifying and Counting objects using OpenCv
---

To accomplish this, we leveraged contour approximation, the process of reducing the number of points on a curve to form a closed loop and draw the loops found. OpenCv provides two functions [cv2.findContours()](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html) and [cv2.drawContours()](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html) to identify closed loops in an image and to draw the loops respectively.


For this purpose we do the same in the following pattern:

+ Firstly, we read an input image and convert it into a gray-scaled image.

+ Then we apply various filter like the blur filter to reduce noise in the image, and thresholding to have an image with only the objects visible, to identify it efficiently.

Note: Prior to applying thresholding operation, it is necessary to grayscale the image, as [cv2.threshold()](https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html) function accepts only a gray-scaled image.

+ Now, using [cv2.findContours()](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html) function we find all the contours (or closed loops) in the processed image.

+ Lastly, all the contours are drawn over the source image, using the [cv2.drawContours()](https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html) function, and displayed.



**Note:**
*The [cv2.GaussianBlur()](https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html) function give the parameters for smoothening the image and reducing noise in the image. Similarly, [cv2.threshold()](https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html) function provides parameters to threshold the image in different ways.*

*In order to apply this on different images one needs to play with these values of the parameters of the functions. Please click on the functions to know more about the parameters and use of these functions.  *


## Running
---

The prerequisite is that you need to have the OpenCV library installed. Refer to some tutorials on how to do that.
To run the program open terminal and change the current working directory to the one which contains the project and run the following command:
```shell
python Contour.py -i Desktop/images/shapes.jpg
```

Please checkout the example below to know properly.


## Original image
Input images of 'shapes' and 'stars' in the two images:


## 1
![shapessmall](https://user-images.githubusercontent.com/30645315/40272613-d728e0a2-5bcd-11e8-8129-e541020b2802.jpg)

## 2
![starsmall](https://user-images.githubusercontent.com/30645315/40272687-1f7fda62-5bcf-11e8-8116-2af88ef92075.jpg)



## Image after applying gaussian blur & thresholding
The images after the blur and threshold filter:


## 1
![shapethresh](https://user-images.githubusercontent.com/30645315/40272679-020f6952-5bcf-11e8-927c-53ff14fdfbc1.jpg)

## 2
For this image the blur filter is removed and parameter values for threshold function are altered as follows:
```shell
ret, thresh = cv2.threshold(gray,33,255,cv2.THRESH_BINARY)
```
![thresh1](https://user-images.githubusercontent.com/30645315/40272691-3057400a-5bcf-11e8-9cb3-7b77c0030aeb.jpg)


## Contoured image
These are the final contoured images in the two cases:


## 1
![shapecontoured](https://user-images.githubusercontent.com/30645315/40272678-01e310fa-5bcf-11e8-8e1b-e63507f327ca.jpg)

## 2
![contour1](https://user-images.githubusercontent.com/30645315/40272692-3a087b6e-5bcf-11e8-8fc5-653a81dccc5d.jpg)



## Result
---
Terminal results of final calculated number of identified shapes in the images:


## 1
![newshape](https://user-images.githubusercontent.com/30645315/40272792-438e529c-5bd1-11e8-9857-7539d3524a0a.jpeg)

## 2
![newstar](https://user-images.githubusercontent.com/30645315/40272793-43bccad2-5bd1-11e8-930e-b76985c7e550.jpeg)
