import numpy as np
import json

def contar_elementos(lst):
    # Crea un diccionario para almacenar el conteo de cada elemento
    conteo_elementos = {}
    for elemento in lst:
        # Incrementa el conteo para cada elemento
        conteo_elementos[elemento] = conteo_elementos.get(elemento, 0) + 1
    return conteo_elementos


class AgenteSeguidorLinea():
    def __init__(self):
        '''Orientacion: Vector de orden 1x2 con la lectura del propioceptor (orientacion del agente)
        derecha(0,1), izquierda(0,-1), arriba(-1,0), abajo(1,0)
        Posicion: Vector 1x2 con la ubicación del agente en el ambiente
        '''
        # Inicializa la posición y orientación del agente
        self.posicion = []  # Valor inicial: (1,2)
        self.orientacion = []  # Valor inicial: -> derecha
        self.celda_color = ''
        self.celdas_adelante = ['','','']
        self.contacto = 0
        self.ambiente = []
        self.reglas_encontradas = []
        self.nro_accion_avanzar = 0
        self.nro_accion_rotar = 0
        self.contar_N = 0
        self.contar_B = 0

    def accion_rotar(self, sentido_rotacion):
        '''La accion rotar recibe como parametro el sentido (horario, antihorario) para la rotación y luego rota al agente 90 grados sobre su eje'''
        matriz_rota_horario = np.array([[0,-1],
                                    [1,0]])
        matriz_rota_antihorario = np.array([[0,1],
                                            [-1,0]])
        if sentido_rotacion == 'horario':
            norientacion = np.dot(self.orientacion, matriz_rota_horario)
        elif sentido_rotacion == 'antihorario':
            norientacion = np.dot(self.orientacion, matriz_rota_antihorario)
        return norientacion

    def accion_avanzar (self):
        '''La accion avanzar le suma a la posicion la orientacion'''
        self.posicion = np.add(self.posicion,self.orientacion)
        return self.posicion

    def sensor_celda_color(self, ambiente):
        '''Devuelve la lectura del sensor que ve la celda actual (B o N)'''
        # Sensor 1: Obtiene el color de la celda actual
        self.celda_color = ambiente[self.posicion[0]][self.posicion[1]]
        if self.celda_color == 'N':
            self.contar_N = self.contar_N +1
        elif self.celda_color == 'B':
            self.contar_B = self.contar_B +1
        return self.celda_color

    def sensor_tres_celdas_adelante(self, ambiente):
        '''Devuelve la lectura del sensor que ve las 3 celdas delanteras (B, N o P)'''
        # Sensor 2: Obtiene los colores de las tres celdas adelante
        celda_delante_B = np.add(self.posicion,self.orientacion)
        #print(celda_delante_B)
        celda_delante_A = np.add(celda_delante_B, self.accion_rotar('antihorario'))
        #print(celda_delante_A)
        celda_delante_C = np.add(celda_delante_B, self.accion_rotar('horario'))
        #print(celda_delante_C)
        self.celdas_adelante[0] = ambiente[celda_delante_A[0]][celda_delante_A[1]]
        self.celdas_adelante[1] = ambiente[celda_delante_B[0]][celda_delante_B[1]]
        self.celdas_adelante[2] = ambiente[celda_delante_C[0]][celda_delante_C[1]]
        #print(self.celdas_adelante)

    def sensor_contacto_pared(self):
        # Sensor 4: Verifica si el agente ha chocado con una pared
        pass

    def reglas(self):
        '''conjunto de reglas ejecutadas por el agente'''
        reglas = {
                'regla1': {'camara1':'B','camara2':['B','B','B'],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla2': {'camara1':'B','camara2':['B','B','B'],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla3': {'camara1':'B','camara2':['B','B','B'],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla4': {'camara1':'B','camara2':['B','B','B'],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla5': {'camara1':'B','camara2':["N","B","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla6': {'camara1':'B','camara2':["N","B","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla7': {'camara1':'B','camara2':["N","B","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla8': {'camara1':'B','camara2':["N","B","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla9': {'camara1':'B','camara2':["B","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla10': {'camara1':'B','camara2':["B","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla11': {'camara1':'B','camara2':["B","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla12': {'camara1':'B','camara2':["B","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla13': {'camara1':'B','camara2':["B","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla14': {'camara1':'B','camara2':["B","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla15': {'camara1':'B','camara2':["B","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla16': {'camara1':'B','camara2':["B","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla17': {'camara1':'B','camara2':["N","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla18': {'camara1':'B','camara2':["N","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla19': {'camara1':'B','camara2':["N","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla20': {'camara1':'B','camara2':["N","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla21': {'camara1':'B','camara2':["B","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla22': {'camara1':'B','camara2':["B","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla23': {'camara1':'B','camara2':["B","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla24': {'camara1':'B','camara2':["B","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla25': {'camara1':'B','camara2':["N","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla26': {'camara1':'B','camara2':["N","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla27': {'camara1':'B','camara2':["N","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla28': {'camara1':'B','camara2':["N","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla29': {'camara1':'B','camara2':["N","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla30': {'camara1':'B','camara2':["N","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla31': {'camara1':'B','camara2':["N","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla32': {'camara1':'B','camara2':["N","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla33': {'camara1':'B','camara2':["P","B","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla34': {'camara1':'B','camara2':["P","B","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla35': {'camara1':'B','camara2':["P","B","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla36': {'camara1':'B','camara2':["P","B","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla37': {'camara1':'B','camara2':["B","B","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla38': {'camara1':'B','camara2':["B","B","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla39': {'camara1':'B','camara2':["B","B","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla40': {'camara1':'B','camara2':["B","B","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla41': {'camara1':'B','camara2':["P","P","P"],'contacto':0,'orientacion':[0,1],'accion1':'horario','accion2':None},
                'regla42': {'camara1':'B','camara2':["P","P","P"],'contacto':0,'orientacion':[0,-1],'accion1':'horario','accion2':None},
                'regla43': {'camara1':'B','camara2':["P","P","P"],'contacto':0,'orientacion':[-1,0],'accion1':'horario','accion2':None},
                'regla44': {'camara1':'B','camara2':["P","P","P"],'contacto':0,'orientacion':[1,0],'accion1':'horario','accion2':None},
                'regla45': {'camara1':'B','camara2':["P","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla46': {'camara1':'B','camara2':["P","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla47': {'camara1':'B','camara2':["P","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla48': {'camara1':'B','camara2':["P","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla49': {'camara1':'B','camara2':["N","B","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla50': {'camara1':'B','camara2':["N","B","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla51': {'camara1':'B','camara2':["N","B","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla52': {'camara1':'B','camara2':["N","B","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla53': {'camara1':'B','camara2':["P","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla54': {'camara1':'B','camara2':["P","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla55': {'camara1':'B','camara2':["P","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla56': {'camara1':'B','camara2':["P","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla57': {'camara1':'B','camara2':["N","N","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla58': {'camara1':'B','camara2':["N","N","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla59': {'camara1':'B','camara2':["N","N","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla60': {'camara1':'B','camara2':["N","N","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla61': {'camara1':'B','camara2':["B","N","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla62': {'camara1':'B','camara2':["B","N","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla63': {'camara1':'B','camara2':["B","N","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla64': {'camara1':'B','camara2':["B","N","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla65': {'camara1':'B','camara2':["P","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla66': {'camara1':'B','camara2':["P","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla67': {'camara1':'B','camara2':["P","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla68': {'camara1':'B','camara2':["P","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla69': {'camara1':'N','camara2':['B','B','B'],'contacto':0,'orientacion':[0,1],'accion1':'horario','accion2':None},
                'regla70': {'camara1':'N','camara2':['B','B','B'],'contacto':0,'orientacion':[0,-1],'accion1':'horario','accion2':None},
                'regla71': {'camara1':'N','camara2':['B','B','B'],'contacto':0,'orientacion':[-1,0],'accion1':'horario','accion2':None},
                'regla72': {'camara1':'N','camara2':['B','B','B'],'contacto':0,'orientacion':[1,0],'accion1':'horario','accion2':None},
                'regla73': {'camara1':'N','camara2':["N","B","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla74': {'camara1':'N','camara2':["N","B","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla75': {'camara1':'N','camara2':["N","B","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla76': {'camara1':'N','camara2':["N","B","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla77': {'camara1':'N','camara2':["B","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla78': {'camara1':'N','camara2':["B","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla79': {'camara1':'N','camara2':["B","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla80': {'camara1':'N','camara2':["B","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla81': {'camara1':'N','camara2':["B","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla82': {'camara1':'N','camara2':["B","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla83': {'camara1':'N','camara2':["B","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla84': {'camara1':'N','camara2':["B","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla85': {'camara1':'N','camara2':["N","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla86': {'camara1':'N','camara2':["N","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla87': {'camara1':'N','camara2':["N","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla88': {'camara1':'N','camara2':["N","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla89': {'camara1':'N','camara2':["B","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla90': {'camara1':'N','camara2':["B","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla91': {'camara1':'N','camara2':["B","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla92': {'camara1':'N','camara2':["B","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla93': {'camara1':'N','camara2':["N","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla94': {'camara1':'N','camara2':["N","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla95': {'camara1':'N','camara2':["N","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla96': {'camara1':'N','camara2':["N","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla97': {'camara1':'N','camara2':["N","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla98': {'camara1':'N','camara2':["N","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla99': {'camara1':'N','camara2':["N","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla100': {'camara1':'N','camara2':["N","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla101': {'camara1':'N','camara2':["P","B","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla102': {'camara1':'N','camara2':["P","B","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla103': {'camara1':'N','camara2':["P","B","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla104': {'camara1':'N','camara2':["P","B","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla105': {'camara1':'N','camara2':["B","B","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla106': {'camara1':'N','camara2':["B","B","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla107': {'camara1':'N','camara2':["B","B","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla108': {'camara1':'N','camara2':["B","B","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla109': {'camara1':'N','camara2':["P","P","P"],'contacto':0,'orientacion':[0,1],'accion1':'horario','accion2':None},
                'regla110': {'camara1':'N','camara2':["P","P","P"],'contacto':0,'orientacion':[0,-1],'accion1':'horario','accion2':None},
                'regla111': {'camara1':'N','camara2':["P","P","P"],'contacto':0,'orientacion':[-1,0],'accion1':'horario','accion2':None},
                'regla112': {'camara1':'N','camara2':["P","P","P"],'contacto':0,'orientacion':[1,0],'accion1':'horario','accion2':None},
                'regla113': {'camara1':'N','camara2':["P","B","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla114': {'camara1':'N','camara2':["P","B","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla115': {'camara1':'N','camara2':["P","B","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla116': {'camara1':'N','camara2':["P","B","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla117': {'camara1':'N','camara2':["N","B","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla118': {'camara1':'N','camara2':["N","B","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla119': {'camara1':'N','camara2':["N","B","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla120': {'camara1':'N','camara2':["N","B","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla121': {'camara1':'N','camara2':["P","N","N"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'horario'},
                'regla122': {'camara1':'N','camara2':["P","N","N"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'horario'},
                'regla123': {'camara1':'N','camara2':["P","N","N"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'horario'},
                'regla124': {'camara1':'N','camara2':["P","N","N"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'horario'},
                'regla125': {'camara1':'N','camara2':["N","N","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':'antihorario'},
                'regla126': {'camara1':'N','camara2':["N","N","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':'antihorario'},
                'regla127': {'camara1':'N','camara2':["N","N","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla128': {'camara1':'N','camara2':["N","N","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':'antihorario'},
                'regla129': {'camara1':'N','camara2':["B","N","P"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla130': {'camara1':'N','camara2':["B","N","P"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla131': {'camara1':'N','camara2':["B","N","P"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla132': {'camara1':'N','camara2':["B","N","P"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None},
                'regla133': {'camara1':'N','camara2':["P","N","B"],'contacto':0,'orientacion':[0,1],'accion1':'avanzar','accion2':None},
                'regla134': {'camara1':'N','camara2':["P","N","B"],'contacto':0,'orientacion':[0,-1],'accion1':'avanzar','accion2':None},
                'regla135': {'camara1':'N','camara2':["P","N","B"],'contacto':0,'orientacion':[-1,0],'accion1':'avanzar','accion2':None},
                'regla136': {'camara1':'N','camara2':["P","N","B"],'contacto':0,'orientacion':[1,0],'accion1':'avanzar','accion2':None}
        }
        #reglas_encontradas = [  ]
        #print('valores a buscar:',self.celda_color,self.celdas_adelante,self.contacto, self.orientacion)
        for regla_id, regla in reglas.items():
            if (regla["camara1"] == self.celda_color
                #and regla["camara2"] == self.celdas_adelante
                and np.array_equal(regla["camara2"],self.celdas_adelante)
                and regla["contacto"] == self.contacto
                and np.array_equal(regla["orientacion"], self.orientacion)
                ):
                #reglas_encontradas.append(regla_id)
                self.reglas_encontradas.append(regla_id)
    
                print('encontrado: ',regla_id, regla["camara1"],regla["camara2"], regla["contacto"], regla["orientacion"], regla["accion1"], regla["accion2"])

                # Ejecutar regla 1
                if regla["accion1"] == "avanzar":
                    self.accion_avanzar()
                    self.nro_accion_avanzar = self.nro_accion_avanzar + 1
                elif regla["accion1"] == "horario":
                    self.orientacion=self.accion_rotar('horario')
                    self.nro_accion_rotar = self.nro_accion_rotar + 1
                elif regla["accion1"] == "antihorario":
                    self.orientacion=self.accion_rotar('antihorario')
                    self.nro_accion_rotar = self.nro_accion_rotar + 1
                ## Ejecutar regla 2
                if regla["accion2"] == "avanzar":
                    self.accion_avanzar()
                    self.nro_accion_avanzar = self.nro_accion_avanzar + 1
                elif regla["accion2"] == "horario":
                    self.orientacion=self.accion_rotar('horario')
                    self.nro_accion_rotar = self.nro_accion_rotar + 1
                elif regla["accion2"] == "antihorario":
                    self.orientacion=self.accion_rotar('antihorario')
                    self.nro_accion_rotar = self.nro_accion_rotar + 1
                print('ACCION:',regla["accion1"],regla["accion2"])
                break

        self.sensor_celda_color(ambiente)
        self.sensor_tres_celdas_adelante(ambiente)
        self.sensor_contacto_pared()


        #print("Reglas que coinciden con los valores buscados:", reglas_encontradas)

# Ejemplo de uso: Matriz 8x7
grid = [
    ["P", "P", "P", "P", "P", "P", "P", "P", "P"],#0
    ["P", "B", "B", "B", "N", "B", "B", "B", "P"],#1
    ["P", "B", "B", "B", "N", "B", "B", "B", "P"],#2
    ["P", "B", "B", "B", "N", "N", "N", "B", "P"],#3
    ["P", "B", "B", "B", "B", "N", "N", "N", "P"],#4
    ["P", "B", "B", "B", "B", "B", "B", "N", "P"],#5
    ["P", "B", "B", "B", "B", "B", "B", "N", "P"],#6
    ["P", "N", "N", "N", "N", "N", "N", "N", "P"],#7
    ["P", "B", "B", "B", "B", "B", "B", "B", "P"],#8
    ["P", "P", "P", "P", "P", "P", "P", "P", "P"] #9
    #["0", "1", "2", "3", "4", "5", "6", "7", "8"]
]
ambiente = np.array(grid)

# Variables estadisticas


# Instanciamos la clase
agente = AgenteSeguidorLinea()
agente.ambiente = ambiente
agente.posicion = np.array([5,3])
agente.orientacion = np.array([0,1]) 


print(ambiente)
agente.sensor_celda_color(ambiente)
agente.sensor_tres_celdas_adelante(ambiente)
print('Estado0: ','| posicion: ', agente.posicion, '| orientacion: ',agente.orientacion, ' | camara1: ',agente.celda_color, '| camara2: ',agente.celdas_adelante)

for i in range(50):
  print('====> Estado',i,': ','| posicion: ', agente.posicion, '| orientacion: ',agente.orientacion, ' | camara1: ',agente.celda_color, '| camara2: ',agente.celdas_adelante)
  agente.reglas()

resultado = contar_elementos(agente.reglas_encontradas)
print("STD", "nro_accion_avanzar:", agente.nro_accion_avanzar,"nro_acciones_rotar", agente.nro_accion_rotar)
print("STD", "Negras:", agente.contar_N,"Blancas:", agente.contar_B)
for elemento, cantidad in resultado.items():
    print(f"{elemento}, cantidad {cantidad}")



