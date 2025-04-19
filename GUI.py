from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import tkinter as tk
from Clases import *
from algoritmoVoraz import salida
import os
import traceback

archivo_generado= None

def cargar_archivo():
    
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if archivo:
        archivo_seleccionado.set(archivo)  
        return archivo  
    return None

def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = [linea.strip() for linea in archivo.readlines()]

        if len(lineas) < 3:
            print("El archivo no tiene suficientes líneas.")
            return None

        primera_linea = int(lineas[0])
        ultima_linea = int(lineas[-1])

        datos_intermedios = []
        for linea in lineas[1:-1]:
            numeros = linea.split(',')
            fila = [int(n) if i < 3 else float(n) for i, n in enumerate(numeros)]
            datos_intermedios.append(fila)

        return [primera_linea, datos_intermedios, ultima_linea]

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    

def crear_RedSocial(datos):
    sag = []
    grupo = datos[1]
    for agente in grupo:
        sag.append(Agentes(agente[0], agente[1], agente[2], agente[3]))
        
    
    
    return RedSocial(sag, datos[2])
           

def escribir_archivo(ruta_archivo, contenido):
    try:
        
        if not ruta_archivo.lower().endswith('.txt'):
            ruta_archivo += '.txt'
            
        with open(ruta_archivo, 'w') as file:
            file.write(f"{contenido.ci}\n")
            file.write(f"{contenido.esfuerzo}\n")
            for tupla in contenido.nuevaRed.sag:
                print("esto es un tupla")
                print(tupla)
                
                info = [tupla.n, tupla.o1, tupla.o2, tupla.r]  
                valores = [str(valor) for valor in info]   
                linea = ", ".join(valores)                  
                file.write(f"{linea}\n")  
            print("salio del for de tupla")
        
        print(f"Archivo generado en: {os.path.abspath(ruta_archivo)}")  
        return os.path.abspath(ruta_archivo)
    except Exception as e:
        print(f"Error al escribir archivo: {e}")  
        raise  

def enviar_info():
    global archivo_generado
    
    nombre_archivo = archivo_seleccionado.get()

    
    
    try:
       
        datos = leer_archivo(nombre_archivo)
        res = crear_RedSocial(datos)
        
        
        alg = opcion_alg.get()
        if alg == "Voraz":
            sol = salida(res)
            print("hallo la sol")
            archivo_generado = escribir_archivo("resultados.txt", sol)
        elif alg == "Fuerza Bruta":
            print("f")
            archivo_generado = escribir_archivo("resultados.txt", res)
        elif alg == "Dinámica":
            print("d")
            archivo_generado = escribir_archivo("resultados.txt", res)
        else:
            messagebox.showerror("Error", "Algoritmo no válido.")
            return
            
        if archivo_generado:
            messagebox.showinfo("Éxito", f"Archivo generado en:\n{archivo_generado}")
        else:
            messagebox.showerror("Error", "No se generó ningún archivo.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar: {str(e)}")
        print(f"Error detallado: {traceback.format_exc()}")  # Para depuración
    
def descargar_resultados():
    global archivo_generado

    if not archivo_generado:
        messagebox.showerror("Error", "No hay resultados para descargar. Procesa un archivo primero.")
        return

    try:
        
        with open(archivo_generado, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

       
        archivo_guardar = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo_guardar:
            archivo_guardar.write(contenido)  # Escribir el contenido en la nueva ubicación
            archivo_guardar.close()
            messagebox.showinfo("Éxito", "Archivo descargado exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo generado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al descargar el archivo: {str(e)}")

ventana = tk.Tk()
ventana.title("Moderador del conflicto interno")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Encabezado
frame_encabezado = tk.Frame(ventana, pady=10)
frame_encabezado.pack()
texto_inicial = tk.Label(frame_encabezado, text="MCI", font=("Arial", 16, "bold"))
texto_inicial.pack()
subtexto_inicial = tk.Label(frame_encabezado, text="Complete los campos para procesar su red social", font=("Arial", 10))
subtexto_inicial.pack()

# Entrada para cargar archivo
frame_archivo = tk.Frame(ventana, pady=10)
frame_archivo.pack(fill="x", padx=20)
texto_archivo = tk.Label(frame_archivo, text="Seleccione un archivo:", anchor="w")
archivo_seleccionado = tk.StringVar()
campo_archivo = tk.Entry(frame_archivo, textvariable=archivo_seleccionado, width=40, state="readonly")
campo_archivo.pack(side="left", pady=5, padx=5)
boton_cargar = tk.Button(frame_archivo, text="Cargar Archivo", command=cargar_archivo,bg="#D1C4E9", fg="black")
boton_cargar.pack(side="left", pady=5, padx=5)

# Selección de algoritmo
frame_algoritmo = tk.Frame(ventana, pady=10)
frame_algoritmo.pack(fill="x", padx=20)
texto_algoritmo = tk.Label(frame_algoritmo, text="Seleccione un algoritmo:", anchor="w")
texto_algoritmo.pack(fill="x")
opcion_alg = tk.StringVar()
combobox_alg = Combobox(frame_algoritmo, textvariable=opcion_alg, state="readonly", values=["Fuerza Bruta", "Dinámica", "Voraz"])
combobox_alg.current(0)
combobox_alg.pack(pady=5)

# Botón de procesar archivo
frame_boton = tk.Frame(ventana, pady=10)
frame_boton.pack()
boton = tk.Button(frame_boton, text="Obtener Resultados", command=enviar_info, width=20, bg="#F8BBD0", fg="black")
boton.pack()

# Botón de descargar resultados
boton_descargar = tk.Button(frame_boton, text="Descargar Resultados", command=descargar_resultados, width=20,  bg="#D1C4E9", fg="black")
boton_descargar.pack(pady=10)

# Iniciar la interfaz
ventana.mainloop()