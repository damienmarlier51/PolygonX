from operator import itemgetter

class Dart:

	def __init__(self, vertex, edges, polygon, direction=None):
		
		#A dart is defined by a vertex, edges and the network (polygon) it belongs to
		self.vertex = vertex
		self.polygon = polygon

		#Sort edges by angle (in anti-clockwise)
		edges = sorted(edges, key=itemgetter(2))
		self.edges = edges
		self.direction = direction

	def theta_0(self):

		#Go to dart on opposite side of the edge
		next_dart = self.polygon.get_dart(self.direction)
		next_dart.set_direction(self.vertex)
		return next_dart

	def theta_1(self):

		#Go one step counter clock-wise
		idx = [x[0] for x in self.edges].index(self.direction)
		if idx<len(self.edges)-1:
			idx += 1
		else:
			idx = 0
		self.set_direction(self.edges[idx][0])
		return self

	def set_direction(self,next_vertex):
		self.direction = next_vertex