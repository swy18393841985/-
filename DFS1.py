def dfs(x, y):
    global num
    for i in range(0, 4):    # 每次搜索有四个方向可以选择
        dir = [(-1, 0), (0, -1), (1, 0), (0, 1)]             # 四个方向左、上、右、下
        nx, ny = x + dir[i][0], y + dir[i][1]   # 新坐标
        print(i)
        if mp[nx][ny]=='#':
            print('!1',end=' ')
            print(x, y, i, nx, ny);
        if nx < 0 or nx >= hx or ny < 0 or ny > wy:          # 判断出局：不在地图内
            print('!2',end=' ')
            print(x, y, i, nx, ny);
            continue                                         # 换个方向，继续找下一个路径
        if mp[nx][ny]== '*':                                 # 到达终点一次
            num += 1
            print('!3',end=' ')
            print(x, y, i, nx, ny);
            print("%d:%s->%d%d" % (num, p[x][y], nx, ny))    # 打印路径:起点到上一个点的路径->终点
            continue                                         # 换个方向，继续找下一个路径
        if mp[nx][ny]== ".":                                 # 可以走的路
            mp[nx][ny]="#"     # 保存现场(用#表示)。这个点在这次更深的dfs中不能再用
            p[nx][ny] = p[x][y] + '->' + str(nx) + str(ny)# 记录路径：起点到上一个点的路径——>下一个点
            print('!4',end=' ')
            print(x, y, i, nx, ny);
            print(mp)
            print(p)
            dfs(nx, ny)
            mp[nx][ny] = '.'     # 恢复现场。回溯之后，这个点可以再次用
            print("改变后，mp为:",mp,nx,ny)
num = 0                     # 统计路径个数
#wy, hx = map(int, input().split())  #Wy行，Hx列。
wy=5
hx=3
#a = [""] * 10                       # 用来保存迷宫
#for i in range(wy):                 #  读迷宫,每次读一行
#    a[i] = list(input())
a=[['.','#','.'],['#', '@', '.'],['*', '.', '.'],['.', '.', '.'],['#', '.', '#']]
#print(a)
mp = [[' '] * 10 for i in range(10)]  #二维矩阵mp[][]表示迷宫
 
# 把a存到mp中（x,y颠倒，因为第一维坐标是y，第二维坐标是x）；找到起点和终点
for x in range(hx):
    for y in range(wy):
        mp[x][y] = a[y][x]
        if mp[x][y] == '@': sx = x; sy = y  #  起点
        if mp[x][y] == "*": tx = x; ty = y  #  终点
print("from %d%d to %d%d" % (sx, sy, tx, ty))
p = [[''] * 10 for i in range(10)]          # 记录从起点到点path[i][i]的路径
p[sx][sy] = str(sx) + str(sy)               # 把起点存进路劲
dfs(sx, sy)                                 # 从起点开始搜索并输出所有的路径