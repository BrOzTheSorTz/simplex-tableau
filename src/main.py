# src/main.py
import ast, json,csv
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from models.Simplex import Simplex

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    # Leer los datos como texto
    data = request.data.decode('utf-8')
    print(f'Data recibida: {data}')  # Imprimir el contenido de data para verificar

    # Verificar si se recibieron datos
    if data:

        try:
            # Intentar cargar como JSON
            matriz = json.loads(data)
            print('Matriz:', matriz)  # Imprimir la matriz
            ruta = '../data/problem_data.csv'
            crear_csv(matriz,ruta)
            #Ejecutamos el algoritmo
            console = False
            simplex = Simplex(ruta)
            result = simplex.execute(console)

            print("Before rendering solution.html")
            #return render_template('solution.html', result=result)
            return jsonify(result)



        except json.JSONDecodeError as e:
            print(f'Error al decodificar JSON: {e}')
            return jsonify({'error': 'Datos mal formateados'}), 400  # Respuesta de error
    return "No hay datos"
def crear_csv(matriz,ruta):
    num_variables = len(matriz[0])
    with open(ruta,'w') as csvfile:
        fieldnames = ["B"] + ["X" + str(i) for i in range(1, num_variables)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        funcion = matriz[0]
        restricciones = matriz[1]
        # Escribimos restricciones
        for restriccion in restricciones:
            i=0
            row = {}
            for coef in restriccion:
                row[fieldnames[i]] = coef
                i=i+1
            writer.writerow(row)

        # Por último escribimos función objetivo
        row = {}
        for i in range(0,len(funcion)):
            row[fieldnames[i]] = funcion[i]
        writer.writerow(row)



if __name__ == '__main__':
    app.run(debug=True)

