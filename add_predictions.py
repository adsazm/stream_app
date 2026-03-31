# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 09:31:18 2026

@author: lddelnido
"""

import numpy as np
import pandas as pd
import math
import time
import datetime 
from astropy.time import Time
import os
import matplotlib.pyplot as plt
import sqlite3

day = 61129

#Path to app local repository
direc2 = "C:/Users/34626/Downloads/EOP Predictions/Pruebas/stream_app"

################### AUXILIARY  FUNCTIONS ################################
def read_db(num,lista):
    table = ['fcn_cpo']
    conn = sqlite3.connect(f"{direc2}/eop_predictions.db")
    cursor = conn.cursor()
    cursor.execute(f""" {to_str(lista,num)}  """)
    conn.commit()
    conn.close()
    return 0

"""
SI ERROR AL EJECUTAR CON RESTART EL KERNEL SUELE FUNCIONAR
"""

def greg_to_mjd(f):   
    """
    Parameters
    ----------
    f : datetime.datetime
        Gregorian time date

    Returns
    -------
    mjd : int
        f at 00:00h in MJD
    """
    y,m,d=f.timetuple()[:3]
    jd = 367*y-int((7*(y+int((m+9)/12.0)))/4.0)+int((275*m)/9.0)+d+1721013.5-0.5*math.copysign(1,100*y+m-190002.5)+0.5
    mjd = int(jd-2400000.5)
    return mjd

def to_str(lst,num):
    aa = ['fcn_cpo']
    st = f'INSERT INTO {aa[num]} (date, epoch, ac, as, x0, y0, dx, dy) VALUES '
    for x in lst:
        st = st+str(tuple(x))+','
    #print(st[:-1]+';')
    return st[:-1]+';'
            
###################### EOP_OLD & NEW ###########################

d = Time(day,format = 'mjd')
d.format = 'iso'
d = d.value[:-4]


direc = os.getcwd()+'/fcn_cpo/'
dirs1 = [f'{direc}FCN_CPO_IERS_C0420_20260329.txt',
        f'{direc}si_eam/eoppcc_168_{day}.txt']
dirs2 = [f'{direc}no_eam_new/eoppcc_185_{day}.txt',
        f'{direc}si_eam_new/eoppcc_186_{day}.txt']


f= open(dirs1[0],'r')
data = f.readlines()
f.close()

data = list(np.transpose([j.split() for j in data[13063:]]))

data[0] = [int(float(x)) for x in data[0]]
for j in range(1,7):
    data[j] = [float(x) for x in data[j]]
    
rows = []
a= data[0]
mjd = [Time(j,format = 'mjd') for j in a]
date = [j.iso for j in mjd]
rows.append(date)
for j in range(0,7):
    rows.append(data[j])

rows1 = [[fila[i] for fila in rows] for i in range(len(rows[0]))]
 
print(rows1)

df_old= read_db(0,rows1)

"""
for i in range(2):
    f = open(dirs1[i],'r')
    data = f.readlines()
    f.close()
    
    data = list(np.transpose([j.split() for j in data]))
    
    names = ['MJD','ac','as','x0','y0','dx','dy']
    num = [0,1,2,3,7,8]
    
    data[0] = [int(x) for x in data[0]]
    for j in range(1,6):
        data[num[j]] = [float(x) for x in data[num[j]]]
      
    
    rows1 = []
    for j in range(len(names)):
        aux = [d,names[j],i]
        if num[j] == 0:
            aux = aux+data[num[j]]
        else:
            aux = aux+ data[num[j]]
        rows1.append(aux)
     
    df_old= read_db(0,rows1)
    
    

    f = open(dirs2[i],'r')
    data = f.readlines()
    f.close()

    data = list(np.transpose([j.split() for j in data]))

    names = ['epoch','dx','dy']
    num = [0,7,8]

    data[0] = [int(x) for x in data[0]]
    for j in range(1,3):
        data[num[j]] = [float(x) for x in data[num[j]]]
        
    rows2 = []
    for j in range(len(names)):
        aux = [d,names[j],i]
        if num[j] == 0:
            aux = aux+data[num[j]]
        else:
            aux = aux+ data[num[j]]
        rows2.append(aux)
     
    df_new = read_db(1,rows2)
    
"""
