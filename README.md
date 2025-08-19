# Proyecto: Puzzle y Maze Solver

Este proyecto implementa algoritmos de búsqueda para resolver problemas de inteligencia artificial, específicamente el **8-Puzzle** y el **Maze Solver**. La aplicación está desarrollada en Python utilizando el framework **Kivy** para la interfaz gráfica.

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Algoritmos Implementados](#algoritmos-implementados)
4. [Heurísticas](#heurísticas)
5. [Instrucciones de Uso](#instrucciones-de-uso)
6. [Requisitos](#requisitos)
7. [Ejemplo de Uso](#ejemplo-de-uso)
8. [Créditos](#créditos)

---

## Descripción General

El proyecto incluye dos módulos principales:

- **8-Puzzle Solver**: Resuelve el problema del 8-puzzle utilizando algoritmos de búsqueda como BFS, DFS, A*, entre otros.
- **Maze Solver**: Encuentra el camino más corto en un laberinto desde un punto de inicio hasta un objetivo.

Ambos módulos permiten al usuario seleccionar algoritmos y heurísticas para observar su comportamiento y rendimiento.

---

## Estructura del Proyecto

```
Project/
├── main.py                # Menú principal de la aplicación
├── utils.py               # Utilidades generales (colas, pilas, manejo de errores)
├── puzzle/
│   ├── ui.py              # Interfaz gráfica del 8-Puzzle
│   ├── state.py           # Representación del estado del puzzle
│   ├── heuristics.py      # Heurísticas para el 8-Puzzle
│   ├── algorithms.py      # Algoritmos de búsqueda para el 8-Puzzle
├── maze/
│   ├── ui.py              # Interfaz gráfica del Maze Solver
│   ├── state.py           # Representación del estado del laberinto
│   ├── heuristics.py      # Heurísticas para el Maze Solver
│   ├── algorithms.py      # Algoritmos de búsqueda para el Maze Solver
```

---

## Algoritmos Implementados

### 8-Puzzle Solver
- **BFS (Breadth-First Search)**: Búsqueda en amplitud.
- **DFS (Depth-First Search)**: Búsqueda en profundidad.
- **UCS (Uniform Cost Search)**: Búsqueda de costo uniforme.
- **A***: Búsqueda informada con heurísticas.
- **IDA***: Búsqueda iterativa con heurísticas.
- **Greedy Search**: Búsqueda voraz.
- **RBFS (Recursive Best-First Search)**: Búsqueda recursiva.
- **Bidirectional Search**: Búsqueda bidireccional.

### Maze Solver
- **BFS**: Encuentra el camino más corto explorando en amplitud.
- **A***: Utiliza heurísticas para optimizar la búsqueda.
- **Greedy Search**: Prioriza los nodos más cercanos al objetivo.

---

## Heurísticas

### 8-Puzzle
1. **Manhattan Distance**: Suma de las distancias Manhattan de cada ficha a su posición objetivo.
2. **Misplaced Tiles**: Número de fichas fuera de lugar.
3. **Linear Conflict**: Extiende la distancia Manhattan considerando conflictos lineales.

### Maze Solver
1. **Manhattan Distance**: Distancia Manhattan entre dos puntos.
2. **Euclidean Distance**: Distancia euclidiana entre dos puntos.
3. **Chebyshev Distance**: Distancia máxima entre las coordenadas.

---

## Instrucciones de Uso

1. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

2. **Seleccionar un módulo**:
   - **8-Puzzle Solver**: Resolver el problema del 8-puzzle.
   - **Maze Solver**: Resolver un laberinto.

3. **Configurar parámetros**:
   - Seleccionar el algoritmo de búsqueda.
   - Elegir la heurística (si aplica).

4. **Interacción**:
   - En el **8-Puzzle**, puedes mezclar el tablero o resolverlo.
   - En el **Maze Solver**, puedes editar el laberinto y resolverlo.

---

## Requisitos

- **Python 3.7+**
- **Kivy**: Framework para la interfaz gráfica.
- **Dependencias adicionales**:
  - `pip install kivy`

---

## Ejemplo de Uso

### 8-Puzzle Solver
1. Selecciona el algoritmo "A* Manhattan".
2. Presiona el botón "Resolver".
3. Observa los pasos necesarios, nodos expandidos y tiempo de ejecución.

### Maze Solver
1. Edita el laberinto para agregar paredes.
2. Selecciona el algoritmo "BFS".
3. Presiona "Resolver" para encontrar el camino más corto.

---

## Créditos

- **Autor**: Santiago Castañeda Pérez
- **Curso**: Inteligencia Artificial
- **Institución**: UTP
