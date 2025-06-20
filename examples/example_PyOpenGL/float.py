from math import *
import numpy as np

# numpy.float32
dtype = np.float32

if __name__ == '__main__':
    fp   = dtype(1.0)

    expo = 0
    eps  = dtype(1.0)
    # eps
    while True:
        result = fp + eps
        print(expo, ":", eps)

        if result == fp: # no difference in addition
            break

        expo -= 1
        eps  /= dtype(2.0)

    value = fp + dtype(10e-8)
    print(fp == value, value)

    value = fp + dtype(10e-9)
    print(fp == value, value)

    
