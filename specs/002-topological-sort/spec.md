# Feature Specification: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`

**Created**: 2026-10-31

**Status**: Clarified

**Input**: User description: "Feature 2: ordenamiento topológico de grafos dirigidos y diagnóstico preciso de ciclos."

## Clarifications

### Session 2026-10-31

- Q: ¿Cuál es la sintaxis exacta de invocación y el formato de salida para el ordenamiento topológico? (FR-013, FR-014) → A: Se invoca con la bandera `--sort` (ej. `py -m graphlab <path_to_csv> --sort`). Cuando el grafo es un DAG, `stdout` emite el encabezado `Topological Order:` seguido de cada vértice indentado por dos espacios en orden topológico.
- Q: ¿Cómo se resuelven los empates cuando múltiples vértices tienen todas sus dependencias resueltas? (FR-015) → A: Regla determinista lexicográfica estricta: entre los vértices listos para ser ordenados, se selecciona siempre el menor en orden alfabético ascendente.
- Q: ¿Cómo debe estructurarse el diagnóstico en `stderr` cuando se detecten ciclos? (FR-016, FR-017, FR-018) → A: Se imprime un mensaje indicando que el grafo contiene ciclos y que el orden topológico no es posible, seguido del desglose explícito de los ciclos identificados (incluyendo auto-bucles y ciclos indirectos) y, por separado, la lista de vértices bloqueados que no forman parte de ningún ciclo pero dependen de uno. La aplicación finaliza con código de salida 1.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ordenamiento Topológico Determinista de Grafos Acíclicos (Priority: P1)

Como usuario que necesita planificar tareas o compilar paquetes, quiero solicitar un orden topológico válido del grafo de dependencias para procesar cada elemento antes que todos aquellos que dependen de él.

**Why this priority**: Es la funcionalidad principal de la Feature 2. Permite resolver el problema de secuenciación de dependencias para cualquier DAG.

**Independent Test**: Se prueba ejecutando la herramienta con `--sort` sobre archivos acíclicos (`small-dag.csv` y `cs-curriculum.csv`), verificando que cada vértice anteceda a sus sucesores y que la secuencia sea determinista.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario ejecuta `py -m graphlab data/small-dag.csv --sort`, **Then** el sistema emite el orden topológico determinista de los 9 vértices donde para toda arista `u -> v`, `u` aparece antes que `v` con desempate lexicográfico, con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario ejecuta `py -m graphlab data/cs-curriculum.csv --sort`, **Then** el sistema emite el orden topológico determinista de los 19 cursos donde cada prerrequisito antecede a sus cursos dependientes, con código de salida 0.

---

### User Story 2 - Diagnóstico Preciso de Ciclos y Vértices Bloqueados (Priority: P1)

Como usuario que analiza dependencias defectuosas, quiero que el sistema detecte si el grafo contiene ciclos, rechace el ordenamiento topológico y explique con precisión qué elementos forman ciclos y cuáles están bloqueados sin formar parte de un ciclo.

**Why this priority**: Permite al usuario diagnosticar y corregir dependencias circulares sin confundir paquetes que causan el ciclo con paquetes que solo son víctimas colaterales bloqueadas.

**Independent Test**: Se prueba invocando el ordenamiento sobre `data/build-with-cycle.csv`, comprobando que finaliza con código de salida 1, emite error a `stderr`, e identifica el ciclo (`auth -> session -> user-profile -> auth` y el bucle `metrics -> metrics`) distinguiéndolo de nodos dependientes bloqueados (`api`, `web`).

**Acceptance Scenarios**:

1. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario ejecuta `py -m graphlab data/build-with-cycle.csv --sort`, **Then** el sistema detecta ciclos, imprime en `stderr` los ciclos detectados (`metrics -> metrics`, `auth -> session -> user-profile -> auth`) y lista los vértices bloqueados no pertenecientes al ciclo (`api`, `web`), finalizando con código de salida 1.

---

### User Story 3 - Integración Fluida en la Interfaz CLI (Priority: P2)

Como usuario de la herramienta, quiero solicitar el ordenamiento topológico mediante la opción `--sort` manteniendo el comportamiento de inspección de la Feature 1 cuando no se use dicha opción.

**Why this priority**: Preserva la compatibilidad con Feature 1 y añade la nueva funcionalidad de forma limpia.

**Independent Test**: Se prueba ejecutando la CLI con y sin `--sort` comprobando la salida esperada en cada caso.

**Acceptance Scenarios**:

1. **Given** cualquier grafo válido, **When** el usuario no pasa la opción `--sort`, **Then** se ejecuta la visualización de Feature 1 con código de salida 0.
2. **Given** un DAG válido, **When** el usuario especifica `--sort`, **Then** se muestra el orden topológico con código de salida 0.

---

### Edge Cases

- **Múltiples órdenes válidos**: La regla de desempate determinista es el orden lexicográfico entre vértices sin dependencias pendientes.
- **Vértices aislados**: Tienen in-degree 0 desde el inicio; son seleccionados cuando su orden lexicográfico corresponda.
- **Auto-bucles reflexivos (`metrics,metrics`)**: Se diagnostican como ciclos de longitud 1.
- **Ciclos indirectos con nodos bloqueados**: Diferenciar entre vértices en ciclos y vértices aguas abajo (*downstream*).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-013**: El sistema DEBE admitir la opción `--sort` en la invocación por línea de comandos para solicitar el ordenamiento topológico.
- **FR-014**: Para cualquier grafo acíclico dirigido (DAG), el sistema DEBE generar una secuencia completa de todos sus vértices tal que si existe la arista dirigida `u -> v`, `u` preceda estrictamente a `v` en la salida.
- **FR-015**: Ante múltiples órdenes topológicos válidos, el sistema DEBE aplicar una regla de desempate determinista basada en el orden lexicográfico ascendente de los vértices listos.
- **FR-016**: El sistema DEBE detectar la presencia de ciclos dirigidos (tanto auto-bucles como ciclos indirectos entre múltiples vértices).
- **FR-017**: Cuando el grafo contenga uno o más ciclos, el sistema DEBE rechazar la generación del ordenamiento topológico, emitir un mensaje de diagnóstico a `stderr` y finalizar con código de salida 1.
- **FR-018**: En el diagnóstico de ciclos, el sistema DEBE distinguir explícitamente entre los vértices que forman parte de los ciclos y los vértices que están bloqueados por depender de ellos sin pertenecer a ningún ciclo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-006**: El cálculo del orden topológico en DAGs de referencia se completa en menos de 100 milisegundos.
- **SC-007**: El 100% de los órdenes topológicos emitidos son formalmente válidos (verificable mediante oráculo de pruebas).
- **SC-008**: Para `build-with-cycle.csv`, el sistema reporta con exactitud los ciclos reales sin atribuir condición de ciclo a los vértices dependientes `api` o `web`.
- **SC-009**: Las salidas ante grafos acíclicos son 100% deterministas e idénticas en cualquier entorno.

## Assumptions

- **A-005**: La bandera `--sort` puede colocarse antes o después de la ruta del archivo CSV.
- **A-006**: Si no se pasa `--sort`, la aplicación preserva íntegramente el comportamiento de inspección de Feature 1.
