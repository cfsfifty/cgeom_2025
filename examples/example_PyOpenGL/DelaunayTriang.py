import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import FileObj

# Projection clipping area
# clipAreaXLeft, clipAreaXRight, clipAreaYBottom, clipAreaYTop;
state   = FileObj.FileObj()

np.random.seed(2)
n_points = 20
X = np.random.randn(n_points, 2)
plt.scatter(X[:, 0], X[:, 1])

def tris2edges(tris):
    edges = set([])
    for tri in tris:
        for k in range(3):
            i, j = tri[k], tri[(k+1)%3]
            i, j = min(i, j), max(i, j)
            edges.add((i, j))
    return np.array(list(edges), dtype=int)
        
def writeDelaunay(X, tris):
    state.points = list()
    state.indices= list()
    for i in range(X.shape[0]):
        state.points.append((X[i][0], X[i][1]))
    for tri in tris:
        state.indices.append(list())
        state.indices[-1].extend([ tri[0], tri[1], tri[2] ])
    state.updateBBox()
    state.writeObj("../../randomDelaunay20.obj", state.points, state.indices)

tri = Delaunay(X)
print(tri.simplices)
writeDelaunay(X, tri.simplices)
edges = tris2edges(tri.simplices)
plt.scatter(X[:, 0], X[:, 1])
for [i, j] in edges:
    xi = X[i]
    xj = X[j]
    plt.plot([xi[0], xj[0]], [xi[1], xj[1]])
    
# Euclidean distances in an array parallel to the edges
distances = []
for [i, j] in edges:
    xi = X[i]
    xj = X[j]
    d = ((xi[0]-xj[0])**2 + (xi[1]-xj[1])**2)**0.5
    distances.append(d)
# Longest edge
idx = np.argmax(distances)
xi = X[edges[idx][0]]
xj = X[edges[idx][1]]
plt.plot([xi[0], xj[0]], [xi[1], xj[1]], linestyle='--', linewidth=3, c='k')
plt.show()
