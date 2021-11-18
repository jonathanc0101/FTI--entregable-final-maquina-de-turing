import csv



def imprimirCSV(filename = '.\configuracion\Maquina1.csv'):

    rows = []

    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile, delimiter = ';', lineterminator = ";;;")
        
        # extracting each data row one by one
        rows = [row for row in csvreader]

        print(rows)

imprimirCSV()