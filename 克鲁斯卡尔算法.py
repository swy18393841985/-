import numpy as np
def kuskal(A,vexset,alpha):   
    kuskal={}
    list=[]
    for i in range(0,len(alpha)):
        for k in range(i+1,len(alpha)):
            if A[i,k]<inf:
                kuskal['{}<-->{}'.format(alpha[i],alpha[k])]=A[i,k]
    kuskal=sorted(kuskal.items(),key=lambda x:x[1])
    for k in kuskal:
        if vexset[k[0][0]]!=vexset[k[0][-1]]:
            if vexset[k[0][0]]<vexset[k[0][-1]]:
                x=vexset[k[0][0]]
                for key in vexset.keys():
                    if vexset[key]==x:
                        vexset[key]=vexset[k[0][-1]]
            else:
                vexset[k[0][-1]]=vexset[k[0][0]]
            list.append(k)
        last_value=vexset[alpha[0]]
        flag=0
        for value in vexset.values():
            if last_value!=value:
                flag=1
                break            
            else:
                last_value=value
        if flag==0:
            break
    return list
inf=300000
vexset={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5}
alpha=['A','B','C','D','E','F']
A=np.array([0,6,1,5,inf,inf,6,0,5,inf,3,inf,1,5,0,5,6,4,5,inf,5,0,inf,2,inf,3,6,inf,0,6,inf,inf,4,2,6,0]).reshape(6,6)
print(kuskal(A,vexset,alpha))