import numpy as np
list=[]
for i in range(5):
    a=np.array([[1,2,3],
                [4,5,6],
                [7,8,9]])
    v=np.diag(np.random.normal(loc=0,scale=a))
    x=np.array(v).reshape(-1,1)
    b=np.array([
        [100],
        [200],
        [200]
    ])
    list.append(b+x)

print(list)