import math
import locale
import matplotlib.pyplot as plt # gantt chart
import numpy as np
import colormap_from_named_colors_rgb

''' '''
class BarplotList:
    # 
    def __init__(self, indices : list, data : list):
        self.indices = indices
        self.data    = data
        # value interval
        self.d_min   = min([ self.data[idx][0] for idx in self.indices])
        self.d_max   = max([ self.data[idx][0] for idx in self.indices])

        self.row      = 0
        print(len(self.indices), 'in', self.d_min, self.d_max)
        self.bardata = np.empty(shape=(len(self.indices),), dtype=float)

    def plot (self, part : tuple):
        #for i, idx in enumerate(self.indices):
        #    self.dataline[self.row,i] = self.data[idx][0]

        self.row += 1

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title('Iteration %i' % self.row)
        # zeichne Rahmen fuer part
        label = list()
        color = list()
        for i, idx in enumerate(self.indices):
            self.bardata[i] = self.data[idx][0]-self.d_min
            label.append(str(idx))
            color.append("r" if part[0] <= i and i < part[1] else "b")
        ax.barh(left=self.d_min, 
                y=range(len(self.indices)), 
                width=self.bardata, 
                tick_label=label,
                color =color,
                height=1, alpha=0.9, edgecolor='k')
            # linker Rand, mitte Zeile
            #ax.text(self.data[idx][0]+0.5, i, str(idx), fontsize=8, color="k")

        # bestimme xrange, xlabel
        xrange = list()
        xlabel = list()

        #ax.set_xticks (xrange, labels=xlabel)
        #ax.set_yticks (range(self.maxrow), labels=[str(v) for v in range(1, self.maxrow+1)])

        plt.show()


    