# Feature Specification: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`

**Created**: 2026-10-30

**Status**: Clarified

**Input**: User description: "Feature 1: cargar y visualizar un grafo dirigido sin pesos desde un archivo CSV."

## Clarifications

### Session 2026-10-30

- Q: ¿Cómo debe ser el modo de presentación y orden en el CLI? (FR-005) → A: Salida integrada y determinista en `stdout` que presenta el conteo cuantitativo de vértices y aristas, seguido por la lista de todos los vértices y la lista de todas las aristas (`origen -> destino`), ambas ordenadas lexicográficamente en orden alfabético ascendente. No se agregan flags opcionales de filtrado para mantener la interfaz simple.
- Q: ¿Cómo debe tratarse una fila con sintaxis `,destino` (sin origen)? (FR-007) → A: Se rechaza como fila malformada, finalizando con código de salida 1 y mensaje de error en `stderr`. La declaración de un vértice sin aristas salientes es exclusivamente `vertice,`; esta declaración es aditiva e idempotente, por lo que no elimina ninguna arista previa o posterior que otras filas hayan definido para ese vértice.
- Q: ¿Cómo deben tratarse las aristas duplicadas en el archivo CSV? (FR-008) → A: Se deduplican silenciosamente de forma idempotente, sin emitir advertencias en consola. El modelo resultante es un grafo dirigido que admite auto-bucles reflexivos (`u -> u`), pero no aristas paralelas (multigrafo).
- Q: ¿Cómo se normalizan los identificadores de vértices respecto a espacios en blanco exteriores? (FR-010) → A: El sistema ignora los espacios en blanco iniciales y finales en los nombres de los vértices (haciendo que `"  A  "` y `"A"` correspondan exactamente al mismo vértice observable `"A"`), preservando la distinción entre mayúsculas y minúsculas en el texto.
- Q: ¿Cuáles son los conteos estructurales exactos de los archivos de prueba oficiales? (FR-003, Escenarios de Aceptación) → A:
  - `data/small-dag.csv`: 9 vértices únicos (`belt`, `jacket`, `pants`, `shirt`, `shoes`, `socks`, `tie`, `undershorts`, `watch`) y 9 aristas dirigidas (provenientes de 10 filas de datos: 9 aristas + 1 vértice aislado `watch,`).
  - `data/cs-curriculum.csv`: 19 vértices únicos y 23 aristas dirigidas (provenientes de 24 filas de datos, tras deduplicar silenciosamente la repetición de `Data Structures,Algorithms`).
  - `data/build-with-cycle.csv`: 11 vértices únicos y 13 aristas dirigidas (provenientes de 13 filas de datos, incluyendo la arista reflexiva `metrics -> metrics`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Carga y Consulta de Resumen Estructural (Priority: P1)

Como usuario de la herramienta de línea de comandos, quiero cargar un archivo CSV con dependencias dirigidas y consultar un resumen del grafo para conocer rápidamente la cantidad total de vértices y aristas que contiene.

**Why this priority**: Es la funcionalidad nuclear del producto mínimo viable (MVP). Permite verificar de inmediato si un archivo de dependencias fue procesado correctamente y su escala general.

**Independent Test**: Puede probarse de manera aislada ejecutando la herramienta con cualquier archivo CSV de dependencias y comprobando que emite los conteos correctos de vértices y aristas en la salida estándar sin errores.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario ejecuta la herramienta con dicho archivo, **Then** el sistema reporta exactamente 9 vértices y 9 aristas dirigidas en la salida estándar y finaliza con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario ejecuta la herramienta con dicho archivo, **Then** el sistema reporta exactamente 19 vértices y 23 aristas dirigidas en la salida estándar (habiendo deduplicado silenciosamente la arista repetida) y finaliza con código de salida 0.
3. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario ejecuta la herramienta con dicho archivo, **Then** el sistema reporta exactamente 11 vértices y 13 aristas dirigidas en la salida estándar (incluyendo el auto-bucle `metrics -> metrics`) y finaliza con código de salida 0.

---

### User Story 2 - Inspección Detallada de Vértices y Aristas (Priority: P1)

Como usuario que analiza dependencias complejas, quiero consultar el listado completo y ordenado de los vértices y de las aristas dirigidas para entender con precisión qué elementos existen y cómo se conectan entre sí.

**Why this priority**: La visualización completa es un requisito explícito del laboratorio para poder inspeccionar dependencias y auditar la estructura del grafo.

**Independent Test**: Se prueba ejecutando la herramienta sobre un archivo CSV y verificando que cada vértice y cada arista aparezca listado de forma determinista, lexicográficamente ordenada y legible.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario ejecuta la herramienta, **Then** la salida estándar muestra el listado ordenado alfabéticamente de los 9 vértices (`belt`, `jacket`, `pants`, `shirt`, `shoes`, `socks`, `tie`, `undershorts`, `watch`) y el listado ordenado de las 9 aristas dirigidas en formato `origen -> destino` (ej. `undershorts -> pants`), finalizando con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario ejecuta la herramienta, **Then** la salida estándar muestra los 19 vértices ordenados y las 23 conexiones dirigidas ordenadas sin duplicar la arista `Data Structures -> Algorithms`, finalizando con código de salida 0.
3. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario ejecuta la herramienta, **Then** la salida estándar lista los 11 paquetes ordenados y las 13 aristas ordenadas (incluyendo la arista cíclica reflexiva `metrics -> metrics`), finalizando con código de salida 0.

---

### User Story 3 - Robustez de Entrada y Diagnóstico de Anomalías (Priority: P2)

Como usuario que trabaja con datos del mundo real, quiero que la herramienta maneje apropiadamente anomalías comunes (espacios en blanco periféricos, codificación UTF-8 con o sin BOM) y rechace archivos corruptos, inexistentes o con filas malformadas con mensajes de error comprensibles.

**Why this priority**: Garantiza que la herramienta no falle silenciosamente ni exponga excepciones internas cuando los archivos presenten errores o variaciones no válidas de formato.

**Independent Test**: Se prueba invocando la herramienta con rutas de archivo inexistentes, archivos vacíos y archivos con formatos no conformes (ej. filas con `,destino` o número de campos erróneo), verificando que los errores vayan a `stderr` y el código de salida sea distinto de 0.

**Acceptance Scenarios**:

1. **Given** una ruta a un archivo que no existe en el disco, **When** el usuario intenta cargarlo, **Then** el sistema emite un mensaje de error claro en `stderr` explicando que el archivo no fue encontrado y termina con código de salida 2 (error de archivo / entrada).
2. **Given** un archivo CSV completamente vacío (0 bytes), **When** el usuario intenta cargarlo, **Then** el sistema emite un mensaje de error en `stderr` informando que el archivo carece de encabezado y datos válidos y termina con código de salida 1 (error de validación de datos).
3. **Given** un archivo CSV sin el encabezado `source,target` o con filas de más de 2 columnas, **When** el usuario intenta cargarlo, **Then** el sistema informa el error de estructura en `stderr` y termina con código de salida 1.
4. **Given** un archivo CSV con una fila con origen vacío como `,destino`, **When** el usuario intenta cargarlo, **Then** el sistema lo rechaza como fila malformada en `stderr` y termina con código de salida 1.

---

### Edge Cases

- **Vértice aislado con coma final (`watch,`)**: Fila válida que declara el vértice `watch` sin aristas dirigidas incidentes ni salientes desde esa línea. Si el vértice ya poseía aristas definidas en otras líneas, esta fila no las altera ni elimina.
- **Vértice sin origen con coma inicial (`,destino`)**: Fila malformada inválida. Debe rechazarse con error a `stderr` y código 1.
- **Aristas duplicadas (`Data Structures,Algorithms`)**: Múltiples declaraciones idénticas se deduplican silenciosamente en una sola arista dirigida en el grafo sin incrementar el conteo total ni advertencias en consola.
- **Auto-bucles reflexivos (`metrics,metrics`)**: Una arista dirigida donde el origen y el destino coinciden es admisible y se contabiliza como 1 arista válida en el resumen e inspección.
- **Espacios en blanco exteriores**: Espacios iniciales y finales en los identificadores de vértices son ignorados transparentemente; `"  Calculus I  "` se normaliza a `"Calculus I"`.
- **Sensibilidad a mayúsculas y minúsculas**: Se preserva la distinción de mayúsculas y minúsculas (`Calculus I` y `calculus i` son vértices distintos).
- **Codificación de texto**: Soporte transparente tanto para UTF-8 estándar como para UTF-8 con marca de orden de bytes (BOM).
- **Líneas en blanco**: Las líneas vacías o compuestas exclusivamente de espacios dentro del CSV se ignoran silenciosamente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE cargar un grafo dirigido a partir de un archivo en formato CSV provisto como argumento en la línea de comandos.
- **FR-002**: El sistema DEBE exigir la presencia de la cabecera `source,target` en la primera fila no vacía del archivo CSV (tolerando diferencias de mayúsculas/minúsculas y espacios en blanco periféricos en los nombres de columna).
- **FR-003**: El sistema DEBE calcular y presentar el resumen cuantitativo del grafo cargado: número total de vértices únicos y número total de aristas dirigidas únicas.
- **FR-004**: El sistema DEBE presentar la lista completa de vértices y la lista completa de aristas dirigidas en formato `u -> v`.
- **FR-005**: El sistema DEBE presentar en `stdout` una salida única, integrada y determinista que combine el resumen cuantitativo, la lista ordenada lexicográficamente de vértices y la lista ordenada lexicográficamente de aristas, sin requerir banderas o parámetros adicionales.
- **FR-006**: El sistema DEBE admitir filas con sintaxis `vértice,` como la declaración explícita de un vértice sin aristas salientes originadas en dicha fila, integrándolo al conjunto de vértices de forma aditiva e idempotente.
- **FR-007**: El sistema DEBE rechazar cualquier fila que omita el origen (como `,destino`) reportando un mensaje descriptivo en `stderr` y finalizando con código de salida 1.
- **FR-008**: El sistema DEBE deduplicar silenciosamente aristas dirigidas repetidas, asegurando que cada par dirigido `(source, target)` exista a lo sumo una vez en el grafo.
- **FR-009**: El sistema DEBE admitir aristas dirigidas reflexivas (auto-bucles `u -> u`), contabilizándolas como aristas dirigidas válidas.
- **FR-010**: El sistema DEBE normalizar los identificadores ignorando espacios en blanco al principio y al final de cada nombre, manteniendo la distinción exacta de mayúsculas y minúsculas del texto interior.
- **FR-011**: El sistema DEBE interpretar correctamente archivos de texto codificados en UTF-8 con o sin marca de orden de bytes (BOM).
- **FR-012**: El sistema DEBE validar rigurosamente el formato de entrada; ante archivos inexistentes, archivos sin datos o filas con cantidad de columnas distinta de 2, DEBE abortar de inmediato, emitir el mensaje correspondiente a `stderr` y finalizar con código de error no nulo (código 2 para error de acceso o inexistencia de archivo, código 1 para error de formato o validación de datos).

### Key Entities

- **Grafo Dirigido (Directed Graph)**: Estructura algebraica compuesta por un conjunto finito de vértices identificables unívocamente y un conjunto de aristas dirigidas que admite auto-bucles pero descarta aristas paralelas (no multigrafo).
- **Vértice (Vertex)**: Entidad identificada por una cadena de caracteres visible no vacía que representa un nodo en el sistema de dependencias.
- **Arista Dirigida (Directed Edge)**: Vínculo ordenado `source -> target` que expresa una dependencia unidireccional entre el vértice de origen y el vértice de destino.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El usuario obtiene el resumen y visualización completa de cualquier archivo CSV válido de dependencias en menos de 1 segundo de tiempo de ejecución.
- **SC-002**: El sistema procesa con exactitud matemática y determinismo los archivos de referencia del laboratorio:
  - `small-dag.csv`: 9 vértices y 9 aristas dirigidas.
  - `cs-curriculum.csv`: 19 vértices y 23 aristas dirigidas.
  - `build-with-cycle.csv`: 11 vértices y 13 aristas dirigidas.
- **SC-003**: El 100% de las anomalías tolerables (aristas duplicadas, vértices aislados `watch,`, auto-bucles, espacios exteriores, UTF-8/BOM) se resuelven sin excepciones no controladas ni alteración de datos.
- **SC-004**: El 100% de los errores no recuperables (archivos inexistentes, vacíos, o con filas malformadas como `,target`) producen un mensaje en `stderr` y finalizan con código 1 o 2 según corresponda.
- **SC-005**: La salida producida para cualquier entrada válida es 100% determinista e idéntica en cualquier plataforma y ejecución.

## Assumptions

- **A-001**: La interfaz CLI por defecto ejecuta la visualización completa e integrada cuando se proporciona la ruta del archivo CSV como argumento posicional principal.
- **A-002**: Los identificadores de vértices son sensibles a mayúsculas y minúsculas tras ignorar espacios periféricos (`Case-Sensitive`).
- **A-003**: No existen pesos ni atributos numéricos en las aristas para la Feature 1.
- **A-004**: El análisis de aciclicidad, orden topológico y ciclos queda reservado para la Feature 2.
