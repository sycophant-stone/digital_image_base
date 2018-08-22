import numpy as np
import math
from convs import *
def pascalSmooth(n): 
    pascalSmooth=np.zeros([1,n],np.float32)
    for i in range(n):
        pascalSmooth[0][i]=math.factorial(n-1)/(math.factorial(i)*math.factorial(n-1-i)) # 利用二项式展开计算系数
    return pascalSmooth

def pascalDiff(n):
    if n<=0:
        print("n should bigger than 0")
        return
    pascalDiff=np.zeros([1,n],np.float32)
    pascal_prev=pascalSmooth(n-1)
    for i in range(n):
        if i==0:
            pascalDiff[0][i]=pascal_prev[0][i]
        elif i==n-1:
            pascalDiff[0][i]=-pascal_prev[0][i-1] # 在n-1基础上左右扩展成0,然后在做差的时候的值是可以定下来的.
        else:
            pascalDiff[0][i]=pascal_prev[0][i]-pascal_prev[0][i-1] # 在n-1的分布上,由后项减前项
    return pascalDiff

#得到一个sobel kerne.实际上在使用sobel时这步是不需要的.因为我们这步可以实现分离的kernel相乘.
def getSobelKernel(n):
    pascalSmoothKernel=pascalSmooth(n)
    pascalDiffKernel=pascalDiff(n)
    print(pascalSmoothKernel)
    print(pascalDiffKernel)
    cx=cy=int(n/2)
    sobelKernel_x=conv2d_same(pascalSmoothKernel.transpose(),pascalDiffKernel,cx,cy,stride=1)
    sobelKernel_y=conv2d_same(pascalSmoothKernel,pascalDiffKernel.transpose(),cx,cy,stride=1)
    return (sobelKernel_x,sobelKernel_y)