import re
import math
from mpl_toolkits.basemap import Basemap
import itertools
import io

def grid(f,trip_path,bm):    
    for line in iter(f.readline,''):
        l=[]
        coord=line.split(",",8)[8]        
        for c in re.finditer("(-?\d+.\d+),(-?\d+.\d+)",coord):
            c_m=bm(float(c.group(1)),float(c.group(2)))
            square_ind=(math.ceil(c_m[0]/100),math.ceil(c_m[1]/100))
            if (square_ind[0]*square_ind[1])<0:
                continue
            if (l):
                if (square_ind!=l[-1]):
                    l.append(square_ind)
            else:
                l.append(square_ind)    
        trip_path[line.split(",",8)[0].strip('"')]=l
    f.close()

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def find_id(id,bm):
    with open("train.csv","r") as f:
        for line in iter(f.readline,''):
           #print(line.split(",",8)[0])
            if (line.split(",",8)[0].strip('"')==id):
                find={}
                grid(io.StringIO(line),find,bm)
                print(list(find.values())[0])
    
