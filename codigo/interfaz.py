
from tkinter import Message, Tk, StringVar, N, W, E, S, ttk, Toplevel, Label, messagebox
from tkinter.constants import LEFT
from tkinter.filedialog import askopenfilename
    
from pathlib import Path
from os import getcwd

from codigo.clases import maquinaDeTuring

miOffset = 15
ubicacionIcono = Path('icono/original.ico')


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class interfazSimulador:

    def __init__(self) -> None:
        
        self.direccionArchivo =  Path("configuracion/MaquinaEjemplo.csv")
        
        self.maquina = maquinaDeTuring()
        self.maquina.cargarGrafoListaTrayectorias(self.direccionArchivo)
        
        self.inicializarInterfaz()

        self.inicializarBindEventos()

        self.aniadirTooltips()
        
        self.iniciarLoop()

    def iniciarLoop(self):
        self.root.mainloop()
        
    def inicializarInterfaz(self):
        self.root = Tk()
        self.root.title("Simulador de máquina de Turing")
        
        #colocamos icono
        self.root.iconbitmap(ubicacionIcono)    

        ##si cambiamos el tamaño de fuente a algo distinto de 20 hay que ajustar el coeficiente
        ancho = int((len(self.maquina.cinta.cinta) + miOffset) * (18.5))

        self.root.geometry("".join([str(ancho),"x",str(340)]))
        self.root.resizable(0,0)

        ##frame principal donde van las cosas
        self.mainframe = ttk.Frame(self.root, padding="12 12 12 12")
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

        ##nuestro label de posición cabezal
        self.textoPosicionCabezal = StringVar()
        ttk.Label(self.mainframe,textvar = self.textoPosicionCabezal , font = ("Lucida Console", 10)).grid(column=0, row=2, sticky =(N, W, E))
        self.actualizarLabelPosicionCabezal()

        ##nuestro label de alfabeto
        self.textoAlfabeto = StringVar()
        ttk.Label(self.mainframe,textvar = self.textoAlfabeto, font = ("Lucida Console", 10)).grid(column=0, row=3, sticky =(N,W,E,S))
        self.actualizarLabelAlfabeto()

        ##nuestra label de cinta de la maquina de turing
        self.textoCinta = StringVar()
        ttk.Label(self.mainframe, textvariable=self.textoCinta, font = ("Lucida Console", 20)).grid(column=1, row=3, sticky=(W,E), columnspan=1)
        self.actualizarTextoCinta()
        

        ##button // avanzar un momento
        self.botonAvanzar = ttk.Button(self.mainframe, text="Avanzar un momento en el tiempo", command=self.avanzarUnMomento)
        self.botonAvanzar.grid(column=0, row=4, sticky=(N, S, W, E), columnspan=1)
        
        ##button 2//avanzar hasta el final
        self.botonAvanzarCienPasos =ttk.Button(self.mainframe, text="Avanzar cien pasos", command=self.AvanzarCienPasos)
        self.botonAvanzarCienPasos.grid(column=0, row=5, sticky=(N, S, W, E), columnspan=1)
        
        ##button 3//cargar archivo de turing
        self.botonSeleccionarArchivo = ttk.Button(self.mainframe, text="Seleccionar archivo de configuración", command=self.seleccionarArchivo)
        self.botonSeleccionarArchivo.grid(column=0, row=6, sticky=(N, S, W, E), columnspan=1)
        
        ##button 4//reiniciar maquina
        self.botonReiniciar = ttk.Button(self.mainframe, text="Reiniciar", command=self.reiniciarMaquina)
        self.botonReiniciar.grid(column=0, row=7, sticky=(N, S, W, E), columnspan=1)
        
        ##button 5//generar cinta aleatoria
        self.botonCintaAleatoria = ttk.Button(self.mainframe,text = "Generar cinta random", command=self.generarCintaRandom)
        self.botonCintaAleatoria.grid(column=0, row=8, sticky=(N, S, W, E), columnspan=1)


        ##polishing
        self.mainframe.columnconfigure(0,weight=0)

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def inicializarBindEventos(self):
        self.root.bind("<space>", self.avanzarUnMomento)
        self.root.bind("<Shift_L><space>",self.AvanzarCienPasos)
        self.root.bind("<Button-1>", self.enfocarRoot)

        self.root.bind("<Shift_L>R",self.reiniciarMaquina)
        self.root.bind("<Shift_L>r",self.reiniciarMaquina)

    def avanzarUnMomento(self,*args):
        self.maquina.pasarUnTiempo()

        self.actualizarMaquina()

    def AvanzarCienPasos(self,*args):
        for i in range(100):
            ejecucionFinalizada = self.maquina.ejecucionDetenida
            if (not ejecucionFinalizada):
                self.maquina.pasarUnTiempo()
    
        self.actualizarMaquina()

        if ejecucionFinalizada:
            messagebox.showinfo(title="Máquina de Turing", message="Ejecución finalizada")


    def actualizarMaquina(self):
        self.actualizarTextoCinta()

        self.actualizarTextoEstado()

        self.actualizarLabelUltimaAccion()
        
        self.actualizarLabelAlfabeto()
        
        self.actualizarLabelPosicionCabezal()
        
    def actualizarTextoEstado(self):
        self.textoEstado.set(self.maquina.estado())

    def actualizarTextoCinta(self):
        self.textoCinta.set(self.maquina.obtenerStringCintaActualConOffset(miOffset))

    def actualizarLabelUltimaAccion(self):
        self.textoUltimaAccion.set("".join(["ultima acción: ",self.maquina.ultimaAccion()]))

    def actualizarLabelAlfabeto(self):
        self.textoAlfabeto.set("".join([ "Alfabeto: " ,str(self.maquina.alfabeto())]))
    
    def actualizarLabelPosicionCabezal(self):
        self.textoPosicionCabezal.set("".join([ "posición: " ,str(self.maquina.posicionCabezal())]))

    def seleccionarArchivo(self,*args):
        filetypes = (
        ('Archivos csv', '*.csv'),
        ('Todos los archivos', '*.*')
        )

        # ('archivos csv', 'csv',)
        direccionArchivoNueva = askopenfilename(initialdir= Path("configuracion"), title = "seleccionar archivo de configuración", filetypes = filetypes)  

        if direccionArchivoNueva != "":
            self.direccionArchivo = direccionArchivoNueva
            self.reiniciarMaquina()
        
        self.actualizarMaquina()

    def reiniciarMaquina(self,*args):
        self.maquina = None
        self.maquina = maquinaDeTuring()

        self.maquina.cargarGrafoListaTrayectorias(self.direccionArchivo)

        self.actualizarTextoCinta()
        self.actualizarTextoEstado()
        self.actualizarLabelUltimaAccion()
    
    def generarCintaRandom(self, *args):
        self.maquina.generarCintaRandom()
        self.actualizarMaquina()
    
    def enfocarRoot(self,*args):
        if self.root.focus_get() != self.root:
            self.root.focus()

    def aniadirTooltips(self, wrapLengthVar=200):
        CreateToolTip(self.botonAvanzar, "Espacio")
        CreateToolTip(self.botonAvanzarCienPasos, "Shift + Espacio")

        CreateToolTip(self.botonReiniciar, "Shift + R")


