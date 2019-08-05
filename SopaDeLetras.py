import sys
from math import sqrt, ceil
from random import randrange, shuffle,choice
from pattern.web import Wiktionary
from pattern.es import verbs, tag, spelling, lexicon
import string
import json
from os import listdir,getcwd
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg


def LookAndFeel():
    """

    Se utilizan los datos del archivo 'datos-oficina' para calcular el promedio de temperatura a partir de los daots obtenidos
    de la raspberry. A partir de este promedio se selecciona un look and feel que se retorna como valor para una variable
    """
    tot = 0
    cant = 0
    layoutT = [
        [sg.Text('¿En que oficina se encuentra?')],
        [sg.InputText(key='ofi')],
        [sg.Button('Aceptar')]
    ]
    windowT = sg.Window('seleccion de oficina').Layout(layoutT)
    events,val = windowT.Read()
    if events =='Aceptar':
        try:
          arch = open('datos-oficinas.json','r')
        except IOError:
          windowT.Close()
          sg.Popup('El archivo JSON datos-oficinas.json no existe o no tiene permisos para abrirlo.\n' + 'Se utilizará un tema por defecto')
          return 'Topanga'
        datos = json.load(arch)
        arch.close()
        print(datos)
        windowT.Close()
        if val['ofi'] in datos.keys():
            k = val['ofi']
            for elem in datos[k]:
              tot += elem['temp']
              cant += 1
            prom = tot/cant
            if prom > 25:
                return 'Reds'
            elif prom < 15:
                return 'NeutralBlue'
            else:
                return 'SandyBeach'
        else:
            sg.Popup("La oficina no existe en el archivo JSON, se utilizará un tema por defecto")
            return 'Topanga'


def totalCaracteres(lista):
    """
    Representamos palabras con strings y su largo con Ints
    totalCaracteres : List(Str) -> Int
    totalCaracteres recibe una lista de palabras y devuelve la suma total de todos sus caracteres
    Ejemplos:
    totalCaracteres(["Perro","gato","cobayo"]) => 15
    totalCaracteres([]) => 0
    """
    sum = 0
    for i in lista:
        sum += len(i)
    return sum


def largoPalabraMasLarga(lista):
    """
    Representamos palabras con strings y su largo con Ints
    largoPalabraMasLarga : List(Str) -> Int
    largoPalabraMasLarga recibe una lista de palabras, devuelve el largo de la palabra mas larga
    Ejemplos:
    largoPalabraMasLarga(["Perro","gato","Encefalograma"]) => 13
    largoPalabraMasLarga([]) => 0
    """
    largo = 0
    for i in lista:
        if len(i) > largo:
            largo = len(i)
    return largo


def rellenarTablero(tablero,ABECEDARIO,v):
    """
    Se utilizan letras de la constante ABECEDARIO
    rellenarTablero : List(List(Str | Int)) -> List(List(Str))
    rellenarTablero recibe un tablero de Sopa de letras incompleto y llena los espacios vacios (0) con letras al azar del ABECEDARIO
    """
    Nfilas = len(tablero)
    Ncolumnas = len(tablero[0])
    for y in range(Nfilas):
        for x in range(Ncolumnas):
            if tablero[y][x] == 0:
                posletra = randrange(len(ABECEDARIO))
                letra = ABECEDARIO[posletra]
                #tablero[y][x] = letra
                if v['mayus']:
                    tablero[y][x] = letra.upper()
                else:
                    tablero[y][x] = letra.lower()
    return tablero,Nfilas,Ncolumnas


def palabraIncluida(palabra, lista):
    """
    Representamos una palabra con un string
    palabraIncluida : List(Str) List(List(Str)) -> Bool
    palabraIncluida recibe una palabra y una lista de palabras, devuelve True si la palabra (o su inversa) se encuentra en la lista o incluida dentro de otra palabra
    Ejemplos:
    palabraIncluida("ola",["arena","mar","ola","playa"]) => True
    palabraIncluida("no",["yo","tu","el","nosotros","vosotros","ellos"]) => True
    palabraIncluida("True",[]) => False
    palabraIncluida("comer",["fisurar","remocar","limpiar"]) => True
    """
    for i in lista:
        if palabra in i:
            return True
        return False


def eliminaIncluidos(lista):
    """
    Representamos palabras con Strings
    eliminaIncluidos : List(Str) -> List(Str)
    eliminaIncluidos recibe una lista de palabras (solo strings)
    Devuelve la lista sin las palabras repetidas o que se incluyen dentro de otras
    Ejemplos:
    eliminaIncluidos(["ola","arena","mar","ola","hola","playa"]) => ["arena","mar","hola","playa"]
    eliminaIncluidos(["comer","fisurar","remocar","limpiar"]) => ["fisurar","remocar","limpiar"]
    eliminaIncluidos(["chau","tirar","saludar"]) => ["chau","tirar","saludar"]
    """
    for palabra in lista:
        i = lista.index(palabra)
        resto = lista[:i] + lista[i + 1:]
        if palabraIncluida(palabra, resto):
            lista = resto
    return lista


def generaTablero(n):
    """
    generaTablero : Int -> List(List(Int))
    generaTablero recibe un numero natural N, devuelve una matriz de NxN con todos sus elementos 0
    Ejemplos:
    generaTablero(3) => [[0,0,0],[0,0,0],[0,0,0]]
    generaTablero(1) => [[0]]
    generaTablero(4) => [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    """
    tablero = [[0 for x in range(n)] for i in range(n)]
    return tablero


def generaListaPalabras():
    lista = []
    n = int(input("Ingrese la cantidad total de palabras: "))
    contador = 1
    while contador <= n:
        palabra = input("Ingrese la palabra n°" + str(contador) + ": ")
        lista += [palabra]
        contador += 1
    for i in lista:
        p = lista.index(i)
        lista[p] = i
    return lista


def faltaPoner(palabras):
    """
    faltaPoner : List(Str) | List(List(Str | Tuple(Int))) -> Bool
    faltaPoner recibe una lista palabras y devuelve True si aun quedan palabras por colocar
    (si en la lista principal hay strings)
    Ejemplos:
    faltaPoner(["PERRO","GATO","PAJARO"]) => True
    faltaPoner([["PERRO",(1,2),(3,1)],"GATO","PAJARO"]) => True
    faltaPoner([["PERRO",(1,2),(3,1)],["GATO",(3,1),(4,5)],["PAJARO",(6,7),(9,8)]]) => False
    """
    for i in palabras:
        if type(i) == str:
            return True
    return False


def cualPoner(palabras):
    """
    cualPoner : List(Str) | List(List(Tuple(Int) | Str)) -> Tuple(Str | Int)
    cualPoner recibe una lista de palabras con al menos una no colocada en el tablero (no reemplazada por una lista de tuplas)
    Devuelve una tupla con la palabra y su indice en la lista
    Ejemplos:
    cualPoner(["PERRO","GATO","PAJARO"]) => ("PERRO",0)
    cualPoner(["PERRO",(1,2),(3,1)],"GATO","PAJARO"]) => ("GATO",1)
    cualPoner([["PERRO",(1,2),(3,1)],["GATO",(3,1),(4,5)],["PAJARO",(6,7),(9,8)]],"OSO") => ("OSO",3)
    """
    for i in palabras:
        if type(i) == str:
            indice = palabras.index(i)
            return (i, indice)



def lugares(tablero, direccion, palabra):
    """
    Representamos los lugares posibles con una lista de tuplas, cada tupla representa un par coordenado X,Y
    lugares : List(List(Int | Str)) Tuple(Int) Str -> List(Tuple(Int))
    lugares recibe el tablero, la direccion y la palabra
    Devuelve todas las posiciones donde la palabra puede empezar para asegurar entrar en el tablero
    Ejemplos:
    lugares(generaTablero(6),(1,1),"PERRO") => [(0,0),(0,1),(1,0),(1,1)]
    lugares(generaTablero(5),(1,0),"OLA") => [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5)]
    lugares(generaTablero(3),(0,1),"MANO") => []
    """
    anchoAlto = len(tablero)
    lpalabra = len(palabra)
    posibles = []
    if direccion == (1, 0):
        maxX = anchoAlto - lpalabra + 1
        maxY = anchoAlto
    elif direccion == (0, 1):
        maxX = anchoAlto
        maxY = anchoAlto - lpalabra + 1
    for x in range(maxX):
        for y in range(maxY):
            posibles += [(x, y)]
    return posibles


def validarPalabraLugar(tablero, posini, direccion, palabra):
    """
    Representamos posiciones con una tupla X,Y
    Representamos direccion con una tupla (0,1), (1,0) o (1,1)
    Representamos palabras con Strings y todos sus caracteres en mayúscula
    validarPalabraLugar : List(List(Int | Str)) Tuple(Int) Tuple(Int) Str -> Bool
    validarPalabraLugar recibe un tablero, una posicion, una direccion y una palabra
    Devuelve True si se puede colocar la palabra con esas condiciones
    Ejemplos:
    validarPalabraLugar(generaTablero(5),(0,0),(1,0),"HOLA") => True
    validarPalabraLugar([["A","B","C"],[0,0,0],[0,0,0]],(0,2),(0,1),"OLA") => False
    """
    t = (posini[0], posini[1], direccion[0], direccion[1])
    for letra in palabra:
        if tablero[t[0]][t[1]] == 0 or tablero[t[0]][t[1]] == letra:
            t = (t[0] + t[2], t[1] + t[3], t[2], t[3])
        else:
            return False
    return True


def ponerPalabra(tablero, posini, direccion, palabra, val):
    """
    Representamos posiciones con una tupla X,Y
    Representamos direccion con una tupla (0,1), (1,0) o (1,1)
    Representamos palabras con Strings y todos sus caracteres en mayúscula
    ponerPalabra : List(List(Int | Str)) Tuple(Int) Tuple(Int) Str -> List(Str | Tuple)
    ponerPalabra recibe un tablero, una posicion, una direccion y una palabra
    Coloca la palabra en el tablero comenzando por la posicion inicial y siguiendo en la direccion dada
    Devuelve una lista con la palabra como primer elemento y tuplas que representan la posicion y el valor que tenian en donde se posicionaron las letras
    """
    tuplas = []
    tp = (posini[0], posini[1], direccion[0], direccion[1])
    for i in palabra:
        tuplas += [(tp[0], tp[1], tablero[tp[0]][tp[1]])]
        if val['mayus']:
            tablero[tp[0]][tp[1]] = i.upper()
        else:
            tablero[tp[0]][tp[1]] = i.lower()
        tp = (tp[0] + tp[2], tp[1] + tp[3], tp[2], tp[3])
    return tuplas


def quitarPalabra(tablero, postupla):
    """
    Representamos las posiciones a revertir con una tupla de 3 elementos (columna,fila,valoranterior)
    quitarPalabra : List(List(Str | Int)) List(Tuple(Int)) -> List(List(Str | Int))
    quitarPlabra recibe un tablero y una lista de posiciones a revertir, devuelve el tablero con los valores anteriores a poner la palabra
    Ejemplos:
    quitarPalabra([["H","O","L","A"],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[(0,0,0),(0,1,0),(0,2,0),(0,3,0)]) => [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    """
    for i in postupla:
        tablero[i[0]][i[1]] = i[2]
    return tablero


def ponerPalabras(tablero, palabras, val):
    """
    Representamos el tablero con una matriz NxN
    ponerPalabras : List(LIst(Int)) -> List(LIst(Int | Str))
    ponerPalabras recibe un tablero vacio (todos sus elementos son 0) y una lista de palabras, devuelve el tablero con las palabras colocadas
    """
    while faltaPoner(palabras):
        palabraAct = cualPoner(palabras)
        if val['hori']:
            direccionP = (1, 0)
        else:
            direccionP = (0 ,1)
        listaLugares = lugares(tablero, direccionP, palabraAct[0])
        shuffle(listaLugares)
        sePuede = False
        p = 0
        while not sePuede and p < len(listaLugares):
            if validarPalabraLugar(tablero, listaLugares[p], direccionP, palabraAct[0]):
                sePuede = True
                reemplazo = ponerPalabra(tablero, listaLugares[p], direccionP, palabraAct[0],val)
                palabras[palabraAct[1]] = reemplazo
                ponerPalabras(tablero, palabras,val)
                if palabraAct[1] < len(palabras) - 1 and type(palabras[palabraAct[1] + 1]) == str:
                    sePuede = False
                    quitarPalabra(tablero, reemplazo)
            p += 1
        if type(palabras[palabraAct[1]]) == str:
            return tablero
    return tablero


def imprimeTablero(tablero,val,p,filas,columnas,cantSust,cantAdj,cantVerb,definiciones,col,listaPorTipo):
  """

    ImprimeTablero muestra el tablero en una interfaz gafrica en el que cada boton es una letra. Permite jugar a la sopa
    seleccionando el color para pintar cada letra y un boton (Termine) que perimte finalizar el juego mostrando un mensaje de
    felicitaciones en caso de terminar la sopa con exito o mostrando las palabras faltantes en caso de haberlas
  """
  sg.ChangeLookAndFeel(col)
  c = None
  ayu = []
  contS = 0
  contA = 0
  contV = 0
  layout=[[sg.Button('Termine',key='Termine'),sg.Button('Salir')],
          [sg.Button('Sustantivos', button_color=(val['col_sust'],'black'))],
          [sg.Button('Adjetivos', button_color=(val['col_adj'],'black'))],
          [sg.Button('Verbos', button_color=(val['col_verb'],'black'))]
          ]
  if val['mostrarPal']:
    t = []
    for elemento in p:
      ayu.append(sg.Text(elemento))
    t.append(sg.Text('Palabras a encontrar en la sopa:'))
    layout.append(t)
    layout.append(ayu)
  if val['mostrarDef']:
    t = []
    t.append(sg.Text('Definiciones de las palabras a encontrar en la sopa:'))
    layout.append(t)
    for elemento in p:
      ayu = []
      ayu.append(sg.Text(definiciones[elemento]))
      layout.append(ayu)
  pos = 0
  largoAlto = len(tablero)
  claves = []
  for n in range(largoAlto * largoAlto):
    claves.append(str(n))
  for y in range(largoAlto):
    row = []
    for x in range(largoAlto):
      row.append(sg.Button(tablero[x][y],size=(4,1), pad=(1,1) ,button_color=('black', 'white'),
                                     enable_events=True, key=claves[pos]))
      pos += 1
    layout.append(row)
  window = sg.Window('Table', grab_anywhere=False).Layout(layout)
  while True:
    event, values = window.Read()
    if event == 'Salir' or None:
      break
    elif event == 'Sustantivos':
        c = val['col_sust']
    elif event == 'Adjetivos':
        c = val['col_adj']
    elif event == 'Verbos':
        c = val['col_verb']
    elif event in claves:
      if val['col_sust'] in window.FindElement(event).ButtonColor or val['col_adj'] in window.FindElement(event).ButtonColor or val['col_verb'] in window.FindElement(event).ButtonColor:
        window.FindElement(event).Update(button_color=('black','white'))
        window.FindElement(event).ButtonColor = ('black','white')
      elif c != None:
        window.FindElement(event).Update(button_color=('black',c))
        window.FindElement(event).ButtonColor = ('black',c)
    elif event == 'Termine':
      su= ""
      ad= ""
      ver = ""
      print(filas,columnas)
      i = 0
      d = {}
      d['letras'] = []
      finalP = p.copy()
      if val['ver']:
        for c in range(columnas):
          aux = []
          for f in range(filas):
            j = window.FindElement(str(i))
            aux.append(j)
            i += 1
          d['letras'].append(aux)
        print(d['letras'])
        a = d['letras']
        ind = 0
        for ind in range(columnas):
          for l in a:
            if val['col_sust'] in l[ind].ButtonColor:
              su = ''.join([su, l[ind].GetText()])
            if val['col_adj'] in l[ind].ButtonColor:
              ad = ''.join([ad, l[ind].GetText()])
            if val['col_verb'] in l[ind].ButtonColor:
              ver = ''.join([ver, l[ind].GetText()])
        print(su)
        print(ad)
        print(ver)
        print(cantSust,cantAdj,cantVerb)
        for ele in listaPorTipo[0]:
          if ele.lower() in su.lower():
            finalP.remove(ele)
            contS+=1
        for ele in listaPorTipo[1]:
          if ele.lower() in ad.lower():
            finalP.remove(ele)
            contA+=1
        for ele in listaPorTipo[2]:
          if ele.lower() in ver.lower():
            finalP.remove(ele)
            contV+=1
      if val['hori']:
        for c in range(columnas):
          for f in range(filas):
            j=window.FindElement(str(i))
            if val['col_sust'] in j.ButtonColor:
              su = ''.join([su, j.GetText()])
            if val['col_adj'] in j.ButtonColor:
              ad = ''.join([ad, j.GetText()])
            if val['col_verb'] in j.ButtonColor:
              ver = ''.join([ver, j.GetText()])
            i+=1
        print(su)
        print(ad)
        print(ver)
        for ele in listaPorTipo[0]:
          if ele.lower() in su.lower():
            finalP.remove(ele)
            contS+=1
        for ele in listaPorTipo[1]:
          if ele.lower() in ad.lower():
            finalP.remove(ele)
            contA+=1
        for ele in listaPorTipo[2]:
          if ele.lower() in ver.lower():
            finalP.remove(ele)
            contV+=1
      print(contS,contA,contV)
      print(finalP)
      if contS == cantSust and contA == cantAdj and contV == cantVerb :
        sg.Popup('FELICIDADES, LA SOPA DE LETRAS HA SIDO COMPLETADA')
        window.FindElement('Termine').Update(disabled=True)
      else:
        cad = ', '.join(finalP)
        sg.Popup('Resultados','¡HAS PERDIDO!\n' + 'Faltaron encontrar y marcar correctamente las siguientes palabras:\n' + cad + '\nFIN DEL JUEGO')
        window.FindElement('Termine').Update(disabled=True)

def generaSopa(p,v,cantSust,cantAdj,cantVerb,definiciones,colour,listaPorTipo):

    """
      Realiza las distintas invocaciones para generar la sopa de letras.
    """
    ABECEDARIO = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                  "ñ", "o", "p", "q", "r", "s", "t", "u", "v","w","x", "y", "z")

    palabras = p[:]
    palabras = eliminaIncluidos(palabras)
    tamaño = totalCaracteres(palabras)
    tamaño = sqrt(tamaño)
    tamaño = ceil(tamaño)
    masLarga = largoPalabraMasLarga(palabras)
    if tamaño < masLarga:
        tamaño = masLarga
    tamaño = tamaño + 2  # Si sumar 2 no funciona, multiplicar por 2
    tablero = generaTablero(tamaño)
    ponerPalabras(tablero, palabras,v)
    contador = 1
    while type(palabras[0]) == str and contador < len(palabras):
        palabras = palabras[1:] + palabras[0]
        ponerPalabras(tablero, palabras,v)
    if type(palabras[0]) == str:
        sg.Popup("NO SE PUDO")
    tablero,filas,columnas = rellenarTablero(tablero,ABECEDARIO,v)
    imprimeTablero(tablero,v,p,filas,columnas,cantSust,cantAdj,cantVerb,definiciones,colour,listaPorTipo)

def clasificar(palabra):
  """
    Clasifica la palabra recibida en base al tipo definido por Pattern.

  """
  print(tag(palabra, tokenize=True, encoding='utf-8'))
  a = tag(palabra, tokenize=True, encoding='utf-8')
  aux =a[0][1]
  if aux == 'JJ':
    return 'adjetivo'
  elif aux == 'NN':
    return 'sustantivo'
  elif aux == 'VB':
    return 'verbo'

def definirPalabra(p,palabras,definiciones):

  """
      Define el tipo de palabra y su definición en base a Wikcionario.
      Se toma como definición la sección ETIMOLOGÍA de Wikcionario, de no tenerla se pide que se ingrese una definición.
      Si la palabra no existe en Wikcionario utiliza el tipo que retorna Pattern y pide que se ingrese una definición.
      De no encontrar la palabra en ninguno de los dos recursos se informa de la situación y no se considera para la sopa.
      El método retorna dos diccionarios: uno con palabras y otro con definiciones.
      EL método también escribe en el archivo reporte.txt las situaciones a informar según pide el trabajo.
  """
  repo = open('reporte.txt','a')
  encontre = False
  hayDef = False
  tipoW =None
  contenido = None
  defi = None
  wiki = Wiktionary(language='es')
  article = wiki.search(p)
  if article != None:
    for section in article.sections:
      if hayDef == False:
        if (section.title).upper() == 'ETIMOLOGÍA':
          defi = section.content[21:]
          hayDef= True
          print(defi)
      if encontre == False:
        if (section.title).upper() in ('ADJETIVO','FORMA ADJETIVA'):
          encontre = True
          tipoW = 'adjetivo'
        elif (section.title).upper() in ('VERBO','VERBO TRANSITIVO','VERBO INTRANSITIVO','FORMA VERBAL'):
          encontre = True
          tipoW = 'verbo'
        elif (section.title).upper() in ('SUSTANTIVO','SUSTANTIVO FEMENINO','SUSTANTIVO MASCULINO','SUSTANTIVO PROPIO','SUSTANTIVO MASCULINO Y FEMENINO','SUSTANTIVO FEMENINO Y MASCULINO'):
          encontre = True
          tipoW= 'sustantivo'
    print("tipo W=" + str(tipoW))
    if p not in palabras[tipoW]:
      palabras[tipoW].append(p)
      if defi != None:
        definiciones[p] = defi
      else:
        defi = sg.PopupGetText('No se encontró una definición en Wikcionario para ' + str(p) + ' .Ingrese una: ')
        if defi != None and defi not in (""," "):
          definiciones[p] = defi
    else:
      sg.Popup("Ya ha ingresado esa palabra")
      return palabras
  else:
    tipoW=""
    print(tipoW)
  if p.lower() in verbs or p.lower() in lexicon or p.lower() in spelling:
    tipoP = clasificar(p)
    print(tipoP)
  else:
      tipoP=""
  if tipoW == "" and tipoP =="":
      aux2 = str(p) + ': La palabra no existe en Wikcionario ni en Pattern \n'
      repo.write(aux2)
      sg.Popup(aux2)
  elif tipoW == "" and tipoP != "":
    if p not in palabras[tipoP]:
      palabras[tipoP].append(p)
      defi = text = sg.PopupGetText('Ingresar definición para ' + str(p))
      if defi != None and defi not in (""," "):
        definiciones[p] = defi
    else:
      sg.Popup("Ya ha ingresado esa palabra")
      return palabras
  elif tipoW != tipoP:
    aux = str(p) + ': el tipo de palabra de Pattern no coincide con la de Wikcionario \n'
    repo.write(aux)
    sg.Popup(aux)
  return palabras,definiciones


def configuracion():
  """
      Genera una interfaz donde el usuario podrá ingresar la cantidad de palabras a buscar, las palabras a aparecer en la sopa,
      la orientación de las palabras en la sopa, si la letras en la sopa apareceran en mayúsculas o minúsculas y los colores que
      corresponden a cada tipo de palabra (sustantivo,adjetivo,verbo).
      Se guardará en un archiso JSON la configuración ingresada.
  """
  palabras = {}
  palabras['sustantivo'] = []
  palabras['adjetivo'] = []
  palabras['verbo'] = []
  listaPalabras = []
  listaSust = []
  listaAdj = []
  listaVer = []
  listaPorTipo = []
  definiciones = {}
  config = {}
  totS = 0
  totA = 0
  totV = 0
  configuracion = [
            [sg.Text('VAMOS A PREPARAR LA SOPA DE LETRAS', text_color='red')],
            [sg.Text('Seleccione la cantidad de sustantivos adjetivos y verbos a insertar en la sopa')],
            [sg.Text('Sustantivos'),sg.InputText(0,size=(2, 1),key='sus'), sg.Text('Adjetivos'), sg.InputText(0, size=(2, 1),key='adj'),
             sg.Text('Verbos'), sg.InputText(0, size=(2, 1),key='verb')],
             [sg.Button('Aceptar')],
            [sg.Text('Ingrese las palabras una a una'), sg.InputText(size=(10, 1),key='pal')],
            [sg.Button('Agregar',disabled=True,key='Agregar'), sg.Button('Eliminar',disabled=True,key='Eliminar')],
            [sg.Frame(layout=[
                [sg.Text('Seleccione ayuda:'),sg.Radio(' Sin ayuda',"Radio1", default=True,key='sinAyuda'),sg.Radio(' Mostrar definicion',"Radio1",key='mostrarDef'),
                 sg.Radio(' Mostrar palabras',"Radio1",key='mostrarPal')],
                [sg.Text('Seleccione orientacion de las palabras:'),sg.Radio(' Horizontal',"Radio2",default=True,key='hori'),sg.Radio(' Vertical',"Radio2",key='ver')],
                [sg.Text('Seleccione forma de las letras'), sg.Radio(' Mayuscula',"Radio3", default=True,key='mayus'), sg.Radio(' Minuscula',"Radio3",key='minus')],
                 ],
                title='Opciones', title_color='red', relief=sg.RELIEF_SUNKEN)
             ],
             [sg.Text('Seleccione el color de los sustantivos :'),
              sg.InputCombo(('red','black','yellow','pink','blue','brown','lightpink','green',),default_value='red',key='col_sust')],
             [sg.Text('Seleccione el color de los adjetivos :'),
              sg.InputCombo(('red','black','yellow','pink','blue','brown','lightpink','green'),default_value='blue',key='col_adj')],
             [sg.Text('Seleccione el color de los verbos :'),
              sg.InputCombo(('red','black','yellow','pink','blue','brown','lightpink','green'),default_value='yellow',key='col_verb')],
            [sg.Button('Generar sopa',disabled=True,key='Generar sopa'),sg.Button('Cancelar')]
        ]
  window2 = sg.Window('configuracion').Layout(configuracion)
  while True:
    event,valores = window2.Read()
    if event == 'Cancelar' or None:
      break
    elif event == 'Aceptar':
      if valores['sus'] not in ('',' ') and valores['adj'] not in ('',' ') and valores['verb'] not in ('',' '):
        cantSust = int(valores['sus'])
        cantAdj = int(valores['adj'])
        cantVerb = int(valores['verb'])
        window2.FindElement('Agregar').Update(disabled=False)
        window2.FindElement('Eliminar').Update(disabled=False)
        window2.FindElement('Generar sopa').Update(disabled=False)
      else:
        sg.Popup('Complete los tres campos antes de hacer clic en Aceptar')
    elif event == 'Eliminar':
      if valores['pal'] not in (""," "):
        p = valores['pal'].lower()
        if p in palabras['sustantivo'] or p in palabras['adjetivo'] or p in palabras['verbo']:
            if p in palabras['sustantivo']:
                palabras['sustantivo'].remove(p)
            elif p in palabras['adjetivo']:
                palabras['adjetivo'].remove(p)
            elif p in palabras['verbo']:
                palabras['verbo'].remove(p)
        else:
            sg.Popup('La palabra ingresada no existe')
      else:
        sg.Popup('Ingrese una palabra antes de hacer clic en Eliminar')
    elif event == 'Agregar':
      if valores['pal'] not in (""," "):
        palabra= valores['pal'].lower()
        palabras,definiciones = definirPalabra(palabra,palabras,definiciones)
      else:
        sg.Popup('Ingrese una palabra antes de hacer clic en Agregar')
    elif event == 'Generar sopa':
      s = palabras['sustantivo']
      ad = palabras['adjetivo']
      ver = palabras['verbo']
      if valores['col_sust'] != valores['col_adj'] and valores['col_sust'] != valores['col_verb'] and valores['col_adj'] != valores['col_verb']:
        if s or ad or ver:
          if s:
            if len(s) >= cantSust:
                totS = cantSust
                for i in range(cantSust):
                    aux = choice(s)
                    listaSust.append(aux)
                    listaPalabras.append(aux)
                    s.remove(aux)
            else:
              totS = len(s)
              for i in range(len(s)):
                  aux = choice(s)
                  listaSust.append(aux)
                  listaPalabras.append(aux)
                  s.remove(aux)
          if ad:
            if len(ad) >= cantAdj:
                totA= cantAdj
                for i in range(cantAdj):
                    aux = choice(ad)
                    listaAdj.append(aux)
                    listaPalabras.append(aux)
                    ad.remove(aux)
            else:
              totA = len(ad)
              for i in range(len(ad)):
                  aux = choice(ad)
                  listaAdj.append(aux)
                  listaPalabras.append(aux)
                  ad.remove(aux)
          if ver:
            if len(ver) >= cantVerb:
              totV= cantVerb
              for i in range(cantVerb):
                aux = choice(ver)
                listaVer.append(aux)
                listaPalabras.append(aux)
                ver.remove(aux)
            else:
              totV = len(ver)
              for i in range(len(ver)):
                aux = choice(ver)
                listaVer.append(aux)
                listaPalabras.append(aux)
                ver.remove(aux)
          listaPorTipo.append(listaSust.copy())
          listaPorTipo.append(listaAdj.copy())
          listaPorTipo.append(listaVer.copy())
          config = valores.copy()
          config['sus'] = totS
          config['adj'] = totA
          config['verb']= totV
          config['listaP'] = listaPalabras.copy()
          config['listaD'] = definiciones.copy()
          config['listaPP'] = listaPorTipo.copy()
          print(config)
          with open('configuración.json','w') as file:
            json.dump(config,file,indent=4)
          generaSopa(listaPalabras,valores,totS,totA,totV,definiciones,color,listaPorTipo)
        else:
          sg.Popup("No ha ingresado palabras")
      else:
        sg.Popup("Los colores para los tipos de palabras no pueden repetirse")



repo = open('reporte.txt','w')
color = LookAndFeel()
print(color)
sg.ChangeLookAndFeel(color)
repo.close()
inicio = [
            [sg.Text('BIENVENIDO A LA SOPA DE LETRAS', text_color= 'white')],
            [sg.Button('Jugar'),sg.Button('Configuración')]
         ]

window = sg.Window('Inicio').Layout(inicio)
event, values = window.Read()
window.Close()
if event == 'Configuración':
  configuracion()
elif event == 'Jugar':
  r = getcwd()
  contenido = listdir(r)
  print(contenido)
  if 'configuración.json' in contenido:
    try:
      with open('configuración.json','r') as file:
        data = json.load(file)
    except IOError:
      sg.Popup('El archivo configuración.json no existe o no tiene permisos para abrirlo.\n'+'Deberá definir una configuración')
    print(data)
    generaSopa(data['listaP'],data,data['sus'],data['adj'],data['verb'],data['listaD'],color,data['listaPP'])
  else:
    sg.Popup('No hay una configuración definida, debe definir una configuración')
    configuracion()
