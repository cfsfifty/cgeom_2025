import math
import locale
import matplotlib.pyplot as plt # gantt chart
import numpy as np
import colormap_from_named_colors_rgb
import matplotlib.colors as mcolors

''' '''
class ColorplotList:
    # 
    def __init__(self, indices : list, data : list):
        self.indices = indices
        self.data    = data
        # value interval
        self.d_min   = min([ self.data[idx][0] for idx in self.indices])
        self.d_max   = max([ self.data[idx][0] for idx in self.indices])

        # selbst-erzeugt oder per Name
        self.cmap     = colormap_from_named_colors_rgb.colormap_from_named_colors_rgb (
            ['white', 'red', 'yellow', 'lightcyan', 'deepskyblue', 'darkviolet']) #'blue', 'navy'
        self.row      = 0
        self.maxrow   = 2*len(self.indices)
        print(len(self.indices), self.maxrow, 'in', self.d_min, self.d_max)
        self.dataline = -np.inf*np.ones(shape=(self.maxrow,len(self.indices)), dtype=float)

    def plot (self, part : tuple, color : str="black"):
        if self.row >= self.maxrow:
            print("WARNING: all rows used")
            return
        
        for i, idx in enumerate(self.indices):
            self.dataline[self.row,i] = self.data[idx][0]

        self.row += 1
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.imshow(self.dataline, origin='upper', interpolation='none', 
                       #cmap="tab20")
                        cmap=self.cmap)
        for i, idx in enumerate(self.indices):
            # linker Rand, mitte Zeile, fontsize=9
            ax.text(i-0.5, self.row-0.5, str(idx), fontsize=9, color="black")

        def subdivide_part (d : int, dmax : int, part : tuple[int], func) -> None:
            if d >= dmax:
                # part-size 4 ist kleinste 
                return
            mid   = int(math.ceil((part[0] + part[1])/2))
            # in-order traversal
            
            part1  = (part[0], mid)
            func(part1)
            subdivide_part (d+1, dmax, part1, func)
            part2  = (mid,     part[1])
            func(part2)
            subdivide_part (d+1, dmax, part2, func)

        # bestimme xrange, xlabel
        xrange = list()
        xlabel = list()
        def generate_xlabel(part : tuple): 
            xrange.append(part[0])
            xlabel.append(str(xrange[-1]))

        subdivide_part(0, 3, (0, len(self.indices)), generate_xlabel)
        ax.set_xticks (xrange, labels=xlabel)
        ax.set_yticks (range(self.maxrow), labels=[str(v) for v in range(1, self.maxrow+1)])

        # zeichne colorbar in default position
        plt.colorbar(im, shrink=1.0)
        # zeichne Rahmen fuer part
        plt.plot([part[0]-0.5, part[1]-0.5, part[1]-0.5, part[0]-0.5], 
                 [self.row-1.5, self.row-1.5, self.row-0.5, self.row-0.5], 
                 color=color)

        plt.show()


    