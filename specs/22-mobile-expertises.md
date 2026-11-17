# Expertises mobile — titres, cadres et lecture

Statut : modifications validées par Eric (« tu peux push, je valide les modifications »). Intégration sur main autorisée.

## Demande et rendu

Sous 800 px uniquement :

- Deux phrases de titre sur la pleine largeur, l’une sous l’autre : « KISSARI votre partenaire transformation ... » puis « ... ou 4 façons de vous faire aimer toutes les matières ». Les retours à la ligne sont naturels sur les téléphones : pas de réduction à une taille illisible pour forcer deux lignes physiques.
- Quatre personnages masqués (`.card-person`) ; quatre pictogrammes, numéros et fichiers de fond coloré conservés.
- Grille à deux colonnes conservée, coins droits sur le conteneur et les cartes.
- Cartes de hauteur automatique, texte remis dans le flux et sur toute la largeur intérieure de chaque carte. Paragraphes en 14 px / interligne 1,5 ; aucun texte réécrit ni supprimé.

Le titre desktop reste exactement le même grâce à des variantes de texte conditionnées par le CSS ; seules les variantes visibles sont exposées à la lecture. Les anciennes césures desktop sont conservées.

## Vérifications réelles

- Navigateur : 320 / 390 / 425 / 799 px, quatre cartes complètes et tous les rectangles de texte dans leur cadre, numéros et icônes présents, personnages invisibles, arrondis à 0.
- 1920 px : géométrie, fontes, arrondis et affichage des éléments desktop identiques à la référence avant modification.
- Preuves : `livrables/recette-mobile-expertises/{desktop-before.json,verification.json,expertises-mobile-390.png}`.

## Présentation

Aperçu : <http://127.0.0.1:18824/>. Section : <http://127.0.0.1:1313/#ce-qui-nous-anime>.

Fichiers : `layouts/index.html`, `static/css/mobile.css`. Lot autorisé à l’intégration GitHub après validation ; les lots précédents validés restent intacts.
