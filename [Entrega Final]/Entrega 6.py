from matplotlib.pylab import *
from matplotlib import pyplot

a = 1.    	 #Ancho del dominio
b = 1.           #Largo del dominio
c = 1.           #Profundidad del dominio
Nx = 20    	 #Numero de intervalos en x
Ny = 20   	 #Numero de intervalos en Y
Nz = 20          #Numero de intervalos en Z
dy = a / Ny   	 #Discretizacion espacial en Y
dx = b / Nx   	 #Discretizacion espacial en X
dz = c / Ny   	 #Discretizacion espacial en Z
h = dx    # = dy  

if dx != dy and dx !=dz:
	print("ERRROR!!!!! dx != dy , dx!= dz")
	exit(-1)   #-1 le dice al SO que el programa fallo.....

#Parametros del problema hormigon H30
dt = 1.0       # hr
K = 9.5        # m^2 / s   
c = 950.       # J / kg C
rho = 2400.    # kg / m^3
alpha = K*dt/(c*rho*dx**2)
alpha_bueno = 0.0001
dt = alpha_bueno*(c*rho*dx**2)/K
alpha = K*dt/(c*rho*dx**2)

#Se llama el archivo .txt de la temperatura ambiente
archivo = open('TemperaturaAmbiente.txt','r')
TempAmbiente = []
for linea in archivo.readlines():
    TempAmbiente.append(float(linea))

#Se crea una matriz llena de temperatura inicial ambiente
u_k = TempAmbiente[0]*ones((Nx+1,Ny+1,Nz+1), dtype=double)     #dtype es el tipo de datos (double, float, int32, int16...)
u_km1 = TempAmbiente[0]*ones((Nx+1,Ny+1,Nz+1), dtype=double)   #dtype es el tipo de datos (double, float, int32, int16...)

#Loop en el tiempo 
dnext_t = 60   #  cada 60 segundos se imprime un grafico
next_t = 0.  
framenum = 0
valores = []
#listas para cada sensor, sensor vs temperatura
ListaSensor1, ListaSensor2, ListaSensor3, ListaSensor4, ListaSensor5, ListaSensor6, ListaSensor7, ListaSensor8, ListaSensor9 = [],[],[],[],[],[],[],[],[] 

#funcion del cemento que genera calor a traves del tiempo #cemento 7OPC 308kg
def Q(t): 
    C3S,C2S,C3A,C4AF,SO3,CaO,MgO,pcem,pslag,hfa,pfa,betha,thau,hh,Huau,E,R= 197.12,56.72,15.4,28.13,11.,198.,8.,0.25,0.,1800.,0.,0.98,9.8,9.8,358.963,27.096,8.314
    Ht = 500.*C3S + 260.*C2S + 866.*C3A + 420.*C4AF + 624.*SO3 + 1186.*CaO + 850.*MgO #Calor de hidratacion
    Hu = Ht*pcem + 461.*pslag + hfa*pfa #Calor total de hidratacion al 100%
    return Hu*1140.*(thau/t)**betha*(betha/t)*0.7*exp(-(thau/t)**betha)*exp((E/R)*(1./(273.+66.)-1./(273.+20.75)))*10**-7 #formula de calor paper SAF

for k in range(int32(200./dt)): #se imprimimen 200 pares ordenados de puntos
    t = dt*(k+1)
    print "k = ", k, " t = ", t
    #CB esencial
    u_k[:,-1,:] = TempAmbiente[k] #La cara expuesta obtiene el valor de la temperatura ambiente
    if k % 15 == 0: #al probar con tiempo = 1, en numero de iteraciones es 15, por lo que tienen que ser multiplos de 15 para que el grafico vaya de 1 en 1 (segundos)
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

                if t < 10: #las primeras 10 horas se comporta de un modo diferente al superior a 10 horas
                    #Forward euler..
                    u_km1[i,j,l] = u_k[i,j,l] + alpha*nabla_u_k + Q(t)
                else:
                    u_km1[i,j,l] = u_k[i,j,l] + alpha*nabla_u_k
    #CB natural
    u_km1[Nx,:,:] = u_km1[Nx-1,:,:]
    u_km1[:,Ny,:] = u_km1[:,Ny-1,:]
    u_km1[:,:,Nz] = u_km1[:,:,Nz-1]
    #Avanzar la solucion a k + 1
    u_k = u_km1
    #CB esencial una ultima vez
    u_k[:,-1,:] = TempAmbiente[k] #Por cada iteracion recorre +1 en la lista 
    print "Tmax = ", u_k.max()

eje_tiempo = list(range(1, len(ListaSensor1)+1)) #crea una lista del eje x con el mismo numero de elementos que la ListaSensorX
plt.title( "Curvas de Temperatura v/s Tiempo en cada sensor" )
plt.ylabel( "Temperatura (C)" )
plt.xlabel( "Tiempo (hrs)" )
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
pyplot.legend(loc = 'upper right')
pyplot.show()
savefig('Grafico Entrega 6.png')
