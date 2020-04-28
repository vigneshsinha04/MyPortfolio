import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video = cv2.VideoCapture(0)
while True:
	return_value, image = video.read()

	faces = face_cascade.detectMultiScale(image,
		scaleFactor=1.05,
		minNeighbors=5)

	for x,y,w,h in faces:
		image=cv2.rectangle(image, (x,y),(x+w,y+h),(0,255,0))

	cv2.imshow("Video", image)
	key = cv2.waitKey(1)
	if key == ord('c'):
		break
	if cv2.getWindowProperty('Video',cv2.WND_PROP_VISIBLE) < 1:        
            break

video.release()
cv2.destroyAllWindows()