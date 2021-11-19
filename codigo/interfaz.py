
from tkinter import Tk, StringVar, N, W, E, S, ttk
from tkinter.filedialog import askopenfilename

from clases import maquinaDeTuring

miOffset = 15

class interfazSimulador:

    def __init__(self) -> None:
        
        self.direccionArchivo = '.\configuracion\Maquina1.csv'
        
        self.maquina = maquinaDeTuring()
        self.maquina.cargarGrafoListaTrayectorias(self.direccionArchivo)
        
        self.inicializarInterfaz()

        self.inicializarBindEventos()

        self.root.mainloop()

    def inicializarInterfaz(self):
        self.root = Tk()
        self.root.title("Simulador de máquina de Turing")
        
        ##si cambiamos el tamaño de fuente a algo distinto de 20 hay que ajustar el coeficiente
        ancho = int((len(self.maquina.cinta.cinta) + miOffset) * (18.5))

        self.root.geometry("".join([str(ancho),"x",str(300)]))
        self.root.resizable(0,0)

        ##frame principal donde van las cosas
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ##nuestro label de estado
        self.textoEstado = StringVar()
        ttk.Label(self.mainframe, textvariable=self.textoEstado, font = ("Lucida Console", 12)).grid(column=0, row=0, sticky=(N, W, E))
        self.textoEstado.set(self.maquina.estado())

        ##nuestro label de ultima cosa hecha
        self.textoUltimaAccion = StringVar()
        ttk.Label(self.mainframe, textvariable=self.textoUltimaAccion, font = ("Lucida Console", 10)).grid(column=0, row=1, sticky=(N, W, E))
        self.actualizarLabelUltimaAccion()

        ##nuestra label de cinta de la maquina de turing
        self.textoCinta = StringVar()
        ttk.Label(self.mainframe, textvariable=self.textoCinta, font = ("Lucida Console", 20)).grid(column=0, row=2, sticky=(E))
        self.textoCinta.set(self.maquina.obtenerStringCintaActualConOffset(miOffset))


        ##button // evento
        ttk.Button(self.mainframe, text="Avanzar un momento en el tiempo", command=self.avanzarUnMomento).grid(column=0, row=3, sticky=W)
        ##button 2//avanzar hasta el final
        ttk.Button(self.mainframe, text="Avanzar hasta el final", command=self.avanzarHastaElFinal).grid(column=0, row=4, sticky=W)
        ##button 3//cargar archivo de turing
        ttk.Button(self.mainframe, text="Seleccionar archivo de configuración", command=self.seleccionarArchivo).grid(column=0, row=5, sticky=W)
        ##button 4//reiniciar maquina
        ttk.Button(self.mainframe, text="Reiniciar", command=self.reiniciarMaquina).grid(column=0, row=6, sticky=W)

        ##polishing
        self.mainframe.columnconfigure(0,weight=0)

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def inicializarBindEventos(self):
        self.root.bind("<space>", self.avanzarUnMomento)
        self.root.bind("<Shift_L><space>",self.avanzarHastaElFinal)
        self.root.bind("<Button-1>", self.enfocarRoot)

        self.root.bind("<Shift_L>R",self.reiniciarMaquina)
        self.root.bind("<Shift_L>r",self.reiniciarMaquina)

    def avanzarUnMomento(self,*args):
        self.maquina.pasarUnTiempo()

        self.actualizarTextoCinta()

        self.actualizarTextoEstado()

        self.actualizarLabelUltimaAccion()

    def avanzarHastaElFinal(self,*args):
        while(not self.maquina.ejecucionDetenida):
            self.maquina.pasarUnTiempo()
            self.textoCinta.set(self.maquina.obtenerStringCintaActualConOffset(miOffset))

        self.actualizarTextoEstado()
        self.actualizarLabelUltimaAccion()

    def actualizarTextoEstado(self):
        self.textoEstado.set(self.maquina.estado())

    def actualizarTextoCinta(self):
        self.textoCinta.set(self.maquina.obtenerStringCintaActualConOffset(miOffset))

    def actualizarLabelUltimaAccion(self):
        self.textoUltimaAccion.set("".join(["ultima acción: ",self.maquina.ultimaAccion()]))

    def seleccionarArchivo(self,*args):
        direccionArchivoNueva = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        # print("DEBUG: " + str(direccionArchivoNueva == ""))
        # print("DEBUG: " + direccionArchivoNueva)

        if direccionArchivoNueva != "":
            self.direccionArchivo = direccionArchivoNueva
            self.reiniciarMaquina()
            # print("DEBUG: reiniciando maquina")
            
    # maquina.cargarGrafoListaTrayectorias(
    def reiniciarMaquina(self,*args):
        self.maquina = None
        self.maquina = maquinaDeTuring()

        self.maquina.cargarGrafoListaTrayectorias(self.direccionArchivo)

        self.actualizarTextoCinta()
        self.actualizarTextoEstado()
        self.actualizarLabelUltimaAccion()
        
    def enfocarRoot(self,*args):
        if self.root.focus_get() != self.root:
            self.root.focus()

def main():
    ventana = interfazSimulador()

main()
