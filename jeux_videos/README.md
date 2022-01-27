# Projet jeu vidéo: Base Steering
Paul LORGUE

## Fonctionnalités
J'ai implémenté 2 fonctionnalités majeurs au projet initial de steering.

- Les véhicules ralentissent à l'approche d'un virage
- Un véhicule ralenti s'il voit un autre véhicule devant lui

J'ai aussi ajouté la possibilité de faire pause dans la simulation en appuyant sur la touche *p*. Il est possible de quitter la simulation avec la touche *q*.

Pour avoir des circuits un peu plus complexe j'ai ajouté un notebook *circuit_helper.ipynb* qui permet de convertir une image monochrome (comme *catalogne.png*) d'un circuit en suite de point pour le simulateur. 

## Description technique des fonctionnalités

### Freinage à l'approche d'un virage

Cette opération est commentée en détail dans la fonction `steerPathFolow()` de *Base-Steering.py*

Le principe est le suivant: on calcule l'angle du prochain virage pour ajouter une force de freinage colinéaire et inverse à la vitesse et proportionnelle à l'angle du prochain virage.

L'angle est calculé en déterminant deux points:
- la position dans *x* pas de temps si aucune force n'est appliqué (le vehicule va tout droit)
- la position souhaité sur au milieu de la piste dans *x* pas de temps 

Pour éviter de louper une chicane en regardant trop loin on effectue deux fois cette opération pour deux pas de temps différent et on garde l'angle du virage le plus serré. 

### Freinage pour éviter la collision

Cette opération est commentée en détail dans les fonctions `updatePositions()` et `isAhead()` de *Base-steering.py* 

Avec le vecteur vitesse et la position d'un véhicule on peut calculer les équations de 4 droites formant un rectangle devant ce véhicule. 

On calcule ainsi dans `isAhead()` les paramètres de ces équations et on détermine si un autre véhicule est dans ce rectangle ou non.

On ne calcule les équations uniquement pour les véhicules proches: dans un rayon de la longueur du rectangle pour limiter les calculs.

Si un véhicule est devant alors on réduit la vitesse proportionnelement à la distance. 

### Démonstration

[Vidéo](jeux_videos/demo_jv_pl.mp4) (demo_jv_pl.mp4)