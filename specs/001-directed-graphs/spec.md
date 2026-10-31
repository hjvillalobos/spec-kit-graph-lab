# Feature Specification: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`

**Created**: 2026-10-30

**Status**: Draft

**Input**: User description: "Feature 1: cargar y visualizar un grafo dirigido sin pesos desde un archivo CSV."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Carga y Consulta de Resumen Estructural (Priority: P1)

Como usuario de la herramienta de línea de comandos, quiero cargar un archivo CSV con dependencias dirigidas y consultar un resumen del grafo para conocer rápidamente la cantidad total de vértices y aristas que contiene.

**Why this priority**: Es la funcionalidad nuclear del producto mínimo viable (MVP). Permite verificar de inmediato si un archivo de dependencias fue procesado correctamente y su escala general.

**Independent Test**: Puede probarse de manera aislada ejecutando la herramienta con cualquier archivo CSV de dependencias y comprobando que emite los conteos correctos de vértices y aristas en la salida estándar sin errores.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario solicita el resumen del grafo, **Then** el sistema reporta exactamente 9 vértices y 9 aristas dirigidas, con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario solicita el resumen del grafo, **Then** el sistema reporta exactamente 19 vértices y 23 aristas dirigidas (habiendo deduplicado la arista repetida), con código de salida 0.
3. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario solicita el resumen del grafo, **Then** el sistema reporta exactamente 11 vértices y 13 aristas dirigidas (incluyendo el auto-bucle `metrics -> metrics`), con código de salida 0.

---

### User Story 2 - Inspección Detallada de Vértices y Aristas (Priority: P1)

Como usuario que analiza dependencias complejas, quiero consultar el listado completo y ordenado de los vértices y de las aristas dirigidas para entender con precisión qué elementos existen y cómo se conectan entre sí.

**Why this priority**: La visualización completa es un requisito explícito del laboratorio para poder inspeccionar dependencias y auditar la estructura del grafo.

**Independent Test**: Se prueba ejecutando la consulta detallada sobre un archivo CSV y verificando que cada vértice y cada arista aparezca listado de forma determinista y legible.

**Acceptance Scenarios**:

1. **Given** el archivo `data/small-dag.csv`, **When** el usuario solicita la visualización detallada, **Then** el sistema muestra los 9 vértices en orden determinista (incluyendo el vértice aislado `watch`) y las 9 aristas dirigidas (ej. `undershorts -> pants`), finalizando con código de salida 0.
2. **Given** el archivo `data/cs-curriculum.csv`, **When** el usuario solicita la visualización detallada, **Then** el sistema lista los 19 cursos y las 23 conexiones dirigidas sin repetir la arista `Data Structures -> Algorithms`, finalizando con código de salida 0.
3. **Given** el archivo `data/build-with-cycle.csv`, **When** el usuario solicita la visualización detallada, **Then** el sistema lista los 11 paquetes y las 13 aristas (incluyendo la arista cíclica reflexiva `metrics -> metrics`), finalizando con código de salida 0.

---

### User Story 3 - Robustez de Entrada y Diagnóstico de Anomalías (Priority: P2)

Como usuario que trabaja con datos del mundo real, quiero que la herramienta maneje apropiadamente anomalías comunes (espacios en blanco, codificación UTF-8 con o sin BOM) y rechace archivos corruptos o inexistentes con mensajes de error comprensibles.

**Why this priority**: Garantiza que la herramienta no falle silenciosamente ni exponga excepciones internas cuando los archivos presenten errores o variaciones menores de formato.

**Independent Test**: Se prueba invocando la herramienta con rutas de archivo inexistentes, archivos vacíos y archivos con formatos no conformes, verificando que los errores vayan a `stderr` y el código de salida sea distinto de 0.

**Acceptance Scenarios**:

1. **Given** una ruta a un archivo que no existe en el disco, **When** el usuario intenta cargarlo, **Then** el sistema emite un mensaje de error claro en `stderr` explicando que el archivo no fue encontrado y termina con código de salida 2 (error de archivo / entrada).
2. **Given** un archivo CSV completamente vacío (0 bytes), **When** el usuario intenta cargarlo, **Then** el sistema emite un mensaje de error en `stderr` informando que el archivo no contiene datos ni encabezado válido y termina con código de salida 1 (error de validación de datos).
3. **Given** un archivo CSV sin encabezado `source,target` o con columnas inconsistentes, **When** el usuario intenta cargarlo, **Then** el sistema informa el error de estructura en `stderr` y termina con código de salida 1.

---

### Edge Cases

- **Vértice aislado con coma final (`watch,`)**: Fila válida que define al vértice `watch` sin aristas dirigidas salientes ni entrantes generadas por esa línea.
- **Vértice aislado con coma inicial (`,target`)**: ¿Debe aceptarse como vértice de solo entrada o rechazarse como fila inválida?
- **Aristas duplicadas (`Data Structures,Algorithms`)**: Múltiples declaraciones idénticas deben consolidarse en una sola arista dirigida en el grafo sin incrementar el conteo total.
- **Auto-bucles (`metrics,metrics`)**: Una arista dirigida donde el origen y el destino son idénticos es válida dentro de la estructura de grafo dirigido de Feature 1.
- **Espacios en blanco periféricos**: Nombres como `"  Algorithms "` o `"Data Structures "` deben normalizarse recortando los espacios iniciales y finales.
- **Mayúsculas y minúsculas**: Preservación del estilo original (case-sensitive) para nombres compuestos como `Calculus I` y `Calculus II`.
- **Codificación de texto**: Soporte transparente tanto para UTF-8 estándar como para UTF-8 con marca de orden de bytes (BOM).
- **Líneas en blanco**: Las líneas completamente vacías dentro del archivo CSV deben ser ignoradas sin generar errores.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE cargar un grafo dirigido y no ponderado a partir de un archivo en formato CSV especificado por el usuario mediante la línea de comandos.
- **FR-002**: El sistema DEBE exigir la presencia de la cabecera `source,target` en la primera fila del archivo CSV (tolerando diferencias de mayúsculas/minúsculas y espacios en los nombres de las columnas).
- **FR-003**: El sistema DEBE permitir consultar el resumen cuantitativo del grafo cargado, mostrando con precisión el número total de vértices únicos y el número total de aristas dirigidas únicas.
- **FR-004**: El sistema DEBE permitir consultar la lista completa de vértices y la lista completa de aristas dirigidas.
- **FR-005**: El sistema DEBE mostrar los vértices y aristas en un orden determinista y predecible [NEEDS CLARIFICATION: ¿El orden predeterminado de visualización debe ser estrictamente lexicográfico alfabético, o debe ofrecerse alguna opción alternativa?].
- **FR-006**: El sistema DEBE reconocer y procesar filas con la sintaxis `vértice,` como la declaración explícita de un vértice aislado sin aristas salientes.
- **FR-007**: El sistema DEBE tratar las filas con sintaxis `,vértice` según la política de formato definida [NEEDS CLARIFICATION: ¿Una fila `,vértice` debe interpretarse como vértice aislado o debe rechazarse como fila malformada?].
- **FR-008**: El sistema DEBE deduplicar aristas repetidas en el archivo CSV [NEEDS CLARIFICATION: ¿Las aristas duplicadas deben descartarse silenciosamente en modo idempotente o debe emitirse un aviso de advertencia a stderr?].
- **FR-009**: El sistema DEBE admitir aristas dirigidas reflexivas (auto-bucles como `u -> u`), contabilizándolas como una arista dirigida válida en el resumen e inspección.
- **FR-010**: El sistema DEBE normalizar los nombres de los vértices eliminando espacios en blanco al inicio y al final (`strip`), preservando la capitalización original (distinción de mayúsculas y minúsculas).
- **FR-011**: El sistema DEBE soportar archivos codificados en UTF-8 estándar y UTF-8 con BOM.
- **FR-012**: El sistema DEBE validar la integridad estructural del CSV; ante archivos inexistentes, archivos vacíos o filas con número de columnas distinto de 2, DEBE abortar la ejecución, imprimir un mensaje explicativo en `stderr` y finalizar con un código de salida distinto de cero (código 2 para errores de archivo/invocación, código 1 para errores de validación de contenido).

### Key Entities

- **Grafo Dirigido (Directed Graph)**: Estructura compuesta por un conjunto finito de vértices únicos y un conjunto de aristas dirigidas sin ponderar.
- **Vértice (Vertex)**: Entidad identificada por una cadena de texto no vacía que representa un elemento del dominio (curso, prenda de vestir, paquete de software). Puede tener aristas incidentes, salientes o encontrarse aislado.
- **Arista Dirigida (Directed Edge)**: Par ordenado de vértices `(source, target)` que representa una relación unidireccional de precedencia o dependencia desde `source` hacia `target`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El usuario puede obtener el conteo exacto de vértices y aristas de cualquier archivo CSV de dependencias válido en menos de 1 segundo de ejecución.
- **SC-002**: El sistema procesa con 100% de éxito y exactitud los tres archivos de prueba oficiales (`small-dag.csv`, `cs-curriculum.csv`, `build-with-cycle.csv`), coincidiendo exactamente con los conteos estructurales auditados.
- **SC-003**: El 100% de las anomalías tolerables (aristas duplicadas, vértices aislados `watch,`, auto-bucles, espacios en blanco circundantes) son procesadas sin caídas del programa ni pérdidas de datos.
- **SC-004**: El 100% de los errores no recuperables (archivos no encontrados, archivos vacíos, filas malformadas) producen un mensaje legible en `stderr` y un código de salida no nulo, sin mostrar trazas de error no controladas al usuario.
- **SC-005**: La salida de visualización ante una misma entrada es 100% determinista e idéntica entre múltiples ejecuciones sucesivas.

## Assumptions

- **A-001 (Requisito vs. Propuesta)**: El enunciado original exige poder cargar y visualizar el grafo (vértices, aristas y cantidades). Se propone como comportamiento por defecto mostrar una vista unificada y clara que incluya resumen y listado al ejecutar el comando con la ruta del archivo, dejando la confirmación de banderas opcionales para la fase de clarificación.
- **A-002**: Los identificadores de vértices son sensibles a mayúsculas y minúsculas (`Case-Sensitive`) tras la limpieza de espacios laterales, garantizando fidelidad a nombres formales de cursos o componentes.
- **A-003**: Los grafos tratados en Feature 1 no son ponderados; los archivos CSV únicamente expresan relaciones binarias dirigidas entre origen y destino.
- **A-004**: El algoritmo de ordenamiento topológico y el diagnóstico de ciclos corresponden exclusivamente a la Feature 2 y están explícitamente fuera del alcance de la presente especificación.
