# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 19:56:13 2019

@author: USUARIO
"""
from matplotlib.pylab import *


a = 1.    		#Ancho del dominio
b = 1. 
c = 1         #Largo del dominio
Nx = 40    		#Numero de intervalos en x
Ny = 40 
Nz = 40 		#Numero de intervalos en Y

dx = b / Nx   	#Discretizacion espacial en X
dy = a / Ny   	#Discretizacion espacial en Y
dz = c / Nz
h = dx    # = dy = dz


if dx != dy and dx != dz:
	print("ERRROR!!!!! dx != dy")
	exit(-1)   #-1 le dice al SO que el programa fallo.....

#Funcion de conveniencia para calcular coordenadas del punto (i,j)

# def coords(i,j):
# 	return dx*i, dy*j
# x, y = coords(4,2)  

# i, j = 4, 2 
# x, y = dx*i, dy*j

coords = lambda i, j, k : (dx*i, dy*j, dz*k)
x, y, z = coords(4,2,2) 

print "x = ", x
print "y = ", y
print "z = ", z

#Se crea una matriz llena de 20, que es el valor inicial de la temperatura
u_k = 20*ones((Nx+1,Ny+1, Nz+1), dtype=triple)   #dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = 20*ones((Nx+1,Ny+1, Nz+1), dtype=triple)   #dtype es el tipo de datos (double, float, int32, int16...)

#CB esencial
u_k[0,:] = 20. #Condicion base extremo y inicial
u_k[-1,:] = 20. #Condicion base extremo x inicial

#Buena idea definir funciones que hagan el codigo expresivo
def printbien(u):
	print u.T[Nx::-1,:]

print u_k               #Imprime con el eje y invertido
printbien(u_k)

def imshowbien(u):
	imshow(u.T[Nx::-1,:])
	colorbar(extend='both',cmap='plasma')
	clim(10, 30) #El grafico va desde 10 °C a 30°C

#Parametros del problema (hierro)
dt = 1.0       # s
K = 79.5       # m^2 / s   
c = 450.       # J / kg C
rho = 7800.    # kg / m^3
alpha = K*dt/(c*rho*dx**2)

# dx =  0.166666666667
# dt = 1.0
# alpha =  0.000815384615385

alpha_bueno = 0.0001
dt = alpha_bueno*(c*rho*dx**2)/K
alpha = K*dt/(c*rho*dx**2)


#Informar cosas interesantes
print "dt = ", dt
print "dx = ", dx
print "K = ", K
print "c = ", c
print "rho = ", rho
print "alpha = ", alpha

k = 0

# figure(1)
# imshowbien(u_k)
# title("k = {}   t = {} s".format(k, k*dt))
# savefig("movie/frame_{0:04.0f}.png".format(k))
# close(1)

#Loop en el tiempo 
dnext_t = 1   #  cada 1 segundo se imprime un grafico
next_t = 0.  
framenum = 0
for k in range(int32(50./dt)):
    t = dt*(k+1)
    print "k = ", k, " t = ", t

    #CB esencial
    u_k[0,:] = 20. #condicion de borde
    u_k[-1,:] = 20. #condicion de borde
    u_k[:,-1] = 20. + 10.*sin((2.*math.pi/24.)*t) #Se defina la funcion que generara calor
    #Loop en el espacio   i = 1 ... n-1   u_km1[0] = 0  u_km1[n] = 20
    for i in range(1,Nx):
        for j in range(1,Ny):
            #Algoritmo de diferencias finitas 2-D para difusion            
            #Laplaciano
            nabla_u_k = (u_k[i-1,j] + u_k[i+1,j] + u_k[i,j-1] + u_k[i,j+1] - 4*u_k[i,j])/h**2

            #Forward euler..
            u_km1[i,j] = u_k[i,j] + alpha*nabla_u_k

    #CB natural
    u_km1[Nx,:] = u_km1[Nx-1,:]
    u_km1[:,Ny] = u_km1[:,Ny-1]

    #Avanzar la solucion a k + 1
    u_k = u_km1

    #CB esencial una ultima vez
    u_k[0,:] = 20. #condicion de borde
    u_k[-1,:] = 20. #condicion de borde
    u_k[:,-1] = 20. + 10.*sin((2.*math.pi/24.)*t) #Se defina la funcion que generara calor
    
    print "Tmax = ", u_k.max()
    
    if t > next_t:
        figure(1)
        imshowbien(u_k)
        title("k = {0:4.0f}   t = {1:05.2f} s".format(k, k*dt))
        savefig("movie_1/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)

# figure(2)
# imshowbien(u_k)
# title("k = {}   t = {} s".format(k, (k+1)*dt))


show()