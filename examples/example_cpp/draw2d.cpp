// Drawing a OBJ 2d-polygon
#include <cmath>
#include <ctime>
#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include "FileObj.h"
 
// Global variables
const char* title        = "Polygon"; // Windowed mode's title
int windowWidth  = 600; // Windowed mode's width
int windowHeight = 600; // Windowed mode's height
int windowPosX   = 50;  // Windowed mode's top-left corner x
int windowPosY   = 50;  // Windowed mode's top-left corner y
 
// Projection clipping area
// clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop;
FileObj state;
GLuint  stateGL[] = { GLuint(-1), GLuint(-1), GLuint(-1) };


bool checkErrorGL () 
{
    GLenum err = glGetError(); 
    assert(err == GL_NO_ERROR);
    return (err != GL_NO_ERROR);
}

// Initialize OpenGL Graphics 
void initGL()
{
   glClearColor(0.0, 0.0, 0.0, 1.0); // Set background (clear) color to black
   //glClearDepth(1.0f);
   //glEnable(GL_DEPTH_TEST);
}

// Callback handler for window re-paint event
void display()
{
  glClear  (GL_COLOR_BUFFER_BIT); // Clear the color buffer
  //glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear the color and depth buffer
  glMatrixMode(GL_MODELVIEW); // To operate on the model-view matrix
  glLoadIdentity();           // Reset model-view matrix
	
  // Use triangular segments to form a circle
  glLineWidth(2.0f);
  glBegin(GL_LINE_LOOP);
  glColor3f  (1.0f, 0.0f, 0.0f);  // Red
  auto poly = state.getPolygon();
  for (auto iter = poly.begin(); iter != poly.end(); ++iter) { // Last vertex same as first vertex
      glVertex2f(iter->x, iter->y);
  }
  glEnd();
  checkErrorGL();

  glutSwapBuffers(); // Swap front and back buffers (of double buffered mode)
}
// Callback handler for window re-paint event, using display lists
void displayDisplayList()
{
  glClear     (GL_COLOR_BUFFER_BIT); // Clear the color buffer
  glMatrixMode(GL_MODELVIEW); // To operate on the model-view matrix
  glLoadIdentity();           // Reset model-view matrix

  if (stateGL[0] == GLuint(-1)) {
      stateGL[0] = glGenLists(1);
  }
  glNewList(stateGL[0], GL_COMPILE_AND_EXECUTE); // Use triangular segments to form a circle
    checkErrorGL();
    glLineWidth(2.0);
    glBegin(GL_LINE_LOOP);
    glColor3f  (1.0, 0.0, 0.0); // Red
    auto poly = state.getPolygon();
    for (auto iter = poly.begin(); iter != poly.end(); ++iter) { // Last vertex same as first vertex
	glVertex2fv(*iter);
    }
    glEnd();
  checkErrorGL();
  glEndList();

  glutSwapBuffers(); // Swap front and back buffers (of double buffered mode)
}
// Call back when the windows is re-sized */
void reshape(int width, int height) {
    // Compute aspect ratio of the new window
    if (height == 0) {
        height = 1; // To prevent divide by 0
    }
        float aspect = width / float(height);
        // Set the viewport to cover the new window
        glViewport(0, 0, width, height);

        // Set the aspect ratio of the clipping area to match the viewport
        glMatrixMode(GL_PROJECTION); // To operate on the Projection matrix
        glLoadIdentity();            // Reset the projection matrix
        float clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop;
        if (width >= height) {
            clipAreaXLeft   = state.bbox_min.x; // *aspect;
            clipAreaXRight  = state.bbox_max.x; // *aspect;
            clipAreaYBottom = state.bbox_min.y;
            clipAreaYTop    = state.bbox_max.y;
        }
        else {
            clipAreaXLeft   = state.bbox_min.x;
            clipAreaXRight  = state.bbox_max.x;
            clipAreaYBottom = state.bbox_min.y; // / aspect;
            clipAreaYTop    = state.bbox_max.y; // / aspect;
        }
        gluOrtho2D(clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop);
}
 
// Called back when the timer expired 
//def Timer(value : int) -> None:
//glutTimerFunc(10, Timer, 0) // subsequent timer call at milliseconds
 
// Main function: GLUT runs as a console application starting at main() */
int main(int argc, char* argv[]) 
{
  //state.read("../star.obj");
  state.read("C:/Users/cfuen/source/ComputationGeometry_2025/github/cgeom_2025/examples/nrw.obj");

  glutInit(&argc, argv);            // Initialize GLUT
  glutInitDisplayMode(GLUT_DOUBLE); // Enable double buffered mode
  glutInitWindowSize(windowWidth, windowHeight);  // Initial window width and height
  glutInitWindowPosition(windowPosX, windowPosY); // Initial window top-left corner (x, y)
  glutCreateWindow(title);       // Create window with given title
  glutDisplayFunc (displayDisplayList);      // Register callback handler for window re-paint
  glutReshapeFunc (reshape);      // Register callback handler for window re-shape
  //glutTimerFunc(0, Timer, 0);    // First timer call immediately
  //glutIdleFunc(display);         // Register callback handler for window idling: redisplay
	
  initGL();                      // Our own OpenGL initialization
  glutMainLoop();                // Enter event-processing loop
}
