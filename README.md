# PolygonX

Python implementation of the algorithm described in the paper [Efficient generation of simple polygons for characterizing the shape of a set of points in the plane](http://www.sciencedirect.com/science/article/pii/S0031320308001180) from Matt Duckham et al.

## Introduction

## Prerequisites

* Scipy
* Numpy (optional, used in the examples)

## Installing

```
git clone https://github.com/damienmarlier51/PolygonX.git
cd PolygonX
python setup.py install
```

## Examples

```
import numpy as np
from polygonX import pgx
import matplotlib.pylab as plt

points = np.random.rand(1000,2)
edges = pgx.draw(points,l=0.05)

plt.scatter([x[0] for x in points],[x[1] for x in points])
plt.plot([[points[edge[0]][0], points[edge[1]][0]] for edge in edges], [[points[edge[0]][1], points[edge[1]][1]] for edge in edges], color='red')
plt.show()
```

Additional examples are provided in the file example.py

```
python example.py
```

## Authors

* **Damien Marlier**

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details
