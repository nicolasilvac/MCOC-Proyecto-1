# ENTREGA 6
## Caso 3-D

En esta entrega se realizaron predicciones entregando evoluciones temporales en puntos específicos que representan los sensores térmicos del caso real. En este caso se basó en la investigación del alumno a cargo del profesor Álvaro Paul, para ello se consideraron coordenadas similares a la siguiente imagen:

![al_text](https://github.com/nicolasilvac/MCOC-Proyecto-1/blob/master/%5BEntrega%206%5D/Puntos%20Sensores.png)

Se consideraron 30 segundos para medir la variación de temperatura. 

Cada 89 iteraciones del código se observó que era un segundo, por lo que se utilizaron multiplos de 89 para lograr llegar a los 30 segundos.

Las condiciones de borde que se utilizaron en este caso fueron las siguientes:
- La temperatura inicial de todos los puntos es de 20.75°C, la que corresponde a la temperatura inicial de un hormigón fresco visto en los datos enviados por SAF.
- En todo el volumen, menos los extremos, hay generación de calor según la siguiente fórmula:

![al_text](https://github.com/nicolasilvac/MCOC-Proyecto-1/blob/master/%5BEntrega%206%5D/Funci%C3%B3n.png)


##Resultados

El gráfico que arrojó el programa fue el siguiente:

![al_text](https://github.com/nicolasilvac/MCOC-Proyecto-1/blob/master/%5BEntrega%206%5D/Gr%C3%A1fico%20Entrega%206.png)

Se puede observar que la temperatura cambia según su posición espacial, de forma sinusoidal, donde las con más pendiente son los puntos más al centro y las con menor son los de los extremos. 

