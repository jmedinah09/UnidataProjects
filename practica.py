# /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
####
# Vamos a crear una pequeña red neuronal que compute
# los valores de la tabla XOR
####
##
# Una red neuronal al final son:
# * Una capa de inputs
# * Las conexiones de TODOS LOS INPUTS con TODOS LOS OUTPUTS ( W en la imagen )
# * Una capa de outputs
# La red neuronal se encarga de computar los INPUTS con las CONEXIONES
# para predecir los OUTPUTS
# Para que sea realmente funcional, necesitaremos saber
# cuanto afecta cada conexión al output
##
##Primera parte, generemos un input que sea una matriz
## Matriz de 2x4
## 0 0
## 0 1
## 1 0
## 1 1
INPUT_X = np.array([[0,0],[0,1],[1,0],[1,1]])
print("INPUT_X:\n", INPUT_X)
##Luego la matriz de los resultados esperados
## en nuestro caso
## 0
## 1
## 1
## 0
EXPECTED_RESULT = np.array([[0,1,1,0]]).T # queremos en formato columna
print("EXPECTED_RESULT:\n", EXPECTED_RESULT)
## Resultado: la tabla de verdad de la operación XOR
print("RESULT:\n", np.append(INPUT_X,EXPECTED_RESULT, axis=1))
## Para aprender, la red neuronal debe computar su predicción
## calcular el error, corregir los pesos y volver a computar
## Como tenemos DOS inputs y un OUTPUT, lo que buscamos es conectar
## cada INPUT con el OUTPUT, cada INPUT debe tener un peso, es decir
## cada INPUT modifica MAS o MENOS el output segun su peso.
# Esta es la función de activacion
# que nos permite modelar problemas NO lineales
# Esta mapea cualquier valor a entre 0 y 1
# Aprovechamos la misma función para devolver su derivada, luego lo explicamos.
def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))
#Seteamos una SEED que nos ayudarà a que los numeros esten
# distribuidos de forma random, pero siempre igual para entender
# en qué afecta los cambios que realizamos
np.random.seed(0)
# Inizializamos las CONEXIONES con una media a 0
# Esta es la matriz que irà "aprendiendo"
# La matriz resultando es de 2 x 1 ya que tenemos dos INPUTS y
# un OUTPUT
SYN0 = 2*np.random.random((2,1)) - 1
# Vamos a preparar iteraciones para aprender
for i in range(20000):
# Primero, computamos con nuestra red, a este paso lo llamamos FORWARD
# que resultado tenemos con los pesos
# inicializados de forma random,
    l0 = INPUT_X
#Multiplicamos los INPUTS con las CONEXIONES
    l1 = sigmoid(np.dot(l0, SYN0))
#Computamos el error
    l1_error = EXPECTED_RESULT - l1
#Calculamos la derivada multiplicada por error
#para computar un cambio a realizar en los cambios
    l1_delta = l1_error * sigmoid(l1, True)
    SYN0 += np.dot(l0.T, l1_delta)
    if (i % 1000) == 0 :
        print("Error:" + str(i) + ' ' +
              str(np.mean(np.abs(l1_error))))
print(l1)