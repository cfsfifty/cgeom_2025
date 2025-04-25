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
	glClearColor(1.0, 1.0, 1.0, 1.0) # Set background (clear) color to black

	center_x = 0.5*(state.x[1] + state.x[0])
	center_y = 0.5*(state.y[1] + state.y[0])
	glMatrixMode(GL_MODELVIEW)  # To operate on the ModelView matrix
	glLoadIdentity()
	glTranslatef(-center_x, -center_y, 0.0)

	# for polygonal types, not line types
	glFrontFace  (GL_CCW) # this is the default 
	glPolygonMode(GL_FRONT, GL_FILL) # front face (Vorderseite)
	glPolygonMode(GL_BACK,  GL_LINE) # back  face (Rückseite)

def drawGeometry():
	# Outline polygon
	glLineWidth(2.0)
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

# Callback handler for window re-paint event
def display():
	glClear     (GL_COLOR_BUFFER_BIT) # Clear the color buffer
	glMatrixMode(GL_MODELVIEW)   # To operate on the model-view matrix
	glLoadIdentity()             # Reset model-view matrix

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
	size_x = state.x[1] - state.x[0]
	size_y = state.y[1] - state.y[0]
	scale  = max(size_x, size_y)
	if width >= height:
		clipAreaXLeft   = -0.5*scale * aspect
		clipAreaXRight  =  0.5*scale * aspect
		clipAreaYBottom = -0.5*scale
		clipAreaYTop    =  0.5*scale
	else:
		clipAreaXLeft   = -0.5*scale
		clipAreaXRight  =  0.5*scale
		clipAreaYBottom = -0.5*scale / aspect
		clipAreaYTop    =  0.5*scale / aspect
	gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop)
 
# Called back when the timer expired 
#def Timer(value : int) -> None:
#glutTimerFunc(10, Timer, 0) # subsequent timer call at milliseconds
 
# Main function: GLUT runs as a console application starting at main() */
def main():
	state.read("../star.obj")
	#state.read("../nrw.obj")


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