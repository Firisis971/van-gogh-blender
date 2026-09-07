"""Blender 5.0: --background --factory-startup --python prepare_blender.py -- SOURCE DESTINATION"""
import bpy
import json
import re
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[sys.argv.index('--') + 1:])
destination.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False)
scene_counts = {s.name: len(s.objects) for s in bpy.data.scenes if len(s.objects)}
for scene in list(bpy.data.scenes):
    if not len(scene.objects):
        bpy.data.scenes.remove(scene)
        continue
    if scene.sequence_editor:
        scene.sequence_editor_clear()
    scene.render.use_sequencer = False
    scene.render.image_settings.media_type = 'IMAGE'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = '//renders/'
    # The production file was saved on a partial render interval.
    # Restore access to the complete 3D animation without changing keyframes.
    if scene.name.startswith('09 |'):
        scene.frame_start, scene.frame_end = 1, 1440
        scene.frame_set(684)
    for group in ([scene.compositing_node_group] if scene.compositing_node_group else []):
        for node in group.nodes:
            if node.type == 'R_LAYERS':
                node.scene = scene
            if node.type == 'OUTPUT_FILE':
                if hasattr(node, 'base_path'):
                    node.base_path = '//renders/'
                if hasattr(node, 'directory'):
                    node.directory = '//renders/'

for data_name in ('sounds', 'movieclips', 'texts'):
    for block in list(getattr(bpy.data, data_name)):
        getattr(bpy.data, data_name).remove(block, do_unlink=True)

# Remove unused source remnants, keeping all data referenced by the 3D scenes.
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=False, do_recursive=True)
assert not bpy.data.libraries, 'Linked libraries must be made local before distribution.'
for block in bpy.data.user_map():
    # Append provenance is not a dependency; clear obsolete source-file locations.
    ref = block.library_weak_reference
    if ref:
        ref.filepath = ''
        ref.id_name = ''

# Internal image bytes remain in the .blend; paths no longer refer to the workstation.
for im in bpy.data.images:
    if im.source == 'FILE':
        if not im.packed_file:
            im.pack()
        im.filepath = '//textures/' + Path(im.filepath.replace('\\', '/')).name
        assert im.packed_file

# Clear obsolete prose about the edit and replace local-path metadata with portable names.
for collection_name in ('scenes', 'objects', 'collections', 'materials', 'worlds', 'meshes', 'actions'):
    for block in getattr(bpy.data, collection_name):
        for key in list(block.keys()):
            value = block[key]
            if isinstance(value, str):
                if re.search(r'[A-Za-z]:[\\/]', value):
                    block[key] = re.sub(r'[A-Za-z]:[\\/][^\n\r]*', '[chemin local retiré]', value)
                if any(word in key.lower() for word in ('musique', 'montage')):
                    del block[key]

readme = '''LA NUIT ÉTOILÉE — MODÈLES BLENDER, VERSION V7

Trois scènes 3D conservées depuis le projet final :
09 | PROMENADE : village, relief, ciel, personnages, rigs et marche.
10 | LES HEURES : cycle des éclairages depuis la rue (images 745–984).
13 | LA NUIT RESPIRE : personne aux fenêtres et hirondelle (images 1–144).

Changer de scène avec le sélecteur en haut de Blender.
La scène 09 ouvre sur l'image 684 et expose la plage complète 1–1440.
Les poses, clés, matériaux, modificateurs, caméras et éclairages sont conservés.
Les personnages peuvent être masqués à certaines images par leur animation.
Les textures nécessaires sont intégrées. Aucun fichier externe n'est requis.
Utiliser Fichier > Ajouter (Append) pour réutiliser un objet ou une collection.

Le séquenceur, les pistes sonores, le montage et les rendus du film sont exclus.
Blender 5.0.0. Voir README.md et CREDITS.md dans l'archive.
'''
bpy.data.texts.new('LISEZ-MOI — Modèles V7').write(readme)
main_scene = next(s for s in bpy.data.scenes if s.name.startswith('09 |'))
bpy.context.window.scene = main_scene
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'SEQUENCE_EDITOR':
            area.type = 'VIEW_3D'
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.type = 'MATERIAL'
            if main_scene.camera:
                space.region_3d.view_perspective = 'CAMERA'
                space.region_3d.view_camera_zoom = 0
assert {s.name: len(s.objects) for s in bpy.data.scenes} == scene_counts
assert len(bpy.data.sounds) == 0 and len(bpy.data.movieclips) == 0
assert all(s.sequence_editor is None for s in bpy.data.scenes)
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(destination), compress=True, relative_remap=False)
print('PREPARED', destination, flush=True)
