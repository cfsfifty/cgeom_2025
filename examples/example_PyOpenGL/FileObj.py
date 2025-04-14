import math
import time
import datetime
import collections

''' '''
class FileObj:
    # 
    def __init__(self):
        pass

    #
    def read (self, filename : str) -> None:
        self.points   = list()
        self.indices  = list()
        self.filename = filename
        self.x        = [ math.inf, -math.inf]
        self.y        = [ math.inf, -math.inf]
        with open(self.filename, 'r') as file:
            num_line = 0
            while file:
                line      = file.readline()
                num_line += 1
                print(line)
                if not line: # line==None, so end-of-file
                    break
                #print(line)
                elements = line.split(sep=None)
                #print(elements)
                if len(elements) < 1 or elements[0] == "#": # skip empty line or comment line
                    continue 

                assert(len(elements) >= 1)
                if elements[0] == "v":
                    assert(2 <= len(elements) and len(elements) <= 4)
                    if len(elements) == 2: # 1d
                        coord = (float(elements[1]))    
                    if len(elements) == 3: # 2d
                        self.x[0] = min(self.x[0], float(elements[1]))
                        self.x[1] = max(self.x[1], float(elements[1]))
                        self.y[0] = min(self.y[0], float(elements[2]))
                        self.y[1] = max(self.y[1], float(elements[2]))
                        coord = (float(elements[1]), float(elements[2]))    
                    if len(elements) == 4: # 3d
                        coord = (float(elements[1]), float(elements[2]), float(elements[3]))    
                    self.points.append(coord)
                    continue
                if elements[0] == "f":
                    if len(self.indices) > 0:
                        print("WARNING: skipped additional face in line", num_line)
                        self.indices.clear() # clear list with each tag 'f', so only last face persists
                    for i in range(1, len(elements)): 
                        # indices in OBJ are 1 based
                        self.indices.append(int(elements[i])-1)
                    continue
        print("read points", len(self.points), "polygon", len(self.indices))
        if len(self.indices) == 0:
            for i in range(len(self.points)):
                self.indices.append(i) 

    # List of coords tuples of all points read 
    def getPointCoords (self) -> list:
        return self.points
    
    # List of indices into PointCoords list
    def getPolygonIndices (self) -> list:
        return self.indices
    
    # List of polygon coords tuples
    def getPolygon (self) -> list:
        assert(0 <= min(self.indices) and max(self.indices) < len(self.points))
        polygon   = [ self.points[idx] for idx in self.indices ]
        return polygon