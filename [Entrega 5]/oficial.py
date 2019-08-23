from matplotlib.pylab import *
from matplotlib import pyplot

a = 1.    		#Ancho del dominio
b = 1.           #Largo del dominio
c = 1.           #Profundidad del dominio
Nx = 30    		#Numero de intervalos en x
Ny = 30   		#Numero de intervalos en Y
Nz = 30          #Numero de intervalos en Z
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

#CB esencial
u_k[0,:,:] = 20. #Condicion base extremo y inicial
u_k[-1,:,:] = 20. #Condicion base extremo x inicial

#Buena idea definir funciones que hagan el codigo expresivo
def printbien(u):
    print u.T[Nx::-1,:,:]

#print u_k               #Imprime con el eje y invertido
printbien(u_k)  

def imshowbien(u):
	imshow(u.T[Nx::-1,:,:])
	colorbar(extend='both',cmap='plasma')
	clim(10, 30) #El grafico va desde 10C a 30C


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

ListaSensor1, ListaSensor2, ListaSensores3, ListaSensores4, ListaSensores5, ListaSensores6, ListaSensores7, ListaSensores8, ListaSensores9 = [],[],[],[],[],[],[],[],[]

coordenadas_k = [[15,0,15],[15,15,15] ,[15,29,15] ,[15,0,29],[15,15,29] ,[15,29,29] ,[29,0,29],[29,15,29] ,[29,29,29]] #coordenada de cada sensor, arbitrario


for k in range(int32(1./dt)):

    t = dt*(k)
    print "k = ", k, " t = ", t

    #CB esencial
    u_k[0,:,:] = 20. #condicion de borde
    u_k[-1,:,:] = 20. #condicion de borde
    u_k[:,-1,:] = 20.75 + 10.*sin((2.*math.pi/24.)*t) #Se defina la funcion que generara calor
    u_k[:,:,0] = 20.

    #al probar con tiempo = 1, en numero de iteraciones es 202, por lo que tienen que ser multiplos de 202 para que el grafico vaya de 1 en 1 (segundos)
    if k == 200 or k ==  410 or k == 615 or k == 815 or k == 1015 or k == 1216 or k == 1417 or k == 1618 or k == 1819 or k == 2020 or k == 2221 or k == 2422 or k == 2623 or k == 2824 or k == 3025 or k == 3226 or k == 3427 or k == 3628 or k == 3829 or k == 4030:
        ListaSensores1.append(u_k[15, 0,  15])
        ListaSensores2.append(u_k[15, 15, 15])            
        ListaSensores3.append(u_k[15, 29, 15])
        ListaSensores4.append(u_k[15, 0,  29])
        ListaSensores5.append(u_k[15, 15, 29])
        ListaSensores6.append(u_k[15, 29, 29])
        ListaSensores7.append(u_k[29, 0,  29])
        ListaSensores8.append(u_k[29, 15, 29])
        ListaSensores9.append(u_k[29, 29, 29])

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
    u_k[0,:,:] = 0. #condicion de borde
    u_k[-1,:,:] = 0. #condicion de borde
    u_k[:,-1,:] = 20.75 + 10.*sin((2.*math.pi/24.)*t) #Se defina la funcion que generara calor
    u_k[:,:,0] = 0.

    print "Tmax = ", u_k.max()

print "hola"
print ListaSensores1
numeros=  [1,2, 3,4,5]# ,6,7,8 ,9, 10]#, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
pyplot.plot(numeros, ListaSensores1)
pyplot.plot(numeros, ListaSensores2)
pyplot.plot(numeros, ListaSensores3)
pyplot.plot(numeros, ListaSensores4)
pyplot.plot(numeros, ListaSensores5)
pyplot.plot(numeros, ListaSensores6)
pyplot.plot(numeros, ListaSensores7)
pyplot.plot(numeros, ListaSensores8)
pyplot.plot(numeros, ListaSensores9)


pyplot.show()