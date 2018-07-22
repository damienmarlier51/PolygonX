import math
from scipy.spatial import Delaunay
from operator import itemgetter
from .dart import Dart

def distance(x,y):
	return math.sqrt(math.fsum([(a-b)*(a-b) for a,b in zip(x,y)]))

#Delaunay triangulation
def triangularize(self,points):

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
		edge.append(Polygon.distance(points[edge[0]],points[edge[1]]))

	return edges

class Polygon:

	points = []
	edges = []
	darts = {}
	vertex_boundary_dic = {}

	def __init__(self):
		self.points = []

	def draw(l=0.05):

		points = self.points
		edges = triangularize(points)
		triangulation = Triangulation(edges=edges, points=points)

		for i,point in enumerate(points):
			triangulation.vertex_boundary_dic[i] = False
		
		boundary_edges = triangulation.get_boundary_edges()
		
		for edge in boundary_edges:
			triangulation.vertex_boundary_dic[edge[0]] = True
			triangulation.vertex_boundary_dic[edge[1]] = True

		#Sort boundary edges by distance
		boundary_edges_remain = [x for x in boundary_edges if x[2] <= l]
		boundary_edges = [x for x in sorted(boundary_edges, key=itemgetter(2))[::-1] if x[2] > l]

		while len(boundary_edges)>0:

			#Get head of list
			boundary_edge = boundary_edges[0]

			if len(boundary_edges)>1:
				boundary_edges = boundary_edges[1:]
			else:
				boundary_edges = []

			dart = triangulation.get_dart(boundary_edge[1])
			dart.set_direction(boundary_edge[0])
			is_regular_bool, vertex = polygon.is_regular(dart)

			if is_regular_bool:

				#Add edge to B
				edge = [boundary_edge[1],vertex]
				edge.sort()
				edge.append(Polygon.distance(polygon.points[edge[0]],polygon.points[edge[1]]))

				if edge[2]>l:
					#insert edge
					iter_idx = 0
					if len(boundary_edges)>0:
						while boundary_edges[iter_idx][2]>edge[2]:
							iter_idx += 1
							if iter_idx == len(boundary_edges):
								break
					boundary_edges.insert(iter_idx,edge)
				else:
					boundary_edges_remain.append(edge)

				#Add edge to B
				edge = [boundary_edge[0],vertex]
				edge.sort()
				edge.append(Polygon.distance(polygon.points[edge[0]],polygon.points[edge[1]]))

				if edge[2]>l:
					#insert edge
					iter_idx = 0
					if len(boundary_edges)>0:
						while boundary_edges[iter_idx][2]>edge[2]:
							iter_idx += 1
							if iter_idx == len(boundary_edges):
								break
					boundary_edges.insert(iter_idx,edge)
				else:
					boundary_edges_remain.append(edge)

				#Update edges
				polygon.edges = [x for x in polygon.edges if not (x[0]==boundary_edge[0] and x[1]==boundary_edge[1])]
				polygon.vertex_boundary_dic[dart.direction] = True

				del polygon.darts[boundary_edge[0]]
				del polygon.darts[boundary_edge[1]]

			else:

				boundary_edges_remain.append(boundary_edge)

		import matplotlib.pyplot as plt
		plt.scatter([x[0] for x in points],[x[1] for x in points],s=1)
		for edge in boundary_edges_remain:
			plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
		plt.title('l = %.2f' % l)
		plt.show()

		#Sort list to make it a connected chain
		ordered_chain = []
		vertex = boundary_edges_remain[0][0]
		nb_boundary_edges = len(boundary_edges_remain)

		while len(ordered_chain)!=nb_boundary_edges:
			#Find vertex edge
			edge = [[i,x] for i,x in enumerate(boundary_edges_remain) if x[0]==vertex or x[1]==vertex][0]
			new_vertex = [x for x in edge[1] if x!=vertex][0]
			ordered_chain.append([vertex,new_vertex])
			prev_vertex = vertex
			vertex = new_vertex
			#Remove visited edge
			boundary_edges_remain.pop(edge[0])

		return ordered_chain