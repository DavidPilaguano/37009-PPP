# Comparativa funcional y estrategia de búsqueda



## Funciones requeridas para el prototipo

| Función | Decisión inicial |
| --- | --- |
| Obtención de imagen | Cámara o galería |
| Validación | Formato, archivo legible y RGB |
| Diagnóstico | Clasificación local después del preprocesamiento |
| Historial | Preparado para almacenamiento local |
| Conectividad | El flujo principal no depende de Internet |

## Estrategia de revisión bibliográfica

- Fuentes previstas: IEEE Xplore, Scopus y Google Scholar.
- Términos: `avocado leaf disease`, `plant disease classification`, `MobileNet`, `transfer learning`, `offline mobile diagnosis`.
- Criterios de selección: estudios con imágenes de hojas, métricas reportadas, modelo descrito y contexto agrícola identificable.

## Criterios de comparación del prototipo

| Criterio | Importancia | Regla adoptada |
| --- | --- | --- |
| Uso sin conectividad | Alta | El preprocesamiento y la inferencia deberán poder ejecutarse localmente. |
| Entrada desde cámara o galería | Alta | La interfaz futura deberá aceptar ambos orígenes. |
| Validación antes de inferir | Alta | No se procesarán archivos ilegibles, no RGB o con formato no permitido. |
| Trazabilidad | Media | Se conservarán metadatos y resultado para una futura consulta local. |
| Tamaño del modelo | Media | Se prefiere una arquitectura móvil antes que una red pesada. |

## Registro de búsqueda reproducible

Las consultas se estructuraron combinando cultivo, síntoma, técnica y entorno de uso. Ejemplos: `plant disease classification AND transfer learning`, `leaf image MobileNet`, `offline mobile plant diagnosis`. Para incluir una fuente en la matriz se revisa que exponga al menos el conjunto de datos, el modelo y una métrica de evaluación.

## Decisión de alcance

La comparación se usa para definir requisitos técnicos, no para afirmar que el proyecto replica una aplicación comercial concreta. La primera versión prioriza la integridad del dato y una inferencia local reproducible.
