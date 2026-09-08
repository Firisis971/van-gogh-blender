# Using the models in Blender

## Explore the three scenes

Open `blender/La_Nuit_Etoilee_V7.blend`. Use the **Scene** selector at the top of Blender to switch between PROMENADE, LES HEURES, and LA NUIT RESPIRE. Original French names inside Blender are retained; the table below explains their contents.

The project opens in PROMENADE at frame 684. Press **Numpad 0** to enter or leave camera view; use the middle mouse button to orbit around the models. The Outliner lists collections of buildings, terrain, vegetation, sky, inhabitants, props, and lights.

**Material Preview** mode is useful for exploration. The final render can differ from the viewport because it uses the scene lighting, world, and compositing settings preserved in the file.

## Inspect the animations

| Scene | Useful frames |
|---|---|
| PROMENADE — village and characters | 265–384 and 625–744 for walking; opens at 684 |
| LES HEURES — lighting cycle | 745–984 for lighting changes |
| LA NUIT RESPIRE — windows and swallow | 1–144 for the character at the windows and the swallow |

All three scenes retain their original frame numbers. PROMENADE's full range is restored to 1–1440; the production file had been saved with a partial rendering range. Keyframes are not shifted.

Some objects have visibility animations. Choose a frame where a character is visible before inspecting it. For the character at the windows, Boolean modifiers intentionally limit the visible geometry to the window openings: keep their mask object when importing.

## Import into another project

1. Open the destination project.
2. Choose **File → Append** and select `La_Nuit_Etoilee_V7.blend`.
3. Open **Collection** for a group or **Object** for an individual object.
4. Select the elements and confirm the append operation.

Prefer a complete collection for rigged characters, animated groups, and objects that use masks. Append creates a local, editable copy in the destination project.

To transfer a complete scene with its world, cameras, and settings, choose **Scene** instead of Collection.

## Resources and performance

The reference texture is packed into the file. Most environment materials are procedural. No path to the original workstation is required.

Each scene evaluates approximately 3.2 million vertices in the checks performed. Solid mode may be more responsive for editing. This project is not an optimized export for a browser or game engine.

## Reproduce the verification

From the project root, with `blender` available in your terminal:

```sh
blender --background blender/La_Nuit_Etoilee_V7.blend --python-exit-code 1 --python scripts/verify_blender.py -- docs/verification.json
```

This check reopens the file, verifies the inventory, packed textures, and absence of sequencer and audio/video media, then evaluates animations and modifiers at eleven frames.
