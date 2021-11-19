from os import truncate
from tkinter import Tk, StringVar, N, W, E, S, ttk
from tkinter.filedialog import askopenfilename

from clases import maquinaDeTuring

miOffset = 15

def avanzarUnMomento(*args):
    maquina.pasarUnTiempo()

    actualizarTextoCinta()

    actualizarTextoEstado()

    actualizarLabelUltimaAccion()

def avanzarHastaElFinal(*args):
    while(not maquina.ejecucionDetenida):
        maquina.pasarUnTiempo()
        textoCinta.set(maquina.obtenerStringCintaActualConOffset(miOffset))

    actualizarTextoEstado()
    actualizarLabelUltimaAccion()

def actualizarTextoEstado():
    textoEstado.set(maquina.estado())

def actualizarTextoCinta():
    textoCinta.set(maquina.obtenerStringCintaActualConOffset(miOffset))

def actualizarLabelUltimaAccion():
    textoUltimaAccion.set("".join(["ultima acción: ",maquina.ultimaAccion()]))

def seleccionarArchivo(*args):
    direccionArchivoNueva = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print("DEBUG: " + str(direccionArchivoNueva == ""))
    
    if direccionArchivoNueva != "":
        direccionArchivo = direccionArchivoNueva
        
        reiniciarMaquina()

def reiniciarMaquina(*args):
    maquina.ejecucionDetenida = False
    maquina.cargarGrafoListaTrayectorias(direccionArchivo)

    actualizarTextoCinta()
    actualizarTextoEstado()
    actualizarLabelUltimaAccion()

def enfocarRoot(*args):
    if root.focus_get() != root:
        root.focus()


direccionArchivo = '.\configuracion\Maquina1.csv'
maquina = maquinaDeTuring()
maquina.cargarGrafoListaTrayectorias(direccionArchivo)


root = Tk()
root.title("Simulador de máquina de Turing")

##si cambiamos el tamaño de fuente a algo distinto de 20 hay que ajustar el coeficiente
ancho = int((len(maquina.cinta.cinta) + miOffset) * (18.5))

root.geometry("".join([str(ancho),"x",str(300)]))
root.resizable(0,0)


##frame principal donde van las cosas
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

##nuestro label de estado
textoEstado = StringVar()
ttk.Label(mainframe, textvariable=textoEstado, font = ("Lucida Console", 12)).grid(column=0, row=0, sticky=(N, W, E))
textoEstado.set(maquina.estado())

##nuestro label de ultima cosa hecha
textoUltimaAccion = StringVar()
ttk.Label(mainframe, textvariable=textoUltimaAccion, font = ("Lucida Console", 10)).grid(column=0, row=1, sticky=(N, W, E))
actualizarLabelUltimaAccion()

##nuestra label de cinta de la maquina de turing
textoCinta = StringVar()
ttk.Label(mainframe, textvariable=textoCinta, font = ("Lucida Console", 20)).grid(column=0, row=2, sticky=(E))
textoCinta.set(maquina.obtenerStringCintaActualConOffset(miOffset))



##button // evento
ttk.Button(mainframe, text="Avanzar un momento en el tiempo", command=avanzarUnMomento).grid(column=0, row=3, sticky=W)
##button 2//avanzar hasta el final
ttk.Button(mainframe, text="Avanzar hasta el final", command=avanzarHastaElFinal).grid(column=0, row=4, sticky=W)
##button 3//cargar archivo de turing
ttk.Button(mainframe, text="Seleccionar archivo de configuración", command=seleccionarArchivo).grid(column=0, row=5, sticky=W)
##button 4//reiniciar maquina
ttk.Button(mainframe, text="Reiniciar", command=reiniciarMaquina).grid(column=0, row=6, sticky=W)


##polishing
mainframe.columnconfigure(0,weight=0)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.bind("<space>", avanzarUnMomento)
root.bind("<Shift_L><space>",avanzarHastaElFinal)
root.bind("<Button-1>", enfocarRoot)

root.bind("<Shift_L>R",reiniciarMaquina)
root.bind("<Shift_L>r",reiniciarMaquina)

root.mainloop()