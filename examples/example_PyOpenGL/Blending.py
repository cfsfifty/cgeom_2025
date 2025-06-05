'''
 Drawing a OBJ 2d-polygon
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
 
# Global variables
title        = b"without blending of background color" # Windowed mode's title
windowWidth  = 600 # Windowed mode's width
windowHeight = 600 # Windowed mode's height
windowPosX   = 50  # Windowed mode's top-left corner x
windowPosY   = 50  # Windowed mode's top-left corner y
 
# Projection clipping area
# clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop;
state   = (False, False)

# Initialize OpenGL Graphics 
def initGL():
	# blending other AND src
	# dest = alpha_src*src + (1-alpha_src)*other
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def drawGeometry():
	glLineWidth(2.0)

	glBegin(GL_LINES)
	glColor4f  (1.0, 0.0, 0.0, 0.2)  # Red, alpha=0.2
	glVertex2f (-2.0, 1.0)
	glVertex2f ( 1.0, 3.0) # 2, -3
	glColor4f  (1.0, 0.0, 0.0, 1.0)  # Red, alpha=1.0
	glVertex2f (0.0, -2.0)
	glVertex2f (3.0, 0.0)
	glEnd()

# Callback handler for window re-paint event
def display():
	glClear(GL_COLOR_BUFFER_BIT) # Clear the color buffer
	center_x = 0.0
	center_y = 0.0
	glMatrixMode(GL_MODELVIEW)  # To operate on the ModelView matrix
	glLoadIdentity()
	glTranslatef  (-center_x, -center_y, 0.0)

	drawGeometry()
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
	size_x = 0.5*10.0 
	size_y = 0.5*10.0
	size   = max(size_x, size_y)
	if width >= height:
		clipAreaXLeft   = -size * aspect
		clipAreaXRight  =  size * aspect
		clipAreaYBottom = -size
		clipAreaYTop    =  size
	else:
		clipAreaXLeft   = -size
		clipAreaXRight  =  size
		clipAreaYBottom = -size / aspect
		clipAreaYTop    =  size / aspect
	gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop)
 
# Called back when the timer expired 
#def Timer(value : int) -> None:
#glutTimerFunc(10, Timer, 0) # subsequent timer call at milliseconds

# key-press event 
def key_press(kcode, x, y):
	global state
	
	modstate = glutGetModifiers()
	print(kcode)
	if kcode == b' ':
		blend = not state[0]
		state = (blend, state[1])
		if state[0]:
			title = b'with blending of background color'
			glEnable   (GL_BLEND)
		else:
			title = b'without blending of background color'
			glDisable   (GL_BLEND)
		glutSetWindowTitle(title)
	if kcode == b'b':
		backgroundWhite = not state[1]
		state = (state[0], backgroundWhite)
		if state[1]:
			glClearColor(1.0, 1.0, 1.0, 1.0) # Set background (clear) color to white
		else:
			glClearColor(0.0, 0.0, 0.0, 1.0) # Set background (clear) color to black
	glutPostRedisplay()
# key-release event 
def key_release(kcode, x, y):
	global state
	glutPostRedisplay()

# Main function: GLUT runs as a console application starting at main() */
def main():
	glutInit(sys.argv)             # Initialize GLUT
	glutInitDisplayMode(GLUT_DOUBLE) # double buffer
	glutInitWindowSize (windowWidth, windowHeight)  # Initial window width and height
	glutInitWindowPosition(windowPosX, windowPosY)  # Initial window top-left corner (x, y)
	glutCreateWindow(title)       # Create window with given title
	glutReshapeFunc(reshape)      # Register callback handler for window re-shape
	glutDisplayFunc(display)      # Register callback handler for window re-paint
	glutKeyboardFunc(key_press)
	glutKeyboardUpFunc(key_release)

	initGL()                      # Our own OpenGL initialization
	glutMainLoop()                # Enter event-processing loop

if __name__ == '__main__':
	main()