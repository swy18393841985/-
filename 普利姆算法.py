import heapq#堆
 
class Prim:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adjacency_list = {vertex: [] for vertex in vertices}
        self.minimum_spanning_tree = []
 
    def add_edge(self, u, v, weight):
        """添加边到邻接列表"""
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))
 
    def prim(self, start):
        """Prim算法实现"""
        visited = set()
        min_heap = [(0, start)]  # 使用堆存储候选边 (weight, vertex)
        while min_heap:
            weight, current_vertex = heapq.heappop(min_heap)
            if current_vertex not in visited:
                visited.add(current_vertex)
                for neighbor, edge_weight in self.adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        heapq.heappush(min_heap, (edge_weight, neighbor))
                if len(self.minimum_spanning_tree) < len(self.vertices) - 1:
                    # 添加到最小生成树
                    self.minimum_spanning_tree.append((current_vertex, neighbor, weight))
        return self.minimum_spanning_tree
 
# 示例用法:
vertices = ['A', 'B', 'C', 'D', 'E']
prim = Prim(vertices)
prim.add_edge('A', 'B', 4)
prim.add_edge('A', 'C', 6)
prim.add_edge('B', 'C', 2)
prim.add_edge('B', 'D', 9)
prim.add_edge('C', 'D', 7)
prim.add_edge('C', 'E', 8)
prim.add_edge('D', 'E', 3)
 
minimum_spanning_tree = prim.prim('A')
print(minimum_spanning_tree)