# Notas de estado del arte



## Hallazgos técnicos revisados

- Las enfermedades y alteraciones foliares se reconocen a partir de patrones como manchas, coloración, textura y distribución sobre la hoja.
- Las redes neuronales convolucionales permiten extraer patrones visuales de forma automática.
- El aprendizaje por transferencia aprovecha un modelo entrenado previamente y reduce la cantidad de datos y tiempo requeridos para una primera versión funcional.

## Decisión técnica inicial

Se seleccionó MobileNet como base de preparación para el modelo por su orientación a dispositivos con recursos limitados y por su compatibilidad con flujos de visión por computador.

## Implicación para los datos

Las fotografías deben convertirse a RGB, normalizarse a un tamaño consistente y conservar su procedencia para evitar que variantes de una misma captura aparezcan en particiones distintas.

## Evidencia bibliográfica y decisión

| Referencia | Aporte aprovechado | Decisión aplicada al proyecto |
| --- | --- | --- |
| Mohanty, Hughes y Salathé (2016) | Demuestra la viabilidad de clasificar enfermedades de plantas a partir de imágenes de hojas con CNN. | Usar una clasificación supervisada y reportar métricas sobre datos retenidos. |
| Ferentinos (2018) | Evalúa modelos de aprendizaje profundo para identificación de enfermedades vegetales. | Tratar las métricas de laboratorio con cautela y reservar una partición de prueba. |
| Howard et al. (2017) | Presenta MobileNet como arquitectura eficiente para visión móvil y embebida. | Preparar imágenes a tamaño fijo y mantener una ruta de despliegue móvil. |
| Sandler et al. (2018) | Describe MobileNetV2 y sus bloques eficientes para distintos tamaños de modelo. | Usar preprocesamiento compatible con MobileNetV2 como punto de partida. |



## Limitación importante

Los resultados publicados en conjuntos controlados no predicen directamente el desempeño en las imágenes de este proyecto. La iluminación, el fondo, la calidad de la cámara y el número de muestras pueden modificar de forma importante la capacidad de generalización.
