# GraphLab Constitution

## Core Principles

### I. Python 3.11+ y Arquitectura CLI
- La aplicación debe ser una herramienta de línea de comandos (CLI) desarrollada exclusivamente para Python 3.11+.
- La entrada de datos se realiza mediante argumentos y/o flujos estándar (`stdin`); los resultados procesados se dirigen a `stdout`; los mensajes de error y advertencias se dirigen a `stderr`.
- La arquitectura debe ser simple y concisa (KISS / YAGNI), evitando sobreingeniería, abstracciones innecesarias o bibliotecas ajenas a las estrictamente requeridas.

### II. Implementación Propia de Grafos y Algoritmos (Cero Librerías en Producción)
- Queda terminantemente prohibido el uso de bibliotecas externas o módulos del sistema dedicados a grafos (como `networkx`, `graphlib`, `igraph`, `scipy.sparse.csgraph`, etc.) en el código de producción de la aplicación.
- Tanto la estructura de datos para representar el grafo en memoria como todos los algoritmos (recorridos, detección de ciclos, adyacencias, ordenamientos) deben ser implementados desde cero por el equipo y fundamentados en los documentos de diseño (`plan.md` y `research.md`).

### III. Pruebas Exhaustivas y Oráculos de Verificación (NON-NEGOTIABLE)
- Todo escenario de aceptación definido en una especificación funcional DEBE contar con al menos una prueba automatizada correspondiente.
- Se adopta la disciplina de desarrollo guiado por pruebas (TDD): los casos de prueba deben definirse y validarse antes de considerar completada la implementación.
- Se autoriza y recomienda el uso de bibliotecas de grafos reconocidas (como `networkx`) **exclusivamente como oráculos de prueba** dentro de la suite de tests, para verificar matemáticamente que las salidas de la implementación propia sean rigurosamente correctas.

### IV. Salidas Deterministas y Manejo Explícito de Errores
- Para una misma entrada y parámetros idénticos, la aplicación DEBE emitir siempre la misma salida sin fluctuaciones entre ejecuciones ni plataformas.
- Cuando un algoritmo o consulta admita múltiples resultados válidos (ej. ordenamientos topológicos concurrentes o listado de vértices), la regla de desempate DEBE ser determinista y explícita (p. ej., orden lexicográfico).
- Cualquier condición anómala o error en los datos de entrada DEBE generar un mensaje comprensible en `stderr` y finalizar con un código de salida distinto de cero (ej. código 1 para datos/formato inválido, código 2 para uso incorrecto de CLI), impidiendo la exposición de trazas de excepción no controladas (`tracebacks`) al usuario final.

### V. Correspondencia Estricta entre Especificación y Código
- La especificación funcional (`spec.md`) y el código implementado deben coincidir fielmente en todo momento.
- Si durante la implementación o las pruebas se detecta una discrepancia o necesidad de cambio, debe corregirse primero la especificación antes de modificar el código. Nunca se mantendrá código que contradiga la especificación.
- Ninguna funcionalidad o comportamiento no documentado debe introducirse en el código.

### VI. Flujo por Ramas y Trazabilidad por Fases
- Cada funcionalidad debe desarrollarse en su propia rama dedicada (`001-directed-graphs`, `002-topological-sort`) a partir de la rama `main`.
- La Feature 1 debe ser completamente completada, probada y fusionada (*merged*) en `main` antes de comenzar la especificación de la Feature 2.
- El historial de Git debe evidenciar con absoluta claridad el avance fase por fase (`specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`), contando con al menos un commit individual por cada fase de cada funcionalidad.

## Additional Constraints & Quality Standards

- **Estilo y Tipado**: Código conforme a PEP 8 con anotaciones de tipo (*type hints*) estáticas verificables y docstrings explicativos.
- **Manejo Robusto de Entrada**: Resistencia ante espacios en blanco accidentales, líneas vacías, codificaciones UTF-8 con o sin BOM (`utf-8-sig`) y formatos CSV imprevistos.
- **Integración Continua (CI)**: Se mantendrá un flujo de GitHub Actions que ejecute automáticamente la suite completa de pruebas en cada push o solicitud de extracción (*pull request*).

## Development Workflow & Quality Gates

1. **Gate 1 (Specify & Clarify)**: La especificación funcional debe estar completa, con todos los casos de borde y sin marcadores de clarificación pendientes antes de iniciar la planificación.
2. **Gate 2 (Plan & Research)**: El plan debe justificar la representación de grafos y las complejidades temporal y espacial, comprobando el cumplimiento de las restricciones constitucionales.
3. **Gate 3 (Tasks & Analyze)**: El desglose de tareas debe cubrir todos los requisitos y pasar el análisis de consistencia sin advertencias críticas o altas sin resolver.
4. **Gate 4 (Implement & Verify)**: Todo el código debe tener pruebas automatizadas pasando al 100% y ejecutarse satisfactoriamente sobre los conjuntos de datos del laboratorio (`data/`).

## Governance

- Esta constitución representa la ley fundamental del proyecto y prevalece sobre cualquier otra decisión técnica o de proceso.
- Las enmiendas a este documento deben justificarse explícitamente, versionarse según reglas de versionado semántico y registrarse en el historial de commits.
- Toda revisión de código, plan o tarea debe validar explícitamente su conformidad con los principios aquí ratificados.

**Version**: 1.0.0 | **Ratified**: 2026-10-30 | **Last Amended**: 2026-10-30
