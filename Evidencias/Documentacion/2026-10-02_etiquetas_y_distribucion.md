# Etiquetas, metadatos y distribución inicial

**Fecha planificada:** 2 de octubre de 2026

## Catálogo de clases revisado

| Identificador | Etiqueta técnica | Nombre de presentación | Estado | Decisión |
| --- | --- | --- | --- | --- |
| 0 | `algal_leaf_spot` | Mancha algal foliar | Aprobada | Se incorpora al clasificador foliar. |
| 1 | `healthy_leaf` | Hoja sana | Aprobada | Se incorpora como clase de referencia sana. |
| 2 | `branch_canker` | Cancro de rama | Pendiente | Se excluye de la primera versión por no ser una clase foliar aprobada. |

## Metadatos registrados por muestra

El manifiesto del dataset registra identificador, ruta relativa, partición, etiqueta, origen, grupo de captura, dimensiones, canales, hash SHA-256, formato de anotación y estado de revisión. Esta información permite rastrear cada archivo aceptado y explicar los descartes.

## Distribución generada

La revisión de calidad reporta 27 imágenes internas válidas y 186 imágenes externas separadas. La partición interna mantiene muestras de ambas clases en entrenamiento, validación y prueba; se conservan tres imágenes rechazadas para revisión en vez de eliminarlas sin registro.

## Controles aplicados

- La etiqueta debe aparecer en el catálogo de clases aprobado.
- La muestra debe pertenecer a una sola partición.
- La misma captura no puede pasar a entrenamiento, validación y prueba de forma simultánea.
- Los totales por clase se resumen en `metadata/quality_review.csv`.
- Las clases pendientes se documentan, pero no se incorporan de manera silenciosa al entrenamiento.

## Archivos de evidencia

- `avocado_mobilenet_v1_final/classes.csv`
- `avocado_mobilenet_v1_final/manifest.csv`
- `avocado_mobilenet_v1_final/metadata/quality_review.csv`
