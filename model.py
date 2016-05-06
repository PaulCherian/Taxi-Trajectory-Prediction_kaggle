import pandas as pd
from mpl_toolkits.basemap import Basemap
import re
import math
import datetime
import importlib
import functions as fn
import numpy as np
import io
import multiprocessing as mp
from functools import partial
import itertools
from scipy import ndimage

def datetime_parser(dt):
    return datetime.date.fromtimestamp(float(dt))

#reading train csv files
data=pd.read_csv('train.csv',parse_dates=[5],date_parser=datetime_parser,usecols=[0,1,2,3,4,5,6,7])
data.set_index(['TRIP_ID'],inplace=True)

#setting basemap coordinate 
bm=Basemap(llcrnrlat=37,llcrnrlon=-9.5,urcrnrlat=41.5 ,urcrnrlon=-6.5,epsg=3763)
x=math.ceil(bm.xmax/100)
y=math.ceil(bm.ymax/100)

train_path={}

#dividing into grids
#grid("train.csv",train_path,bm)

#binning test paths into grids
test_path={}
fn.grid(open("test.csv",'r'),test_path,bm)

test_match=[]
for i in test_path:
    nearest_n={}  
    file=open("train.csv","r")
    file.readline();
    for j in iter(file.readline,''):   
        train={}
        dist=[]
        fn.grid(io.StringIO(j),train,bm)
        n=min(len(list(train.values())[0]),len(test_path[i]),6)
        if (n<3):
            continue
        b=np.array(test_path[i][:n])
        for k in range(0,len(list(train.values())[0])-n+1):
            a=np.array(list(train.values())[0][k:n+k])
            dist.append(np.sum(np.sqrt(np.diagonal(np.dot(a-b,np.transpose(a-b))))))
        nearest_n[j.split(",",8)[0]]=min(dist)
    nearest_n=sorted(nearest_n,key=nearest_n.get)[:10]
    test_match.append(nearest_n)
    print(i)
    file.close()


def mp_fn(j,nearest_n,bm,test):     
    train={}
    dist=[]    
    fn.grid(io.StringIO(j),train,bm)
    n=min(len(list(train.values())[0]),len(test),6)
    if (n<3):
        return(False)
    b=np.array(test[len(test)-n:])
    for k in range(0,len(list(train.values())[0])-n+1):
        a=np.array(list(train.values())[0][k:n+k])
        dist.append(np.sum(np.sqrt(np.diagonal(np.dot(a-b,np.transpose(a-b))))))
    nearest_n[j.split(",",8)[0].strip('"')]=min(dist)
    return(True)

'''
working on this part- vectorization 
def filter(train,test):
    return(np.sum(np.sqrt(np.diagonal(np.dot(train-test,np.transpose(train-test))))))

def mp_fn(j,nearest_n,bm,test):     
    train={}
    dist=[]    
    fn.grid(io.StringIO(j),train,bm)
    n=min(len(list(train.values())[0]),len(test),6)
    if (n<3):
        return(False)    
    b=np.array(test[len(test)-n:])
    filter_p=partial(filter,test=b)
    dist=scipy.ndimage.generic_filter(np.array(list(train.values())[0]),filter_p,size=(n,2))
    nearest_n[j.split(",",8)[0].strip('"')]=min(dist)
    return(True)

test_match=[]
manager=mp.Manager()
for i in test_path:
    nearest_n={}  
    file=open("train.csv","r")
    file.readline();
    dist=[]
    nearest_n=manager.dict({})
    p=partial(mp_fn,nearest_n=nearest_n,bm=bm,test=test_path[i])
    count=1
    for chunk in fn.grouper(iter(file.readline,''),50000):
        pool=mp.Pool(5)
        cond=pool.map(p,chunk)
        pool.close()
        pool.join()
        count=count+1
        print(len(nearest_n.keys()))
    nearest_n=sorted(nearest_n.items(),key=lambda x:x[1])[:10]
    test_match.append(nearest_n)
    print(i)
    file.close()

fn.find_id("1372636858620000589",bm)
fn.find_id('1400289863620000518',bm)


def filter_p(x):
    print(x.reshape(-1,2))
    return(1)
a=np.array([(1,2),(2,3),(3,4),(2,3),(4,5)])    
c=ndimage.generic_filter(a,filter_p,size=(2,2),mode='constant')
'''
    
            
        
    
        
    

