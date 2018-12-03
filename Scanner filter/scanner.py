from PIL import Image
import numpy as np
import cv2

"""Scanner effect
	A module that applies a scanner effect to an image.
"""

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def sharp(image):
	# Create our shapening kernel, it must equal to one eventually
	kernel = np.zeros( (9,9), np.float32)
	kernel[4,4] = 2.0   #Identity, times two 

	#Create a box filter:
	boxFilter = np.ones( (9,9), np.float32) / 97.0

	#Subtract the two:
	kernel = kernel - boxFilter

	# applying the sharpening kernel to the input image & displaying it.
	sharpened = cv2.filter2D(image, -1, kernel)
	sharpened = cv2.bilateralFilter(sharpened, 9, 75, 75) # Noise reduction
	return sharpened

def saturation(image):
	hsvimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV).astype("float32")

	(h,s,v) = cv2.split(hsvimage)
	s=s*1.2
	v=v+2
	h=h-2
	s = np.clip(s,0,255)
	v = np.clip(v,0,255)
	h = np.clip(h,0,255)
	hsvimage = cv2.merge([h,s,v])

	return hsvimage

def whitebalance(image):

	value = 125
	h, s, v = cv2.split(image)
	
	lim = 255 - value
	v[((v > lim) & (v < 190))] = 200
	
	v[v <= lim] += 13#map(v,0,lim,0,255)
	cv2_image = cv2.merge((h, s, v))
	return cv2_image

# Method to process the red band of the image
def normalizeRed(intensity):
	iI = intensity
	minI = 59
	maxI = IR[1]

	minO = 0
	maxO = 255

	iO = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)+20
	return iO


# Method to process the green band of the image
def normalizeGreen(intensity):
	iI = intensity  
	minI = 54
	maxI = IG[1]

	minO = 0
	maxO = 255

	iO = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)+20
	return iO


# Method to process the blue band of the image
def normalizeBlue(intensity):
	iI = intensity
	minI = 59
	maxI = IB[1]

	minO = 0
	maxO = 255

	iO = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)+20
	return iO 

# Create an image object

image = cv2.imread("./doc.jpg")

cv2_image = sharp(image)
cv2_image = cv2.resize(cv2_image,(500,700))
cv2_image = saturation(cv2_image)

cv2_image = whitebalance(cv2_image)

cv2_image = cv2.cvtColor(cv2_image.astype("uint8"),cv2.COLOR_HSV2RGB)

imageObject = Image.fromarray(cv2_image)

imageObject.show()

# Split the red, green and blue bands from the Image
multiBands = imageObject.split()


IR = multiBands[0].getextrema()
IG = multiBands[1].getextrema()
IB = multiBands[2].getextrema()


# Apply point operations that does contrast stretching on each color band
normalizedRedBand = multiBands[0].point(normalizeRed)

normalizedGreenBand = multiBands[1].point(normalizeGreen)

normalizedBlueBand = multiBands[2].point(normalizeBlue)

# Create a new image from the contrast stretched red, green and blue brands
normalizedImage = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))

normalizedImage.show()
normalizedImage.save("normalizedImage.jpg","JPEG")

# Display the image before contrast stretching(original image)
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
image = Image.fromarray(image)
image = image.resize((500,700))

image.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
