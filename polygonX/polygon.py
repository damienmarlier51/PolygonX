import math
from scipy.spatial import Delaunay
from operator import itemgetter
from .dart import Dart
from .triangulation import Triangulation

def distance(x,y):
	return math.sqrt(math.fsum([(a-b)*(a-b) for a,b in zip(x,y)]))

#Delaunay triangulation
def triangularize(points):

	edges = []

	#Run Delaunay triangularization
	triangles = Delaunay(points).simplices
	for triangle in triangles:
		triangle.sort()
		if not [triangle[0],triangle[1]] in edges:
			edges.append([triangle[0],triangle[1]])
		if not [triangle[1],triangle[2]] in edges:
			edges.append([triangle[1],triangle[2]])
		if not [triangle[0],triangle[2]] in edges:
			edges.append([triangle[0],triangle[2]])

	#No need to compute the distance for all edges
	for edge in edges:
		edge.append(distance(points[edge[0]],points[edge[1]]))

	return edges

class Polygon:

	points = []
	edges = []
	darts = {}
	vertex_boundary_dic = {}

	def __init__(self,points=[]):
		self.points = points

	def draw(self,l=0.05):

		#1.1
		points = self.points
		edges = triangularize(points)
		triangulation = Triangulation(edges=edges, points=points)

		import matplotlib.pyplot as plt
		plt.scatter([x[0] for x in points],[x[1] for x in points],s=1)
		for edge in triangulation.edges:
			plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
		plt.title('l = %.3f' % l)
		plt.show()

		for i,point in enumerate(points):
			triangulation.vertex_boundary_dic[i] = False
		
		#1.2
		boundary_edges = triangulation.get_boundary_edges()

		#1.3
		boundary_edges = [x for x in sorted(boundary_edges, key=itemgetter(2))][::-1]

		#1.4
		for edge in boundary_edges:
			triangulation.vertex_boundary_dic[edge[0]] = True
			triangulation.vertex_boundary_dic[edge[1]] = True

		#1.9
		while len(boundary_edges)>0:

			#1.10
			boundary_edge = boundary_edges[0]

			#1.11
			if len(boundary_edges)>1:
				boundary_edges = boundary_edges[1:]
			else:
				boundary_edges = []

			#1.12
			if boundary_edge[2]>l and triangulation.is_regular(boundary_edge):
				
				#1.13
				new_edges = [x for x in triangulation.edges if x != boundary_edge]
				new_triangulation = Triangulation(edges=triangulation.edges, points=triangulation.points, vertex_boundary_dic=triangulation.vertex_boundary_dic)
				
				#1.14				
				dart1 = new_triangulation.get_dart(vertex=edge[0],direction=edge[1])
				new_dart1 = new_triangulation.reveal(dart1)
				edge1 = [new_dart1.vertex, new_dart1.direction, distance(points[new_dart1.vertex],points[new_dart1.direction])]

				dart2 = new_triangulation.get_dart(vertex=edge[1],direction=edge[0])
				new_dart2 = new_triangulation.reveal(dart2)
				edge2 = [new_dart2.vertex, new_dart2.direction, distance(points[new_dart1.vertex],points[new_dart1.direction])]

				iter_idx = 0
				if len(boundary_edges)>0:
					while boundary_edges[iter_idx][2]>edge1[2]:
						iter_idx += 1
						if iter_idx == len(boundary_edges):
							break
					boundary_edges.insert(iter_idx,edge1)

				iter_idx = 0
				if len(boundary_edges)>0:
					while boundary_edges[iter_idx][2]>edge2[2]:
						iter_idx += 1
						if iter_idx == len(boundary_edges):
							break
					boundary_edges.insert(iter_idx,edge2)

				#1.15
				new_triangulation.vertex_boundary_dic[new_dart1.vertex] = True

				triangulation = new_triangulation

		#1.16
		boundary_edges = triangulation.get_boundary_edges()

		import matplotlib.pyplot as plt
		plt.scatter([x[0] for x in points],[x[1] for x in points],s=1)
		for edge in boundary_edges:
			plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
		plt.title('l = %.3f' % l)
		plt.show()
