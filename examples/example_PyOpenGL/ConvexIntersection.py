'''
 Grahams Scan
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import numpy as np
import FileObj
import random
import math
 
# Global variables
title        = b"Polygon" # Windowed mode's title
windowWidth  = 600 # Windowed mode's width
windowHeight = 600 # Windowed mode's height
windowPosX   = 50  # Windowed mode's top-left corner x
windowPosY   = 50  # Windowed mode's top-left corner y
 
# Projection clipping area
# clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop;
state   = (FileObj.FileObj(), FileObj.FileObj())
stateGL = [ -1 ]
#bbox_minx = -1.0
#bbox_maxx = +1.0
#bbox_miny = -1.0
#bbox_maxy = +1.0

# Initialize OpenGL Graphics 
def initGL():
	glClearColor(1.0, 1.0, 1.0, 1.0) # Set background (clear) color to black
	# for polygonal types, not line types
	glFrontFace  (GL_CW) # GL_CCW is the default 
	glPolygonMode(GL_FRONT, GL_FILL) # front face (Vorderseite)
	glPolygonMode(GL_BACK,  GL_LINE) # back  face (Rückseite)

def drawGeometry():
	# Outline polygon
	glLineWidth(2.0)
	glPointSize(5.0)
	glEnable(GL_POINT_SMOOTH)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glBegin(GL_TRIANGLE_FAN)
	#glBegin(GL_LINE_LOOP)
	poly = state.getPolygon()
	glColor3f  (1.0, 0.0, 0.0)  # Red
	#glVertex2fv(poly[0])
	#glVertex2fv(poly[2])
	#glVertex2fv(poly[3])
	for poly_point in poly: # Last vertex same as first vertex
		#glColor3f  (random.random(), random.random(), random.random())  # Red
		glVertex2fv(poly_point)
	glEnd()
	glColor3f  (0.0, 0.0, 0.0)  # Red
	glBegin(GL_POINTS)
	for poly_point in state.getPointCoords(): # Last vertex same as first vertex
		#glColor3f  (random.random(), random.random(), random.random())  # Red
		glVertex2fv(poly_point)
	glEnd()

# Callback handler for window re-paint event
def display():
	glClear     (GL_COLOR_BUFFER_BIT) # Clear the color buffer
	center_x = 0.5*(state.x[1] + state.x[0]) # refactor: move to "state"
	center_y = 0.5*(state.y[1] + state.y[0])
	print("model-center", center_x, center_y)
	glMatrixMode(GL_MODELVIEW)  # To operate on the ModelView matrix
	glLoadIdentity()
	glTranslated  (-center_x, -center_y, 0.0)

	drawGeometry()
	glutSwapBuffers()  # Swap front and back buffers (of double buffered mode)

# Callback handler for window re-paint event, using display lists
def displayDisplayList():
	glClear     (GL_COLOR_BUFFER_BIT) # Clear the color buffer
	glMatrixMode(GL_MODELVIEW)   # To operate on the model-view matrix
	glLoadIdentity()             # Reset model-view matrix

	if stateGL[0] < 0: # not compiled, then compile and execute
		glNewList(stateGL[0], GL_COMPILE_AND_EXECUTE)
		drawGeometry()
		glEndList()
	else: # execute display-list
		glCallList(stateGL[0])
	glutSwapBuffers()  # Swap front and back buffers (of double buffered mode)
 
# Call back when the windows is re-sized */
def reshape(width, height):
	# Compute aspect ratio of the new window
	if height == 0: 
		height = 1 # To prevent divide by 0
	aspect = width / float(height)
	# Set the viewport to cover the new window
	glViewport(0, 0, width, height)
 
	# Set the aspect ratio of the clipping area to match the viewport
	glMatrixMode(GL_PROJECTION)  # To operate on the Projection matrix
	glLoadIdentity()             # Reset the projection matrix
	size_x = 0.5*(state.x[1] - state.x[0]) # refactor: move to "state"
	size_y = 0.5*(state.y[1] - state.y[0])
	size   = max(size_x, size_y)
	if width >= height:
		clipAreaXLeft   = -size * aspect
		clipAreaXRight  = size * aspect
		clipAreaYBottom = -size
		clipAreaYTop    = size
	else:
		clipAreaXLeft   = -size
		clipAreaXRight  = size
		clipAreaYBottom = -size / aspect
		clipAreaYTop    = size / aspect
	gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop)

def rightTurn (p, r, q) -> bool:
	n  = ( -(q[1]-p[1]), (q[0]-p[0]))
	dr = (  r[0]-p[0],    r[1]-p[1])
	len = math.sqrt(np.dot(n, n))
	n  = (n[0]/len, n[1]/len) # normalized
	#print(type(n[0]))
	# scalar product <n, dr>
	return (np.dot(n, dr) >= 0.0)

def rightTurnDet (p, r, q) -> bool:
	eps = np.float64(1e-14)
	d1  = (r[0]-p[0], r[1]-p[1])
	d2  = (q[0]-p[0], q[1]-p[1])
	diag1 =   d1[0]*d2[1] 
	diag2 = -(d1[1]*d2[0])
	return (-(diag1+diag2) <= eps)

def pointOf (curr : tuple, p : list, f1, f2):
	if curr[0] == 1: # poly1
		idx = curr[1] % len(f1)
		return p[f1[idx]]
	else: # poly2
		idx = curr[1] % len(f2)
		return p[f2[idx]]

def intersect (edge1 : tuple, edge2 : tuple, p : list, f1, f2):
	p11 = pointOf ( edge1, p, f1, f2)
	p12 = pointOf ((edge1[0], edge1[1]+1), p, f1, f2)
	p21 = pointOf ( edge2, p, f1, f2)
	p22 = pointOf ((edge2[0], edge2[1]+1), p, f1, f2)
	d1x = p12[0]-p11[0]
	d1y = p12[1]-p11[1]
	d2x = p22[0]-p21[0]
	d2y = p22[1]-p21[1]
	n1x = -d1y
	n1y =  d1x
	# (p-p11)*n == 0
	# (p21+t*d2)*n == p21*n +t*d2*n == 0
	t = -(p21[0]*n1x+p21[1]*n1y)/(d2x*n1x+d2y*n1y)
	print(edge1, edge2, "=", t)
	if t > 0.0 and t < 1.0:
		ip = (p21[0]+t*d2x, p21[1]+t*d2y)
		return (t, ip)
	return (-1.0, None)
		
def convexIntersect (poly : tuple[object, object]):
	p1 = poly[0].getPointCoords()
	f1 = poly[0].getPolygonIndices()
	p2 = poly[1].getPointCoords()
	f2 = poly[1].getPolygonIndices()
	# append points p2 to p1
	p1deg = len(p1)
	p1.extend(p2)
	p  = p1
	for i, f in enumerate(f2):
		# skip indexes of p1
		f2[i] = f+p1deg

    # find polygon chains
	left1  = 0
	right1 = left1
	print(p, f1, f2)
	E = list()
	for i, f in enumerate(f1):
		if p[f] < p[f1[left1]]:
			left1  = i
		if p[f] > p[f1[right1]]:
			right1 = i
	left2  = 0
	right2 = left2
	for i, f in enumerate(f2):
		if p[f] < p[f2[left2]]:
			left2  = i
		if p[f] > p[f2[right2]]:
			right2 = i

	print(left1, right1)
	print(left2, right2)
	curr1 = left1
	curr2 = left2
	while curr1 != right1 or curr2 != right2:
		if pointOf((1, curr1), p, f1, f2) < pointOf((2, curr2), p, f1, f2):
			E.append((1, curr1))
			curr1 = (curr1+1) % len(f1)
		else:
			E.append((2, curr2))
			curr2 = (curr2+1) % len(f2)
	while curr1 != right1:
		E.append((1, curr1))
		curr1 = (curr1+1) % len(f1)
	while curr2 != right2:
		E.append((1, curr1))
		curr2 = (curr2+2) % len(f2)
			
	# run event list
	last = E[0]
	for i, e in enumerate(E):
		print("upper index", last)
		if e[0] != last[0]: # test intersection
			q = intersect(e, last, p, f1, f2)
			if q[0] >= 0.0:
				print("new point coord", q)
				plast = pointOf (last, p, f1, f2)
				# one must be upper: q/e or last
				if plast[1] > q[1][1]:
				    last = (e[0], e[1]+1)
	#state.getPolygonIndices() = idx

# Called back when the timer expired 
#def Timer(value : int) -> None:
#glutTimerFunc(10, Timer, 0) # subsequent timer call at milliseconds
 
# Main function: GLUT runs as a console application starting at main() 
def main():
	state[0].read("../star2.obj")
	state[1].read("../quad_xdifferent.obj")
	convexIntersect(state)
	return 

	glutInit(sys.argv)             # Initialize GLUT
	glutInitDisplayMode(GLUT_DOUBLE) # Enable double buffered mode
	glutInitWindowSize (windowWidth, windowHeight)  # Initial window width and height
	glutInitWindowPosition(windowPosX, windowPosY)  # Initial window top-left corner (x, y)
	glutCreateWindow(title)       # Create window with given title
	glutReshapeFunc(reshape)      # Register callback handler for window re-shape
	glutDisplayFunc(display)      # Register callback handler for window re-paint
	#glutIdleFunc(display)         # Register callback handler for window idling: redisplay
	#glutTimerFunc(0, Timer, 0)    # First timer call immediately
	
	initGL()                      # Our own OpenGL initialization
	glutMainLoop()                # Enter event-processing loop

if __name__ == '__main__':
	main()