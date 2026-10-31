# GraphLab — Procesamiento de Grafos de Dependencias y Ordenamiento Topológico

Aplicación de línea de comandos en **Python 3.11+** para la carga, validación, visualización e inspección de grafos dirigidos de dependencias, así como el cálculo de su **ordenamiento topológico determinista** y el diagnóstico exhaustivo de **ciclos dirigidos**.

Desarrollada íntegramente mediante la metodología **Spec-Driven Development** con [Spec Kit](https://github.com/github/spec-kit), cumpliendo con la restricción de **cero bibliotecas de grafos en producción** (implementación propia de estructuras y algoritmos).

---

## Características Principales

* **Implementación Propia de Grafos**: Estructura en memoria de lista de adyacencia optimizada ($O(V + E)$ en espacio y $O(1)$ en operaciones de arista), desarrollada exclusivamente con colecciones nativas de Python.
* **Ordenamiento Topológico Determinista**: Algoritmo de Kahn asistido por cola de prioridad (min-heap con `heapq`), garantizando resolución determinista de empates en orden alfabético ascendente ($O(V \log V + E)$).
* **Diagnóstico Preciso de Ciclos**: Identificación de Componentes Fuertemente Conexas (SCC con algoritmo de Tarjan) que diferencia con rigor matemático entre vértices pertenecientes a ciclos y vértices dependientes bloqueados aguas abajo.
* **Manejo Robusto de Entrada**: Soporte transparente de UTF-8 con y sin BOM (`utf-8-sig`), tolerancia a espacios en blanco periféricos, descarte silencioso de líneas vacías e idempotencia en aristas repetidas.
* **Oráculos de Verificación**: Suite de pruebas automatizadas que utiliza `networkx` exclusivamente como oráculo de verificación para contrastar la exactitud matemática de los algoritmos propios.

---

## Requisitos e Instalación

### Requisitos del Sistema
* **Python 3.11** o superior (probado en Python 3.11 a 3.14).
* Sistema operativo: Linux, macOS o Windows.

### Instalación
Clonar el repositorio y situarse en el directorio raíz:

```bash
git clone https://github.com/heifryl/spec-kit-graph-lab.git
cd spec-kit-graph-lab
```

Para ejecutar la aplicación en producción **no se requiere instalar ninguna dependencia externa** (solo la biblioteca estándar de Python).

Para ejecutar la suite de pruebas automatizadas y los oráculos:

```bash
pip install pytest networkx
```

---

## Uso de la Línea de Comandos (CLI)

La herramienta puede invocarse como módulo ejecutable:

```bash
python -m graphlab <ruta_del_csv> [--sort]
# En Windows:
py -m graphlab <ruta_del_csv> [--sort]
```

### Opciones
* `<ruta_del_csv>`: Ruta al archivo CSV con formato `source,target`.
* `--sort`: *(Opcional)* Solicita el ordenamiento topológico del grafo en lugar de la visualización estructural.

---

## Ejemplos con Conjuntos de Datos Reales

### 1. Grafo Acíclico Pequeño (`data/small-dag.csv`)

Representa dependencias de vestimenta matutina (CLRS, Fig. 22.7). Contiene **9 vértices** y **9 aristas dirigidas**, incluyendo el vértice aislado `watch`.

#### Visualización Estructural (Feature 1):
```bash
py -m graphlab data/small-dag.csv
```
**Salida en `stdout`:**
```text
Vertices: 9
Edges: 9

Vertices:
  belt
  jacket
  pants
  shirt
  shoes
  socks
  tie
  undershorts
  watch

Edges:
  belt -> jacket
  pants -> belt
  pants -> shoes
  shirt -> belt
  shirt -> tie
  socks -> shoes
  tie -> jacket
  undershorts -> pants
  undershorts -> shoes
```

#### Ordenamiento Topológico Determinista (Feature 2):
```bash
py -m graphlab data/small-dag.csv --sort
```
**Salida en `stdout`:**
```text
Topological Order:
  shirt
  socks
  tie
  undershorts
  pants
  belt
  jacket
  shoes
  watch
```

---

### 2. Plan de Estudios de Ciencias de la Computación (`data/cs-curriculum.csv`)

Representa los prerrequisitos académicos de una carrera universitaria. Contiene **19 cursos únicos** y **23 aristas dirigidas** (la repetición de `Data Structures,Algorithms` se deduplica silenciosamente).

#### Visualización Estructural:
```bash
py -m graphlab data/cs-curriculum.csv
```
**Salida en `stdout`:**
```text
Vertices: 19
Edges: 23

Vertices:
  Algorithms
  Calculus I
  Calculus II
  Capstone Project
  Compilers
  Computer Architecture
  Computer Networks
  Data Structures
  Databases
  Discrete Mathematics
  Distributed Systems
  Linear Algebra
  Machine Learning
  Object-Oriented Programming
  Operating Systems
  Probability and Statistics
  Programming Fundamentals
  Software Engineering
  Theory of Computation

Edges:
  Algorithms -> Compilers
  Algorithms -> Machine Learning
  Calculus I -> Calculus II
  Calculus I -> Linear Algebra
  Calculus II -> Probability and Statistics
  Computer Architecture -> Operating Systems
  Computer Networks -> Distributed Systems
  Data Structures -> Algorithms
  Data Structures -> Databases
  Data Structures -> Operating Systems
  Databases -> Software Engineering
  Discrete Mathematics -> Data Structures
  Discrete Mathematics -> Theory of Computation
  Distributed Systems -> Capstone Project
  Linear Algebra -> Machine Learning
  Object-Oriented Programming -> Data Structures
  Object-Oriented Programming -> Software Engineering
  Operating Systems -> Distributed Systems
  Probability and Statistics -> Machine Learning
  Programming Fundamentals -> Computer Architecture
  Programming Fundamentals -> Object-Oriented Programming
  Software Engineering -> Capstone Project
  Theory of Computation -> Compilers
```

#### Ordenamiento Topológico:
```bash
py -m graphlab data/cs-curriculum.csv --sort
```
**Salida en `stdout`:**
```text
Topological Order:
  Calculus I
  Calculus II
  Computer Networks
  Discrete Mathematics
  Linear Algebra
  Probability and Statistics
  Programming Fundamentals
  Computer Architecture
  Object-Oriented Programming
  Data Structures
  Algorithms
  Databases
  Machine Learning
  Operating Systems
  Distributed Systems
  Software Engineering
  Capstone Project
  Theory of Computation
  Compilers
```

---

### 3. Grafo con Ciclos de Compilación (`data/build-with-cycle.csv`)

Representa dependencias de módulos de software con interbloqueos circulares. Contiene **11 paquetes** y **13 aristas**, incluyendo un auto-bucle (`metrics -> metrics`) y un ciclo multilateral (`auth -> session -> user-profile -> auth`).

#### Visualización Estructural (Feature 1):
```bash
py -m graphlab data/build-with-cycle.csv
```
**Salida en `stdout` (Código de salida: 0):**
```text
Vertices: 11
Edges: 13

Vertices:
  api
  auth
  config
  core
  logging
  metrics
  session
  storage
  user-profile
  utils
  web

Edges:
  api -> web
  auth -> api
  auth -> session
  config -> core
  core -> auth
  core -> storage
  logging -> core
  metrics -> metrics
  session -> user-profile
  storage -> api
  user-profile -> auth
  utils -> config
  utils -> logging
```

#### Diagnóstico de Ciclos al Solicitar Ordenamiento (Feature 2):
```bash
py -m graphlab data/build-with-cycle.csv --sort
```
**Salida en `stderr` (Código de salida: 1):**
```text
Error: Graph contains cycle(s). Topological ordering is not possible.
Cycles detected:
  - metrics -> metrics
  - auth -> session -> user-profile -> auth
Blocked vertices (not in cycle):
  - api
  - web
```

---

## Códigos de Salida del CLI

| Código | Significado | Ejemplos de Causa |
| :---: | :--- | :--- |
| **`0`** | Éxito | Visualización completada u orden topológico generado correctamente en `stdout`. |
| **`1`** | Error de Validación o Datos | Archivo CSV vacío, cabecera inválida, fila malformada (ej. `,target`), o presencia de ciclos al solicitar `--sort`. |
| **`2`** | Error de Acceso o Parámetros | Archivo no encontrado, permisos denegados o argumentos de CLI ausentes/inválidos. |

---

## Explicación de Anomalías en los Datos de Muestra

1. **Vértices Aislados (`watch,` en `small-dag.csv`)**:
   * Línea 11 contiene `watch,` (un origen sin destino).
   * La aplicación lo reconoce como la declaración de un vértice sin aristas salientes ni entrantes. Se contabiliza en los vértices del grafo sin generar aristas fantasmas.
2. **Aristas Duplicadas (`Data Structures,Algorithms` en `cs-curriculum.csv`)**:
   * La relación se repite textualmente en las líneas 11 y 25.
   * La aplicación deduplica las aristas en tiempo $O(1)$ usando conjuntos matemáticos de forma silenciosa e idempotente, preservando la exactitud del conteo estructural (23 aristas únicas).
3. **Auto-bucles Reflexivos (`metrics,metrics` en `build-with-cycle.csv`)**:
   * Línea 14 declara un vértice que depende de sí mismo.
   * Es una arista válida en Feature 1; en Feature 2, el diagnóstico de ciclos la identifica de inmediato como un ciclo elemental de longitud 1.
4. **Ciclos vs. Vértices Bloqueados (`build-with-cycle.csv`)**:
   * `auth -> session -> user-profile -> auth` forman un ciclo cerrado.
   * Vértices como `api` y `web` no forman parte de ningún ciclo, pero no pueden procesarse porque dependen de `auth`. El analizador de componentes fuertemente conexas (SCC) los distingue con precisión matemática.

---

## Ejecución de Pruebas Automatizadas

La suite incluye 41 pruebas automatizadas que cubren unitarias, integración del CLI y oráculos con NetworkX:

```bash
# Configurar PYTHONPATH y ejecutar todas las pruebas
pytest tests/ -v
```

### Categorías de Pruebas:
- `tests/test_core.py`: Operaciones in-memory de `DirectedGraph` (adición, deduplicación, bucles, getters ordenados).
- `tests/test_loader.py`: Casos de borde de CSV (BOM, espacios en blanco, filas sin origen, cabeceras erróneas).
- `tests/test_algo.py`: Algoritmo de Kahn, min-heap tie-break y Tarjan SCC para aislamiento de ciclos vs bloqueados.
- `tests/test_cli.py`: Invocación de subprocesos sobre el CLI verificando códigos de salida, `stdout` y `stderr`.
- `tests/test_oracle.py`: Contrastación formal de conteos y ordenamientos topológicos contra `networkx`.

---

## Integración Continua (CI)

El proyecto cuenta con un flujo automatizado de GitHub Actions configurado en `.github/workflows/ci.yml`, el cual ejecuta la suite de pruebas bajo Python 3.11, 3.12, 3.13 y 3.14 en cada *push* y *pull request*.
