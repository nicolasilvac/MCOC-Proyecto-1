from matplotlib.pylab import *
from matplotlib import pyplot

a = 1.    		#Ancho del dominio
b = 1.           #Largo del dominio
c = 1.           #Profundidad del dominio
Nx = 20    		#Numero de intervalos en x
Ny = 20   		#Numero de intervalos en Y
Nz = 20          #Numero de intervalos en Z
dy = a / Ny   	#Discretizacion espacial en Y
dx = b / Nx   	#Discretizacion espacial en X
dz = c / Ny   	#Discretizacion espacial en Z
h = dx    # = dy  

if dx != dy and dx !=dz:
	print("ERRROR!!!!! dx != dy , dx!= dz")
	exit(-1)   #-1 le dice al SO que el programa fallo.....

#Se crea una matriz llena de 20, que es el valor inicial de la temperatura
u_k = 20.75*ones((Nx+1,Ny+1,Nz+1), dtype=double)   #dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = 20.75*ones((Nx+1,Ny+1,Nz+1), dtype=double)   #dtype es el tipo de datos (double, float, int32, int16...)

#Parametros del problema (hierro)
dt = 1.0       # s
K = 79.5       # m^2 / s   
c = 450.       # J / kg C
rho = 7800.    # kg / m^3
alpha = K*dt/(c*rho*dx**2)

alpha_bueno = 0.0001
dt = alpha_bueno*(c*rho*dx**2)/K
alpha = K*dt/(c*rho*dx**2)

#Informar cosas interesantes
print "dt = ", dt
print "dx = ", dx
print "dz = ", dz
print "K = ", K
print "c = ", c
print "rho = ", rho
print "alpha = ", alpha

#Loop en el tiempo 
dnext_t = 1   #  cada 1 segundo se imprime un grafico
next_t = 0.  
framenum = 0

#listas para cada sensor, sensor vs temperatura
ListaSensor1, ListaSensor2, ListaSensor3, ListaSensor4, ListaSensor5, ListaSensor6, ListaSensor7, ListaSensor8, ListaSensor9 = [],[],[],[],[],[],[],[],[] 

for k in range(int32(30./dt)):

    t = dt*(k)
    print "k = ", k, " t = ", t

    #CB esencial
    u_k[-1,:,:] = 20.75
    u_k[0,:,:] = 20.75
    u_k[:,-1,:] = 20.75 + 10.*sin((2.*math.pi/24.)*t) #Se define la funcion que generara calor


    #al probar con tiempo = 1, en numero de iteraciones es 89, por lo que tienen que ser multiplos de 89 para que el grafico vaya de 1 en 1 (segundos)
    if k == 89 or k ==  178 or k == 267 or k == 356 or k == 445 or k == 534 or k == 623 or k == 712 or k == 801 or k == 890 or k == 979 or k == 1068 or k == 1157 or k == 1246 or k == 1335 or k == 1424 or k == 1513 or k == 1602 or k == 1691 or k == 1780 or k == 1869 or k == 1958 or k == 2047 or k == 2136 or k == 2225 or k == 2315 or k == 2403 or k == 2492 or k == 2581 or k == 2670:
        ListaSensor1.append(u_k[10, 0,  10]) 
        ListaSensor2.append(u_k[10, 10, 10])            
        ListaSensor3.append(u_k[10, 19, 10])
        ListaSensor4.append(u_k[10, 0,  19])
        ListaSensor5.append(u_k[10, 10, 19])
        ListaSensor6.append(u_k[10, 19, 19])
        ListaSensor7.append(u_k[19, 0,  19])
        ListaSensor8.append(u_k[19, 10, 19])
        ListaSensor9.append(u_k[19, 19, 19])

    #Loop en el espacio   i = 1 ... n-1   u_km1[0] = 0  u_km1[n] = 20
    for i in range(1,Nx):
        for j in range(1,Ny):
            for l in range(1,Nz):
                #Algoritmo de diferencias finitas 3-D para difusion            
                #Laplaciano
                nabla_u_k = (u_k[i-1,j,l] + u_k[i+1,j,l] + u_k[i,j-1,l] + u_k[i,j+1,l] + u_k[i,j,l-1] + u_k[i,j,l+1] - 6*u_k[i,j,l])/h**2

                #Forward euler..
                u_km1[i,j,l] = u_k[i,j,l] + alpha*nabla_u_k

    #CB natural
    u_km1[Nx,:,:] = u_km1[Nx-1,:,:]
    u_km1[:,Ny,:] = u_km1[:,Ny-1,:]
    u_km1[:,:,Nz] = u_km1[:,:,Nz-1]
    #Avanzar la solucion a k + 1
    u_k = u_km1
    #CB esencial una ultima vez
    #u_k[-1,:,:] = 20.75
    #u_k[0,:,:] = 20.75
    u_k[:,-1,:] = 20.75 + 10.*sin((2.*math.pi/24.)*t) #Se define la funcion que generara temperatura
    print "Tmax = ", u_k.max()

eje_tiempo = list(range(1, 31)) #crea una lista del eje x como tiempo

plt.title( "Curvas de Temperatura v/s Tiempo en cada sensor" )
plt.ylabel( "Temperatura" )
plt.xlabel( "Tiempo" )
pyplot.plot(eje_tiempo, ListaSensor1)
pyplot.plot(eje_tiempo, ListaSensor2)
pyplot.plot(eje_tiempo, ListaSensor3)
pyplot.plot(eje_tiempo, ListaSensor4)
pyplot.plot(eje_tiempo, ListaSensor5)
pyplot.plot(eje_tiempo, ListaSensor6)
pyplot.plot(eje_tiempo, ListaSensor7)
pyplot.plot(eje_tiempo, ListaSensor8)
pyplot.plot(eje_tiempo, ListaSensor9)
pyplot.plot( ListaSensor1, label = 'Sensor 1')
pyplot.plot( ListaSensor2, label = 'Sensor 2')
pyplot.plot( ListaSensor3, label = 'Sensor 3')
pyplot.plot( ListaSensor4, label = 'Sensor 4')
pyplot.plot( ListaSensor5, label = 'Sensor 5')
pyplot.plot( ListaSensor6, label = 'Sensor 6')
pyplot.plot( ListaSensor7, label = 'Sensor 7')
pyplot.plot( ListaSensor8, label = 'Sensor 8')
pyplot.plot( ListaSensor9, label = 'Sensor 9')
pyplot.legend(loc = 'upper left')
pyplot.show()