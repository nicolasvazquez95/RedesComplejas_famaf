#!/usr/bin/env python
# coding: utf-8

# # Problema 2 - Guía 5

# In[5]:


import numpy as np
from tqdm import tqdm
from loky import ProcessPoolExecutor
from itertools import repeat
import pickle


# In[13]:


# Algoritmo para implementar la red
class WS_1D(object):
    """
    Implementa una red Watts-Strogatz sobre un anillo, añadiendo conexiones al azar con probabilidad p.
    La red se implementa como un diccionario que representa la lista de vecinos del grafo.
    Además se retorna un array de spines inicializados aleatoriamente de acuerdo a la semilla.
    """
    # Implementamos los nodos
    def __init__(self,p,seed,N=10**5):
        nodes = [i for i in range(N)]

        neighbors_list = {}

        # Vecinos para todos los nodos excepto el primero y el último
        for node in nodes[1:-1]:
            neighbors_list[node] = [node-1,node+1]
        # Fijamos condiciones periódicas
        neighbors_list[0] = [1,N-1]
        neighbors_list[N-1] = [N-2,0]
    
        # Ahora agregamos conexiones aleatorias con probabilidad p
        ## Inicializamos generador de números aleatorios
        random_state = np.random.RandomState(seed)
        for i in range(N):
            j = i
            while i == j: # Esto es para que no haya auto enlaces en la red
                j = random_state.randint(0,N)
            ### Agregamos j a la lista de vecinos de i y viceversa
            if random_state.random() < p:
                neighbors_list[i].append(j)
                neighbors_list[j].append(i)
        self.neighbors_list = neighbors_list
        # Inicializamos array de spines
        self.spins = random_state.choice(a=[1,-1],size=N)

# Ahora implementamos la dinámica de Ising en otra clase
class IsingExp(object):
    """
    Clase para realizar simulación Montecarlo del Modelo de Ising
    """
    def __init__(self,p,seed,N=10**5,T=10**6):
        self.p = p
        self.seed = seed
        self.N = N
        self.T = T
        self.network = WS_1D(p,seed)
        self.random_state = np.random.RandomState(self.seed)
        self.flips = 0 # Esto es sólo para debug, lleva registro de los flips aceptados
    # Funciones para la simulación
    def __deltaE(self,i):
        """
        Calcula el cambio de energía al flipear el spin del sitio i
        """
        spin_i = self.network.spins[i]
        neighbors_i = self.network.neighbors_list[i]
        ## Energía inicial
        E0 = - sum(spin_i * self.network.spins[j] for j in neighbors_i)
        ## Energía haciendo flip de spin_i
        E = - sum( (-spin_i) * self.network.spins[j] for j in neighbors_i)
        return E-E0
    def __MCstep(self):
        i = self.random_state.randint(0,self.N)
        deltaE = self.__deltaE(i)
        # ΔE <0 -> Aceptamos flip
        if deltaE < 0:
            self.network.spins[i] = - self.network.spins[i]
            self.flips += 1
        # ΔE = 0 se sortea
        elif deltaE == 0:
            if self.random_state.random() < 0.5:
                self.network.spins[i] = - self.network.spins[i]
                self.flips += 1
    def run(self):
        for t in range(self.T):
            self.__MCstep()
        return self.network.neighbors_list,self.network.spins


# In[14]:


## Función main paralelizable
def main(p,seed):
    experiment = IsingExp(p,seed)
    return experiment.run()


# In[15]:


# Vamos a hacer el experimento unas 256 veces
runs = 16
p = 0.01
with ProcessPoolExecutor() as ppe:
    results = list(tqdm(ppe.map(main,repeat(p,runs),range(runs)),total=runs))

with open('ising_p001_16runs','wb') as f:
    pickle.dump(results,f)
del(results) # Hay que hacer lugar en memoria para la siguiente simulación


# In[16]:


runs = 16
p = 0.02
with ProcessPoolExecutor() as ppe:
    results = list(tqdm(ppe.map(main,repeat(p,runs),range(runs)),total=runs))
with open('ising_p002_16runs','wb') as f:
    pickle.dump(results,f)
del(results)


# In[17]:


runs = 16
p = 0.04
with ProcessPoolExecutor() as ppe:
    results = list(tqdm(ppe.map(main,repeat(p,runs),range(runs)),total=runs))
with open('ising_p004_16runs','wb') as f:
    pickle.dump(results,f)
del(results)    


# In[18]:


runs = 16
p = 0.06
with ProcessPoolExecutor() as ppe:
    results = list(tqdm(ppe.map(main,repeat(p,runs),range(runs)),total=runs))
with open('ising_p006_16runs','wb') as f:
    pickle.dump(results,f)
del(results)    


# In[19]:


runs = 16
p = 0.10
with ProcessPoolExecutor() as ppe:
    results = list(tqdm(ppe.map(main,repeat(p,runs),range(runs)),total=runs))
with open('ising_p010_16runs','wb') as f:
    pickle.dump(results,f)
del(results)    

