# The Starry Night — Blender Models

The 3D scenes of **The Starry Night**, inspired by Vincent van Gogh, from the **V7 version used in the final film**. The village, sculpted sky, cypress trees, landscape, inhabitants, swallows, props, and lighting are available in one editable Blender file.

**[Download the complete Blender project](https://github.com/Firisis971/van-gogh-blender/releases/latest)** · [Blender guide](docs/GUIDE_BLENDER.md) · [Credits](CREDITS.md)

![The village in 3D](previews/village.png)

## Download and open

1. Go to **Releases** and download **La_Nuit_Etoilee_V7_Blender.zip**.
2. Extract the archive.
3. Open `blender/La_Nuit_Etoilee_V7.blend` in **Blender 5.0 or a compatible version**. The project was verified with **Blender 5.0.0**.

Required textures are packed into the `.blend` file. No third-party add-ons, external Blender libraries, music, or image sequences are required.

> **Code → Download ZIP** downloads the documentation and scripts. The **complete Blender file is available under Releases**, because it exceeds the regular Git file size limit.

## What's included

| Blender scene | Available content | Animation |
|---|---|---|
| **09 · PROMENADE — Regards dans la nuit** (A walk through the night) | Village, landscape, cypress trees, moon, stars, frame, characters, street props, cameras, and lights | Frames 1–1440; opens at frame 684 |
| **10 · LES HEURES — Depuis la rue** (The hours, seen from the street) | Village and lighting cycle | Frames 745–984 |
| **13 · LA NUIT RESPIRE — Fenêtre et hirondelle** (The breathing night: window and swallow) | Character at two windows, props, window masks, and swallow | Frames 1–144 |

The file contains **750 objects**, **473 mesh data blocks**, **675 materials**, **13 armatures**, and **220 animation data blocks**. These totals include the variants needed by the three scenes and data retained from the source file; they do not represent 750 unique models.

Procedural materials, modifiers, rigs, animated poses, cameras, lights, worlds, and compositing settings are preserved. Visibility animations remain active: some characters are intentionally hidden at certain frames.

| Characters and props | Life at the windows |
|---|---|
| ![Characters in the village](previews/personnages.png) | ![The window scene](previews/fenetres.png) |

## Release scope

This release contains **only the V7 Blender models and 3D scenes**. The film, MP4 files, music, sound, image sequences, and sequencer edit are not distributed. The images above are still previews rendered from the shared Blender file.

Earlier model versions are not included. Original French scene, object, and collection names are preserved so they remain easy to locate in Blender; English explanations are provided in the documentation.

## Reuse an element

In another Blender project, choose **File → Append**, select the `.blend` file, then open **Collection** or **Object**. For an animated character, append its collection together with its armature and props. See the [detailed guide](docs/GUIDE_BLENDER.md).

## Verification and scripts

- [Verification report](docs/verification.json): inventory, absence of external dependencies, sound, and sequencer data, plus evaluation of eleven representative animation frames.
- `scripts/prepare_blender.py`: creates a 3D-only copy from the original V7 file; source and destination paths are supplied as arguments.
- `scripts/verify_blender.py`: checks the shared file in Blender.
- `scripts/render_previews.py`: renders the three still previews.
- `scripts/package_release.py`: builds the complete downloadable archive and its SHA-256 checksum.

The scripts are optional: the Blender file opens directly. The preparation script requires the original production file, which is not distributed because it contains the edit.

## Credits and reuse permissions

See [CREDITS.md](CREDITS.md) for Van Gogh and the MakeHuman anatomical bases. Third-party licenses continue to apply to their respective assets. This release does not assign a general reuse license to the project's original creations; contact [Firisis971](https://github.com/Firisis971) for permission.
