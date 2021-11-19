import time
from csv import reader
from tkinter import Misc

class caracteresEspeciales():
    """permite un facil acceso a los caracteres especiales usados en la teoria de la computación."""
    def __init__(self) -> None:
        self.lambd ='λ'
        self.delta = 'Δ'

class CintayCabezal:
    """modela una cinta y el cabezal de la maquina de Turing"""
    
    def __init__(self, universoDeSimbolos = None, cinta = None, pos = None) -> None:
        self.chars = caracteresEspeciales()

        self.universoDeSimbolos = universoDeSimbolos
        self.cinta = cinta
        self.pos = pos ##nos indica la posicion del cabezal

        self.ejecucionDetenida = False
        self.accionAnterior = ""

    def comprobarInicializacion(self):
        assert(self.universoDeSimbolos is not None), "CintayCabezal: no hay self.universoDeSimbolos"
        assert(self.pos is not None), "CintayCabezal: no hay self.pos"
        assert(self.cinta is not None), "CintayCabezal: no hay self.cinta"

    def siguiente(self):
        self.comprobarInicializacion()
    
        self.pos += 1

        """la cinta es infinita"""
        if self.pos == len(self.cinta):
            self.cinta = "".join([self.cinta, self.chars.delta])

        # print("DEBUG: pos: " + str(self.pos) + "len: " + str(len(self.cinta)))
    def anterior(self):
        self.comprobarInicializacion()

        self.pos -= 1

        """la cinta es infinita"""
        if self.pos == -1:
            self.cinta = "".join([self.chars.delta, self.cinta])
            self.pos = 0


    def actual(self) -> chr:
        self.comprobarInicializacion()

        return self.cinta[self.pos]
    
    def escribir(self, simbolo):
        self.comprobarInicializacion()

        if (simbolo not in self.universoDeSimbolos) and (simbolo != self.chars.delta):
            raise Exception("el simbolo a escribir no está en el universo de simbolos y no es delta")
        else:
            # print("DEBUG: escribir, pos = " + str(self.pos) + " simbolo = " + simbolo) 

            cintaIzquierda = self.cinta[:self.pos]
            cintaDerecha = self.cinta[self.pos + 1:]

            if (self.pos == len(self.cinta) - 1) and (self.pos != 0):
                self.cinta = "".join([cintaIzquierda, simbolo])

            elif self.pos == 0:
                self.cinta = "".join([simbolo, cintaDerecha])

            elif 0 < self.pos < len(self.cinta):
                self.cinta = "".join([cintaIzquierda, simbolo, cintaDerecha])
            
    def borrar(self):
        # print("DEBUG: borrando simbolo: " + self.cinta[self.pos])        
        self.escribir(self.chars.delta)

    def ejecutarSecuenciaDeInstrucciones(self, secuencia):
        for instruccion in secuencia:
            self.ejecutarInstruccion(instruccion)

    def ejecutarInstruccion(self, instruccion):
        if not self.ejecucionDetenida:
            self.accionAnterior = instruccion

        """ejecuta la instrucción recibida"""
        if instruccion == "R":
            # print("DEBUG: R")
            self.siguiente()
        elif instruccion[0] == "R" and len(instruccion) > 1 and instruccion != "R" + self.chars.delta:
            posibleSimbolo = instruccion[1:]
            
            self.siguiente()
            simboloActual = self.actual()

            if posibleSimbolo[0] != "!":
                simboloBuscado = posibleSimbolo
               
                ##vamos un lugar a la derecha y despues preguntamos si es igual
                while simboloActual != simboloBuscado and (self.pos < (len(self.cinta))):
                    self.siguiente()
                    simboloActual = self.actual()
                
                ##en caso de que lleguemos al final
                if (self.pos == (len(self.cinta) - 1)) and self.actual() != simboloBuscado:

                    if simboloBuscado != self.chars.delta:
                        #nunca vamos a encontrar el simbolo
                        self.ejecucionDetenida = True
                        self.levantarExcepcionBucle()
                    
                    else:
                        self.siguiente()
            else:

                simboloNoBuscado = posibleSimbolo[1:]
                while simboloActual == simboloNoBuscado and self.pos != (len(self.cinta) - 1):
                    self.siguiente()
                    simboloActual = self.actual


                ##en caso de que lleguemos al final
                if (self.pos == (len(self.cinta) - 1)) and self.actual == simboloNoBuscado:
            
                    if simboloNoBuscado == self.chars.delta:
                        #nunca vamos a dejar de encontrar el simbolo delta
                        self.ejecucionDetenida = True
                        self.levantarExcepcionBucle()
                    else:
                        self.siguiente()
        
        elif instruccion == "L":
            self.anterior()
        
        elif instruccion[0] == "L" and len(instruccion) > 1 and instruccion != "L" + self.chars.delta:
            posibleSimbolo = instruccion[1:]
            
            self.anterior()
            simboloActual = self.actual()

            if posibleSimbolo[0] != "!":
                simboloBuscado = posibleSimbolo

                ##vamos un lugar a la izquierda y despues preguntamos si es igual
                while simboloActual != simboloBuscado and self.pos > 0:
                    self.anterior()
                    simboloActual = self.actual()
                
                if self.pos == 0 and self.actual() != simboloBuscado:

                    if simboloBuscado != self.chars.delta:
                        #nunca vamos a encontrar el simbolo
                        self.ejecucionDetenida = True
                        self.levantarExcepcionBucle()
            
                    else:
                        self.anterior()

            else:
                simboloNoBuscado = posibleSimbolo[1:]
                while simboloActual == simboloNoBuscado and self.pos > 0:
                    self.anterior()
                    simboloActual = self.actual()

                if self.pos == 0 and self.actual() == simboloNoBuscado:
                
                    if simboloNoBuscado == self.chars.delta:
                        #nunca vamos a dejar de encontrar el delta mas hacia la izquierda
                        self.ejecucionDetenida = True
                        self.levantarExcepcionBucle()

                    else:
                        self.anterior()                       
        
        elif instruccion[0] == "S" and len(instruccion) > 1:
            simbolo = instruccion[1:]
            self.escribir(simbolo)

        elif instruccion[0] == "D": 
            self.borrar()

        elif instruccion == self.chars.lambd:
            pass ##no hacemos nada

        #casos especiales de Lsimbolo y Rsimbolo
        elif instruccion == "R" + self.chars.delta:
            ##vamos manualmente hasta el final
            self.pos = len(self.cinta) - 1
            self.siguiente()

        elif instruccion == "L" + self.chars.delta:
            ##vamos manualmente hasta el principio
            self.pos = 0
            self.anterior()
        
        elif instruccion == "END":        #aceptamos
            self.ejecucionDetenida = True
            print("El programa ha finalizado con éxito.")
        
        else:
            raise Exception("Error: instrucción no soportada - Clase: cintaYCabezal")

    def levantarExcepcionBucle(self):
        raise Exception("Error: No es posible seguir con la ejecución del programa dada la detección de un bucle infinito.")

    def imprimirCintaYCabezal(self):
        print("".join([self.pos*' ', "▾"]))
        print(self.cinta)

    def __str__(self) -> str:
        miStr = "".join([self.pos*' ', "▾", "\n", self.cinta])
        return(miStr)

    def stringRecortado(self,offset) -> str:
        """retorna la cinta y el cabezal dado un offset"""
        miStr = str(self.cinta)
        posActual = self.pos

        izquierda = 0
        derecha = len(miStr)

        if not(posActual - offset < 0):
            izquierda = posActual - offset 
        if not(posActual + offset > len(miStr) - 1):
            dereha = posActual + offset

        if posActual < offset:
            espaciosAntesDeCinta = offset - posActual
        else:
            espaciosAntesDeCinta = 0

        miStr = "".join([offset*' ', "▾", "\n", ' '*espaciosAntesDeCinta,miStr[izquierda:derecha]])
        
        return miStr

    def ultimaAccion(self):

        if self.accionAnterior == "" or self.accionAnterior is None:
            return ""

        if self.accionAnterior in ["L", "R"] or self.accionAnterior[0] in ["L", "R"]:
            return self.accionAnterior
        elif self.accionAnterior == "D":
            return self.chars.delta
        elif self.accionAnterior == self.chars.lambd:
            return ""
        elif self.accionAnterior == "END":
            return self.accionAnterior
        else:
            return ""

class GrafoTuring:
    """modela la clase grafo con el uso de listas de
    adyacencia"""
    
    def __init__(self):
        """inicializa el grafo, recibe como parametro un boolean que nos
        indica si es dirigido o no"""
        self.listaDeVertices = {}
        self.numArcos = 0
        self.nodoActual = None

    def settearNodoInicial(self, nodo):
        self.nodoActual = nodo
    
    def numVertices(self):
        return len(self.listaDeVertices)

    def vertices(self):
        """retorna el diccionario que representa la lista de vertices"""
        return self.listaDeVertices

    def numArcos(self):
        return self.numArcos

    def insertar(self, x, z, simbolo, accion):
        """inserta la conexion entre x y z dentro del grafo, x y z
        siendo x el origen y z el destino"""

        if x not in self.listaDeVertices:
            self.listaDeVertices[x] = []

        if z not in self.listaDeVertices:
            self.listaDeVertices[z] = []           

        self.listaDeVertices[x].append([z, simbolo, accion])
        
        self.numArcos += 1

    """vamos con la parte de turing"""
    def accionSiguiente(self,simbolo)->str:
        """a partir de un simbolo retorna la accion siguiente a efectuar en la cinta y nos mueve al siguiente nodo posible del grafo"""

        chars = caracteresEspeciales()

        trayectoriasPosibles = self.listaDeVertices[self.nodoActual]
        
        simbolosEnTrayectoriasPosibles = [trayectoria[1] for trayectoria in trayectoriasPosibles]

        if chars.lambd in simbolosEnTrayectoriasPosibles:
            #hay que hacer primero las trayectorias que no requieren simbolos para concretarse
            for trayectoria in trayectoriasPosibles:
                if trayectoria[1] == chars.lambd:
                    self.nodoActual = trayectoria[0]
                    return trayectoria[2]

        #si llegamos hasta acá es porque no hay trayectorias obligatorias

        #comprobamos primero la trayectoria negada
        
        listaAuxiliar = [x[0] for x in simbolosEnTrayectoriasPosibles]
                
        
        if "!" in listaAuxiliar:
            
            indice = listaAuxiliar.index("!")
            simboloEncontrado = simbolosEnTrayectoriasPosibles[indice]
    
            # print("DEBUG: " + simboloEncontrado)
    
            simboloNegado = simboloEncontrado[1:]
    
            # print("DEBUG: " + simboloNegado)

            if simbolo != simboloNegado:
                # print("DEBUG: Simbolo: " + simbolo + " Negado: " + simboloNegado)
                trayectoria = trayectoriasPosibles[indice]
                self.nodoActual = trayectoria[0]
                                
                return trayectoria[2]

        # print("DEBUG: Simbolo: " + simbolo + "Trayectorias posibles:  " + str(trayectoriasPosibles))

        if simbolo in simbolosEnTrayectoriasPosibles:
            for trayectoria in trayectoriasPosibles:
                if trayectoria[1] == simbolo:
                    self.nodoActual = trayectoria[0]
                    return trayectoria[2]
        else:
            raise Exception("Error: Error del programa, no se puede seguir la ejecución de la máquina de Turing, no hay salidas del nodo con el símbolo indicado, Salidas: " + str(trayectoriasPosibles))

    def imprimir(self):
        for vertice in self.listaDeVertices:
            print(vertice, end = "  ")
            arco = self.listaDeVertices[vertice]
            if arco != None:
                print("->", end = "  ")
                print(*arco)
            else:
                print(" ")
        
        print("nodo actual: " + str(self.nodoActual))

    def __str__(self):
        return "G = ("+str(self.numVertices())+" V, "+str(self.numArcos)+" A)"
       
class maquinaDeTuring:
    def __init__(self, grafo = None, cinta = None) -> None:
        self.grafo = grafo
        self.cinta = cinta

        self.ejecucionDetenida = False

    def comprobarInicializacion(self):
        assert(self.grafo is not None), "maquinaDeTuring: no hay self.grafo"
        assert(self.cinta is not None), "maquinaDeTuring: no hay self.cinta"

    def pasarUnTiempo(self):
        
        if not self.ejecucionDetenida:
            simboloActual = self.cinta.actual()
            instruccionActual = self.grafo.accionSiguiente(simboloActual)
            self.cinta.ejecutarInstruccion(instruccionActual)

            self.ejecucionDetenida = self.cinta.ejecucionDetenida
        
        else:
            print("Ejecución detenida")

        if not self.ejecucionDetenida and not self.cinta is None:
            if self.cinta.ultimaAccion() == "":
                self.pasarUnTiempo()

    def pasarNTiempos(self, n):
        
        i = 0
        while i <= n and not self.ejecucionDetenida:
            
            self.pasarUnTiempo()
            
            i += 1

    def ejecutarHastaFinalConsola(self):
        while not self.ejecucionDetenida :
            self.cinta.imprimirCintaYCabezal()
            self.pasarUnTiempo()
            time.sleep(0.1)

    def cargarGrafoListaTrayectorias(self, filename):
        """Carga un grafo a partir de un archivo csv que contiene una lista de trayectorias"""
        cinta = CintayCabezal()
        grafo = GrafoTuring()

        rows = []

        with open(filename, 'r') as csvfile:
            # creating a csv reader object
            csvreader = reader(csvfile, delimiter = ';', lineterminator = ";;;")
            
            # extracting each data row one by one
            rows = [row for row in csvreader]
    
        alfabeto = rows[1]
        textoCinta = rows[3][0]
        posCabezal = int(rows[5][0])
        transiciones = rows[8:]

        ##cargamos la cinta
        cinta.universoDeSimbolos = alfabeto
        cinta.cinta = textoCinta 
        cinta.pos = posCabezal

        #grafo
        for transicion in transiciones:
            for i in range (len(transicion)):
                # csv no soporta los simbolos delta ni lambda
                transicion[i] = transicion[i].replace("delta", caracteresEspeciales().delta)
                transicion[i] = transicion[i].replace("lambda", caracteresEspeciales().lambd)
                # print("DEBUG: " + str(transicion[i]))
            transicion[0] = int(transicion[0])
            transicion[1] = int(transicion[1])

            ##si no es una accion elemental es un simbolo
            simbolosYAccionesPosibles = ["R", "L", "D", caracteresEspeciales().lambd]
            if transicion[3][0] not in simbolosYAccionesPosibles and transicion[3] != "END":
                transicion[3] = "".join(["S", transicion[3]])

            # print("DEBUG: transicion: "+ str(transicion))            
            grafo.insertar(*(transicion[0:4]))
        
        grafo.settearNodoInicial(1)
        
        self.cinta = cinta
        self.grafo = grafo

    def obtenerStringCintaActualConOffset(self, offset):
        return self.cinta.stringRecortado(offset)

    def estado(self) -> str:
        if self.ejecucionDetenida:
            return "Programa detenido"
        else:
            return "Ejecutando programa"

    def ultimaAccion(self):
        if not self.cinta is None:
            return self.cinta.ultimaAccion()
        else:
            return ""

