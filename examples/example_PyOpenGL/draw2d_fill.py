'''
 Drawing a OBJ 2d-polygon
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import FileObj
import random
 
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
	glClearColor(0.0, 0.0, 0.0, 1.0) # Set background (clear) color to black
	# for polygonal types, not line types
	glFrontFace  (GL_CW) # this is the default 
	glPolygonMode(GL_FRONT, GL_FILL) # front face (Vorderseite)
	glPolygonMode(GL_BACK,  GL_LINE) # back  face (Rückseite)

def drawGeometry():
	# Outline polygon
	glLineWidth(2.0)
	glBegin(GL_LINE_LOOP)
	glColor3f  (1.0, 0.0, 0.0)  # Red
	for poly_point in state.getPolygon(): # Last vertex same as first vertex
		#glColor3f  (random.random(), random.random(), random.random())  # Red
		glVertex2fv(poly_point)
	glEnd()
def drawGeometryFill():
	# Outline polygon
	glLineWidth(2.0)
	glBegin(GL_TRIANGLE_FAN)
	#glBegin(GL_POLYGON)
	glColor3f  (1.0, 0.0, 0.0)  # Red
	for poly_point in state.getPolygon(): # Last vertex same as first vertex
		#glColor3f  (random.random(), random.random(), random.random())  # Red
		glVertex2fv(poly_point)
	glEnd()

# Callback handler for window re-paint event
def display():
	glClear     (GL_COLOR_BUFFER_BIT) # Clear the color buffer
	glMatrixMode(GL_MODELVIEW)   # To operate on the model-view matrix
	glLoadIdentity()             # Reset model-view matrix
	drawGeometryFill()
	glutSwapBuffers()  # Swap front and back buffers (of double buffered mode)

# Callback handler for window re-paint event, using display lists
def displayDisplayList():
	glClear     (GL_COLOR_BUFFER_BIT) # Clear the color buffer
	glMatrixMode(GL_MODELVIEW)   # To operate on the model-view matrix
	glLoadIdentity()             # Reset model-view matrix
	if stateGL[0] < 0: # not compiled, then compile and execute
		glNewList(stateGL[0], GL_COMPILE_AND_EXECUTE)
		drawGeometryFill()
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
	if width >= height:
		clipAreaXLeft   = state.x[0] #* aspect
		clipAreaXRight  = state.x[1] #* aspect
		clipAreaYBottom = state.y[0]
		clipAreaYTop    = state.y[1]
	else:
		clipAreaXLeft   = state.x[0]
		clipAreaXRight  = state.x[1]
		clipAreaYBottom = state.y[0] #/ aspect
		clipAreaYTop    = state.y[1] #/ aspect
	gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop)
 
# Called back when the timer expired 
#def Timer(value : int) -> None:
#glutTimerFunc(10, Timer, 0) # subsequent timer call at milliseconds
 
# Main function: GLUT runs as a console application starting at main() */
def main():
	#state.read("../star.obj")
	state.read("../nrw.obj")
	# call to update self.indices once
	state.getPolygonIndices()

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