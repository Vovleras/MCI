from tkinter import filedialog, messagebox, scrolledtext 
from tkinter.ttk import Combobox
import tkinter as tk
from Clases import *
import funcionesAuxiliares
import os
import traceback

archivo_generado= None

def cargar_archivo():
    global datos
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if archivo:
        archivo_seleccionado.set(archivo)  
        try:
            datos = leer_archivo(archivo_seleccionado.get())
        except Exception as e:
            print(f"Error al leer el archivo: {e}")  
            raise 
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

        ventana_entrada.configure(state="normal")
        ventana_entrada.delete('1.0', tk.END)
        grupos = '\n'.join(str(sublista) for sublista in datos_intermedios)
        ventana_entrada.insert(tk.INSERT,"DATOS DE ENTRADA\n\nCantidad de grupos: " +str(primera_linea)+"\n\nEsfuerzo máximo: "+str(ultima_linea)+"\n\nGrupos de agentes:\n"+grupos)
        ventana_entrada.configure(state="disabled")
        
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
           

def escribir_archivo(contenido):
    try:
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            title="Guardar archivo como"
        )
                
        if not ruta_archivo:
            print("Guardado cancelado por el usuario.")
            return None
            
        with open(ruta_archivo, 'w') as file:
            file.write(f"{contenido.ci}\n")
            file.write(f"{contenido.esfuerzo}\n")
            for e in contenido.e:
                file.write(f"{e}\n")  
            print("salio del for de e")
        
        print(f"Archivo generado en: {os.path.abspath(ruta_archivo)}")  
        return os.path.abspath(ruta_archivo)
    except Exception as e:
        print(f"Error al escribir archivo: {e}")  
        raise  

def enviar_info():
    global archivo_generado, datos  
    try:
        res = crear_RedSocial(datos)
        alg = opcion_alg.get()
        sol = funcionesAuxiliares.salida(res,alg)
        archivo_generado = escribir_archivo(sol) 
            
        if archivo_generado:
            ventana_resultado.configure(state="normal")
            ventana_resultado.delete('1.0', tk.END)
            ventana_resultado.insert(tk.INSERT,"RESULTADO\n\nConflicto Interno: " +str(sol.ci)+"\n\nEsfuerzo: " +str(sol.esfuerzo)+"\n\nSolución: " +str(sol.e))
            ventana_resultado.configure(state="disabled")
            messagebox.showinfo("Éxito", f"Archivo generado en:\n{archivo_generado}")
        else:
            messagebox.showerror("Error", "No se generó ningún archivo.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar: {str(e)}")
        print(f"Error detallado: {traceback.format_exc()}")  # Para depuración
    
ventana = tk.Tk()
ventana.title("Moderador del conflicto interno")
ventana.geometry("600x625")
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
campo_archivo = tk.Entry(frame_archivo, textvariable=archivo_seleccionado, width=72, state="readonly")
campo_archivo.pack(side="left", pady=5, padx=5)
boton_cargar = tk.Button(frame_archivo, text="Cargar Archivo", command=cargar_archivo,bg="#D1C4E9", fg="black")
boton_cargar.pack(side="left", pady=5, padx=5)

#Ventana para mostrar entrada:
ventana_entrada = scrolledtext.ScrolledText(wrap = tk.WORD,  width = 40,  height = 10, font =("Arial", 12)) 
ventana_entrada.config(state=tk.DISABLED)
ventana_entrada.pack()

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

#Ventana para mostrar resultados:
ventana_resultado = scrolledtext.ScrolledText(wrap = tk.WORD,  width = 40,  height = 10, font =("Arial", 12)) 
ventana_resultado.config(state=tk.DISABLED)
ventana_resultado.pack()

# Iniciar la interfaz
ventana.mainloop()