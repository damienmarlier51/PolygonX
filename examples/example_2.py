import pandas as pd
from polygonX import pgx
import matplotlib.pylab as plt

df = pd.read_csv("metropolitan_french_cities.csv",header=None)
df = df.sample(n=1000)
points = df[[1,2]].values

for l in [0.5,1,3]:
	plt.scatter([x[0] for x in points],[x[1] for x in points],s=1)
	edges = pgx.draw(points,l)
	for edge in edges:
		plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
	plt.title('l = %.2f' % l)
	plt.show()