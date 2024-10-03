from queue import Queue
#通过path找到最短路径
def shortest_path(path):
    shortestpath = []
    curNode = path[-1]
    while curNode != path[0]:
        shortestpath.append(curNode)
        curNode = path[curNode[2]]   # 找到前一个位置
    shortestpath.append(path[0])
    shortestpath.reverse()
    return shortestpath
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,0,0,1,0,1],
    [1,0,0,1,0,0,0,1,0,1],
    [1,0,0,0,0,1,1,0,0,1],
    [1,0,1,1,1,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,0,1],
    [1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]
dirs = [
    lambda x,y:(x+1,y),
    lambda x,y:(x,y+1),
    lambda x,y:(x-1,y),
    lambda x,y:(x,y-1),]

def go_maze(x1,y1,x2,y2):
    queue = Queue()
    path = []
    queue.put((x1,y1,-1))# 起点
    maze[y1][x1] = -1   # 标记起点已经走过
    while queue.qsize()>0:
        curNode = queue.get()
        path.append(curNode)
        if curNode[0] == x2 and curNode[1] == y2:
            for x,y,_ in shortest_path(path):print('%d %d' % (x,y))
            return True
        for dir in dirs:  # 找四个方向
            nextNode = dir(curNode[0],curNode[1])
            if maze[nextNode[1]][nextNode[0]] == 0 :
                queue.put((nextNode[0],nextNode[1],len(path)-1))#找到下一格路
                maze[nextNode[1]][nextNode[0]] = -1  # 标记这格走过，防止死循环
    print(-1)
    return False
go_maze(1,1,8,8)
