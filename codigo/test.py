from time import sleep
from clases import caracteresEspeciales, GrafoTuring, CintayCabezal, maquinaDeTuring

def main():

    chars = caracteresEspeciales()
    grafo = GrafoTuring()

    # inicializacion de la cinta 
    universo = ["a", "b", "c", "*"]
    pos = 0
    cinta = "abababcbcbca*b*ababababb*"
    MiCintaYCabezal = CintayCabezal(universo,cinta,pos)

    ##inicializamos el grafo
    grafo.insertar(1,2,chars.lambd,"S*")
    grafo.insertar(2,3,chars.lambd,"R")
    grafo.insertar(3,2,"!" + chars.delta, "D")
    grafo.insertar(3,4,chars.delta, chars.lambd)
    grafo.insertar(4,5,chars.lambd, "L")
    grafo.insertar(5,4,"!*", chars.lambd)
    grafo.insertar(5,6,"*","D")
    grafo.insertar(6,7,chars.lambd,"END")

    grafo.settearNodoInicial(1)

    maquinaTuring = maquinaDeTuring(grafo,MiCintaYCabezal)
    while not maquinaTuring.ejecucionDetenida :
        maquinaTuring.cinta.imprimirCintaYCabezal()
        maquinaTuring.pasarUnTiempo()
        sleep(0.1)


if __name__ == "__main__":
    main()
