import cv2
import numpy as np

#selecting image from a list
'''images=['colours.jpg','fadednature.jpg','shapes.jpg','audi.jpg','table.jpg','Demo_Median.jpg','road.jpeg','frank.jpg','old.jpg']
images = []
imagelocation = []
for i in range(13):
	images.append('leaf'+str(i))
	imagelocation.append('leaf'+ str(i) + '.jpg')

print images
im=input("\nEnter the no. of image you want to apply mean filter on (0 to 12):")

im=input("\nEnter the name of image you want to apply mean filter on:")
'''
img=cv2.imread('Demo_Median.jpg',0)

cv2.imshow('Original Image',img)
print('Size of the image:')
print(img.shape)

#input the window propeties

w1=input('\nEnter length of the square window:')
w2=input('\nEnter height of the square window:')

div1=(w1-1)/2
div2=(w2-1)/2
#adding border padding
top=div2
bottom=top
left=div1
right=left
img=cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT, None, (255,255,255))

for y1 in range(0,img.shape[1]-div1):
	for x1 in range(0,img.shape[0]-div2):
		
		#finding arithematic median of the window elements 
		pp=[x1-div2,x1,x1+div2]
		cc=[y1-div1,y1,y1+div1]
		k=[]
		for i in pp:
			for j in cc:
				k.append(img[i][j])
		
		def sort(k):
			for p in range(1,len(k)):
				a = k[p]
				q = p-1
		      		while q>=0 and a<k[q]:
					k[q+1] = k[q]
			   		q=q-1
			  	k[q+1] = a  
		sort(k)
		c=len(k)	

		#exporting new value to the image at the window
		for i in range(x1-div2,x1+div2):
			for j in range(y1-div1,y1+div1):
				img[x1][y1]=k[c/2]

#cropping the image to exclude the padding
cropped = img[top:(img.shape[0]-top),left:(img.shape[1]-left)]
print('\nMean filter applied successfully!')
print('\nPress q to quit')
	
while True: 
	cv2.imshow('Mean filter',img)
	cv2.imshow('cropped',cropped)
	if cv2.waitKey(1) &0xFF==ord('q'):	
		break
cv2.destroyAllWindows()
