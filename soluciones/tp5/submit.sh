#!/bin/bash

## Dos numerales para comentar
## Un numeral para pasarle parámetros a SLURM con la palabra SBATCH

## Nombre del trabajo
#SBATCH --job-name=WS_ISING

## Listado de nodos en donde se quiere ejecutar la simulación,
## puede estar vacío para que Slurm los elija solo.
#SBATCH --nodelist=toko07

## Cantidad de nodos que se quieren utilizar
#SBATCH --nodes=1

# Cantidad de procesos que se ejcutarán por nodo,
#SBATCH --ntasks-per-node=32

## Número de procesos en los cuales se quiere ejecutar el trabajo
## ntask-per-node * nodes = ntasks.
#SBATCH --ntasks=32

## Partición en la cual se quiere enviar el trabajo.
#SBATCH --partition=Large

##Tiempo estimado de ejecución
#SBATCH --time=72:00:00

##NO BORRAR
. /etc/profile

## MODULOS a cargar
module purge


./run.sh