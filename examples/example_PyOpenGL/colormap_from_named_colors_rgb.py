'''
DKRZ example 

Generate colormaps from given named colors

This script generates a new Matplotlib color object of n-colors from a given
list of named colors. Furthermore we write the RGB tuples of the color object
into a text file with two header lines needed for the use with NCL. And of
course we check the results in each case.

-------------------------------------------------------------------------------
2023 copyright DKRZ licensed under CC BY-NC-SA 4.0
               (https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)
-------------------------------------------------------------------------------
'''
import os
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def colormap_from_named_colors_rgb (color_list : list) -> mcolors.Colormap:
    #-- Choose named colors
    #
    # We want to create a colormap that goes from white to red, yellow, light cyan,
    # lightblue to dark blue. Therefore we create a list of the appropriate named
    # colors.
    #color_list = ['white', 'red', 'yellow', 'lightcyan', 'lightblue', 'navy']
    
    # Let's have a look at the RGB values of the color_list.
    for color in color_list:
        print(mcolors.to_rgba(color))
    
    #-- Create colormap from linear mapping segments (color_list)
    #
    # In the next step we want to generate the a colormap with 100 colors named
    # cmap_wryb. The color_list can be converted into an matplotlib.colors object
    # with `matplotlib.colors.LinearSegmentedColormap.from_list`.
    colormap_name = 'cmap_wryb'
    ncolors = 100
    
    color_obj = mcolors.LinearSegmentedColormap.from_list(colormap_name,
                                                          color_list,
                                                          N=ncolors)
    
    # Within the notebook, we can call the colormap object directly and it will
    # automatically display the corresponding colorbar. In a script nothing happens.
    color_obj
    
    for i in range(5):
        print(color_obj(i)[0:3])
    return color_obj