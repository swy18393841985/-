import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

matplotlib.rcParams['font.family']='simHei'   #中文显示
matplotlib.rcParams['axes.unicode_minus'] = False #解决负号'-'显示为方块的问题 

def fun(x):
    return 10*np.sin(5*x)+7*np.abs(x-5)+10

def sishewuru(x):
    x[x<0.5]=0
    x[x>=0.5]=1
    return x

class Genetic:
    def __init__(self,fun,dimension_num,popsize,p_cross,p_mutation,inter_max):#适应度函数，决策变量维度，种群规模，交叉概率，变异概率，最大迭代次数
        self.fun=fun#适应度函数
        self.dimension_num=dimension_num#决策变量维度
        self.popsize=popsize#种群规模
        self.p_cross=p_cross#交叉概率
        self.p_mutation=p_mutation#变异概率
        self.inter_max=inter_max#最大迭代次数
        self.chromlength=20#初始化二进制编码位数
        self.bestfit=-np.inf;#初始化适应度值为-∞
        self.bestindividual=0;#初始化最优解
        self.result=np.zeros([2,self.inter_max])#对存储每轮迭代最优解的result矩阵预分配内存，提高运行速率
        self.pop=sishewuru(np.random.uniform(0,1,(self.popsize,self.chromlength)))#初始化种群
        self.px=np.size(self.pop,0)
        self.py=np.size(self.pop,1)
    def Decimal_conversion(self,pop):#进制转换
        pop1=np.zeros([len(pop),self.chromlength])
        for j in range(self.py):
            pop1[:,j]=pop[:,j]*2**(self.py-j)#按位权值展开
        temp=np.sum(pop1,1)
        pop2=0+temp*((10-0)/2**self.chromlength)
        return pop2
    def pop_choose(self,fitvalue):#选择操作（轮盘赌法）
        newpop=[]
        p_fitvalue1=fitvalue/np.sum(fitvalue)
        p_fitvalue=np.cumsum(p_fitvalue1)
        p_rand=np.sort(np.random.uniform(0,1,(self.px,1)))#px行，1列个由小到大排序的随机数
        #用p_rand去与做完了累计和的p_fitvalue作比较
        #适应度越高就有越大的几率在p_fitvalue的累计和中占据更大的区间
        #将会有更多的p_rand值落在中间
        #用这种方法保留下了适应度值较大的基因
        i=0#指向随机数的指针
        j=0#指向累计和区间的指针
        while i<self.px:
            if p_rand[i]<p_fitvalue[j]:
                newpop.append(self.pop[j,:])#适应度高的基因以较大概率保留到了新种群中
                i+=1
            else:
                j+=1
        newpop=np.array(newpop)
        return newpop
    def pop_cross(self,newpop):#交叉操作（单点交叉）
        newpop2=np.zeros([self.px,self.py])
        for i in range(0,self.px,2):#让i与i+1进行交叉，所以i遍历染色体中编号为奇数的就可以了
            x=[]
            y=[]    
            if random.random()<self.p_cross:
                point=round(random.random()*(self.py))
                for z in range(point):
                    x.append(newpop[i][z])
                    y.append(newpop[i+1][z])
                for n in range(point,self.py):
                    x.append(newpop[i+1][n])
                    y.append(newpop[i][n])
            else:
                for n in range(self.py):
                    x.append(newpop[i][n])
                    y.append(newpop[i+1][n])
            newpop2[i,:]=x
            newpop2[i+1]=y   
        return newpop2
    def pop_mutation(self,newpop2):
        newpop3=np.zeros([self.px,self.py])
        for i in range(self.px):
            if random.random()<self.p_mutation:
                ex_mutation_point=np.round(random.random()*self.py)#发生变异时的点位
                mutation_point=np.int(ex_mutation_point)
                if mutation_point<0:
                    mutation_point=0
                if mutation_point>19:
                    mutation_point=19
                newpop3[i]=newpop2[i]
                if newpop3[i,mutation_point]==0:
                    newpop3[i,mutation_point]=1
                else:
                    newpop3[i,mutation_point]=0
            else:
                newpop3[i]=newpop2[i]
        #print(newpop3)
        return newpop3
    def main(self):
        x=np.linspace(0,20,1000)
        y=fun(x)
        plt.plot(x,y,'b-',label='函数图像')
        for inter in range(self.inter_max):
            #进制转换
            pop2=self.Decimal_conversion(self.pop)
            #计算目标函数值
            fitvalue=self.fun(pop2)
            #选择操作（轮盘赌法）
            newpop=self.pop_choose(fitvalue)
            #交叉操作（单点交叉）
            newpop2=self.pop_cross(newpop)
            #变异操作
            newpop3=self.pop_mutation(newpop2)
            #更新种群，重新计算种群的适应度，更新Best记录
            self.pop=newpop3
            #进制转换
            pop2=self.Decimal_conversion(self.pop)
            fitvalue=self.fun(pop2)#将pop2矩阵代入目标函数计算适应度
            self.px=np.size(self.pop,0)
            self.py=np.size(self.pop,1)
            for i in range(self.px):
                if self.bestfit<fitvalue[i]:
                    self.bestfit=fitvalue[i]#找到本轮迭代的最优f(x)
                    self.bestindividual=pop2[i]
            self.result[0,inter]=self.bestindividual#矩阵其一行存储每轮迭代的最优x
            self.result[1,inter]=self.bestfit#矩阵第2行存储每轮迭代的最优f(x)            
            plt.plot(self.result[0,inter],self.result[1,inter],'b*')
            plt.title('当前迭代次数：%d'%(inter+1))
            plt.pause(0.03)
        plt.show()
        a=np.array([i for i in range(1,self.inter_max+1)])
        plt.plot(a,self.result[1],'r-',label='最优适应度值')
        plt.title('最优适应度值随迭代代数发生变化曲线')
        plt.legend(loc=3)
        plt.show()
        print('The best x is --> %f'%self.bestindividual)
        print('The fitness value is -->%f'%self.bestfit)
GA=Genetic(fun,1,20,0.7,0.1,200)
GA.main()