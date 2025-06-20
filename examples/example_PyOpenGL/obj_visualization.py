'''
 Drawing a OBJ 2d-polygon
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import FileObj3d
import copy 
import ColorplotList 
import BarplotList 
 
# Loader/writer for OBJ files
state   = FileObj3d.FileObj3d()

def merge_lists (part1 : tuple[int, int], part2 : tuple[int, int], work : list[int], index : list[int], data):
	start1, end1 = part1
	start2, end2 = part2
	assert(start1 < end1)
	assert(start2 < end2)
	assert(end1 == start2)

	p1 = start1
	p2 = start2
	p  = start1
	# copy of first part
	work[start1:end1] = index[start1:end1]
	#print(work[start1:end1], index[start1:end1])

	while (p1 < end1 and p2 < end2):
		assert(start1 <= p and p < end2)
		if data[work[p1]][0] <= data[index[p2]][0]:
			#print(data[work[p1]], data[index[p2]])
			index[p] = work[p1]
			p  += 1
			p1 += 1
		elif data[work[p1]][0] >  data[index[p2]][0]:
			index[p] = index[p2]
			p  += 1
			p2 += 1
	
	# remainder of both halfs
	if p1 < end1:
		#print(p1, end1, p, end2)
		assert(end2-p == end1-p1)
		# copy remainder of p1, end1
		index[p:end2] = work[p1:end1]
	if p2 < end2:
		assert(end2-p == end2-p2)
		# copy remainder of p2, end2; already in place
		#index[p:end2] = index[p2:end2]
		pass

def merge_sort (part : tuple[int, int], work : list[int], index : list[int], data : list, plot) -> None:
	start, end = part
	if end-start == 1:
		#plot.plot(part)
		# nothing to do, sorted
		return
	if end-start == 2:
		# compare the two
		if data[index[start]][0] > data[index[start+1]][0]:
			(index[start+1], index[start]) = (index[start], index[start+1]) 
		#plot.plot(part)
		return
	
	# part1 nicht kuerzer als part2
	mid   = (start+end)//2+1
	part1 = (start, mid)
	part2 = (mid,   end)
	#print      (part1, part2)
	# sortiere part1, part2, dann zusammenfuegen
	merge_sort (part1, work, index, data, plot)
	merge_sort (part2, work, index, data, plot)
	# vor merge
	plot.plot(part, "darkgray")
	merge_lists(part1, part2, work, index, data)
	# nach merge
	plot.plot(part, "black")

def insertion_sort (index : list[int], data : list, plot) -> None:
	pos = 0
	while (pos < len(index)):
		# einsortieren von element pos
		current = index[pos]
		#print(pos, current, data[current])
		plot.plot((pos, pos+1))
		for i in range(pos-1, -1, -1):
			if data[index[i]][0] <= data[current][0]:
				# index[0:(i+1)] ist sortiert
				#index[i+1] = current
				break
			index[i+1] = index[i]
			index[i]   = current
			plot.plot((i, pos+1))
		pos += 1
	


# Main function: GLUT runs as a console application starting at main() */
def main():
	print(os.getcwd())
	state.read("../../dodecahedron.obj")
	data  = state.getPointCoords()

	index = list(range(0, len(data)))
	work  = copy.deepcopy(index) 
	all   = (0, len(index))
	#print(index)
	plot    = ColorplotList.ColorplotList(index, data) 
	#plot    = BarplotList.BarplotList(index, data) 
	merge_sort (all, work, index, data, plot)
	#insertion_sort(index, data, plot)
	plot.plot(all)
	#print(index)

	# filter triangles
	left_points_indices   = index[0:len(index)//2]
	right_points_indices  = index[len(index)//2:len(index)]	
	def filter_indices (inIndices : list, filter : list) -> list:
		outIndices = []
		for ids in inIndices:
			outIndices.append(list())
			for id in ids:
				if id in filter:
					outIndices[-1].append(id)
				#else:
				#	outIndices.pop()
				#	break
			if len(outIndices[-1]) < 3:
				outIndices.pop()
		return outIndices
	leftFaces  = filter_indices(state.getFaces(), left_points_indices)
	rightFaces = filter_indices(state.getFaces(), right_points_indices)

	# left
	state.writeObj("left.obj",  data, leftFaces)
	# right
	state.writeObj("right.obj", data, rightFaces)

	'''
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
	'''

if __name__ == '__main__':
	main()