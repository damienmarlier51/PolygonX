import math
from scipy.spatial import Delaunay
from operator import itemgetter
from .dart import Dart

class Polygon:

	points = []
	edges = []
	darts = {}
	vertex_boundary_dic = {}

	def __init__(self):
		self.points = []
		self.edges = []
		self.darts = {}
		self.vertex_boundary_dic = {}

	def get_dart(self,idx):
		#Get existing dart or create its instance
		if idx in self.darts:
			dart = self.darts[idx]
		else:
			dart = self.create_dart(idx)

		return dart

	def create_dart(self,idx):

		#get dart edges (list of points opposite to the vertex)
		point_edges = [x for x in self.edges if x[0]==idx or x[1]==idx]
		point_opposites = [[y for k,y in enumerate(x) if y!=idx or (k!=0 and k!=1)] for x in point_edges]
		for j,point_opposite in enumerate(point_opposites):
			point_opposites[j].append(Polygon.compute_edge_angle(self.points[idx],self.points[point_opposite[0]]))

		dart = Dart(idx,point_opposites,self)
		
		#Add to cache dictionnary not to recreate it again
		self.darts[idx] = dart

		return dart

	#Check network regularity after edge removal
	def is_regular(self,dart):

		#Check that vertex revealed by edge removal is interior
		vertex = self.reveal(dart).theta_0().vertex
		is_regular = not self.is_vertex_boundary(vertex)

		return [is_regular,vertex]

	def reveal(self,dart):

		#Make a copy for later reuse
		init_dart = Dart(dart.vertex,dart.edges,self,dart.direction)

		init_vertex = dart.vertex
		init_direction = dart.direction

		dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [init_vertex,init_direction] != [dart.vertex,dart.direction]:
			dart = init_dart.theta_0().theta_1().theta_0().theta_1().theta_0()
		else:
			dart = dart.theta_1()

		return dart

	#Check if vertex belongs to a boundary edge
	def is_vertex_boundary(self,vertex):
		return self.vertex_boundary_dic[vertex]

	#Check if an edge is on the boundary
	def is_edge_boundary(self,edge):

		boundary = False

		# Run through the combinatorial map for three cycles
		prev_idx = edge[1]
		current_idx = edge[0]

		dart = self.get_dart(current_idx)
		dart.set_direction(prev_idx)

		dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [dart.vertex,dart.direction] != [current_idx,prev_idx]:
			boundary = True

		#Try reverse cycle order
		prev_idx = edge[0]
		current_idx = edge[1]

		dart = self.get_dart(current_idx)
		dart.set_direction(prev_idx)

		dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [dart.vertex,dart.direction] != [current_idx,prev_idx]:
			boundary = True

		return boundary

	#Find polygon boundary edges
	def get_boundary_edges(self,edges):

		boundary_edges = []

		for edge in edges:
			
			boundary = self.is_edge_boundary(edge)

			if boundary:
				boundary_edges.append(edge)

		return boundary_edges

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

	@staticmethod
	def distance(x,y):
		return math.sqrt(math.fsum([(a-b)*(a-b) for a,b in zip(x,y)]))

	@staticmethod
	def compute_edge_angle(point_1,point_2):

		d0 = point_2[0]-point_1[0]
		d1 = point_2[1]-point_1[1]
		
		if d0>0:
			theta = math.atan(d1/d0)
		elif d0<0:
			theta = math.atan(d1/d0) + math.pi
		elif d0==0:
			if d1>0:
				theta = 1/2*math.pi
			elif d1<0:
				theta = 3/2*math.pi
			else:
				theta = 0

		theta /= math.pi
		
		return theta

	@staticmethod
	def draw(points=[],l=0.05):

		polygon = Polygon()
		polygon.points = points
		polygon.edges = polygon.triangularize(polygon.points)

		for i,point in enumerate(polygon.points):
			polygon.vertex_boundary_dic[i] = False
		
		boundary_edges = polygon.get_boundary_edges(polygon.edges)
		
		for edge in boundary_edges:
			polygon.vertex_boundary_dic[edge[0]] = True
			polygon.vertex_boundary_dic[edge[1]] = True

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

			dart = polygon.get_dart(boundary_edge[1])
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