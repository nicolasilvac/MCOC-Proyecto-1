# -*- coding: utf-8 -*-
from matplotlib.pylab import *

L = 1.     #Largo del dominio
n = 100   #Numero de intervalos

dx = L/n  #Discretizacion espacial

#Vector con todos los x... puntos del espacio
x = linspace(0,L,n+1)


#Condicion inicial
def fun_u0(x):
    return 10*exp(-(x-0.5)**2/0.1**2)
u0 = fun_u0(x)

#Creando el vector de solucion u en el tiempo o paso K
u_k = u0.copy()  #copy crea una nueva instancia del vector en me

#Condiciones de borde (esenciales)
u_k[0] = 0.
u_k[n] = 20.

#Temperatura en el tiempo K+1 t = dt * (K+1)
u_km1 = u_k.copy()

#Parametros del problema (hierro)
dt = 1.        #s
K = 79.5      #m^2/s
c = 450.       #J/Kg C
rho = 7800.    #Kg/m^3
alpha = K*dt/(c*rho*dx**2)

print "dt = ", dt
print "dx = ", dx
print "K = ", K
print "c = ", c
print "rho = ", rho
print "alpha = ", alpha

plot(x,u0,"k--")


#Loop en el tiempo
k = 0
for k in range (5000):
    t = dt*k
    
    u_k[0] = 0.
    u_k[n] = 20.
    #Loop en el espacio  i = 1... n-1  u_Km1[0] = 0  u_Km1[n] = 
    
    for i in range(1,n):
        # print i 
        #Algoritmo de diferencias finitas 1-D para difusion
        u_km1[i] = u_k[i] + alpha*(u_k[i+1] - 2*u_k[i] + u_k[i-1])
        
    #Avanzar la solucion a  K+1
    u_k = u_km1
    
    if k % 200 == 0:
        plot (x,u_k)
        
title("k = {}  t = {} s".format(k, k*dt))

show()