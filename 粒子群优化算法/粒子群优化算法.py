import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random

matplotlib.rcParams['font.family']='simHei'   #中文显示
matplotlib.rcParams['axes.unicode_minus'] = False #解决负号'-'显示为方块的问题 

def fun(x):
    g,b,h=x[0],x[1],x[2]
    x_value=(3*np.cos(g))/10 + (6*np.cos(b)*np.cos(g))/5 + (3*np.cos(b)*np.cos(g)*np.cos(h))/10 - (6*np.cos(b)*np.cos(g)*np.sin(h))/5 - (6*np.cos(g)*np.cos(h)*np.sin(b))/5 - (3*np.cos(g)*np.sin(b)*np.sin(h))/10
    y_value= (3*np.sin(g))/10 + (6*np.cos(b)*np.sin(g))/5 + (3*np.cos(b)*np.cos(h)*np.sin(g))/10 - (6*np.cos(b)*np.sin(g)*np.sin(h))/5 - (6*np.cos(h)*np.sin(b)*np.sin(g))/5 - (3*np.sin(b)*np.sin(g)*np.sin(h))/10    
    z_value=(6*np.sin(b)*np.sin(h))/5 - (3*np.cos(b)*np.sin(h))/10 - (3*np.cos(h)*np.sin(b))/10 - (6*np.sin(b))/5 - (6*np.cos(b)*np.cos(h))/5 + 3/5    
    return np.sqrt((x_value-1.5)**2+(y_value-1.2)**2+(z_value-0.2)**2)


class Pso:
    def __init__(self,fun,dimension_num,maxgen,sizepop,popmin,popmax):#目标函数，迭代次数，种群大小，个体边界
        #传入函数
        self.fun=fun
        self.dimension_num=dimension_num
        #参数初始化
        self.c1=1.49445
        self.c2=1.49445       
        self.maxgen=maxgen#进化次数
        self.sizepop=sizepop#种群规模
        self.Vmax=0.3
        self.Vmin=-0.3
        self.popmax=popmax#自变量的范围
        self.popmin=popmin
        self.pop=[]#种群
        self.v=[]#粒子的速度
        self.fitness=[]#用于存储适应度值
        self.fitness_zbest_change=[]#用于存储每一步中变化的适应度值
        self.generation=[i for i in range(1,self.maxgen+1)]#存储迭代次数，方便后续画图
    def Omega(self,x):
        omega_start=0.9
        omega_end=0.4
        omega_x=omega_start-(omega_start-omega_end)*(self.maxgen-x)/self.maxgen
        return omega_x
    def PSO(self):
        def drawing_2D(generation,fitness_zbest_change):
            plt.plot(generation,fitness_zbest_change,'b-',label='适应度函数变化趋势')
            plt.xlabel('进化代数')
            plt.ylabel('适应度函数值')
            plt.title('基于粒子群优化算法的适应度函数变化趋势')
            plt.show()
        for i in range(self.sizepop):
            #随机产生一个种群
            x_pop=[]
            for j in range(self.dimension_num):
                x_pop.append(random.uniform(self.popmin[j],self.popmax[j]))
            self.pop.append(x_pop)#初始化种群
            v_pop=[]
            for j in range(self.dimension_num):
                v_pop.append(random.uniform(self.Vmin,self.Vmax))
            self.v.append(v_pop)#初始化速度
            self.fitness.append(self.fun(self.pop[i]))#计算适应度
        self.pop=np.array(self.pop)
        self.v=np.array(self.v)
        self.fitness=np.array(self.fitness)
        #个体极值和群体极值
        best_fitness=np.min(self.fitness)
        best_index=np.argmin(self.fitness)
        gbest=self.pop#个体最佳适应度值
        zbest=self.pop[best_index]#全局最优值
        fitness_gbest=self.fitness#个体最优适应度值
        fitness_zbest=best_fitness
        #迭代寻优
        for i in range(self.maxgen):
            for j in range(self.sizepop):
                #速度更新
                self.v[j]=self.Omega(i)*self.v[j]+self.c1*random.random()*(gbest[j]-self.pop[j])+self.c2*random.random()*(zbest-self.pop[j])
                self.v[j][self.v[j]>self.Vmax]=self.Vmax
                self.v[j][self.v[j]<self.Vmin]=self.Vmin
                #种群更新
                self.pop[j]=self.pop[j]+self.v[j]
                for z in range(self.dimension_num):
                    if self.pop[j][z]>self.popmax[z]:
                        self.pop[j][z]=self.popmax[z]
                    if self.pop[j][z]<self.popmin[z]:
                        self.pop[j][z]=self.popmin[z]
                #适应度值更新
                self.fitness[j]=self.fun(self.pop[j])
            for n in range(self.sizepop):
                #个体最优值更新
                if self.fitness[n]<fitness_gbest[n]:
                    fitness_gbest[n]=self.fitness[n]
                    gbest[n]=self.pop[n]
                #群体最优值更新
                if self.fitness[n]<fitness_zbest:
                    fitness_zbest=self.fitness[n]
                    zbest=self.pop[n]
            self.fitness_zbest_change.append(fitness_zbest)
        print("全局最优适应度值为{:.4f},全局最优解为：".format(fitness_zbest))
        for i in range(len(zbest)):
            print("x[%d]=%f"%(i+1,zbest[i]),end=' ')
        drawing_2D(self.generation,self.fitness_zbest_change)
popmin=np.array([(-160/180)*np.pi,(-150/180)*np.pi,(-200/180)*np.pi,(-180/180)*np.pi,(-120/180)*np.pi,(-180/180)*np.pi])
popmax=np.array([(160/180)*np.pi,(150/180)*np.pi,(80/180)*np.pi,(180/180)*np.pi,(120/180)*np.pi,(180/180)*np.pi])
solving_problem=Pso(fun,6,100,100,popmin,popmax)
solving_problem.PSO()