# Utiliser les modèles dans Blender

## Explorer les trois scènes

Ouvrir `blender/La_Nuit_Etoilee_V7.blend`. Le sélecteur **Scène**, en haut de Blender, permet de passer de PROMENADE à LES HEURES ou LA NUIT RESPIRE.

Le projet s'ouvre sur la scène PROMENADE à l'image 684. Le pavé numérique **0** quitte ou retrouve la vue caméra ; le bouton central de la souris permet de tourner autour des modèles. L'Outliner liste les collections de bâtiments, reliefs, végétation, ciel, habitants, accessoires et éclairages.

Le mode **Material Preview** facilite l'exploration. Le rendu final peut différer du viewport : il utilise les éclairages de scène, le monde et le compositing conservés dans le fichier.

## Observer les animations

| Scène | Images utiles |
|---|---|
| PROMENADE | 265–384 et 625–744 pour la marche ; 684 à l'ouverture |
| LES HEURES | 745–984 pour les variations d'éclairage |
| LA NUIT RESPIRE | 1–144 pour la personne aux fenêtres et l'hirondelle |

Les trois scènes utilisent leurs repères temporels d'origine. La plage complète de PROMENADE est rétablie à 1–1440 ; le fichier de production avait été enregistré sur un intervalle de rendu partiel. Les images clés ne sont pas décalées.

Certains objets portent des animations de visibilité. Choisir une image où le personnage est présent avant de l'inspecter. Pour la personne aux fenêtres, les modificateurs booléens limitent volontairement la géométrie visible aux ouvertures : conserver leur objet de masquage lors de l'importation.

## Importer dans un autre projet

1. Ouvrir le projet de destination.
2. Choisir **Fichier → Ajouter (Append)** et sélectionner `La_Nuit_Etoilee_V7.blend`.
3. Ouvrir **Collection** pour un ensemble ou **Object** pour un objet isolé.
4. Sélectionner les éléments, puis valider l'ajout.

Préférer une collection entière pour les personnages avec rigs, les ensembles animés et les objets utilisant des masques. Le mode Append crée une copie locale modifiable dans le nouveau projet.

Pour transférer une scène complète avec son monde, ses caméras et ses réglages, choisir **Scene** au lieu de Collection.

## Ressources et performances

La texture de référence est intégrée au fichier. Les matériaux du décor sont largement procéduraux. Aucun chemin vers l'ordinateur d'origine n'est nécessaire.

Chaque scène évalue environ 3,2 millions de sommets dans les contrôles effectués. Le mode solide peut être plus fluide pour l'édition. Le projet n'est pas un export simplifié pour navigateur ou moteur de jeu.

## Contrôle reproductible

Depuis la racine du dossier, avec `blender` disponible dans le terminal :

```sh
blender --background blender/La_Nuit_Etoilee_V7.blend --python-exit-code 1 --python scripts/verify_blender.py -- docs/verification.json
```

Ce contrôle rouvre le fichier et vérifie l'inventaire, les textures intégrées, l'absence de séquenceur et de médias audio/vidéo, puis évalue les animations et les modificateurs sur onze images.
