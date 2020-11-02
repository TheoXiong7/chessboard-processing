import cv2 
import numpy as np 

img = cv2.imread('board.png')

# It converts the BGR color space of image to HSV color space 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

# Threshold of blue in HSV space 
lower_white = np.array([205, 235, 235]) 
upper_white = np.array([220, 240, 240]) 

lower_green = np.array([80, 140, 110]) 
upper_green = np.array([90, 160, 125]) 

# preparing the mask to overlay 
mask_green = cv2.inRange(img, lower_green, upper_green)

mask_white = cv2.inRange(img, lower_white, upper_white) 
mask = mask_white + mask_green
# The black region in the mask has the value of 0, 
# so when multiplied with original image removes all non-blue regions 
result = cv2.bitwise_and(img, img, mask = mask) 

#cv2.imshow('img', img) 
#cv2.imshow('mask', mask) 
#cv2.imshow('result', result) 
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
dst = cv2.Canny(gray, 50, 200, None, 3)
cv2.imshow('gray', gray)
linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, 1, 40, 8)
if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

cv2.imshow('result', img)
cv2.waitKey(0) 

cv2.destroyAllWindows() 