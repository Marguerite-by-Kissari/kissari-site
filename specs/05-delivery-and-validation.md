# 05 — Plan du lot desktop et recette

## Objectif du lot

Finaliser exclusivement la version **desktop française** de la landing annonçant l’arrivée du site KISSARI.

## Séquence de réalisation

1. Installer les fontes Poppins locales et les tokens visuels desktop.
2. Construire le header avec le logo fourni.
3. Construire le hero selon l’ordre de calques documenté.
4. Poser la frise de séparation.
5. Construire le manifeste avec l’asset unique `Femme jaune + logo.png`.
6. Construire le bloc expertises, les quatre cartes statiques et leurs calques.
7. Arrêter le périmètre avant le footer ; le footer sera spécifié après validation du gros du travail.
8. Réaliser la comparaison visuelle desktop avec les deux maquettes source.

## Recette desktop

- Largeur de contrôle : 1920 px ; contrôle complémentaire à 1440 px seulement pour vérifier que la composition reste contenue, sans définir de comportement tablette.
- Ordre des zones : header, hero, frise, manifeste, expertises, footer différé.
- Chaque asset correspond au chemin, à l’espace et au plan indiqués dans `01-homepage.md`.
- Poppins chargée localement avec les tailles desktop prescrites.
- Aucun lien, CTA, `En savoir plus` ou interactivité sur les cartes expertise.
- Aucun blog, newsletter, page interne ou contenu additionnel.

## Validation technique

```bash
hugo --minify --cleanDestinationDir --destination /tmp/kissari-build
```

Résultat attendu : build sans erreur et génération de `index.html`.

## W3C

Une non-conformité éventuellement détectée est enregistrée comme **proposition** avant tout changement. Elle n’entraîne pas une correction directe dans ce lot.

## Non-objectifs

- Responsive tablette/mobile.
- Footer.
- Publication, push, DNS, intégration de service tiers.
