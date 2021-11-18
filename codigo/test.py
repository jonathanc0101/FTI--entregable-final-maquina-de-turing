from time import sleep
from clases import maquinaDeTuring

def main():

    direccionArchivo = '.\configuracion\Maquina1.csv'
   
    maquinaTuring = maquinaDeTuring()

    maquinaTuring.cargarGrafoListaTrayectorias(direccionArchivo)
    
    maquinaTuring.ejecutarHastaFinalConsola()
    
if __name__ == "__main__":
    main()
