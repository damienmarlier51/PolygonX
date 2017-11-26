import numpy as np
import math
import polygonX
from polygonX import pgx
import matplotlib.pylab as plt

def L2_distance(a,b):
	return math.sqrt(sum([(x-y)*(x-y) for (x,y) in zip(a,b)]))

# This function plots a C-shape distribution
def generate_c_shape_distribution(nb_points=1000, c_center=[0.5,0.5], c_inner_radius=0.1, c_outer_radius=0.2):
	c_points = []
	#Generate points till we get the desired number of points
	while len(c_points)<nb_points:
		point = np.random.rand(1,2)[0]
		#Check whether generated point is in C shape
		if point[0]<c_center[0] and L2_distance(point,c_center)>c_inner_radius and L2_distance(point,c_center)<c_outer_radius:
			c_points.append(point)
	return c_points

l = 0.01
c_points = generate_c_shape_distribution(1000, [0.5,0.5], 0.1, 0.2)
#Plot generated points
plt.scatter([x[0] for x in c_points],[x[1] for x in c_points])
edges = pgx.draw(c_points,l)
#Plot polygon edges
for edge in edges:
	plt.plot([c_points[edge[0]][0], c_points[edge[1]][0]], [c_points[edge[0]][1], c_points[edge[1]][1]], color='red')
plt.show()