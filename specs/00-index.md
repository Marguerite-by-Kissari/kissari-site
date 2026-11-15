# KISSARI — dossier de spécifications

> **Statut :** brouillon de travail, à relire et arbitrer avant toute nouvelle implémentation.
>
> **Périmètre :** une landing page française annonçant l’arrivée du futur site, fondée exclusivement sur les éléments visuels du vault. Le lot courant concerne uniquement le desktop ; aucune décision éditoriale, aucun contenu additionnel ni aucune publication ne sont inclus.

## Source de vérité et niveau de preuve

| Source | Rôle | Niveau |
|---|---|---|
| `1024-2623.png` | maquette longue de la page d’accueil | référence principale |
| `960-1639-max.png` | annotations de structure, responsive, design system et composants | référence principale |
| `KISSARI V1/.../SPECS SITE KISSARI V1.rtf` | premiers éléments typographiques et sections | référence complémentaire |
| `KISSARI V1/.../Livrables/` | assets, logo, personnages, pictogrammes, frises | source graphique |
| `Poppins/` | fontes sous licence OFL | source typographique |

## Documents à relire

1. [01 — Page d’accueil et exigences](01-homepage.md)
2. [02 — Système visuel](02-visual-system.md)
3. [03 — Composants et interactions](03-components-interactions.md)
4. [04 — Contenu, navigation et données manquantes](04-content-and-ia.md)
5. [05 — Plan d’implémentation et recette](05-delivery-and-validation.md)
6. [06 — Questions à arbitrer](06-open-questions.md)
7. [07 — Demande de livrables graphiques statiques](07-static-artwork-handoff.md)

## Lot M15 — prototype isolé autorisé

[12 — Rubrique éditoriale du blog et atelier](12-M15-rubrique-editoriale.md). Proposition validée pour spécification et prototype, pas encore acceptée pour intégration dans le site validé. Copie de test : `livrables/prototype-M15/site/`.

## Évolution de l’atelier — GitHub et publication différée

[13 — Pilotage GitHub avec/sans PR et publication planifiée](13-atelier-github-publication-planifiee.md). Cadrage à valider ; aucune connexion au dépôt ni installation de workflow distant. Le test connecté local est inclus dans l’amendement M15.

## Convention de lecture

- **Confirmé** : directement visible/lisible dans une référence.
- **Proposé** : choix d’implémentation nécessaire mais absent des sources.
- **À arbitrer** : décision métier, éditoriale ou juridique manquante.

## État Spec Kit

`specify` est installé (v0.0.22) mais ce prototype n’est **pas initialisé** avec Spec Kit : `.specify/` est absent. Ce dossier `specs/` constitue le référentiel de travail versionnable ; n’initialiser Spec Kit qu’après validation du périmètre, car cela écrira des fichiers additionnels dans le projet.
