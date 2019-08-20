# -*- coding: utf-8 -*-
from matplotlib.pylab import *

a= 1.       #Ancho del dominio
b = 1.     #Largo del dominio
Nx = 6   #Numero de intervalos en x
Ny = 6
dx = b/Nx  #Discretizacion espacial en x
dy = a/Ny #Discretizacion espacial en y
h = dx

if dx != dy:
    print ("ERROR!!!! dx !=dy")
    exit(-1)

#def coords(i,j):
#   return dx*i, dy*j
    
#x, y = coords(4,2)

#i, j = 4, 2
#x, y = dx*i, dy*j

coords = lambda i, j : (dx*i, dy*j)
x,y = coords (4,2)

print "x = ", x
print "y= ", y

u_k = zeros((Nx+1,Ny+1), dtype = double) #dtype es el tipo de tados(double,float,int32)
u_km1= zeros ((Nx+1,Ny+1), dtype = double)

#CBesencial
u_k[0,:] = 20.
u_k[:,0] = 20.


#buena idea definir funciones que hagan el codigo expresivo
def printbien(u):
    print u_k.T[Nx::-1,:] 
    
print u_k #imprime con el eje y invertido
printbien(u_k)

def inshowbien(u):
    inshow(u.T[Nx::-1,:])
figure()    
inshowbien(u_k)
colorbar()
show()
#Vector con todos los x... puntos del espacio







exit (0) #ejecucion llega hasta aqui

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
rho = 7000.    #Kg/m^3
alpha = K*dt/(c*rho*dx**2)

print "dt = ", dt
print "dx = ", dx
print "K = ", K
print "c = ", c
print "rho = ", rho
print "alpha = ", alpha




#Loop en el tiempo
k = 0
figure (1)
inshowbien(u_k)
title("k = {}   t = {}s".format(k,k*dt))
savefig("movie/frame)

for k in range (1000):
    t = dt*k + 1
    print "k =",k, "t =",t
    
    #CBesencial
    u_k[0,:] = 20.
    u_k[:,0] = 20.
    
   
    for i in range(1,Nx-1):
        for j in range (1,Ny-1):
            #Laplaciano
            nabla_u_k[i,j] = (u_k[i-1,j] + u_k[i+1,j] + u_k[i,j-1] + u_k[i, j+1] - 4*u_k[i,j])/h**2
            
            
            u_km[i,j] = u_k[i,j] + alpha*nabla_u_k[i,j]
        # print i 
        #Algoritmo de diferencias finitas 1-D para difusion
        u_km1[i] = u_k[i] + alpha*(u_k[i+1] - 2*u_k[i] + u_k[i-1])
        
        
    u_km1[Nx,:] = u_km1[Nx-1,:]
    u_km1[:,Ny] = u_km1[:,Ny-1]
    
        
    #Avanzar la solucion a  K+1
    u_k = u_km1
    inshowbien(u_k)
    
    
title("k = {}  t = {} s".format(k, k*dt))

show()