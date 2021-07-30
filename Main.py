#Proyecto FInal
#Gómez Cynthia Noelia

import requests
from datetime import date
from datetime import datetime

#Chequeamos que el código de la billetera virtual sea válido
def check_code(mycode):
    while(not mycode.isdigit() or not (len(mycode) == 4)):
        mycode = input("Ingrese un código válido: ")
    mycode = int(mycode)
    return mycode

_ENDPOINT = "https://api.binance.com"
def _url(api):
    return _ENDPOINT+api

def get_price(cripto):
    return requests.get(_url("/api/v3/ticker/price?symbol="+cripto))

def esmoneda(cripto):
    criptos = ["BTC","BCC","LTC"]
    return cripto in criptos

def esnumero(numero):
    return numero.replace('.','',1).isdigit()

def check_moneda(moneda):
    while not esmoneda(moneda):
        print("Nombre inválido de la moneda.")
        moneda=input("Ingrese el nombre de la moneda: ")
    else:
        cantidad = input("Ingrese la cantidad de monedas "+str(moneda))
        while not esnumero(cantidad):
                cantidad = input(("Indique las cantidad de monedas que posee: "))
        else:
                cantidad = float(cantidad)
    return [moneda, cantidad]

def transaccion(destino, origen):

    if (cantidad > origen):
        print("La cantidad de moneda supera el saldo disponible")
    else:
        destino += cantidad 
        origen -= cantidad 
    return [destino, origen]

def calcular_Saldo(mi_billetera, cotizacion):
    saldo =0.0
   
    for cripto in ["BTC","BCC","LTC"]:
        data =get_price(cripto+"USDT").json()
        cotizacion[cripto] = float(data["price"])
        saldo = cotizacion[cripto]* mi_billetera.get(cripto)
        saldo +=saldo
    
    return saldo

# Pedimos al usuario que ingrese el código de su billetera virtual
mycode = input("Ingrese el código(compuesto por 4 digitos) de su billetera virtual: ")
mycode = check_code(mycode)

#Abre Data_file.txt y lee la información inicial de las billeteras
archivo =open("Data_file.txt", "r")
texto = archivo.read()
archivo.close()
lineas =texto.splitlines()

#armamos dos diccionarios con los datos iniciales del usuario.
usuario_1={} #es la persona que va a hacer la transacción
usuario_2={}
for linea in lineas:
    termino = linea.split(":")
    usuario_1[termino[0]]= float(termino[1])
    usuario_2[termino[0]]= float(termino[2])

mi_billetera ={}
otra_billetera = {}
cotizacion ={}
mi_billetera["Codigo"]= mycode
mi_billetera.update(usuario_1)
otra_billetera.update(usuario_2)
dt = datetime.now()
b = dt.strftime("%A %d/%m/%Y %H:%M:%S")
saldo = calcular_Saldo(mi_billetera, cotizacion)

archivo = open("historial.txt","w")

archivo.write("\n               Historial de transacciones. \n")
archivo.write("---------------------------------------------------\n")
archivo.write("Datos de su billetera: \n")

for key,value in mi_billetera.items():
    archivo.write(key+":"+str(value)+"\n")

archivo.write("                        Cotizaciones en USD\n")
for key,value in cotizacion.items():
    archivo.write(key+":"+str(value)+"\n")
archivo.write("saldo total en UDS: "  +str(saldo)+"\nFecha:")
archivo.write(b)
archivo.write("\n---------------------------------------------------\n")
archivo.close()

print(" Transacciones a realizar:")
print(" 1 - Recibir.")
print(" 2 - Transferir.")
print(" 3 - Mostrar el Balance de una moneda.")
print(" 4 - Mostrar el Balance general de su billetera.")
print(" 5 - Mostrar el historial de transacciones.")
print(" 6 - Salir")
i = int(input("Ingrese el código con la transacción a ajecutar: "))

if(i==1 or i==2 or i==3 or i==4 or i==5 or i==6 ):
    while(i!=6):
        if( i==1 ):
            other_code = input("Ingrese el codigo de la billetera de la cual quiere recibir: ")
            other_code = check_code(other_code)
            if (other_code == mi_billetera["Codigo"]):
                print("Los códigos de billeteras coinciden")
            else:
                otra_billetera["Codigo"]= other_code
                moneda =input("Ingrese el nombre de la moneda que quiere recibir: ")
                [moneda, cantidad] = check_moneda(moneda)
                origen = otra_billetera.get(moneda)
                destino = mi_billetera.get(moneda)
                [destino, origen] = transaccion(destino, origen)
                otra_billetera[moneda] = origen
                mi_billetera[moneda] = destino

                saldo = calcular_Saldo(mi_billetera, cotizacion)
                dt = datetime.now()
                b = dt.strftime("%A %d/%m/%Y %H:%M:%S")

                archivo = open("historial.txt","a")
                archivo.write("Transacción: Recepción \n")
                
                for key,value in mi_billetera.items():
                    archivo.write(key+":"+str(value)+"\n")
                archivo.write("                        Cotizaciones en USD\n")
                for key,value in cotizacion.items():
                    archivo.write(key+":"+str(value)+"\n")
                archivo.write("saldo total en UDS: "  +str(saldo)+"\nFecha:")
                archivo.write(b)
                archivo.write("\n---------------------------------------------------\n")
                archivo.close()
                print("Transacción Realizada")
        elif (i==2):
            other_code = input("Ingrese el codigo de la billetera a la cual quiere transferir: ")
            other_code = check_code(other_code)
            if (other_code == mi_billetera["Codigo"]):
                print("Los códigos de billeteras coinciden")
            else:
                otra_billetera["Codigo"]= other_code
                moneda =input("Ingrese el nombre de la moneda que quiere transferir: ")
                [moneda, cantidad] = check_moneda(moneda)
                destino = otra_billetera.get(moneda)
                origen = mi_billetera.get(moneda)
                [destino, origen]= transaccion(destino, origen)
                otra_billetera[moneda] = destino
                mi_billetera[moneda] = origen
                saldo = calcular_Saldo(mi_billetera, cotizacion)
                dt = datetime.now()
                b = dt.strftime("%A %d/%m/%Y %H:%M:%S")
                
                archivo = open("historial.txt","a")
                archivo.write("Transacción: Transferencia \n")
                for key,value in mi_billetera.items():
                    archivo.write(key+":"+str(value)+"\n")
                archivo.write("                        Cotizaciones en USD\n")
                for key,value in cotizacion.items():
                    archivo.write(key+":"+str(value)+"\n")
                archivo.write("saldo total en UDS: "  +str(saldo)+"\nFecha:")
                archivo.write(b)
                archivo.write("\n---------------------------------------------------\n")
                archivo.close()
                print("Transacción Realizada")

        elif( i==3):
            moneda =input("Ingrese el nombre de la moneda a conocer su balance: ")
            while not esmoneda(moneda):
                print("Nombre inválido de la moneda.")
                moneda=input("Ingrese el nombre de la moneda: ")
            else:
                saldo = calcular_Saldo(mi_billetera, cotizacion)
                dt = datetime.now()
                b = dt.strftime("%A %d/%m/%Y %H:%M:%S")
                print(" Ud cuenta con una cantidad de ", mi_billetera.get(moneda), moneda)
                print( "Cotización actual en USD: ", cotizacion.get(moneda))
                print( "BAlance en USD: ", cotizacion.get(moneda)*mi_billetera.get(moneda))
                print(b)
                print("Transacción Realizada")

        elif( i==4):
            saldo = calcular_Saldo(mi_billetera, cotizacion)
            dt = datetime.now()
            b = dt.strftime("%A %d/%m/%Y %H:%M:%S")
            print("los datos de su billetera son:")
            for key,value in mi_billetera.items():
                print(key+":"+str(value))
            print( "Cotizaciones en USD")
            for key,value in cotizacion.items():
                print(key+":"+str(value))
            print("saldo total en UDS: "  +str(saldo)+"\nFecha:")
            print(b)
            print("---------------------------------------------------")
            print("Transacción Realizada")
        elif(i==5):
             print(" El historial de transacciones se puede visualizar en el archivo historial.txt")
             print("Transacción Realizada")     

        i = int(input("Ingrese el código con la transacción a ajecutar: "))
    else:
        exit   
else:
    i = input("Ingresó una clave de transacción inválida: ")
