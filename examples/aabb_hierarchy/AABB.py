import math 
#import numpy as np

class AABB:
    def __init__(self):
        self.k   = 3
        self.extend = [ [math.inf for i in range(self.k)], [-math.inf for i in range(self.k)]]

    def center (self) -> tuple:
        center = [ 0 for i in range(self.k)]
        for i in range(self.k):
            center[i] = 0.5*(self.extend[0][i]+self.extend[1][i])
        return center
    
    def is_intersect (self, b : object) -> bool: # CF why not AABB?
        for i in self.k:
            if (self.extend[1][i] < b.extend[0][i] or self.extend[0][i] > b.extend[1][i]):
                return False
        return True

    def is_inside (self, coord : tuple) -> bool:
        if self.k >= 1 and not(self.extend[0][0] <= coord[0] and coord[0] <= self.extend[1][0]):
            return False
        if self.k >= 2 and not(self.extend[0][1] <= coord[1] and coord[1] <= self.extend[1][1]):
            return False
        if self.k >= 3 and not(self.extend[0][2] <= coord[2] and coord[2] <= self.extend[1][2]):
            return False
        return True

    def add_coords (self, coords : list) -> None:
        for c in coords:
            assert(len(c) <= self.k)
            for i in range(len(c)):
                self.extend[0][i] = min(self.extend[0][i], c[i])                    
                self.extend[1][i] = max(self.extend[1][i], c[i])   
    def add_box (self, b : object) -> None:
        assert(self.k == b.k)
        for i in range(len(self.k)):
            self.extend[0][i] = min(self.extend[0][i], b.extend[0][i])                    
            self.extend[1][i] = max(self.extend[1][i], b.extend[1][i])   
            
    def __str__ (self):
        return str(self.extend)

                            
