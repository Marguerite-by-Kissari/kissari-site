# Corrections éditoriales du blog

Statut : corrections validées par Eric le 17 novembre 2026 : « on push le tout dans github ; je valide l’ensemble des corrections ». Intégration GitHub sur main autorisée ; aucune demande de déploiement sur le serveur de recette. Les mentions « local uniquement » ci-dessous décrivent l’état historique avant cette validation.

## Modifications demandées

- Zoom : « Zoom sur le marketing learning », via `data/blog_editorial.json`, repris aussi dans le catalogue et l’atelier régénéré.
- Pourquoi le marketing learning ne s’arrête jamais ? : remplacement du passage incomplet par « Du coup, une petite idée de la mission du marketing learning by KISSARI ? Bingo ! C’est bien de révéler cette envie, la nourrir et l’entretenir. ». Suite du paragraphe conservée.
- Article aux avant-postes : titre devenu « Le marketing learning aux avant-postes de l’engagement ». URL et nom de fichier inchangés, cartes et bandeau suivant actualisés automatiquement.
- Classe virtuelle : « dispose d’armes de distraction massive » ; suppression du J parasite après frigo ; suppression de la phrase extérieure précédant l’encadré jaune et intégration au titre commun de l’encadré.

## Titre explicite sur deux lignes

```go-html-template
{{< callout tone="yellow" title="Et pour éviter le fameux Vous êtes toujours là…" title_line2="voici cinq incontournables ..." >}}
```

`layouts/shortcodes/callout.html` accepte `title_line2`, optionnel. Les deux textes restent dans le même `.article-callout__title` (non-heading, comme le composant existant), séparés par `<br>`. Texte échappé normalement ; aucun HTML arbitraire activé. Sans `title_line2`, rendu inchangé. Aucun changement CSS global.

Deux lignes physiques vérifiées à 1920 px, toutes deux en 44 px / graisse 700. À 390 px, elles reviennent naturellement à la ligne pour rester lisibles.

## Preuves

- Test ajouté : `scripts/test-blog-copy-corrections.py`, échec initial sur l’ancien Zoom, puis réussite sur un vrai build minifié.
- Build Hugo ; navigation suivante ; navigation générale ; configuration et builds éditoriaux ; PDF légaux ; aperçu connecté ; notes inline ; `git diff --check` : réussis.
- Un nom de test inexistant a été détecté lors du premier enchaînement ; il n’est pas compté comme un test réussi. Contrôles réels effectués ensuite avec les scripts présents.
- Navigateur : blog et trois articles à 1920 et 390 px. Capture `livrables/recette-blog-corrections/classe-virtuelle-titre-1920.png`.
- Limite préexistante : léger débordement de 7 px de l’article Pourquoi à 390 px (largeur utile 375, contenu 382), identique avec l’ancien et le nouveau paragraphe ; non modifié dans ce lot éditorial. Comparaison enregistrée dans `preexisting-mobile-overflow.json`.

## Amendement FormPro — visuel et J orphelin

- Source `corrections-finale/Bandeaux_articles_Formpro.png`, copiée sans retouche dans le bundle de l’article ; front matter `image` mis à jour. Même format 720 × 635 RGBA et même emprise alpha que l’ancien visuel : aucun changement de CSS, taille ou placement du bandeau. Nom distinct pour éviter le cache de l’ancienne image.
- Dans le dernier encadré jaune, item Storytelling : `bien sûr) J !` → `bien sûr) !`. Aucun autre texte de l’article modifié.
- Atelier régénéré depuis les sources. Build minifié et tests de corrections blog/navigation suivante réussis. Navigateur vérifié à 1920, 800 et 390 px : nouveau PNG chargé, octets HTTP identiques au fichier fourni, J absent, pas de débordement horizontal pour FormPro.
- Preuves : `livrables/recette-formpro-visuel/`, dont `article-before.md`, `source-verification.json`, `browser-verification.json`, `formpro-bandeau-800.png`.
- URL conservée : <http://127.0.0.1:1313/blog/parlez-vous-formpro/>. Lot local uniquement, sans push ni déploiement distant.

## Préservation du travail précédent

Les correctifs locaux des cartes Expertises et des PDF finaux restent présents. Aucun push GitHub ni publication sur le serveur de recette. Sources d’avant ce lot conservées sous `livrables/recette-blog-corrections/before/`.
