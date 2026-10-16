# Objetivos, alcance y entregables

**Fecha planificada:** 21 de septiembre de 2026

## Objetivo

Desarrollar la base técnica de un sistema que clasifique imágenes de hojas de aguacate como sanas o con mancha foliar por algas y que pueda integrarse posteriormente en una aplicación móvil.

## Alcance definido

- Procesar únicamente fotografías de hojas de aguacate.
- Validar las imágenes antes de incorporarlas al conjunto de datos.
- Preparar los datos para un modelo de transferencia de aprendizaje basado en MobileNet.
- Mantener los datos de entrenamiento, validación, prueba y prueba externa separados.

## Entregables definidos

1. Dataset procesado con manifiestos y controles de calidad.
2. Módulos de preprocesamiento y validación de imágenes.
3. Entrada reproducible para entrenamiento del modelo.
4. Pruebas automatizadas y documentación técnica.

## Criterios de aceptación

El primer bloque del proyecto se considera completo cuando el dataset procesado se pueda regenerar sin modificar las fuentes, cada imagen tenga una etiqueta y procedencia registradas, y las validaciones detecten archivos inválidos, duplicados y mezclas indebidas entre particiones.

## Límites explícitos

- El sistema clasifica únicamente las clases foliares aprobadas por el conjunto disponible.
- El resultado es una clasificación técnica de la imagen, no un diagnóstico agronómico definitivo.
- La interfaz móvil, el entrenamiento final y la base de datos local pertenecen a fases posteriores; aquí se define la preparación que deberán consumir.

## Riesgos identificados y respuesta prevista

| Riesgo | Posible efecto | Respuesta de diseño |
| --- | --- | --- |
| Imágenes corruptas o con formatos heterogéneos | Fallo del pipeline | Validar apertura, extensión y canales RGB. |
| Duplicados o variantes de una misma captura | Métricas infladas | Calcular SHA-256 y agrupar por captura original. |
| Pocas muestras por clase | Sobreajuste | Usar partición estratificada, pesos de clase y aumento solo en entrenamiento. |
| Diferencia entre móvil y entrenamiento | Predicciones inconsistentes | Centralizar las reglas de preprocesamiento. |
