import time
import json
import os
from DecodificarDatosRaspberry import datos_sensor
import PySimpleGUI as sg


def leer_datos():
	dic_info = datos_sensor()
	dic_info["fecha"]= time.asctime(time.localtime(time.time()))
	return dic_info


def guardar(info, oficina):
	archivo= open('datos-oficinas.json','r')
	json_datos=json.load(archivo)
	archivo.close()
	json_datos[oficina].append(info)
	objeto = json.dumps(json_datos)
	archivo = open('datos-oficinas.json','w')
	archivo.write(objeto)
	archivo.close()


def opciones():
	archivo = open('datos-oficinas.json','r')
	datos = json.load(archivo)
	archivo.close()
	oficinas = list(datos.keys())
	layout = [
		[sg.Text('Seleccione oficina en la que se encuentra')],
		[sg.Combo(oficinas,key='combo_oficina'),sg.Button('Agregar oficina')],
		[sg.Button('Aceptar')]
	]
	window=sg.Window('Opciones').Layout(layout)
	while True:
		event,values=window.Read()
		if event is None or event == 'Aceptar':
			break
		elif event == 'Agregar oficina':
			ultima_oficina = oficinas[-1][-1]
			nueva_oficina = 'oficina'+ultima_oficina
			datos[nueva_oficina]=[]
			objeto = json.dumps(datos)
			archivo = open('datos-oficinas.json','w')
			archivo.write(objeto)
			archivo.close()
			oficinas.append(nueva_oficina)
			window.FindElement('combo_oficina').update(oficinas)
	window.close()
	return values	    


def main():
	oficina=opciones()
	print(oficina)
	while True:
		time.sleep(60)
		#Cada 1 min. Para probarlo, bajarle la cantidad#
		datos = leer_datos()
		print('Datos leídos')
		guardar(datos,oficina)


if __name__ == "__main__":
	main()

