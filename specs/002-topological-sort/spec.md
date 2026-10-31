# Feature Specification: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`

**Created**: 2026-10-31

**Status**: Draft

**Input**: User description: "Feature 2: ordenamiento topológico de grafos dirigidos y diagnóstico preciso de ciclos."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ordenamiento Topológico Determinista de Grafos Acíclicos (Priority: P1)

Como usuario que necesita planificar tareas o compilar paquetes, quiero solicitar un orden topológico válido del grafo de dependencias para procesar cada elemento antes que todos aquellos que dependen de él.

**Why this priority**: Es la funcionalidad principal de la Feature 2. Permite resolver el problema de secuenciación de dependencias para cualquier DAG.

**Independent Test**: Se prueba ejecutando la herramienta con la opción de ordenamiento sobre archivos acíclicos (`small-dag.csv` y `cs-curriculum.csv`), verificando que cada vértice anteceda a sus sucesores y que la secuencia sea determinista.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario solicita el orden topológico, **Then** el sistema emite una secuencia válida de los 9 vértices donde para toda arista `u -> v`, `u` aparece antes que `v` (resolviendo empates lexicográficamente), con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario solicita el orden topológico, **Then** el sistema emite un orden topológico válido de los 19 cursos donde cada prerrequisito antecede a sus cursos dependientes, con código de salida 0.

---

### User Story 2 - Diagnóstico Preciso de Ciclos y Vértices Bloqueados (Priority: P1)

Como usuario que analiza dependencias defectuosas, quiero que el sistema detecte si el grafo contiene ciclos, rechace el ordenamiento topológico y explique con precisión qué elementos forman ciclos y cuáles están bloqueados sin formar parte de un ciclo.

**Why this priority**: Permite al usuario diagnosticar y corregir dependencias circulares sin confundir paquetes que causan el ciclo con paquetes que solo son víctimas colaterales bloqueadas.

**Independent Test**: Se prueba invocando el ordenamiento sobre `data/build-with-cycle.csv`, comprobando que finaliza con código de salida no nulo, emite error a `stderr`, e identifica el ciclo (`auth -> session -> user-profile -> auth` y el bucle `metrics -> metrics`) distinguiéndolo de nodos dependientes bloqueados (`api`, `web`).

**Acceptance Scenarios**:

1. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario solicita el orden topológico, **Then** el sistema detecta la presencia de ciclos, no emite un orden topológico falso, imprime un reporte explicativo en `stderr` identificando los ciclos encontrados y los vértices bloqueados, y termina con código de salida 1.

---

### User Story 3 - Integración Fluida en la Interfaz CLI (Priority: P2)

Como usuario de la herramienta, quiero solicitar el ordenamiento topológico mediante una opción de línea de comandos clara (`--sort`) manteniendo el comportamiento de inspección de la Feature 1 cuando no se use dicha opción.

**Why this priority**: Preserva la compatibilidad con Feature 1 y añade la nueva funcionalidad de forma limpia.

**Independent Test**: Se prueba ejecutando la CLI con y sin `--sort` comprobando la salida esperada en cada caso.

**Acceptance Scenarios**:

1. **Given** cualquier grafo válido, **When** el usuario no pasa banderas, **Then** se ejecuta la visualización de Feature 1.
2. **Given** un DAG válido, **When** el usuario especifica `--sort`, **Then** se muestra el orden topológico.

---

### Edge Cases

- **Múltiples órdenes válidos**: La regla de desempate debe ser determinista (orden lexicográfico entre vértices sin dependencias pendientes).
- **Vértices aislados**: Aparecen en el orden topológico en el momento que su orden lexicográfico lo determine.
- **Auto-bucles reflexivos (`metrics,metrics`)**: Debe diagnosticarse de inmediato como un ciclo de longitud 1.
- **Ciclos indirectos con nodos bloqueados**: Diferenciar entre vértices en componentes fuertemente conexas cíclicas y vértices aguas abajo (*downstream*).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-013**: El sistema DEBE permitir solicitar el ordenamiento topológico del grafo mediante la opción `--sort` en la línea de comandos.
- **FR-014**: Para cualquier grafo acíclico dirigido (DAG), el sistema DEBE generar una secuencia completa de todos sus vértices tal que si existe la arista dirigida `u -> v`, `u` preceda estrictamente a `v` en la salida.
- **FR-015**: Ante múltiples órdenes topológicos válidos, el sistema DEBE aplicar una regla de desempate determinista basada en el orden lexicográfico de los vértices elegibles.
- **FR-016**: El sistema DEBE detectar la presencia de ciclos dirigidos (tanto auto-bucles como ciclos entre múltiples vértices).
- **FR-017**: Cuando el grafo contenga uno o más ciclos, el sistema DEBE rechazar la generación del ordenamiento topológico, emitir un mensaje de diagnóstico a `stderr` y finalizar con código de salida 1.
- **FR-018**: En el diagnóstico de ciclos, el sistema DEBE distinguir explícitamente entre los vértices que forman parte de los ciclos y los vértices que están bloqueados por depender de ellos sin pertenecer a ningún ciclo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-006**: El cálculo del orden topológico en DAGs de referencia se completa en menos de 100 milisegundos.
- **SC-007**: El 100% de los órdenes topológicos emitidos son formalmente válidos (verificable mediante oráculo de pruebas).
- **SC-008**: Para `build-with-cycle.csv`, el sistema reporta con exactitud los ciclos reales sin atribuir condición de ciclo a los vértices dependientes `api` o `web`.
- **SC-009**: Las salidas ante grafos acíclicos son 100% deterministas e idénticas en cualquier entorno.

## Assumptions

- **A-005**: La bandera `--sort` se proporciona junto a la ruta del archivo CSV.
- **A-006**: Si no se pasa `--sort`, la aplicación preserva íntegramente el comportamiento de inspección de Feature 1.
