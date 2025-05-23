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
state   = FileObj.FileObj()
stateGL = [ -1 ]
#bbox_minx = -1.0
#bbox_maxx = +1.0
#bbox_miny = -1.0
#bbox_maxy = +1.0

# Initialize OpenGL Graphics 
def initGL():
	glClearColor(1.0, 1.0, 1.0, 1.0) # Set background (clear) color to black
	# for polygonal types, not line types
	glFrontFace  (GL_CCW) # GL_CCW is the default 
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

def grahamsScan (state : FileObj):
	p   = state.getPointCoords()
	idx = state.getPolygonIndices()
	#print(idx)
	idx.sort(key=lambda i : p[i]) # for idx i return coords tuple, sorting lexicographically
	print(idx)
	# upper segment
	#lower = list(reversed(idx))
	lower = [ idx[0] ]
	i     = 2 
	while i < len(idx):
		# cw: i-2, i-1, i
		while i >= 2:
			pred = rightTurn(p[idx[i-2]], p[idx[i-1]], p[idx[i]])
			print(idx[i-2], idx[i-1], idx[i], pred)
			if pred:
				break
			last = idx[i]
			lower.insert(0, idx.pop(i-1))
			#idx.pop(i-1)
			i -= 1 # idx shrunk by 1 entry
			assert(idx[i] == last) # idx[i] is last known point on convex hull
		i += 1 # move to next point
	lower.insert(0, idx[-1])
	print("upper segment", idx, ", rest", lower)
	# lower strip
	i = 2
	while i < len(lower):
		# cw: i, i-1, i-2>=0
		#print(lower[i], lower[i-1], lower[i-2])
		while i >= 2:
			pred = rightTurn(p[lower[i-2]], p[lower[i-1]], p[lower[i]])
			print(lower[i-2], lower[i-1], lower[i], pred)
			if pred:
				break
			last = lower[i]
			lower.pop(i-1)
			i -= 1 # lower shrunk by 1 entry
			assert(lower[i] == last) # lower[i-1] is last known point on convex hull
		i += 1 # move to next point
	print("lower segment", lower)
	for i in range(1, len(lower)-1):
		idx.append(lower[i])
	print(idx)
	print("CH", len(idx))
	#state.getPolygonIndices() = idx

# Called back when the timer expired 
#def Timer(value : int) -> None:
#glutTimerFunc(10, Timer, 0) # subsequent timer call at milliseconds
 
# Main function: GLUT runs as a console application starting at main() 
def main():
	print(os.getcwd())
	state.points = list()
	state.indices= list()
	num = 20
	bbox_min = (-10.0, -10.0)
	bbox_max = ( 10.0,  10.0)
	radius   = 8.0
	rem = 0.0
	for i in range(num):
		state.points.append((2.0*math.pi)*random.random())
	state.points.sort()
	for i in range(num):
		state.points[i] = ((radius*math.cos(state.points[i]), radius*math.sin(state.points[i])))
		state.indices.append(i)
	state.updateBBox()
	state.writeObj("../../circularPoints20.obj", state.points, state.indices)	

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