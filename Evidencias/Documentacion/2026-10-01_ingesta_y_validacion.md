# Ingesta, etiquetas y validación de imágenes



## Implementación registrada

El módulo `src/build_dataset.py` recorre las carpetas de origen, identifica las clases aprobadas y prepara cada muestra para su incorporación al manifiesto.

## Controles aplicados

- Verificación de extensiones de imagen permitidas.
- Apertura segura de cada archivo para detectar imágenes ilegibles.
- Conversión a RGB antes de la copia al conjunto procesado.
- Registro de etiquetas, origen, hash y grupo de captura.
- Rechazo documentado de archivos duplicados o no válidos.

## Evidencias asociadas

- `src/build_dataset.py`
- `avocado_mobilenet_v1_final/manifest.csv`
- `avocado_mobilenet_v1_final/metadata/rejected_samples.csv`

## Algoritmo de construcción

1. Localizar las carpetas `original` de las clases aprobadas.
2. Validar que cada archivo tenga una extensión permitida y pueda abrirse.
3. Convertir la imagen a RGB para obtener ancho, alto, hash criptográfico y hash perceptual.
4. Asignar el grupo de captura y la partición usando una semilla reproducible.
5. Copiar solo la muestra válida al directorio del split correspondiente.
6. Registrar cada decisión en los CSV de manifiesto, sumas de verificación, rechazos y control de calidad.

## Salidas verificables

| Salida | Contenido | Uso de evidencia |
| --- | --- | --- |
| `manifest.csv` | Ruta, split, clase, grupo, hash y procedencia por muestra aceptada. | Trazar cualquier imagen procesada. |
| `splits.csv` | Resumen de las asignaciones de entrenamiento, validación y prueba. | Revisar la separación de datos. |
| `metadata/rejected_samples.csv` | Archivo y motivo de rechazo. | Probar que los descartes no se ocultan. |
| `metadata/checksums_sha256.csv` | Huellas criptográficas de las muestras aceptadas. | Detectar duplicados exactos. |
| `metadata/quality_review.csv` | Resumen por clase y partición. | Revisar distribución y consistencia. |

## Criterios de aceptación de la ingesta

- Cada fila del manifiesto debe apuntar a un archivo existente.
- Las etiquetas deben pertenecer a las clases aprobadas.
- Las imágenes aceptadas deben ser legibles y tener tres canales RGB.
- No deben existir hashes exactos repetidos entre las muestras aceptadas.
- Los grupos de captura no pueden aparecer en más de una partición.

## Ejecución prevista

Desde la carpeta raíz de la entrega se ejecuta:

```powershell
python .\src\build_dataset.py --source-root .. --output .\avocado_mobilenet_v1_final
python .\src\validate_dataset.py --dataset .\avocado_mobilenet_v1_final
```

La primera instrucción genera el dataset solo cuando la carpeta de salida está vacía; esta medida evita sobrescribir accidentalmente una versión ya revisada.
