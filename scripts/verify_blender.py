"""Blender: --background FILE --python verify_blender.py -- REPORT.json"""
import bpy
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter

scene_rows = []
for scene in bpy.data.scenes:
    scene_rows.append({
        'name': scene.name,
        'objects': len(scene.objects),
        'object_types': dict(sorted(Counter(o.type for o in scene.objects).items())),
        'frames': [scene.frame_start, scene.frame_end],
        'camera': scene.camera.name if scene.camera else None,
        'sequencer': scene.sequence_editor is not None,
        'collections': sorted(c.name for c in scene.collection.children),
    })
external = []
for image in bpy.data.images:
    if image.source in {'FILE','MOVIE','SEQUENCE','TILED'} and not image.packed_file:
        external.append({'name': image.name, 'path': image.filepath})
report = {
    'blender': bpy.app.version_string,
    'file': Path(bpy.data.filepath).name,
    'scenes': scene_rows,
    'counts': {k: len(getattr(bpy.data, k)) for k in ('objects','meshes','materials','armatures','actions','worlds','sounds','movieclips','libraries','cache_files')},
    'textures': [{'name': i.name, 'packed': bool(i.packed_file), 'path': i.filepath} for i in bpy.data.images if i.source == 'FILE'],
    'unpacked_dependencies': external,
    'sha256': hashlib.file_digest(open(bpy.data.filepath, 'rb'), 'sha256').hexdigest(),
}
assert len(scene_rows) == 3
assert not any(s['sequencer'] for s in scene_rows)
assert not external
assert all(len(getattr(bpy.data, k)) == 0 for k in ('sounds','movieclips','libraries','cache_files'))
paths = list(bpy.utils.blend_paths())
assert all(not (':' in p or (p.startswith('/') and not p.startswith('//'))) for p in paths), sorted(set(paths))
# Evaluate the original rigs/modifiers at representative frames in each scene.
evaluations = []
for scene in bpy.data.scenes:
    bpy.context.window.scene = scene
    frames = [265, 384, 625, 684] if scene.name.startswith('09 |') else ([745, 864, 984] if scene.name.startswith('10 |') else [1, 46, 73, 144])
    for frame in frames:
        scene.frame_set(frame)
        graph = bpy.context.evaluated_depsgraph_get()
        graph.update()
        vertices = sum(len(o.evaluated_get(graph).data.vertices) for o in scene.objects if o.type == 'MESH')
        evaluations.append({'scene': scene.name[:2], 'frame': frame, 'evaluated_vertices': vertices})
report['evaluations'] = evaluations
report['status'] = 'passed'
Path(sys.argv[sys.argv.index('--') + 1]).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
