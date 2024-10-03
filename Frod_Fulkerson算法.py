#深度优先搜索实现Ford-Fulkerson思想
class Graph:
    def __init__(self,num):
        self.data_li = [['inf' for i in range(num)] for i in range(num)]
        self.val_li = [['inf' for i in range(num)] for i in range(num)]
 
    def add_edge(self,data_r,data_f):  #记录各点到可到达的其余点的路径长度
        for i in data_r:
            self.data_li[i[0]][i[1]] = i[2]
        for i in data_f:
            self.val_li[i[0]][i[1]] = i[2]
 
    def ford_fulkerson(self,start):
        que = []
        ready = []
        que.append((start,start))
        f_node = (start,start)
        while que:
            curnode = que[-1]
            if curnode[1] == 5:
                val_min = min([self.data_li[j[0]][j[1]] - self.val_li[j[0]][j[1]] if self.data_li[j[0]][j[1]] > 0 else self.val_li[j[0]][j[1]] for j in que[1:]])
                for i in que[1:]:
                    if self.data_li[i[0]][i[1]] > 0:
                        self.val_li[i[0]][i[1]] = self.val_li[i[0]][i[1]] + val_min
                        self.val_li[i[1]][i[0]] = self.val_li[i[1]][i[0]] + val_min
                    else:
                        self.val_li[i[0]][i[1]] = self.val_li[i[0]][i[1]] - val_min
                        self.val_li[i[1]][i[0]] = self.val_li[i[1]][i[0]] - val_min
                que = [que[0]]
                ready = []
                continue
            for i in range(len(self.data_li[curnode[1]])):
                if self.data_li[curnode[1]][i] == 'inf':
                    continue
                else:
                    if self.data_li[curnode[1]][i] > 0:
                        if  self.val_li[curnode[1]][i] < self.data_li[curnode[1]][i] and i != f_node[1] and i != curnode[0] and i not in ready:
                            que.append((curnode[1],i))
                            ready.append(i)
                            break
                    else:
                        if self.val_li[curnode[1]][i] <= abs(self.data_li[curnode[1]][i]) and self.val_li[curnode[1]][i] != 0 and i != f_node[1] and i != curnode[0] and i not in ready:
                            que.append((curnode[1],i))
                            ready.append(i)
                            break
            else:
                f_node = que.pop(-1)
        return self.val_li
if __name__ == '__main__':
    data_r = [(0,1,6),(0,2,8),(1,0,-6),(1,3,5),(2,0,-8),(2,3,3),(2,4,3),(3,1,-5),(3,2,-3),(3,4,3),(3,5,10),(4,2,-3),(4,3,-3),(4,5,5),(5,3,-10),(5,4,-5)]
    data_f = [(0,1,5),(0,2,3),(1,0,5),(1,3,5),(2,0,3),(2,3,0),(2,4,3),(3,1,5),(3,2,0),(3,4,0),(3,5,5),(4,2,3),(4,3,0),(4,5,3),(5,3,5),(5,4,3)]
    d = Graph(6)
    d.add_edge(data_r,data_f)
    path = 0
    for i in d.ford_fulkerson(0)[0]:
        if i != 'inf':
            path = path + i
    print(path)