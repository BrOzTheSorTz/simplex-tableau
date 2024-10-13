# Simplex App

Simplex App es una aplicación web desarrollada para resolver problemas de programación lineal utilizando el **algoritmo simplex tableau**. La aplicación ofrece una interfaz intuitiva que permite a los usuarios agregar restricciones y variables para resolver problemas de maximización donde todas las restricciones son ≤.

## Tecnologías utilizadas

- **Frontend**: HTML, JavaScript y CSS
- **Backend**: Python con Flask
- **Algoritmo**: Implementación del método simplex tableau en Python

## Funcionamiento

El algoritmo toma los datos de un problema de maximización desde un archivo CSV, ejecuta el método simplex y devuelve la solución óptima (si existe). El flujo es el siguiente:

1. **Carga del archivo CSV**: 
    - El archivo debe tener la siguiente estructura:
      - La primera fila contiene los nombres de las columnas: `B` para el término independiente, `X1`, `X2`... para las variables.
      - Las siguientes filas contienen los valores de las restricciones y de la función objetivo (en la última fila).
      - El término independiente de la función objetivo debe tener valor 0.
2. **Ejecución del algoritmo**:
    - Llamar a la función `execute()` para resolver el problema.
    - El resultado se mostrará por consola de forma predeterminada. También se puede devolver como un array de strings si se especifica en los parámetros (ideal para la interfaz gráfica).
3. **Condición de parada**:
    - Si el algoritmo realiza más de 100 iteraciones sin encontrar una solución óptima, se asume que no hay solución y el algoritmo se detendrá devolviendo un valor vacío.

### Ejemplo de CSV

```
B,X1,X2
4,2,1
8,1,2
0,-3,-5
```

Este CSV representa un problema con las siguientes restricciones y función objetivo:

- Restricciones:
  - 2X1 + 1X2 ≤ 4
  - 1X1 + 2X2 ≤ 8
- Función objetivo:
  - Maximizar Z = 3X1 + 5X2

## Interfaz gráfica

La interfaz ha sido diseñada con un enfoque minimalista y fácil de usar. Permite a los usuarios:

- **Agregar restricciones**: Con campos para ingresar los coeficientes y el término independiente de cada restricción.
- **Agregar variables**: Las nuevas variables se añaden automáticamente a la función objetivo y a las restricciones existentes.
- **Eliminar restricciones**: Con un solo clic, puedes eliminar restricciones innecesarias.
- **Definir la función objetivo**: Introduce los coeficientes para cada variable de la función a maximizar.

### Proceso para resolver un problema

1. **Agregar restricciones**: Añade tantas restricciones como necesites utilizando los campos correspondientes.
2. **Agregar variables**: Si el problema requiere más variables, puedes agregarlas fácilmente.
3. **Eliminar restricciones**: Si ya no necesitas una restricción, puedes eliminarla.
4. **Definir la función objetivo**: Introduce los valores de la función objetivo.
5. **Resolver**: Haz clic en el botón de "Resolver" para obtener el resultado.



## Nota importante

El algoritmo está diseñado para resolver **problemas de maximización** donde **todas las restricciones son ≤**.

---

¡Con esto estarás listo para usar Simplex App para resolver tus problemas de programación lineal!

--- 

### Acceso a la aplicación

Puedes acceder a la aplicación web en el siguiente enlace: [**https://thisisjosepablo2.pythonanywhere.com/**].

