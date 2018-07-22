from operator import itemgetter

class Dart:

	def __init__(self, triangulation, vertex, dart_edges, direction=None):
		
		#A dart is defined by a vertex, edges and the network (polygon) it belongs to
		self.triangulation = triangulation
		self.vertex = vertex

		#Sort edges by angle (in anti-clockwise)
		dart_edges = sorted(dart_edges, key=itemgetter(2))
		self.dart_edges = dart_edges
		self.direction = direction

	def theta_0(self):

		triangulation = self.triangulation
		#Go to dart on opposite side of the edge
		next_dart = triangulation.get_dart(vertex=self.direction,direction=self.vertex)
		return next_dart

	def theta_1(self):

		#Go one step counter clock-wise
		idx = [x[0] for x in self.dart_edges].index(self.direction)
		if idx<len(self.dart_edges)-1:
			idx += 1
		else:
			idx = 0
		self.set_direction(self.dart_edges[idx][0])
		return self

	def set_direction(self,next_vertex):
		self.direction = next_vertex