# Acero por Flexión simple para vigas de concreto reforzado

En la materia de **Hormigón Armado**, generalmente el primer tema que se ve es *Flexión simple*.

En este caso, los procesos para calcular el acero a flexión de una viga de hormigón armado son bastante tediosos. Esto se puede automatizar con
Python.

## Verión de Python usada

* Python 3.13.1

## Programa a realizar

En el programa ingresaremos:

* *b [m]*: Ancho de la viga (en metros)
* *h [m]*: Altura de la sección transversal (en metros)
* *recubrimiento al eje [m]* (en metros)
* *fc' [MPa]*: Resistencia a compresión del concreto (en Mega Pascales)
* *fy' [MPa]*: Resistencia del acero (en Mega Pascales)
* *Mu [KN-m]*: Momento en estado límite último (Kilo Newtons metro)

Son los valores típicos para una viga de vivienda.

Lo que vamos a lograr es obtener:

* $cm^{2}$ de Acero a tracción
* $cm^{2}$ de Acero a compresión
* $cm^{2}$ de Acero mínimo
* KN-m, $\phi Mmax$ (Momento máximo)
* Una leyenda que nos dice que *no se necesita acero a compresión*

## Diagrama de flujo de Flexión simple para una viga de hórmigon armado

## Realizar programa

### Datos requeridos

Los vamos a mantener constantes (por ahora)

* Una base
* La altura de nuestra viga
* Recubrimiento $d$ y $d'$, son la distancia de la cara más hasta el eje de los aceros a tracción o el eje de los aceros a compresión respectivamente. No se los vamos a pedir al usuario directamente, sólo le vamos a pedir el recubrimiento a los aceros que van a ser 5 cm
* La resistencia a compresión del concreto
* La resistencia del acero 

```python
b = 0.2
h = 0.4
recub = 0.05
fc = 20
fy = 500
Mu = 70
```

### Cálculo de sección de acero a flexión

Primeramente, tenemos que homogenizar todas nuestras unidades:

* **Metros** para toda la sección transversal
* **Mega Pascales** para la resistencia de los materiales
* **Kilo Newtons** para el momento flector

En este caso, la única medida **Kilo Newtons** la vamos a transformar a **Mega Newtons** para todos nuestros cálculos:

```python
Mu = Mu/1000
```

También necesitamos $d$ y $d'$:

$d$ es igual a la altura de la viga menos el recubrimiento:

$d = h - recubrimiento$

$d'$ es la distancia de la fibra más comprimida de la viga hasta el eje de los aceros a compresión.

En este caso, es la misma que el recubrimiento:

$d' = recubrimiento$

```python
d = h-recub
dp = recub
```

### Calcular la cuantía de nuestro acero

La cuantía para la cual nosotros tenemos la afluencia del acero a tracción.

#### Variables y Parámetros

- $\phi$ = factor de seguridad de diseño para flexión = 0.90
- $\rho_{max}$ = cuantía máxima = 0.005
- $\rho_{cy}$ = cuantía correspondiente a la mínima cantidad de acero a tracción necesaria para que el acero a compresión fluya.
- $A_{s_{max}}$ = Acero máximo a tracción que debe tener la sección sin necesidad de acero a compresión $[m^2]$
- $A_s$ = Acero a tracción de cálculo, que soportará el momento $M_u$ $[m^2]$
- $A_{s'}$ = Acero a compresión de cálculo, que soportará el momento $M_u$ $[m^2]$
- $A_{s'rev}$ = Acero a compresión corregido debido a la no fluencia del mismo $[m^2]$
- $M_2$ = momento no resistido por el par acero $A_{s_{max}}$ - zona de compresión de hormigón $[N m]$
- $a$ = peralte idealizado del bloque de compresión del concreto $[m]$
- $c$ = distancia de la fibra comprimida al eje neutro $[m]$
- $\gamma$ = Parámetro experimental del bloque de compresión del concreto (generalmente 0.85)
- $\epsilon_u$ = deformación unitaria del hormigón (en la mayoría de los casos 0.003)
- $\beta_1$ = parámetro experimental del bloque de compresión del concreto ($0.85$ para $f'_c < 28[MPa]$)


#### **Tabla de valores para $\beta_1$**

Para un cálculo de $\beta_1$ cuando $f'_c$ es mayor a 28 MPa, se utilizará la tabla:

**Tabla 22.2.2.4.3 — Valores de $\beta_1$ para la distribución rectangular equivalente de esfuerzos en el concreto.**

| $f'_c$ , MPa | $\beta_1$ | |
| :--- | :--- | :--- |
| $17 \leq f'_c \leq 28$ | $0.85$ | (a) |
| $28 < f'_c < 55$ | $0.85 - \frac{0.05(f'_c - 28)}{7}$ | (b) |
| $f'_c \geq 55$ | $0.65$ | (c) |

#### Comentarios sobre el acero a compresión

Si bien el algoritmo calcula acero a compresión para casos donde $M_u$ sobrepase $\phi M_{max}$, no es recomendable que se prefiera utilizar
acero a compresión en vez de incrementar la sección de la viga «$b$» o la altura «$h$». Por tanto cada que $M_u$ sobrepase $\phi M_{max}$, te
recomiendo que incrementes «$b$» o «$h$» hasta que $\phi M_{max}$ sea mayor a $M_u$.
---

Entonces:

```python
gamma = 0.85
eu = 0.003

if fc<=28:
    beta1 = 0.85
elif fc>=55:
    beta1 = 0.65
else:
    beta1 = 0.85-0.05*(fc-28)/7

roMax = gamma*beta1*fc/fy*eu/(eu+0.005) # Cuantía máxima de acero (adimensional)
AsMax = roMax*b*d                       # Acero máximo
fiMmax = 0.9*AsMax*fy*(d-AsMax*fy/(2*gamma*fc*b)) # En Mega Newtons

AsMin1 = fc**0.5/(4*fy)*b*d
AsMin2 = 1.4*b*d/fy

AsMin = max(AsMin1, AsMin2) # Acero mínimo
```

$\phi M_{max}$ es el máximo momento flector que puede resistir nuestra viga sin necesidad de acero a compresión. Calcularlo nos sirve para compararlo con el momento último $M_{u}$.

### Comparación

Si $M_{u} > \phi M_{max}$, nuestra viga necesita acero a compresión, y si no, lo calculamos de otra manera.

Invertimos el condicional:

```python
if Mu<fiMmax:
    numerador = 0.9*d-(0.81*d**2 - 1.8*Mu/(gamma*fc*b))**0.5
    denominador = 0.9*fy/(gamma*fc*b)
    As = numerador/denominador

    texto1 = "Acero a tracción = " + str(As) # m^2
    texto2 = "Acero a compresión = 0"
    texto3 = "Acero mínimo a tracción = " + str(AsMin)
    texto4 = "La viga no necesita acero a compresión"
else:
    M2 = (Mu-fiMmax)/0.9
    As2 = M2/(fy*(d-dp))
    As = AsMax+As2
    Asp = As2

    roY = gamma*fc/fy*beta1*eu/(eu-fy/Es)*dp/d+Asp/(b*d)
    ro = As/(b*d)

    if ro>roY:
        texto1 = "Acero a tracción = " + str(As) # m^2
        texto2 = "Acero a compresión = " + str(Asp)
        texto3 = "Acero mínimo a tracción = " + str(AsMin)
        texto4 = "La viga NECESITA acero a compresión. As' fluye"
    else:
        a = (As-Asp)*fy/(gamma*fc*b)
        c = a/beta1
        fsp = eu*Es*(c-dp)/c
        AsRev = Asp*fy/fsp
        texto1 = "Acero a tracción = " + str(As) # m^2
        texto2 = "Acero a compresión = " + str(Asp)
        texto3 = "Acero mínimo a tracción = " + str(AsMin)
        texto4 = "La viga NECESITA acero a compresión. As' no fluye"
```

$A_{s_{2}}$ es la cantidad de acero absorbido por nuestra viga, en el par **acero a compresión** y **acero a tracción**.

$\rho_{y}$ es la cantidad mínima de **acero a tracción** que nosotros necesitamos para que el **acero a compresión** fluya.

Si $\rho > \rho_{y}$, entonces el acero a compresión fluye, y si no, tenemos que hacer un reajuste en el acero a compresión.

$E_{s}$ es el módulo elástico de nuestro acero. Va a ser igual a Giga Pascales.

Si le aumentamos 3 ceros, vamos a estar en Mega Pascales:

```python
Es = 200e3
```

$f_{s'}$ es el esfuerzo de acero a compresión.

Muchas veces es interesante saber que el acero a compresión no fluye y en algunos casos por cuanto no fluye e imprimir cuál es el esfuerzo real
del acero a compresión.

Esto generalmente sucede cuándo el acero a compresión esta muy abajo, cuando tiene un recubrimiento muy fuerte de concreto arriba o en vigas
planas. En esos casos, el acero a compresión muchas veces es incluso inútil, no fluye nada, es casi como no ponerlo.

### Imprimir datos

```python
print(texto1)
print(texto2)
print(texto3)
print(texto4)
```

Hay cosas que nos interesa corregir.

El acero a tracción, nos interesa que es en $cm^2$. Entonces, lo vamos a corregir:

```python
if Mu<fiMmax:
    numerador = 0.9*d-(0.81*d**2 - 1.8*Mu/(gamma*fc*b))**0.5
    denominador = 0.9*fy/(gamma*fc*b)
    As = numerador/denominador

    texto1 = "Acero a tracción = " + str(round(As*1e4,2)) # m^2 a cm^2
    texto2 = "Acero a compresión = 0"
    texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) # m^2 a cm^2
    texto4 = "La viga no necesita acero a compresión"
```

Al multiplicarlo por 10,000 los $m^2$ se transforman a $cm^2$.

Redondeamos el acero a compresión en caso de que nuestro momento sea muy grande:

```python
    if ro>roY:
        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) # m^2 a cm^2
        texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) # m^2 a cm^2
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) # m^2 a cm^2
        texto4 = "La viga NECESITA acero a compresión. As' fluye"
    else:
        a = (As-Asp)*fy/(gamma*fc*b)
        c = a/beta1
        fsp = eu*Es*(c-dp)/c
        AsRev = Asp*fy/fsp
        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) # m^2 a cm^2
        texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) # m^2 a cm^2
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) # m^2 a cm^2
        texto4 = "La viga NECESITA acero a compresión. As' no fluye"
```

Si elevamos el momento flector a $Mu = 120$:

```plaintext
Acero a tracción = 9.04
Acero a compresión = 1.45
Acero mínimo a tracción = 1.96
La viga NECESITA acero a compresión. As' fluye
```

Agregamos las unidades:

```python
if Mu<fiMmax:
    numerador = 0.9*d-(0.81*d**2 - 1.8*Mu/(gamma*fc*b))**0.5
    denominador = 0.9*fy/(gamma*fc*b)
    As = numerador/denominador

    texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]" # m^2 a cm^2
    texto2 = "Acero a compresión = 0 [cm2]"
    texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]" # m^2 a cm^2
    texto4 = "La viga no necesita acero a compresión"
else:
    M2 = (Mu-fiMmax)/0.9
    As2 = M2/(fy*(d-dp))
    As = AsMax+As2
    Asp = As2

    roY = gamma*fc/fy*beta1*eu/(eu-fy/Es)*dp/d+Asp/(b*d)
    ro = As/(b*d)
    if ro>roY:
        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto4 = "La viga NECESITA acero a compresión. As' fluye"
    else:
        a = (As-Asp)*fy/(gamma*fc*b)
        c = a/beta1
        fsp = eu*Es*(c-dp)/c
        AsRev = Asp*fy/fsp
        texto1 = "Acero a tracción = " + str(round(As*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto2 = "Acero a compresión = " + str(round(Asp*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto3 = "Acero mínimo a tracción = " + str(round(AsMin*1e4,2)) + "[cm2]" # m^2 a cm^2
        texto4 = "La viga NECESITA acero a compresión. As' no fluye"
```

### Entorno gráfico

Usaremos la librería **Tkinter**.

Creamos la interfaz en un nuevo archivo llamado `interfaz.py` y volvemos todo nuestro código en `flexion.py` en una función:

```python
def calculoFlexion():
    # Código de flexion.py
```
Y pegamos nuestro código dentro de `interfaz.py` (en mi caso, importaré la función dentro de `interfaz.py`).

También vinculamos la función al botón y cambiamos los textos de los labels:

```python
import tkinter as tk
from flexion import *

def calcularAcero():
    # Obtener los valores ingresados por el usuario
    valor1 = float(entry1.get())
    valor2 = float(entry2.get())
    valor3 = float(entry3.get())
    valor4 = float(entry4.get())
    valor5 = float(entry5.get())
    valor6 = float(entry6.get())
    valores = calculoFlexion(valor1, valor2, valor3, valor4, valor5, valor6)
    
    for i in range(len(valores)):
        etiquetas_resultado[i].config(text=valores[i])

# Crear la ventana
ventana = tk.Tk()
ventana.title("")

# Crear las etiquetas y los campos de entrada
label1 = tk.Label(ventana, text="b [m]:")
label1.pack()
entry1 = tk.Entry(ventana)
entry1.pack()

label2 = tk.Label(ventana, text="h [m]:")
label2.pack()
entry2 = tk.Entry(ventana)
entry2.pack()

label3 = tk.Label(ventana, text="recub. al eje [m]:")
label3.pack()
entry3 = tk.Entry(ventana)
entry3.pack()

label4 = tk.Label(ventana, text="fc' [MPa]:")
label4.pack()
entry4 = tk.Entry(ventana)
entry4.pack()

label5 = tk.Label(ventana, text="fy [MPa]:")
label5.pack()
entry5 = tk.Entry(ventana)
entry5.pack()

label6 = tk.Label(ventana, text="Mu [KN-m]:")
label6.pack()
entry6 = tk.Entry(ventana)
entry6.pack()

# Crear el botón para calcular la suma
boton_sumar = tk.Button(ventana, text="Calcular Acero", command=calcularAcero)
boton_sumar.pack()

# Crear la etiqueta para mostrar el resultado
etiqueta_resultado1 = tk.Label(ventana, text="")
etiqueta_resultado1 = tk.Label(ventana, text="")
etiqueta_resultado1.pack()
etiqueta_resultado2 = tk.Label(ventana, text="")
etiqueta_resultado2.pack()
etiqueta_resultado3 = tk.Label(ventana, text="")
etiqueta_resultado3.pack()
etiqueta_resultado4 = tk.Label(ventana, text="")
etiqueta_resultado4.pack()

# Lista de etiquetas de resultado para fácil acceso
etiquetas_resultado = [
    etiqueta_resultado1,
    etiqueta_resultado2,
    etiqueta_resultado3,
    etiqueta_resultado4
]

# Ejecutar la ventana
ventana.mainloop()
```

## Enlace al video de Youtube

* Enlace: [Como programar Acero por Flexión simple para vigas de concreto reforzado en Python](https://youtu.be/jsC9z77-QYA?si=GnO-t3-VyVOkV849)