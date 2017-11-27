# PolygonX

Python implementation of the algorithm described in the paper [Efficient generation of simple polygons for characterizing the shape of a set of points in the plane](http://www.sciencedirect.com/science/article/pii/S0031320308001180) from Matt Duckham et al.

## Introduction

## Prerequisites

* Scipy
* Numpy (optional, used in example 1)
* Pandas (optional, used in example 2)

## Installing

```
git clone https://github.com/damienmarlier51/PolygonX.git
cd PolygonX
python setup.py install
```

## Examples

Draw shape around random 2D distribution.

```
import numpy as np
from polygonX import pgx
import matplotlib.pylab as plt

for l in [0.05,0.1,0.2]:

	points = np.random.rand(1000,2)
	edges = pgx.draw(points,l=l)

	plt.scatter([x[0] for x in points],[x[1] for x in points])
	plt.plot([[points[edge[0]][0], points[edge[1]][0]] for edge in edges], [[points[edge[0]][1], points[edge[1]][1]] for edge in edges], color='red')
	plt.title('l = %.2f' % l)
	plt.show()
```
<p float="center">
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/0.05.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/0.10.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/0.20.png" width="33%"/>
</p>

Additional examples are provided in the folder example

**Example 1** Draw shape around random C letter like distribution.

```
python example_1.py
```

<p float="center">
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/c_0.01.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/c_0.05.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/c_0.10.png" width="33%"/>
</p>

**Example 2** Approximate French borders using French city coordinates.

```
python example_2.py
```

<p float="center">
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/f_0.50.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/f_1.00.png" width="33%"/>
	<img src="https://github.com/damienmarlier51/PolygonX/blob/master/examples/output_examples/f_3.00.png" width="33%"/>
</p>

## Authors

* **Damien Marlier**

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details
