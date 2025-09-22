import tkinter as tk
from tkinter import messagebox
from flexion import calculoFlexion

class CalculadoraAcero(tk.Tk):
    """
    Clase para la interfaz gráfica de la calculadora de acero en Tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title("Cálculo de Acero en Vigas de Concreto")
        self.geometry("600x600")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.entries = {}
        self.result_labels = []

        self._crear_widgets()
        self._organizar_elementos()
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        label_text = [
            "Ancho (b) [m]:",
            "Altura (h) [m]:",
            "Recubrimiento al eje [m]:",
            "Resistencia del concreto (fc') [MPa]:",
            "Resistencia del acero (fy) [MPa]:",
            "Momento último (Mu) [kN-m]:"
        ]

        for i, text in enumerate(label_text):
            label = tk.Label(self, text=text)
            entry = tk.Entry(self)
            self.entries[text] = entry
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        self.calcular_button = tk.Button(self, text="Calcular Acero", command=self._calcular_acero)

        for i in range(4):
            label = tk.Label(self, text="", font=("Helvetica", 11))
            self.result_labels.append(label)

    def _organizar_elementos(self):
        """Organiza los widgets en la ventana principal."""
        self.calcular_button.grid(row=len(self.entries), columnspan=2, pady=20)
        
        for i, label in enumerate(self.result_labels):
            label.grid(row=len(self.entries) + 1 + i, columnspan=2)

    def _calcular_acero(self):
        """Maneja el cálculo y la actualización de la interfaz."""
        try:
            valores = [float(entry.get()) for entry in self.entries.values()]
            
            resultados = calculoFlexion(*valores)
            
            for i in range(len(self.result_labels)):
                if i < len(resultados):
                    self.result_labels[i].config(text=f"{resultados[i]}")
                else:
                    self.result_labels[i].config(text="")
        except ValueError:
            messagebox.showerror("Error de entrada", "Asegúrate de ingresar valores numéricos válidos en todos los campos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en el cálculo: {e}")

if __name__ == "__main__":
    app = CalculadoraAcero()
    app.mainloop()