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
ventana.title("Calculadora de Acero por flexión simple")

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