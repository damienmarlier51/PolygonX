import math
from .dart import Dart

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

class Triangulation:

	def __init__(self,edges=[],darts={},points=[],vertex_boundary_dic={}):
		self.edges = edges
		self.points = points
		self.darts = darts
		self.vertex_boundary_dic = vertex_boundary_dic

	def create_dart(self,vertex,direction):

		#get dart edges (list of points opposite to the vertex)
		point_edges = [x for x in self.edges if x[0]==vertex or x[1]==vertex]
		
		#Get the vertices from these edges
		point_opposites = [[y for k,y in enumerate(x) if y!=vertex or (k!=0 and k!=1)] for x in point_edges]

		#Add angle
		for j,point_opposite in enumerate(point_opposites):
			point_opposites[j].append(compute_edge_angle(self.points[vertex],self.points[point_opposite[0]]))
		
		#Create the dart
		dart = Dart(triangulation=self, vertex=vertex, dart_edges=point_opposites, direction=direction)

		#Add to cache dictionnary not to recreate it again
		self.darts[vertex] = dart

		return dart

	def get_dart(self,vertex,direction=None):
		#Get existing dart or create its instance
		if vertex in self.darts:
			dart = self.darts[vertex]
			dart.direction = direction
		else:
			dart = self.create_dart(vertex=vertex,direction=direction)
		return dart


	#Find polygon boundary edges
	def get_boundary_edges(self):

		boundary_edges = []

		for edge in self.edges:
			boundary = self.is_edge_boundary(edge)
			if boundary:
				boundary_edges.append(edge)

		return boundary_edges

	#Check if an edge is on the boundary
	def is_edge_boundary(self,edge):

		# Run through the combinatorial map for three cycles
		dart = self.get_dart(vertex=edge[0],direction=edge[1])
		new_dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [new_dart.vertex,new_dart.direction] != [edge[0],edge[1]]:
			return True

		#Try reverse cycle order
		dart = self.get_dart(vertex=edge[1],direction=edge[0])
		new_dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [new_dart.vertex,new_dart.direction] != [edge[1],edge[0]]:
			return True

		return False

	#Reveal
	def reveal(self,dart):

		#Make a copy for later reuse
		init_dart = Dart(triangulation=self,vertex=dart.vertex,dart_edges=dart.dart_edges,direction=dart.direction)

		init_vertex = dart.vertex
		init_direction = dart.direction

		dart = dart.theta_1().theta_0().theta_1().theta_0().theta_1().theta_0()

		if [init_vertex,init_direction] != [dart.vertex,dart.direction]:
			dart = init_dart.theta_0().theta_1().theta_0().theta_1().theta_0()
		else:
			dart = dart.theta_1()

		return dart

	#Check regularity
	def is_regular(self,edge):

		if self.is_edge_boundary(edge):

			dart = self.get_dart(vertex=edge[0],direction=edge[1])
			vertex = self.reveal(dart).theta_0().vertex
			if self.vertex_boundary_dic[vertex] == False:
				return True

		return False




