# Entorno de desarrollo y estructura del proyecto

**Fecha planificada:** 29 de septiembre de 2026

## Entorno definido

- Python 3.11 o superior.
- Pillow para verificación y transformación de imágenes.
- TensorFlow como integración opcional para el cargador de entrenamiento.
- Git como control de versiones del código.

## Estructura creada

```text
src/       módulos de construcción, preprocesamiento, validación y entrada de entrenamiento
tests/     pruebas automatizadas
docs/      documentación y evidencias
avocado_mobilenet_v1_final/  conjunto de datos procesado y sus manifiestos
```

La estructura separa las fuentes, el procesamiento y las pruebas para facilitar la reproducción de resultados.

## Dependencias y responsabilidad de cada módulo

| Componente | Responsabilidad | Archivo principal |
| --- | --- | --- |
| Contrato de datos | Clases aprobadas, etiquetas y extensiones permitidas. | `src/dataset_contract.py` |
| Construcción | Lectura de originales, partición y generación de manifiestos. | `src/build_dataset.py` |
| Preprocesamiento | Inspección RGB, hashes y preparación para inferencia. | `src/preprocess.py` |
| Validación | Revisión de archivos, etiquetas, hashes y particiones. | `src/validate_dataset.py` |
| Entrada de entrenamiento | Carga por lotes y aumento limitado a entrenamiento. | `src/training_input.py` |
| Pruebas | Pruebas de propiedades del preprocesamiento. | `tests/test_preprocess.py` |

## Preparación reproducible

La instalación mínima se documenta en `requirements.txt`. TensorFlow se mantiene como dependencia opcional: permite construir `tf.data.Dataset`, pero no es necesario para inspeccionar, construir o validar el dataset procesado. Esta separación permite revisar los datos aun cuando no se disponga de GPU.

## Controles de versión previstos

- Mantener cambios de código bajo control de versiones.
- No editar las imágenes fuente desde los scripts de construcción.
- Regenerar el dataset en una carpeta vacía a partir de una semilla explícita.
- Conservar manifiestos CSV como evidencia de la versión generada.
