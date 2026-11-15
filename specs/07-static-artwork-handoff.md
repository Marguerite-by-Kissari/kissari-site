# 07 — Demande de livrables graphiques statiques (desktop 1920 px)

> **But :** éliminer le repositionnement fragile de calques photographiques, logos, textures et pictogrammes dans le navigateur. Les compositions graphiques sont livrées **déjà montées** ; le site ne gère que leur emplacement global et les textes HTML.

## Décision de production

- Référence desktop unique : **1920 px de large**, à 100 % de zoom.
- Les compositions contenant une photo, une texture, plusieurs plans ou un pictogramme doivent être livrées sous la forme d'un **PNG RGBA aplati**.
- Le PNG conserve la transparence autour de la composition lorsqu'il est superposé au fond CSS.
- Le SVG est réservé aux éléments réellement vectoriels et indépendants : logo isolé, icône isolée, frise monochrome. Il ne convient pas aux collages photo/texture : y intégrer des photos ne ferait que déplacer le problème dans un fichier XML.
- Les PNG ci-dessous sont les **masters**. Une variante WebP pourra être générée par le site pour optimiser le poids ; elle ne remplace pas la source PNG.
- Aucun texte éditorial ne doit être inclus dans ces images. Les textes restent en HTML/CSS : sélectionnables, accessibles et modifiables sans refaire les visuels.

## Livrable 1 — Hero « Le nouveau site arrive bientôt. »

**Fichier demandé :** `hero-art-desktop-1920.png`  
**Canvas :** `1920 × 1350 px`, PNG RGBA, fond transparent.

### À intégrer dans le PNG, aux positions finales de la maquette

- femme rouge ;
- grand symbole KISSARI blanc sous la femme ;
- carré rose/texturé et logo KISSARI central ;
- cercle bleu ;
- pictogramme lecteur à cheval sur le cercle bleu ;
- tout élément décoratif non textuel associé.

### À exclure impérativement

- le titre, le surtitre et le paragraphe ;
- le mot `bientôt.` et son effet rose : ils seront gérés en CSS avec le titre ;
- le fond ivoire de la section (géré en CSS).

### Règle d'intégration

Le site placera une seule image à largeur `100 %` dans la section hero. Il ne découpe pas, ne recadre pas et ne déplace aucun sous-calque. L'illustration doit donc être visuellement correcte seule sur un fond `#F8F8F5` à 1920 px.

## Livrable 2 — Illustration du manifeste

**Fichier demandé :** `manifest-art-desktop-1920.png`  
**Canvas :** `1920 × 2300 px`, PNG RGBA, fond transparent.

### À intégrer

- personnage jaune ;
- grand symbole KISSARI noir ;
- toute interaction graphique entre le personnage et le symbole.

### À exclure

- fond rose (CSS) ;
- libellé, titre, sous-titre, trois phrases, séparateurs et pastille CTA (HTML/CSS).

La zone gauche destinée au texte doit rester visuellement libre, conformément à la maquette. L'image est un unique décor de section, pas une collection de calques à reconstruire.

## Livrables 3 à 6 — Cartes « Ce qui nous anime »

**Fichiers demandés :**

```text
expertise-01-imaginer.png
expertise-02-transformer.png
expertise-03-creer.png
expertise-04-faire-rayonner.png
```

**Canvas par fichier :** carré strict, `1707 × 1707 px` (ou, si un export plus léger est imposé, `1024 × 1024 px`). PNG RGBA ou PNG opaque si le fond coloré couvre bien tout le carré.

### Composition de chaque carré

- le fond couleur complet ;
- le personnage ;
- le pictogramme ;
- les éventuels éléments décoratifs.

### Zone de texte réservée

Le graphiste fournit la carte avec une zone intentionnellement dégagée pour le texte HTML. Cette zone doit être indiquée dans un mémo de livraison par un rectangle exprimé en pixels : `x`, `y`, `largeur`, `hauteur`, sur le canvas source.

Exemple : `expertise-01-imaginer.png — texte : x=110, y=250, l=690, h=980`.

### Angles : décision technique

**Oui : les quatre livrables doivent être parfaitement carrés, sans arrondi incorporé.**

- CSS appliquera les arrondis sur le **conteneur unique de la grille 2×2**, avec `overflow: hidden`.
- Seuls les quatre angles extérieurs de la grille seront arrondis, exactement comme la maquette.
- Les jonctions intérieures restent parfaitement droites et sans liseré.
- Chaque carte reste un carré ; CSS n'a qu'à faire la grille et positionner le texte dans sa zone réservée.

## Informations nécessaires pour intégrer le texte proprement

Pour chaque zone textuelle, fournir ou valider :

1. **Texte définitif**, avec retours à la ligne voulus, capitales, ponctuation et emphases.
2. **Fonte de référence** et fichiers autorisés (Poppins actuelle : Regular, Bold, ExtraBold), plus le poids exact par élément.
3. **Bloc de placement à 1920 px** : `x`, `y`, largeur maximale et hauteur maximale, en pixels.
4. **Style** : taille en px, interlignage, approche/letter-spacing, couleur, alignement, casse.
5. **Hiérarchie** : surtitre, titre, sous-titre, texte courant, numéro, CTA ; et l'ordre exact d'affichage.
6. **Éléments de séparation** : largeur, épaisseur, couleur et marges des traits sous les phrases.
7. **Règles de débordement** : texte strictement inchangé, nombre maximal de lignes par bloc et comportement si un libellé dépasse.
8. **Une capture de recette à 1920 px**, sans zoom navigateur, servant de référence finale.

## Contrôle de réception des assets

Avant intégration, vérifier :

- dimensions exactes du canvas ;
- absence de texte accidentel dans les PNG ;
- transparence réellement préservée là où elle est demandée ;
- pas de marge blanche involontaire ni de recadrage de personnage ;
- cohérence des couleurs avec la maquette ;
- zone texte réellement libre ;
- rendu validé sur fond CSS à 1920 px.

## Résultat attendu côté intégration

- **Hero :** une illustration statique + texte HTML.
- **Manifeste :** une illustration statique + texte HTML.
- **Expertises :** quatre images carrées statiques, une par carte + texte HTML dans une zone réservée + angles externes en CSS.

C'est volontairement moins « malin ». Donc nettement moins cassable. Bon débarras aux chorégraphies de `z-index`.
