import pandas as pd
from polygonX import polygon
import matplotlib.pylab as plt
import numpy as np

df = pd.read_csv("metropolitan_french_cities.csv",header=None)
df = df.sample(n=2000)
points = df[[1,2]].values

polygon_ = polygon.Polygon(points=points)

for l in [0.00001]:
	edges = polygon_.draw(l)

	# plt.scatter([x[0] for x in points],[x[1] for x in points],s=1)
	# for edge in edges:
	# 	plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
	# plt.title('l = %.2f' % l)
	# plt.show()
