CMAKE_MINIMUM_REQUIRED(VERSION 3.1 FATAL_ERROR)
project (draw2d)

set(CMAKE_PREFIX_PATH "C:/Users/cfuen/source/ComputationGeometry_2025/github/cgeom_2025/lib/freeglut-3.6.0")
set(GLUT_ROOT_PATH    "C:/Users/cfuen/source/ComputationGeometry_2025/github/cgeom_2025/lib/freeglut-3.6.0")
# setting paths directly is not recommended!
#set(GLUT_INCLUDE_DIR "C:/Users/cfuen/source/ComputationGeometry_2025/github/cgeom_2025/lib/freeglut-3.6.0/include")
#set(OPENGL_LIBRARY_DIR "C:/Users/cfuen/source/ComputationGeometry_2025/github/cgeom_2025/lib/freeglut-3.6.0/lib")

# GLUT
find_package(GLUT REQUIRED)
include_directories(${GLUT_INCLUDE_DIR})
if(NOT GLUT_FOUND)
    message(ERROR "GLUT not found!")
endif(NOT GLUT_FOUND)

# OpenGL
find_package(OpenGL REQUIRED)
include_directories(${OpenGL_INCLUDE_DIRS})
if(NOT OPENGL_FOUND)
    message(ERROR "OPENGL not found!")
endif(NOT OPENGL_FOUND)

add_executable(draw2d draw2d.cpp)
target_link_libraries(draw2d ${OPENGL_LIBRARIES} ${GLUT_LIBRARY})
