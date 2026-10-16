# Dependencias reproducibles y base de integración móvil


## Dependencias documentadas

Las dependencias del procesamiento de imágenes se registran en `requirements.txt`. El proyecto separa el pipeline de datos de una futura interfaz móvil para que el modelo pueda integrarse sin modificar la preparación de las imágenes.

## Base para la aplicación móvil

- Entrada prevista desde cámara o galería.
- Validación de tamaño y formato antes de ejecutar la inferencia.
- Uso de una imagen preprocesada compatible con el modelo.
- Preparación para mostrar resultado, confianza y mensajes de error.

## Criterio de integración

La interfaz móvil deberá consumir el mismo preprocesamiento empleado por el modelo, para evitar diferencias entre entrenamiento e inferencia.

## Contrato de integración previsto

| Entrada o salida | Formato acordado | Regla |
| --- | --- | --- |
| Imagen de entrada | Archivo JPEG o PNG legible. | Se convierte a RGB y se valida antes de inferir. |
| Tamaño de entrada | Imagen cuadrada de 224 × 224. | Se obtiene mediante orientación, recorte centrado y redimensionamiento. |
| Salida del clasificador | Índice de clase, etiqueta y confianza. | Se muestra como orientación técnica; no como diagnóstico definitivo. |
| Error de captura | Mensaje para el usuario. | Se explica si el archivo no puede abrirse, no es válido o no cumple el formato. |
| Historial local futuro | Registro de resultado y referencia de imagen. | Debe permanecer en el dispositivo y funcionar sin conexión. |

## Flujo de la futura pantalla de diagnóstico

1. El usuario selecciona una foto desde cámara o galería.
2. La aplicación comprueba permisos y el archivo elegido.
3. El módulo común prepara la imagen con las mismas reglas del entrenamiento.
4. El modelo local calcula una predicción.
5. La interfaz presenta clase, confianza y un mensaje de uso responsable.
6. De ser necesario, se guarda el resultado en el historial local.

## Estado al cierre de la actividad

Se dejó definida la interfaz técnica entre una aplicación móvil futura y el pipeline de IA. No se declara implementada una aplicación Flutter ni una base de datos embebida, porque esas actividades pertenecen a fechas posteriores del cronograma.
