import tkinter as tk
from tkinter import font, messagebox
import time
import json
import os

class TextoPalabraPorPalabra:
    def __init__(self, root):
        self.root = root
        self.root.title("Lectura Rápida")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")  # Color de fondo suave

        # Configuración de la fuente
        self.custom_font = font.Font(family="Arial", size=14)
        self.highlight_font = font.Font(family="Arial", size=14, weight="bold")

        # Ruta para el archivo de estado
        self.estado_archivo = "estado_lectura.json"

        # Crear widgets
        self.crear_widgets()
        self.cargar_estado()

    def crear_widgets(self):
        # Texto de introducción
        self.texto_label = tk.Label(self.root, text="Introduce el texto:", font=self.custom_font, bg="#f0f0f0")
        self.texto_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.texto_entry = tk.Text(self.root, height=6, width=50, font=self.custom_font, wrap=tk.WORD, bg="#ffffff", fg="#000000")
        self.texto_entry.grid(row=1, column=0, padx=10, pady=5, columnspan=3)

        # Velocidad
        self.velocidad_label = tk.Label(self.root, text="Velocidad (palabras por minuto):", font=self.custom_font, bg="#f0f0f0")
        self.velocidad_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.velocidad_entry = tk.Entry(self.root, font=self.custom_font, bg="#ffffff", fg="#000000")
        self.velocidad_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Botones
        self.start_button = tk.Button(self.root, text="Iniciar", command=self.iniciar_lectura, font=self.custom_font, bg="#4CAF50", fg="#ffffff")
        self.start_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.pause_button = tk.Button(self.root, text="Pausar", command=self.pausar_lectura, state=tk.DISABLED, font=self.custom_font, bg="#FFC107", fg="#ffffff")
        self.pause_button.grid(row=4, column=1, padx=10, pady=10)

        self.resume_button = tk.Button(self.root, text="Reanudar", command=self.reanudar_lectura, state=tk.DISABLED, font=self.custom_font, bg="#2196F3", fg="#ffffff")
        self.resume_button.grid(row=4, column=2, padx=10, pady=10)

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.resetear, font=self.custom_font, bg="#F44336", fg="#ffffff")
        self.reset_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar palabras y cronómetro
        self.resultado_label = tk.Label(self.root, text="", font=("Arial", 24), bg="#ffffff", fg="#000000")
        self.resultado_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.cronometro_label = tk.Label(self.root, text="Tiempo transcurrido: 0s\nPalabras leídas: 0", font=("Arial", 12), bg="#ffffff", fg="#000000")
        self.cronometro_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def iniciar_lectura(self):
        texto = self.texto_entry.get("1.0", tk.END).strip()
        velocidad = self.velocidad_entry.get()

        if not texto or not velocidad.isdigit():
            self.resultado_label.config(text="Por favor, ingrese un texto y una velocidad válida.")
            return

        velocidad = int(velocidad)
        if velocidad <= 0:
            self.resultado_label.config(text="La velocidad debe ser un número positivo.")
            return

        self.words = texto.split()
        self.current_word_index = 0
        self.interval = 60 / velocidad
        self.start_time = time.time()
        self.paused = False
        self.next_word_time = self.start_time

        self.resultado_label.config(text="")
        self.actualizar_cronometro()

        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)

        self.mostrar_palabras()

    def pausar_lectura(self):
        self.paused = True
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        self.guardar_estado()

    def reanudar_lectura(self):
        self.paused = False
        self.next_word_time = time.time() + (self.interval - (self.next_word_time - self.start_time) % self.interval)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)

        self.mostrar_palabras()

    def mostrar_palabras(self):
        if self.paused:
            return

        if self.current_word_index < len(self.words):
            current_time = time.time()
            if current_time >= self.next_word_time:
                palabra = self.words[self.current_word_index]
                self.resultado_label.config(text=self.format_palabra(palabra))
                self.current_word_index += 1

                self.actualizar_cronometro()

                self.next_word_time = current_time + self.interval
            self.root.after(10, self.mostrar_palabras)  # Revisar cada 10 ms
        else:
            self.resultado_label.config(text="Lectura completada")
            self.cronometro_label.config(text="Tiempo transcurrido: {}s\nPalabras leídas: {}".format(
                int(time.time() - self.start_time),
                len(self.words)
            ))
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)

    def format_palabra(self, palabra):
        medio = len(palabra) // 2
        palabra_formateada = f"{palabra[:medio]}{palabra[medio:medio+1]}{palabra[medio+1:]}"
        return palabra_formateada

    def actualizar_cronometro(self):
        if not self.paused:
            tiempo_transcurrido = int(time.time() - self.start_time)
            palabras_leidas = self.current_word_index
            self.cronometro_label.config(text="Tiempo transcurrido: {}s\nPalabras leídas: {}".format(
                tiempo_transcurrido,
                palabras_leidas
            ))
            self.root.after(1000, self.actualizar_cronometro)

    def resetear(self):
        self.texto_entry.delete("1.0", tk.END)
        self.velocidad_entry.delete(0, tk.END)
        self.resultado_label.config(text="")
        self.cronometro_label.config(text="Tiempo transcurrido: 0s\nPalabras leídas: 0")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.words = []
        self.current_word_index = 0
        self.interval = 0
        self.start_time = None
        self.next_word_time = None
        self.paused = False
        if os.path.exists(self.estado_archivo):
            os.remove(self.estado_archivo)

    def guardar_estado(self):
        estado = {
            "texto": self.texto_entry.get("1.0", tk.END).strip(),
            "velocidad": self.velocidad_entry.get(),
            "current_word_index": self.current_word_index,
            "start_time": self.start_time,
            "paused": self.paused
        }
        with open(self.estado_archivo, "w") as archivo:
            json.dump(estado, archivo)

    def cargar_estado(self):
        if os.path.exists(self.estado_archivo):
            with open(self.estado_archivo, "r") as archivo:
                estado = json.load(archivo)
                if estado.get("paused", False):
                    self.texto_entry.delete("1.0", tk.END)
                    self.texto_entry.insert(tk.END, estado.get("texto", ""))
                    self.velocidad_entry.delete(0, tk.END)
                    self.velocidad_entry.insert(0, estado.get("velocidad", ""))
                    self.current_word_index = estado.get("current_word_index", 0)
                    self.start_time = estado.get("start_time", time.time())
                    self.paused = estado.get("paused", False)
                    self.interval = 60 / int(self.velocidad_entry.get() or 1)
                    self.next_word_time = self.start_time + (self.interval - (self.start_time - self.start_time) % self.interval)
                    self.start_button.config(state=tk.NORMAL)
                    self.pause_button.config(state=tk.NORMAL if self.paused else tk.DISABLED)
                    self.resume_button.config(state=tk.NORMAL if self.paused else tk.DISABLED)
                    self.mostrar_palabras()

# Crear la ventana principal
root = tk.Tk()
app = TextoPalabraPorPalabra(root)
root.mainloop()
