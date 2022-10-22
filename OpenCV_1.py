import cv2
import RPi.GPIO as GPIO
import time
import numpy as np
image_1=cv2.imread('art.jpg')
def Param(im):
	print(image_1.shape)
	height,widht=im.shape[:2]
	Size=im.size
	print('Size: ',Size)
	print('Width: ', widht)
	print('Height: ',height)
	pixel=image_1[200,500]
	print('BGR for [200;500]=',pixel)
	print('B =',pixel[0])
	print('G =',pixel[1])
	print('R =',pixel[2])	
	
try:
	if __name__=="__main__":
		while True:
			Param(image_1)
			output=cv2.resize(image_1,(560,560)) #BGR 
			#img_RGB=cv2.cvtColor(output,cv2.COLOR_BGR2HSV)
			cv2.imshow('Origin',output)
			cv2.waitKey()
			cv2.destroyAllDisplay()
			
				
				
except KeyboardInterrupt:
    print(' Exit pressed Ctrl+C')
    GPIO.cleanup()
    cv2.destroyAllWindows()


