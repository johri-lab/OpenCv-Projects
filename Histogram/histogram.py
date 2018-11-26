import cv2
import numpy as np

img=cv2.imread('histo.png',0)

#resize if images are large in sizes
#img = cv2.resize(img, (img.shape[1],img.shape[0]))

#displays the input image
cv2.imshow('img',img)

#input image pixel values in a list 'k'
k=[]
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		k.append(img[i][j])
#input list from image
#k=[2,3,5,7,8,1,4,10,3,12,2,3,3,3,3,3,2,4]

c1=len(k)

#finding max number in the list of frequencies
maxn = 0
for j in range(c1):
	if k[j]>maxn:
		maxn = k[j]

#find list of frequency of values in k from 0-max
l=[]
maxnc=maxn
while maxnc>=0:
	count=0
	for j in xrange(c1):	
		if k[j]==maxnc:
			count=count+1
	l.append(count)
	maxnc=maxnc-1

l.reverse()

print('\nList of pixel values:')
print(k)
print('\nList of frequency distribution:')
print(l)

# 'c' will determines the LENGTH of canvas and 'y' determines the HEIGHT of the canvas 
c=len(l)


#y=720
y=maxn*11
p=24
#c*23
#creating a black canvas 'a'
a=np.zeros((y,c*23,3), np.uint8)

y0=y-15


#cv2.namedWindow('Graph',cv2.WINDOW_NORMAL)

#y-axis scaling marked in green
for i in range(maxn+1):
	cv2.line(a,(14,y0),(12,y0),(0,255,0),thickness=1)
	y0=y0-10

for i in range(c):
	
	#x-axis scaling marked in green	
	cv2.line(a,(p,y-15),(p,y-12),(0,255,0),thickness=1)	
	y0=y0-10

	#histogram bars drawn in blue
	cv2.line(a,(p,y-15),(p,y-15-l[i]*2),(255,0,0),thickness=2,lineType=8,shift=0)
	p=p+20
	#l[]*2 helps to alters the height of the histogram bars

#boundary rectangle
cv2.rectangle(a,(4,0),(p+10,y-15+10),(255,255,255),thickness=2)
	
#x-axis
cv2.line(a,(10,y-15),(p,y-15),(0,0,255),thickness=2)

#y-axis
cv2.line(a,(14,10),(14,y-11),(0,0,255),thickness=2)

#graph heading text
cv2.putText(a,"Histogram",(c*11,20+c),cv2.FONT_HERSHEY_DUPLEX,0.05*c,(255,255,255),1)

#resizable window for the graph created
cv2.namedWindow('Graph',cv2.WINDOW_NORMAL)

#display final canvas
cv2.imshow('Graph',a)

cv2.waitKey(0)
cv2.destroyAllWindows()
