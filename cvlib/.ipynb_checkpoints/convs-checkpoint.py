import numpy as np
# full类型卷积操作.
#
# ax,ay: anchor's location

def conv2d_same(src,kernel,ax,ay,stride):
    kw,kh=kernel.shape
    iwo,iho=src.shape
    if kw!=kh or iwo!=iho:
        print("kernel and image should be square")
        return 
    r=int(kw/2)
    dst=src.copy()
    dst_full=np.pad(dst,((r,r),(r,r)),constant_values=(0,0),mode='constant') # 扩充2r个0
    dst_full=dst_full.astype(np.float32)
    #dest = dst_full.copy()
    dest=np.zeros(dst_full.shape,np.float32)
    i=j=r
    iw,ih=dest.shape
    #print("r:%d,iw:%d,ih:%d,pad_iw:%d,pad_ih:%d" %(r,iwo,iho,iw,ih))
    
    # DEBUG: 
    #       True)  打开
    #       Flase) 
    
    DEBUG_EN=False#True
    if DEBUG_EN==True:
        debug_cnt=0
    else:
        debug_cnt=10
    
    if kw%2==1:
        odds=1
    else:
        odds=0
    #print("i:%d,iw:%d,ih:%d,r:%d,odds:%d" %(i,iw,ih,r,odds))
    sax=ax
    say=ay
    while i< (iw-2*r):#(iw+2*r-r-odds-1):
        while j<(ih-2*r):#(ih+2*r-r-odds-1):
            temp=kernel*dst_full[(i-r):(i+r+odds),(j-r):(j+r+odds)]
            
            if debug_cnt<10:
                print("[i:%d,j:%d]origin dest[%d,%d]:%d" %(i,j,ax,ay,dest[ax,ay]))
                print("kernel:",kernel)
                print("dst_full[%d:%d,%d:%d]:%s" %((i-r),(i+r+odds),(j-r),(j+r+odds),dst_full[(i-r):(i+r+odds),(j-r):(j+r+odds)]))
            
            dest[ax,ay]=np.sum(temp)
            
            if debug_cnt<10:
                debug_cnt+=1
                print("[i:%d,j:%d]after dest[%d,%d]:%d" %(i,j,ax,ay,dest[ax,ay]))
            
            j+=stride
            ay+=stride
        i+=stride
        ax+=stride
        j=r
        ay=say # 易忘记,参数的回归,迭代,更新.

    return dest

def conv1d_same(src,kernel,ax,ay,stride):
    kw,kh=kernel.shape
    if kw<=1 and kh <=1:
        print("wrong kernel size")
        return 
    if kh==1: # n行1列的kernel,在列上按行卷积
        r=int(kw/2)
        dst=src.copy()
        dst_full=np.pad(dst,((r,r),(0,0)),constant_values=(0,0),mode='constant') # 扩充2r个0
        dst_full=dst_full.astype(np.float32)
        #dest = dst_full.copy()
        dest=np.zeros(dst_full.shape,np.float32)
        iw,ih=dest.shape
        #odds=(kw%2==1)?1:0
        if kw%2==1:
            odds=1
        else:
            odds=0
        i=j=r
        sax=ax
        say=ay
        debug_cnt=0
        while i<iw-2*r-odds:#iw+2*r-r-odds-1:
            j=r # 注意iterator的更新
            while j<ih-2*r:#ih-r-1:
                #if debug_cnt<10:
                #    print("[i:%d,j:%d]origin dest[%d,%d]:%d" %(i,j,ax,ay,dest[ax,ay]))
                #    print("kernel:",kernel)
                #    print("dst_full[%d:%d,%d:%d]:%s" %((i-r),(i+r+odds),(j-r),(j+r+odds),dst_full[(i-r):(i+r+odds),(j-r):(j+r+odds)]))
                #temp=kernel*dst_full[(i-r):(i+r+odds),j]
                #dest[ax,ay]=np.sum(temp)                
                temp=0
                for ki in range(2*r+odds):
                    temp+=kernel[ki]*dst_full[i][j+ki]
                    #if debug_cnt<10:
                    #    print("kernel[%d]:%s, dst_full[%d]:%s"%(ki,kernel[ki],(j+ki),dst_full[i][j+ki]))
                #print("ax:%d,ay:%d,temp:%d"%(ax,ay,temp))
                dest[ax,ay]=temp
                #if debug_cnt<10:
                #    debug_cnt+=1
                #    print("[i:%d,j:%d]after dest[%d,%d]:%d" %(i,j,ax,ay,dest[ax,ay]))

                ay+=stride
                j+=stride
            i+=stride
            ay=say # 很容易就忘记了迭代
            ax+=stride
    elif kw==1:# n行一列
        debug_cnt=0
        r=int(kh/2)
        dst=src.copy()
        dst_full=np.pad(dst,((0,0),(r,r)),constant_values=(0,0),mode='constant') # 扩充2r个0
        dst_full=dst_full.astype(np.float32)
        #dest = dst_full.copy()
        dest=np.zeros(dst_full.shape,np.float32)
        iw,ih=dest.shape
        #odds=(kh%2==1)?1:0
        if kh%2==1:
            odds=1
        else:
            odds=0
        i=j=r
        sax=ax
        say=ay
        while j<ih-2*r-odds:#ih+2*r-r-odds-1:
            #print("j:%d,ax:%d,ay:%d" %(j,ax,ay))
            i=r #注意iterator的更新
            while i<iw-2*r:#iw-r-1:
                #temp=kernel*dst_full[i,(j-r):(j+r+odds)]
                temp=0
                for ki in range(2*r+odds):
                    #if debug_cnt<10:
                    #    print("kernel[0][%d]:%s, dst_full[%d][%d]:%s"%(ki,kernel[0][ki],(i+ki),j,dst_full[i+ki][j]))
                    temp+=kernel[0][ki]*dst_full[i+ki][j]
                #if debug_cnt<10:
                #    print("temp:%s"%(temp))
                #print("ax:%d,ay:%d,temp:%d"%(ax,ay,temp))
                dest[ax,ay]=temp
                #if debug_cnt<10:
                #    debug_cnt+=1
                #    print("[i:%d,j:%d]after dest[%d,%d]:%d" %(i,j,ax,ay,dest[ax,ay]))
                ax+=stride
                i+=stride
            ax=sax
            ay+=stride
            j+=stride

    
    return dest

def Gaussian_filter(src, sigma=1.0, k_w = 3, k_h = 3):
    #产生高斯核
    h = src.shape[0]
    w = src.shape[1]
    dest = np.zeros((h,w), np.uint8)
    kernel = np.zeros((k_h,k_w), np.float)
    dest = src.copy()
    
    for i in range(k_h):
        for j in range(k_w):
            n = -(np.power(i,2)+np.power(j,2))/(2*np.power(sigma,2))
            #np.exp(n) n意味着e的n次方
            #print("n:", n)
            #print("(%d, %d) np.exp(%d):", i, j, n, np.exp(n))
            kernel[i,j] = np.exp(n)/(2*3.14*np.power(sigma,2))
    #归一化操作
    kernel=kernel/np.sum(kernel)
    #print("kernel,sum", kernel,np.sum(kernel))
    r=int(k_w/2)
    dest=conv2d_same(src,kernel,r,r,stride=1)
    return dest