# Aplicación simple para *timelapses* con cámara web

## Registro de imágenes (`timelapser.py`)
Setear tiempo entre capturas (**intervalo** en segundos), y cámara en archivo de configuración `timelap.cfg`.
Ejecutar en terminal CMD. Crea carpeta **./timelapser_records** y ordena por fecha y hora de inicio cada *timelapse*. Los archivos son **guardados a medida que se hacen las capturas**.  
Registra eventos de cada ejecución en archivo de logging `./timelapser_logs/.log`.

## Edición automática con API de Blender (`editor.py`)
Agregar a sección `[editor]` de archivo `timelap.cfg` la ruta absoluta a la carpeta con las capturas generadas por `timelapser.py` a `dir_imgs` y la ruta absoluta al archivo MP4 que se desea crear a parir de ellas.

> **NOTA:** Para ejecutar scripts de python como instrucciones para Blender, hay que tener agregado `blender` a `PATH`.  

Ejecutar en CMD con:
```CMD
blender -b -P editor.py
```