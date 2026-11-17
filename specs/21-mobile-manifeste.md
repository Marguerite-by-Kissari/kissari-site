# Mobile — manifeste complet et lisible

Statut : version texte à gauche / visuel agrandi au bord droit validée par Eric (« impeccable, je valide ; Tu fais un push avec commentaires détaillés »). Intégration GitHub autorisée.

## Demande

Afficher tous les textes du manifeste sur mobile. La hauteur fixe de 520 px et les deux colonnes héritées du desktop coupaient le troisième engagement et la pastille finale.

## Correction, sous 800 px seulement

Dans `static/css/mobile.css` : hauteur automatique conservée. Essai demandé ensuite par Eric : titres sur la largeur disponible, engagements et pastille à gauche, illustration/photo-logo réduite à droite dans une vraie colonne de grille (colonne entre 88 et 148 px selon l’écran, visuel agrandi de 24 px vers le bord droit pour absorber le padding et toucher le bord). Pas de superposition absolue. Liste en 16 px / interligne 1,6, pastille en 14 px. Aucun texte modifié, aucune illustration recréée, aucune retouche du desktop.

## Preuves

Navigateur à 320, 390, 425, 799 px : trois engagements et pastille intégralement dans la section ; rectangles du texte dans la largeur disponible ; illustration réduite à droite sans chevauchement. À 1920 px, géométrie et tailles de police du manifeste strictement identiques à la référence avant correction.

Variante finale validée : `verification-bord-droit.json` et `manifeste-bord-droit-390.png`. Les captures et contrôles précédents documentent les variantes intermédiaires.

Fichiers de preuve : `livrables/recette-mobile-manifeste/verification.json`, `desktop-before.json`, `manifeste-390.png`.

Aperçu interactif existant : <http://127.0.0.1:18824/>. Site : <http://127.0.0.1:1313/#notre-manifeste>.

La section Expertises suivante reste hors de cette correction ; aucune prétention de recette mobile globale. L’utilisateur vérifie personnellement le push du lot précédent.
