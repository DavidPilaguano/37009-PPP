# Bitácora de planificación y evidencias iniciales

## Propósito

Esta carpeta reúne los documentos de trabajo asociados a las actividades planificadas entre el 21 de septiembre y el 1 de octubre de 2026. Su finalidad es dejar trazabilidad de las decisiones de alcance, requisitos, revisión técnica y preparación del pipeline de datos antes de construir el dataset procesado.

Los documentos distinguen entre tres estados: decisiones de diseño, implementación comprobable y trabajo futuro. No presentan el prototipo móvil ni el entrenamiento del modelo como terminados; esos componentes quedaron planificados para etapas posteriores del cronograma.

## Documentos incluidos

| Fecha planificada | Documento | Propósito de evidencia |
| --- | --- | --- |
| 21 sep. | `2026-09-21_objetivos_y_entregables.md` | Delimitación del proyecto y entregables. |
| 22 sep. | `2026-09-22_problema_y_requisitos.md` | Problema, usuarios, requisitos y criterios de aceptación. |
| 23 sep. | `2026-09-23_notas_estado_del_arte.md` | Decisión de CNN y transferencia de aprendizaje. |
| 24 sep. | `2026-09-24_comparativa_y_estrategia_busqueda.md` | Criterios funcionales y estrategia de búsqueda. |
| 25 sep. | `2026-09-25_matriz_bibliografica_inicial.md` | Matriz de fuentes y decisiones derivadas. |
| 28 sep. | `2026-09-28_metodologia_y_metricas.md` | Protocolo de datos, métricas y evaluación. |
| 29 sep. | `2026-09-29_entorno_y_estructura.md` | Entorno reproducible y estructura de código. |
| 30 sep. | `2026-09-30_dependencias_y_base_movil.md` | Contrato previsto para la integración móvil. |
| 1 oct. | `2026-10-01_ingesta_y_validacion.md` | Flujo de ingesta, validación y trazabilidad. |

## Referencias técnicas consultadas

1. Mohanty, S. P., Hughes, D. P. y Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection*. Frontiers in Plant Science, 7, 1419. https://doi.org/10.3389/fpls.2016.01419
2. Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861
3. Sandler, M. et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks*. arXiv:1801.04381. https://arxiv.org/abs/1801.04381
4. Ferentinos, K. P. (2018). *Deep learning models for plant disease detection and diagnosis*. Computers and Electronics in Agriculture, 145, 311-318. https://doi.org/10.1016/j.compag.2018.01.009

## Criterio de uso de las fuentes

Las referencias respaldan la elección de un enfoque de clasificación de imágenes y de una arquitectura móvil. No sustituyen la evaluación del conjunto de datos propio: el desempeño final debe reportarse solo después de entrenar y probar el modelo con particiones separadas.
