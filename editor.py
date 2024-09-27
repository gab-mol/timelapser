'''
Editar automaticamente video a partir de secuencia de capturas del timelapse.
'''
import bpy
import os

# Directorio donde están las imágenes
DIR = os.getcwd()
directory = os.path.join(DIR,"timelapser_records","start_2024-09-26","start_12.07.16")
output_file = os.path.join(DIR,"videos", f"pr_render2024-09-26--12-07-16.mp4")


image_files = sorted([f for f in os.listdir(directory) if f.endswith('.jpg')]) # or f.endswith('.png')
print("path:",directory)
print(image_files)
sed = bpy.context.scene.sequence_editor
#print(sed)

first = image_files.pop(0)

imstrip = sed.sequences.new_image(
    name="timelapse",
    filepath=first,
    channel=1,
    frame_start=0,
    fit_method='FIT'
)

for image in image_files:
    imstrip.elements.append(image)

scene = bpy.context.scene
scene.sequence_editor_create()

# Configura las propiedades de renderizado
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.fps = 1

# Configura el rango de fotogramas según la cantidad de imágenes
scene.frame_start = 0
scene.frame_end = len(image_files)  

# Establece la ruta de salida para el video
scene.render.filepath = output_file

# Renderiza la animación (crea el video)
try:
    bpy.ops.render.render(animation=True)
except:
    Exception("Falló el ops.render")

print(f"Video guardado en: {output_file}")