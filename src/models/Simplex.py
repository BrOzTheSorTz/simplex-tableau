import pandas as pd
import numpy as np
import math

class Simplex:
    def __init__(self, csv_path='./data/problem_data.csv'):
        """Constructor: inicializa las variables clave y carga los datos del archivo CSV"""
        self.num_max_iter = 100
        self.coef_base = None  # Coeficientes de las variables básicas
        self.coef = None  # Coeficientes originales del problema
        self.tabla = None  # Tabla del método simplex
        self.resultadosZ = None  # Resultado de Z - C
        self.resultadosFinal = {} # Fila y nombre de las variables de los coef base

        # Lee las restricciones y la función objetivo desde el CSV
        self.restricciones, self.objetivo = self.leer_datos(csv_path)

    def execute(self,console=True):
        """Método principal que ejecuta el algoritmo Simplex"""
        self.crear_tabla()  # Inicializa la tabla Simplex
        optimal = False
        iteracion = 0
        while not optimal and iteracion < self.num_max_iter:
            valor_z_menos_c, menor_cero = self.calcular_operacion()
            self.resultadosZ = valor_z_menos_c
            iteracion += 1

            if menor_cero:
                # Determina la columna que entra y la fila que sale
                col_in = self.variable_que_entra(valor_z_menos_c)
                row_out = self.variable_que_sale(col_in)

                # Actualizamos los nombres de los coef base
                self.resultadosFinal[row_out] = "X"+str(col_in)


                # Actualiza la tabla y los coeficientes
                self.recalcular_tabla(row_out, col_in)
                self.actualizar_coeficientes(row_out, col_in)
            else:
                print("Se ha encontrado la solución óptima.")

                optimal = True
        if optimal:
            result = self.mostrar_resultado()
            if console:
                print("Resultados:")
                print(a for a in result)
            else:
                return result
        else:
            if console:
                print("No hay solución")
            else:
                return []


    def crear_tabla(self):
        """Crea la tabla inicial agregando variables de holgura"""
        num_restr = len(self.restricciones)
        num_vars = len(self.restricciones[0])

        # Agrega variables de holgura a la tabla (matriz identidad)
        identidad = np.eye(num_restr)
        self.tabla = np.hstack((self.restricciones, identidad))

        # Extiende la función objetivo con ceros para las variables de holgura
        self.objetivo = np.hstack((self.objetivo, np.zeros(num_restr)))
        self.coef = np.copy(self.objetivo)
        self.coef_base = np.copy(self.objetivo[-num_restr:])

        print("Restricciones tras agregar variables de holgura:")
        print(self.restricciones)
        print("Función objetivo tras agregar variables de holgura:")
        print(self.objetivo)

    def leer_datos(self, csv_path):
        """Lee los datos de restricciones y la función objetivo desde un archivo CSV"""
        print("Leyendo datos del archivo CSV...")
        data = pd.read_csv(csv_path).values
        restricciones = data[:-1, :]  # Todas las filas menos la última (restricciones)
        funcion_objetivo = data[-1, :]  # Última fila (función objetivo)

        print("Restricciones:")
        print(self.mostrar_restricciones(restricciones))
        print("Función objetivo:")
        print(self.mostrar_funcion_objetivo(funcion_objetivo))

        return restricciones, funcion_objetivo

    def mostrar_funcion_objetivo(self, funcion):
        """Genera una representación en string de la función objetivo"""
        ecuacion = "Z = " + " ".join([f"+ {funcion[i]}X{i}" if funcion[i] >= 0 else f"{funcion[i]}X{i}" for i in range(1, len(funcion))])
        return ecuacion

    def mostrar_restricciones(self, restricciones):
        """Genera una representación en string de las restricciones"""
        ecuaciones = []
        for restriccion in restricciones:
            terms = [f"+ {restriccion[i]}X{i}" if restriccion[i] >= 0 else f"{restriccion[i]}X{i}" for i in range(1, len(restriccion))]
            ecuacion = f"{' '.join(terms)} <= {restriccion[0]}"
            ecuaciones.append(ecuacion)
        return ecuaciones

    def calcular_operacion(self):
        """Calcula Z - C y verifica si hay coeficientes negativos"""
        z_menos_c = np.zeros_like(self.tabla[0])
        menor_cero = False

        # Calculo de Z - C
        for i in range(len(z_menos_c)):
            z_menos_c[i] = sum(self.coef_base[j] * self.tabla[j][i] for j in range(len(self.coef_base))) - self.coef[i]
            if z_menos_c[i] < 0:
                menor_cero = True

        return z_menos_c, menor_cero

    def variable_que_entra(self, z_menos_c):
        """Determina qué variable entra a la base (columna con el valor más negativo en Z - C)"""
        return np.argmin(z_menos_c)  # Devuelve el índice de la columna con el valor más negativo

    def variable_que_sale(self, col_in):
        """Determina qué variable sale de la base (test de razón mínima)"""
        ratios = np.array([self.tabla[i][0] / self.tabla[i][col_in] if self.tabla[i][col_in] > 0 else math.inf for i in range(len(self.coef_base))])
        return np.argmin(ratios)  # Fila con el menor ratio

    def recalcular_tabla(self, row_out, col_in):

        pivot_value = self.tabla[row_out][col_in]
        # Hace cero los valores en la columna de entrada excepto el pivote
        for i in range(len(self.tabla)):
            if i != row_out:
                self.tabla[i] -= (self.tabla[i][col_in] / pivot_value) * self.tabla[row_out]
        """Actualiza la tabla para hacer 1 el pivote y 0 el resto de la columna"""

        self.tabla[row_out] /= pivot_value  # Divide la fila pivote por el valor pivote

    def actualizar_coeficientes(self, row_out, col_in):
        """Actualiza los coeficientes básicos después de cambiar la base"""
        self.coef_base[row_out] = self.coef[col_in]

    def mostrar_resultado(self):
        """Imprime los resultados finales de la solución óptima"""

        num_variables = len(self.tabla)
        result = []
        for key, value in self.resultadosFinal.items():
            var = int(value.split("X")[1])
            if var <= num_variables:
                result.append(f"X{var} = {self.tabla[key][0]}")

        result.append(f"Z = {self.resultadosZ[0]}")
        return result

