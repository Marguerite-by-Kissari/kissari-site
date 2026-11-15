# Blog — rails horizontaux de prévisualisation

## Demande

Présenter les articles réels du blog KISSARI sous forme de lignes horizontales par catégorie, sans modifier la charte du site ni le hero. La capture de référence sert uniquement à définir la composition visuelle : elle ne doit jamais être utilisée comme source de faux articles.

## Implémentation actuelle

- Une ligne globale « Zoom sur… » regroupant les articles réels, triés du plus récent au plus ancien.
- Une ligne par catégorie lorsqu’elle contient au moins un article réel : `#Actus`, `#Jusdecerveau`, `#Interviews`, `#Outils`.
- Les quatre filtres de catégorie restent visibles dans la zone de filtrage, même lorsqu’une catégorie ne contient pas encore d’article.
- Les données des cartes proviennent des pages Hugo de `content/blog/`, jamais de cartes de démonstration.
- Les titres, chapeaux, images et liens sont générés depuis le front matter et le contenu des articles.
- Le titre de la ligne globale est éditable via `content/blog/_index.md` :

```yaml
zoom_title: "Zoom sur nos idées"
```

- Les titres des quatre catégories sont pilotés par les identifiants de catégorie et ne nécessitent pas d’édition dans l’interface éditoriale.

## Tri et évolution du contenu

Le tri de toutes les collections utilise `publishDate`, dans l’ordre :

```text
plus récent → plus ancien
```

La date de rédaction (`date`) ne doit pas être utilisée à la place de la date de publication.

Le nombre de cartes évolue automatiquement avec les nouvelles pages publiées dans `content/blog/`. Aucun nombre fixe d’articles n’est attendu.

## Cartes

Chaque carte doit respecter les règles suivantes :

- structure HTML dans un élément `<article>` ;
- largeur fluide : trois cartes complètes par rangée au-dessus de 1100 px, deux entre 701 et 1100 px, une carte principale de 88 % sur mobile ;
- hauteur naturelle homogène par rangée, sans hauteur fixe ni troncature des titres/chapeaux ;
- alignement de la première carte à `74 px` du bord gauche ;
- espace horizontal entre cartes : `28 px` ;
- marge supérieure de rangée : `48 px` sur ordinateur, `40 px` sur mobile ;
- image panoramique de largeur 100 %, hauteur `clamp(180px, 15vw, 250px)` sur ordinateur et `190 px` sur mobile ; `object-fit: cover` et `object-position: center top`, sans déformation ; le recadrage privilégie le haut de l’image pour préserver les visages ;
- coins supérieurs arrondis de manière indicative à `24 px` ;
- corps de carte : padding `24 px` sur ordinateur ;
- métadonnées : catégorie à gauche, date de publication à droite ;
- catégorie et date en Poppins bold, `16 px` sur ordinateur ;
- date au format `jj.mm.aaaa` ;
- titre dans un élément `<h3>`, Poppins bold, `32 px` sur ordinateur ;
- espace métadonnées → titre : `24 px` ;
- résumé intégral en Poppins, `18 px` sur ordinateur ;
- espace titre → résumé : `20 px` ;
- lien final en Poppins, `20 px`, capitales, positionné en bas de carte ;
- marge entre la dernière rangée et le bandeau noir : `135 px` ;
- aucune pastille numérotée ;
- image, catégorie, date, titre et résumé sont du texte/HTML séparé, jamais intégrés dans l’image.

La carte ne contient qu’un seul élément cliquable : le lien final, dont le libellé accessible exact est :

```text
Lire l'article
```

L’image est illustrative et utilise `alt=""`. Le titre et les métadonnées ne sont pas des liens. Le lien final donne accès à la page détaillée de l’article et est accessible au clavier avec `Tab`.

## Affectation des visuels validés

Le bandeau d’article et sa carte utilisent le même champ `image` :

- `marketing-formation-avant-postes-engagement` : `images/blog/Bandeaux_articles_Marketing_1-preview.png` (femme au pull gris, regard au loin).
- `marketing-learning-ne-sarrete-jamais` : `images/blog/Bandeaux_articles_Marketing_2-preview.png` (femme au tee-shirt rose et lunettes).

Les sources sont conservées dans le dossier `run/` du projet Obsidian ; les copies utilisées par ces articles historiques sont dans `static/images/blog/`. Aucun changement de cadrage du bandeau n’est requis ; les cartes conservent le cadrage haut.

## Rails et flèches

Chaque ligne possède :

- un rail horizontal indépendant ;
- une flèche gauche ;
- une flèche droite ;
- un déplacement d’un article par clic sur une flèche ;
- un déplacement clavier avec les flèches gauche/droite et `Home`/`End` ;
- un état désactivé aux extrémités ;
- le respect de `prefers-reduced-motion`.

Les flèches restent des boutons natifs avec nom accessible et focus visible. Leur design graphique pourra être affiné par Christophe sans modifier leur comportement ni leurs attributs d’accessibilité.

## Titres et typographie

- `À lire, à picorer, à partager` : Poppins bold, 20 px ;
- titre général `Tous nos articles` : Poppins bold, 72 px maximum ;
- titre éditable de la ligne globale : Poppins bold, 72 px maximum ;
- titres de catégories : Poppins bold, 72 px maximum ;
- couleur des textes : `#000000`.

Les textes restent du HTML. Les intitulés visuels ne doivent pas être intégrés dans des images.

## Validation

Contrôler avant publication :

- tri par `publishDate` décroissant ;
- absence de Lorem ipsum et de cartes fictives ;
- nombre de cartes variable selon les pages réelles ;
- quatre filtres présents dans le bon ordre ;
- flèches gauche/droite fonctionnelles ;
- déplacement d’un article par clic ;
- cartes accessibles avec un seul lien final `Lire l'article` ;
- hauteur homogène des cartes ;
- absence de chevauchement sur titres longs ;
- images non déformées ;
- navigation clavier et focus visible ;
- rendu desktop et mobile sans débordement horizontal ;
- trois cartes complètes sur ordinateur et deux sur tablette ;
- visages préservés par le cadrage haut, sans modifier la photo source ;
- aucun titre ni chapeau tronqué, aucun chevauchement avec le lien ;
- vérifier le titre de la rangée suivante lorsque la première rangée est cadrée sous le menu, notamment en 1280 × 1000 et 1920 × 1080 ; cette visibilité dépend de la hauteur disponible et du zoom, elle n’est pas garantie sur tout écran ;
- distinguer le rendu de carte du bandeau d’article et de son aperçu dans l’Atelier.
