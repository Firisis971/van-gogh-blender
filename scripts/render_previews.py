"""Render three still previews from the distributed Blender file (no animation export)."""
import bpy
import sys
from pathlib import Path

output = Path(sys.argv[sys.argv.index('--') + 1])
output.mkdir(parents=True, exist_ok=True)
for prefix, frame, name in [('09 |', 505, 'village.png'), ('09 |', 684, 'personnages.png'), ('13 |', 46, 'fenetres.png')]:
    scene = next(s for s in bpy.data.scenes if s.name.startswith(prefix))
    bpy.context.window.scene = scene
    scene.frame_set(frame)
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.use_sequencer = False
    scene.render.image_settings.media_type = 'IMAGE'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(output / name)
    bpy.ops.render.render(write_still=True, scene=scene.name)
    print('PREVIEW', name, flush=True)
