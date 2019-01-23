from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import cv2
import dlib
import time


def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear


#def drowsy(initialT):
	 
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0
blinks = 0
initialT= 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("Loading gaze detector...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cap = cv2.VideoCapture(0)
eyecascade = cv2.CascadeClassifier('haarcascade_eye.xml')


while True:
	ret, frame = cap.read()
	roi_eye = frame

	if ret==True:

		windowClose = np.ones((5,5),np.uint8)
		windowOpen = np.ones((2,2),np.uint8)
		windowErode = np.ones((2,2),np.uint8)
		window = np.ones((2,2),np.uint8)

		frame_width = int(cap.get(3))
		frame_height = int(cap.get(4))

		rects = detector(roi_eye, 0)

		for rect in rects:
			shape = predictor(roi_eye, rect)
			shape = face_utils.shape_to_np(shape)

			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)

			ear = (leftEAR + rightEAR) / 2.0

			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)

			mask = np.zeros(frame.shape,np.uint8)
			cv2.drawContours(mask,[leftEyeHull],0,255)

			cv2.drawContours(mask,[rightEyeHull],0,255)

			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
			BothEyes = [leftEye, rightEye]

			for Eye in BothEyes:
				(x, y, w, h) = cv2.boundingRect(Eye)
				roi_colour = frame[y+3:y+h, x:x+w]

				try:
					roi_eye = cv2.cvtColor(roi_colour, cv2.COLOR_BGR2GRAY)
				except cv2.error:
					continue
				roi_eye = cv2.equalizeHist(roi_eye)
				roi_eye = cv2.medianBlur(roi_eye,9)
				#cv2.imshow('onlyEye',roi_eye)

				_, threshold = cv2.threshold(roi_eye, roi_eye[:].min()+2, 255, cv2.THRESH_BINARY_INV)
				roi_eye = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, windowClose)
				roi_eye = cv2.morphologyEx(roi_eye, cv2.MORPH_ERODE, windowErode)
				roi_eye = cv2.morphologyEx(roi_eye, cv2.MORPH_OPEN, windowOpen)

				_, contours, _ = cv2.findContours(roi_eye, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
				contours = sorted(contours, key=lambda x: cv2.contourArea(x))#, reverse=True)

				rows, cols, _ = roi_colour.shape

				for cnt in contours:
					center = cv2.moments(cnt)
					try:
						cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
					except ZeroDivisionError:
						continue	
					cx = cx -4
					cv2.circle(roi_colour,(int(cx),int(cy)),5,(0,0,255),-1)
					cv2.imshow('Eye detected',roi_colour)
					rh = int(rows/2)
					#Right Left pupil detection
					if cx>(rh+17):
						cv2.putText(frame, "Right", (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 60, 255), 2)
					elif cx<(rh):
						cv2.putText(frame, "Left", (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 60, 255), 2)
					break
				#Thresholded image
				#cv2.imshow("Threshold", frame)


			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter
			if ear < EYE_AR_THRESH:
				COUNTER += 1

			# otherwise, the eye aspect ratio is not below the blink
			# threshold
			else:
				# if the eyes were closed for a sufficient number of
				# then increment the total number of blinks
				if COUNTER >= EYE_AR_CONSEC_FRAMES:
					cv2.putText(frame, "Blinked!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					TOTAL += 1
					if TOTAL==1:
						initialT = time.time()
					blinks += 1 
					freq = blinks/4
					if initialT+5 < time.time():
						initialT = time.time()
						blinks = 0
			
					if freq>1:
						print("Drowsy!")
						

				# reset the eye frame counter
				COUNTER = 0

			#cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			#Full frame captured only when eye detected
			#cv2.imshow("FullFrame", roi_eye)				
		#videoWriter.write(frame)
		
		cv2.imshow('Main', frame)

		if cv2.waitKey(40) &0xFF== ord('q'):
			break
	else:
		break

#videoWriter.release()
cap.release()
cv2.destroyAllWindows()