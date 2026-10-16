# Propuesta metodológica y métricas


## Flujo metodológico

1. Revisar las imágenes originales y sus etiquetas.
2. Validar archivos, formatos y canales RGB.
3. Detectar duplicados exactos y conservar un registro de rechazos.
4. Separar los datos por captura original en entrenamiento, validación y prueba.
5. Preprocesar imágenes para MobileNet y aplicar aumento solo al entrenamiento.
6. Evaluar el modelo sobre datos no usados en entrenamiento.

## Métricas propuestas

- **Accuracy:** proporción global de clasificaciones correctas.
- **Precision:** proporción de predicciones positivas correctas.
- **Recall:** proporción de casos positivos recuperados.
- **F1-score:** equilibrio entre precision y recall.
- **Matriz de confusión:** detalle de aciertos y errores por clase.

## Protocolo de partición y control de fuga

La unidad de partición no será una imagen aumentada, sino la captura original. Primero se identifican las muestras originales y se calcula su hash; después se asigna cada captura a entrenamiento, validación o prueba con una semilla registrada. Las versiones derivadas de una misma captura no pueden cruzar a otra partición.

| Conjunto | Propósito | Transformaciones permitidas |
| --- | --- | --- |
| Entrenamiento | Ajustar los parámetros del modelo. | Redimensionamiento, normalización y aumento moderado. |
| Validación | Ajustar decisiones de entrenamiento. | Solo redimensionamiento y normalización determinista. |
| Prueba | Estimar el desempeño final interno. | Solo redimensionamiento y normalización determinista. |
| Prueba externa | Revisión independiente posterior. | Separada físicamente y sin participación en entrenamiento. |

## Plan de evaluación

1. Registrar la distribución de clases y pesos calculados solo con entrenamiento.
2. Entrenar una versión inicial y conservar configuración, semilla y pesos.
3. Comparar curvas de entrenamiento y validación para identificar sobreajuste.
4. Calcular accuracy, precision, recall y F1-score en la partición de prueba.
5. Examinar la matriz de confusión y ejemplos de error antes de seleccionar una versión.

## Criterio de reporte

No se debe comunicar una métrica global sin indicar el conjunto evaluado. Las métricas de validación se usan para decisiones de entrenamiento; las métricas de prueba se reservan para el resultado de la versión seleccionada.
