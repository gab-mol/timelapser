'''
Editar automaticamente video a partir de secuencia de capturas del timelapse.
'''
import bpy
import os
from pprint import pprint

# Directorio donde están las imágenes
DIR = os.getcwd()
directory = os.path.join(DIR, "timelapser_records", "start_2024-09-26", "start_12.07.16")
output_file = os.path.join(DIR, "videos", f"pr_render2024-09-26--12-07-16.mp4")

# Obtener lista de imágenes
image_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')])
print("path:", directory)
pprint(image_files)

# Asegúrate de crear el editor de secuencias
scene = bpy.context.scene
scene.sequence_editor_create()

# Usar el primer frame para obtener parámetros de resolución
first_image_path = image_files.pop(0)
print("first", first_image_path)
first_image = bpy.data.images.load(first_image_path)
width, height = first_image.size


frame_start = 0

# Crear una tira de imágenes en el canal 1
sed = scene.sequence_editor
imstrip = sed.sequences.new_image(
    name="timelapse",
    filepath=first_image_path,
    channel=1,
    frame_start=frame_start,
    fit_method='ORIGINAL'
)

# Añadir las imágenes restantes a la secuencia
for index, image_path in enumerate(image_files, start=1):
    imstrip = scene.sequence_editor.sequences.new_image(
        name=f"timelapse_{index}",
        filepath=image_path,
        channel=1,
        frame_start=frame_start + index,  # Coloca cada imagen en el siguiente fotograma
        fit_method='ORIGINAL'
    )
    imstrip.frame_final_duration = 1  # Duración de cada fotograma


# Configura las propiedades de renderizado
scene.render.resolution_x = width
scene.render.resolution_y = height
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.fps = 2

# Configurar el rango de fotogramas
scene.frame_start = 0
scene.frame_end = len(image_files)

# Establecer la ruta de salida
scene.render.filepath = output_file

# Renderizar la animación
try:
    bpy.ops.render.render(animation=True)
    print(f"Video guardado en: {output_file}")
except Exception as e:
    print(f"Error al renderizar el video: {str(e)}")
