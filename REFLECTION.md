# Reflexión del Proceso: Desarrollo Guiado por Especificaciones (Spec Kit)

**Proyecto**: GraphLab (Laboratorio 2: Grafos y Ordenamiento Topológico)  
**Entorno y Agente**: Google DeepMind Antigravity (Gemini 3.8 Flash High) con integración oficial `agy` de Spec Kit (v1.2.3)  
**Fecha**: Octubre 2026  

---

## 1. Agente e Integración Utilizados

Para este laboratorio se utilizó **Google Antigravity** en su versión CLI / Agentic IDE, empleando el modelo **Gemini 3.8 Flash**. La integración con Spec Kit se realizó mediante el preset y las habilidades oficiales para Antigravity (`agy`), registradas en `.specify/integration.json` y desplegadas en `.agents/skills/`.

### Aspectos que facilitaron el proceso:
- **Ejecución rigurosa del flujo por fases**: La separación explícita de comandos (`speckit-constitution`, `speckit-specify`, `speckit-clarify`, `speckit-plan`, `speckit-tasks`, `speckit-analyze`, `speckit-implement`) impidió la tentación común de saltar directamente al código antes de tener requisitos y diseños verificados.
- **Trazabilidad estricta**: El entorno permitió crear ramas independientes (`001-directed-graphs`, `002-topological-sort`), aislar artefactos de diseño en carpetas de especificaciones (`specs/001-*/`, `specs/002-*/`) y generar commits atómicos por cada etapa.

### Limitaciones y fricciones encontradas:
- **Interpretación inicial de conteos de datos**: Al analizar por primera vez `data/small-dag.csv`, se produjo una confusión inicial entre el número de filas de datos (10 filas) y el número de vértices únicos conectados e independientes (9 vértices: 8 conectados + 1 aislado `watch`). Fue indispensable contrastar los datos línea por línea y verificar con la fuente clásica del algoritmo (CLRS, Fig. 22.7) para disipar cualquier duda.
- **Manejo de codificación de caracteres en Windows**: La consola de PowerShell bajo codepage OEM mostró en lecturas directas caracteres con acentos distorsionados, lo que requirió verificar a nivel de bytes (`open(..., 'rb')` y `utf-8-sig`) que los archivos en disco se preservaran en UTF-8 puro sin corrupciones.

---

## 2. Preguntas de Clarificación y Decisiones

### Feature 1 — Carga y Visualización de Grafos Dirigidos:
1. **Modo de presentación y orden en CLI**:
   - *Decisión*: Salida integrada única y determinista que imprime conteos, lista de vértices y lista de aristas ordenados lexicográficamente. Se descartó agregar flags opcionales de filtrado para evitar complejidad innecesaria (KISS).
2. **Filas con sintaxis `,destino` (sin origen)**:
   - *Decisión*: Rechazar como fila malformada con mensaje en `stderr` y código de salida 1. La declaración de un vértice sin aristas salientes es exclusivamente `vertice,`, la cual tiene carácter aditivo e idempotente.
3. **Tratamiento de aristas duplicadas**:
   - *Decisión*: Deduplicación silenciosa idempotente. Se admiten bucles reflexivos (`u -> u`), configurando un grafo dirigido con bucles pero sin aristas paralelas (no multigrafo).
4. **Espacios en blanco exteriores**:
   - *Decisión*: Normalizar identificadores ignorando espacios iniciales y finales sin filtrar caracteres internos, manteniendo distinción de mayúsculas/minúsculas (*case-sensitive*).

### Feature 2 — Ordenamiento Topológico y Diagnóstico de Ciclos:
1. **Invocación y formato del ordenamiento**:
   - *Decisión*: Usar la opción `--sort`. En éxito, imprimir encabezado `Topological Order:` seguido de los nodos ordenados uno por línea con sangría.
2. **Regla de desempate en orden topológico**:
   - *Decisión*: Desempate determinista lexicográfico (alfabético ascendente) entre todos los nodos listos con in-degree 0.
3. **Estructura del diagnóstico de ciclos**:
   - *Decisión*: Ante ciclos, abortar el ordenamiento topológico, emitir código de salida 1 y separar explícitamente en `stderr` las secuencias de ciclo reales de los vértices dependientes bloqueados.

### ¿Cuál decisión fue la más difícil y por qué?
La decisión más exigente fue la **diferenciación entre vértices en ciclo y vértices bloqueados** en la Feature 2. Inicialmente, al usar solo el algoritmo de Kahn, los vértices no ordenados forman un conjunto genérico con in-degree > 0. Sin embargo, en `build-with-cycle.csv`, `api` y `web` no forman parte de ningún ciclo; simplemente dependen de `auth`, que a su vez está atrapado en un ciclo con `session` y `user-profile`. Si la herramienta hubiese reportado a `api` o `web` como parte del ciclo, el usuario que intenta depurar sus dependencias recibiría información falsa. Fue necesario planificar un análisis de Componentes Fuertemente Conexas (SCC con algoritmo de Tarjan) sobre el subgrafo no programado para aislar los ciclos verdaderos.

---

## 3. Anomalías en los Datos de Muestra y su Manejo

1. **`data/small-dag.csv` — Vértice Aislado (`watch,`)**:
   - *Anomalía*: Fila con origen pero sin destino.
   - *Comportamiento*: Se registra `watch` en el conjunto de vértices `_vertices`, pero no se genera ninguna arista saliente hacia cadena vacía. En la visualización aparece en la lista de vértices y en el conteo total (9 vértices, 9 aristas). En el orden topológico, tiene in-degree 0 y entra al min-heap normalmente.
2. **`data/cs-curriculum.csv` — Arista Duplicada (`Data Structures,Algorithms`)**:
   - *Anomalía*: La dependencia se declara dos veces (líneas 11 y 25).
   - *Comportamiento*: Al usar conjuntos (`set`) para la adyacencia, la arista se inserta de forma idempotente sin duplicar el conteo de aristas (resultando en exactamente 23 aristas únicas sobre 19 vértices).
3. **`data/build-with-cycle.csv` — Auto-bucle (`metrics,metrics`) y Ciclo Indirecto**:
   - *Anomalía*: `metrics` apunta a sí mismo (ciclo trivial de longitud 1); `auth -> session -> user-profile -> auth` forma un ciclo de longitud 3; `api -> web` quedan bloqueados aguas abajo.
   - *Comportamiento*: En Feature 1, el auto-bucle se registra como arista válida dirigida. En Feature 2, el algoritmo detecta que no es un DAG, aísla `metrics -> metrics` y `auth -> session -> user-profile -> auth` en la sección de ciclos, y lista a `api` y `web` exclusivamente bajo `Blocked vertices (not in cycle)`.

---

## 4. Representación del Grafo en Memoria y su Evolución

### Estructura Elegida:
Lista de adyacencia implementada mediante colecciones nativas de Python:
- `_vertices: set[str]` para identificar el universo de vértices.
- `_adjacency: dict[str, set[str]]` para almacenar los sucesores de cada vértice.

### Alternativas Descartadas:
- **Matriz de Adyacencia (`list[list[int]]`)**: Descartada por su costo espacial $O(V^2)$ (desperdicio masivo en grafos esparcidos reales donde $E \ll V^2$) y la penalización de tener que redimensionar dinámicamente la matriz al leer nodos desde CSV.
- **Lista de Aristas (`list[tuple[str, str]]`)**: Descartada porque consultar sucesores o calcular in-degrees requiere búsquedas lineales $O(E)$, encareciendo los algoritmos de recorrido.
- **Librerías de Terceros (`networkx`, `graphlib`)**: Prohibidas en producción por la Constitución del proyecto.

### ¿Se sostuvo la elección en Feature 2?
Sí, la elección se sostuvo perfectamente. Kahn necesita iterar sobre los sucesores de cada nodo que se extrae de la cola para decrementar sus in-degrees, lo cual toma $O(\text{out-degree}(u))$ con nuestra lista de adyacencia. Asimismo, Tarjan para Componentes Fuertemente Conexas requiere recorrer vecinos adyacentes en tiempo $O(V + E)$. No fue necesario reescribir ni romper la estructura de datos base de Feature 1; únicamente se añadieron métodos de consulta limpia (`get_successors()`).

---

## 5. Reporte de `/speckit-analyze` y Ajustes Realizados

El comando de análisis de consistencia cruzada arrojó:
- **En Feature 1**:
  - *Hallazgos*: 0 Críticos, 0 Altos, 1 Medio, 1 Bajo.
  - *Ajuste Realizado*: El hallazgo medio observó que invocar `python -m graphlab.cli` era funcional pero menos conveniente que el estándar `python -m graphlab`. Se creó `src/graphlab/__main__.py` delegando en `cli.main()`, permitiendo ambas invocaciones. Se confirmó el 100% de cobertura entre los requisitos funcionales FR-001..FR-012 y las tareas T001..T014.
- **En Feature 2**:
  - *Hallazgos*: 0 Críticos, 0 Altos, 0 Medios, 0 Bajos.
  - *Ajuste Realizado*: Verificación plena de alineación con la constitución, oráculo NetworkX y correspondencia unívoca entre requisitos FR-013..FR-018 y tareas T015..T024.

---

## 6. Discrepancias y Desviaciones del Proceso

Un momento ilustrativo ocurrió durante la ejecución de las pruebas unitarias de `test_loader.py` para la comprobación del soporte de codificación UTF-8 con BOM:
- *Situación*: En la prueba `test_whitespace_trimmed_and_bom_support`, el archivo se escribió inicialmente usando el helper `bom_file.write_text(content, encoding='utf-8-sig')` con una cadena que ya contenía explícitamente el caracter `\ufeff`. Python escribió el BOM dos veces (uno por la codificación y otro por el caracter de texto). Al leerlo, el decodificador removió el BOM físico a nivel de bytes, pero dejó intacto el segundo caracter `\ufeff` al inicio de `source`, provocando que el encabezado leído fuese `\ufeffsource` en lugar de `source`.
- *Diagnóstico*: La especificación exigía soporte robusto ante archivos CSV provenientes de editores de Windows (como Excel) que agregan BOM.
- *Corrección*: Se ajustó `CSVLoader` para aplicar `.lstrip("\ufeff")` al primer token además del estándar `utf-8-sig`, blindando la lectura contra cualquier doble marca de orden de bytes, y se corrigió la prueba escribiendo los bytes crudos `b"\xef\xbb\xbfsource,target..."`.
