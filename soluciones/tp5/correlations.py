#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import numpy as np
import networkx as nx

from tqdm import tqdm
from loky import ProcessPoolExecutor


# In[ ]:


def C_experiment(g,s):
    C = {}
    MAX_VALUE = 50 # Máxima distancia a la que vamos a calcular la función de correlación
    for r in range(MAX_VALUE):
            C[r] = []
    g_nx = nx.Graph(incoming_graph_data=g)
    spl = nx.shortest_path_length(g_nx)
     # Vamos a samplear hasta esta distancia entre pares 
    for x in spl:    
        i,l = x
        NL_i = []
        for r in range(MAX_VALUE):
            n_ir = []
            for key,value in l.items():
                if value==r:
                    n_ir.append(key)
            NL_i.append((r,n_ir))
        NL_i = dict(NL_i)
        for r in range(MAX_VALUE):
            n_ir = NL_i[r]
            for n in n_ir:
                C[r].append(s[i] * s[n])
    return C


# In[ ]:


with open('ising_p001_16runs','rb') as f:
    p001 = pickle.load(f)

graphs = [experiment[0] for experiment in p001]
spins = [experiment[1] for experiment in p001]

with ProcessPoolExecutor() as e:
    C_p001 = list(tqdm(e.map(C_experiment,graphs,spins),total=len(p001)))

with open('ising_p002_16runs','rb') as f:
    p002 = pickle.load(f)
    
graphs = [experiment[0] for experiment in p002]
spins = [experiment[1] for experiment in p002]

with ProcessPoolExecutor() as e:
    C_p002 = list(tqdm(e.map(C_experiment,graphs,spins),total=len(p002)))

with open('ising_p004_16runs','rb') as f:
    p004 = pickle.load(f)
    
graphs = [experiment[0] for experiment in p004]
spins = [experiment[1] for experiment in p004]

with ProcessPoolExecutor() as e:
    C_p004 = list(tqdm(e.map(C_experiment,graphs,spins),total=len(p004)))

with open('ising_p006_16runs','rb') as f:
    p06 = pickle.load(f)
    
graphs = [experiment[0] for experiment in p06]
spins = [experiment[1] for experiment in p06]

with ProcessPoolExecutor() as e:
    C_p006 = list(tqdm(e.map(C_experiment,graphs,spins),total=len(p006)))

with open('ising_p010_16runs','rb') as f:
    p010 = pickle.load(f)
    
graphs = [experiment[0] for experiment in p010]
spins = [experiment[1] for experiment in p010]

with ProcessPoolExecutor() as e:
    C_p010 = list(tqdm(e.map(C_experiment,graphs,spins),total=len(p010)))

def concat_dicts(list_of_dicts):
    C = list_of_dicts[0].copy()
    for dicts in list_of_dicts[1:]:
        for key in C.keys():
            # Esto es porque sabemos que el value de los diccionarios es una lista
            C[key].extend(dicts[key])
    return C


# In[ ]:


C_p001 = concat_dicts(C_p001)
C_p002 = concat_dicts(C_p002)
C_p004 = concat_dicts(C_p004)
C_p006 = concat_dicts(C_p006)
C_p010 = concat_dicts(C_p010)


# In[ ]:


with open('C_p001','wb') as f_001:
    pickle.dump(C_p001,f_001)
with open('C_p002','wb') as f_002:
    pickle.dump(C_p002,f_002)
with open('C_p004','wb') as f_004:
    pickle.dump(C_p004,f_004)
with open('C_p006','wb') as f_006:
    pickle.dump(C_p006,f_006)
with open('C_p010','wb') as f_010:
    pickle.dump(C_p010,f_010)

