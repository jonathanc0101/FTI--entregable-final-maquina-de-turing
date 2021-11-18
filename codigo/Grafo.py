##definicion del tipo grafo

class Nodo:
    """modela un nodo, con un dato x y un enlace al siguiente nodo"""
    def __init__(self, x = None, prox = None):
        """inicializa un nodo, si se provee el enlace al siguiente
        elemento entonce se enlaza, sino el valor de proximo es None"""
        self.dato = x
        self.prox= prox
        
    def __str__(self):
        return str(self.dato)

    def contenido(self):
        """retorna el contenido del nodo"""
        return self.dato


class Grafo:
    """modela la clase grafo, ponderado o no, con el uso de listas de
    adyacencia"""
    
    def __init__(self, es_dirigido = False):
        """inicializa el grafo, recibe como parametro un boolean que nos
        indica si es dirigido o no"""
        self.lista_vertices = {}
        self.n_arcos = 0
        self.es_dirigido = es_dirigido

       
    def __str__(self):
        return "G = ("+str(self.n_vertices())+" V, "+str(self.n_arcos)+" A)"

    def n_vertices(self):
        return len(self.lista_vertices)

    def dirigido(self):
        return self.es_dirigido

    def vertices(self):
        """retorna el diccionario que representa la lista de vertices"""
        return self.lista_vertices

    def num_arcos(self):
        return self.n_arcos

    def insertar(self, x, z = None):
        """inserta la conexion entre x y z dentro del grafo, x y z
        siendo x el origen y z el destino"""

        ##nos fijamos si x y z estan en la lista de vertices
        ##si no estan los añadimos como dos listas donde
        ##vamos a guardar sus adyacentes
        if x not in self.lista_vertices:
            self.lista_vertices[x] = []
        if z != None:
            ##si no hay z no hacemos todo esto
            if z not in self.lista_vertices:
                self.lista_vertices[z] = []           


            nw = Nodo(z, self.lista_vertices[x])
            self.lista_vertices[x].append(nw)

            self.n_arcos += 1
            
            if self.es_dirigido == False and z != x:
                ##no tolera enlaces a si mismo(bucles)
                nw = Nodo(x, self.lista_vertices[z])
                self.lista_vertices[z].append(nw)

    def imprimir(self):
        for vertice in self.lista_vertices:
            print(vertice, end = "  ")
            arco = self.lista_vertices[vertice]
            if arco != None:
                print("->", end = "  ")
            ##  preguntar por el metodo imprimeLista
                ##arco.imprimeLista()
                print(*arco)
                ##simplemente lo reemplace por un print
                ##con la lista desempaquetada
            else:
                print(" ")

    def dirigido(self):
        return self.es_dirigido








