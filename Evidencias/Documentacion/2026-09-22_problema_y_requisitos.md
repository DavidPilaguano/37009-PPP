# Análisis del problema y requisitos

**Fecha planificada:** 22 de septiembre de 2026

## Problema identificado

La identificación visual de alteraciones en hojas de aguacate requiere imágenes legibles, etiquetas consistentes y un procesamiento uniforme antes de ejecutar un clasificador.

## Usuarios considerados

- Productores o técnicos que requieren una orientación inicial sobre el estado foliar.
- Personal académico que necesita revisar el comportamiento del modelo y la trazabilidad de los datos.

## Requisitos funcionales iniciales

- Recibir una imagen de hoja desde cámara o galería.
- Verificar formato, tamaño y canales de color.
- Preparar la imagen para inferencia y mostrar una clase estimada.
- Conservar resultados locales para una futura aplicación sin conexión.

## Requisitos no funcionales

- Procesamiento reproducible.
- Separación de datos sin fuga entre entrenamiento y evaluación.
- Mensajes claros cuando una imagen no sea válida.

## Historias de usuario iniciales

| Rol | Necesidad | Criterio de aceptación |
| --- | --- | --- |
| Técnico o productor | Seleccionar una fotografía de hoja. | El sistema acepta cámara o galería y comunica si el archivo no es compatible. |
| Usuario del diagnóstico | Obtener una respuesta comprensible. | La aplicación mostrará la clase estimada y un mensaje de orientación, sin sustituir la revisión experta. |
| Responsable técnico | Repetir la preparación de datos. | El proceso usa parámetros, manifiestos y una semilla identificable. |
| Evaluador académico | Revisar la evidencia del sistema. | Cada muestra procesada conserva ruta, etiqueta, hash y partición. |

## Reglas de validación propuestas

1. Aceptar extensiones de imagen declaradas por el pipeline.
2. Verificar que el archivo pueda abrirse y convertirse a RGB.
3. Rechazar duplicados exactos y registrar el motivo del rechazo.
4. No permitir que un mismo grupo de captura aparezca en más de una partición.
5. Mantener las imágenes de prueba externa fuera del entrenamiento y del cálculo de pesos de clase.

## Fuera de alcance en esta fase

No se incluye recomendación de tratamiento agrícola, geolocalización, sincronización en nube ni una aplicación móvil lista para distribución. Estos elementos requieren validación agronómica, diseño de interfaz y pruebas adicionales.
