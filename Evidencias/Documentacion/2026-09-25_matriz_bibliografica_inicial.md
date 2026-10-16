# Matriz bibliográfica inicial

**Fecha planificada:** 25 de septiembre de 2026

| Campo de revisión | Registro esperado |
| --- | --- |
| Fuente | IEEE Xplore, Scopus o Google Scholar |
| Tema | Clasificación de enfermedades en hojas mediante imágenes |
| Datos | Tipo de cultivo, clases y número de imágenes reportado |
| Modelo | CNN, MobileNet u otro modelo de transferencia |
| Métricas | Accuracy, precision, recall y F1-score |
| Aporte al proyecto | Decisión aplicable al conjunto de datos, entrenamiento o aplicación móvil |

## Fuentes registradas

| Fuente | Datos y enfoque | Métrica reportada por el estudio | Decisión para el proyecto | Limitación a considerar |
| --- | --- | --- | --- | --- |
| Mohanty, Hughes y Salathé (2016) | 54.306 imágenes de hojas y CNN para 38 combinaciones cultivo-enfermedad/estado. | Accuracy de 99,35% en su conjunto de prueba retenido. | Usar evaluación separada y reportar métricas por clase. | Las condiciones del conjunto de referencia no son iguales a las imágenes propias. |
| Ferentinos (2018) | CNN para 58 combinaciones planta-enfermedad o estado sano. | Accuracy de 99,53% sobre imágenes no vistas del estudio. | Considerar CNN como línea base, pero no transferir su cifra al proyecto. | El desempeño depende de datos, clases y condiciones de captura. |
| Howard et al. (2017) | Arquitectura MobileNet para visión eficiente. | Evalúa el intercambio entre latencia y exactitud. | Priorizar un modelo compatible con dispositivos de recursos limitados. | La elección final exige medir tamaño y rendimiento local. |
| Sandler et al. (2018) | MobileNetV2 con bloques residuales invertidos. | Reporta mejoras en varias tareas y tamaños de modelo. | Usar el preprocesamiento de MobileNetV2 como contrato de entrada. | No sustituye la validación sobre las clases de aguacate. |

## Resultado y trazabilidad

La revisión no selecciona todavía un modelo final. Su resultado es una decisión inicial: construir un pipeline de imágenes compatible con MobileNetV2, separar los datos antes de cualquier aumento y evaluar con métricas que permitan identificar errores por clase. Las referencias completas y enlaces se incluyen en `00_indice_y_referencias.md`.
