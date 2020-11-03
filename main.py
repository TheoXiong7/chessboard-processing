import math
import cv2
import numpy as np
import imutils
from Line import Line
from Square import Square
from Board import Board

debug =  True


class board_Recognition:
	def __init__(self):
		pass
		

	def initialize_Board(self):

		corners = []

		# retake picture until board is initialized properly
		while len(corners) < 81:
			board_image = cv2.imread('aa.png')
			img = board_image.copy()
			# Binarize the photo
			# Black out all pixels outside the border of the chessboard
			lower_white = np.array([205, 235, 235]) 
			upper_white = np.array([220, 240, 240]) 

			lower_green = np.array([75, 150, 105])
			upper_green = np.array([80, 160, 110])

			lower_yellow = np.array([35, 205, 175])
			upper_yellow = np.array([105, 255, 245])

			mask_green = cv2.inRange(img, lower_green, upper_green)
			mask_white = cv2.inRange(img, lower_white, upper_white) 
			mask_yellow = cv2.inRange(img, lower_yellow, upper_yellow) 
			mask = mask_white + mask_green
			# Find edges
			if debug:
				cv2.imshow("mask", mask)
				cv2.waitKey(0)
				cv2.destroyAllWindows()
			edges,colorEdges = self.findEdges(mask)

			# Find lines
			horizontal, vertical = self.findLines(edges,colorEdges)

			# Find corners
			corners = self.findCorners(horizontal, vertical, colorEdges)

		# Find squares
		squares = self.findSquares(corners, img)

		# create Board
		board = Board(squares)

		return board


	def findEdges(self, image):
		'''
		Finds edges in the image. Edges later used to find lines and so on
		'''
	
		# Find edges
		edges = cv2.Canny(image, 100, 200, None, 3)
		if debug:
			#Show image with edges drawn
			cv2.imshow("Canny", edges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		# Convert edges image to grayscale
		colorEdges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

		return edges,colorEdges

	def findLines (self, edges, colorEdges):
		'''
		Finds the lines in the photo and sorts into vertical and horizontal
		'''
		
		# Infer lines based on edges
		lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 100,np.array([]), 100, 80)

		# Draw lines
		a,b,c = lines.shape
		for i in range(a):
			cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0,255,0),2,cv2.LINE_AA)

		if  debug:
			# Show image with lines drawn
			cv2.imshow("Lines",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		# Create line objects and sort them by orientation (horizontal or vertical)
		horizontal = []
		vertical = []
		for l in range(a):
			[[x1,y1,x2,y2]] = lines[l]
			newLine = Line(x1,x2,y1,y2)
			if newLine.orientation == 'horizontal':
				horizontal.append(newLine)
			else:
				vertical.append(newLine)

		return horizontal, vertical

	def findCorners (self, horizontal, vertical, colorEdges):
		'''
		Finds corners at intersection of horizontal and vertical lines.
		'''

		# Find corners (intersections of lines)
		corners = []
		for v in vertical:
			for h in horizontal:
				s1,s2 = v.find_intersection(h)
				corners.append([s1,s2])

		# remove duplicate corners
		dedupeCorners = []
		for c in corners:
			matchingFlag = False
			for d in dedupeCorners:
				if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 20:
					matchingFlag = True
					break
			if not matchingFlag:
				dedupeCorners.append(c)

		for d in dedupeCorners:
			cv2.circle(colorEdges, (d[0],d[1]), 10, (0,0,255))


		if debug:
			#Show image with corners circled
			cv2.imshow("Corners",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return dedupeCorners

	def findSquares(self, corners, colorEdges):
		'''
		Finds the squares of the chessboard 
		'''

		# sort corners by row
		corners.sort(key=lambda x: x[0])
		rows = [[],[],[],[],[],[],[],[],[]]
		r = 0
		for c in range(0, 81):
			if c > 0 and c % 9 == 0:
				r = r + 1

			rows[r].append(corners[c])

		letters = ['a','b','c','d','e','f','g','h']
		numbers = ['1','2','3','4','5','6','7','8']
		Squares = []
		
		# sort corners by column
		for r in rows:
			r.sort(key=lambda y: y[1])
		
		# initialize squares
		for r in range(0,8):
			for c in range (0,8):
				c1 = rows[r][c]
				c2 = rows[r][c + 1]
				c3 = rows[r + 1][c]
				c4 = rows[r + 1][c + 1]

				position = letters[r] + numbers[7-c]
				newSquare = Square(colorEdges,c1,c2,c3,c4,position)
				newSquare.draw(colorEdges,(0,0,255),2)
				newSquare.drawROI(colorEdges,(255,0,0),2)
				newSquare.classify(colorEdges)
				Squares.append(newSquare)



		if debug:
			#Show image with squares and ROI drawn and position labelled
			cv2.imshow("Squares", colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return Squares

board = board_Recognition().initialize_Board()
