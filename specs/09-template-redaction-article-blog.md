# Template de rédaction — article de blog KISSARI

**Statut :** modèle éditorial et technique validé pour transposition Hugo  
**Format source :** Markdown  
**Destination :** nouveau format `content/blog/<jj-mm-aaaa>-<slug>/index.md` avec ses images dans le même dossier. Le format historique `content/blog/<slug>.md` reste compatible.

**Export Atelier et intégration :** voir `10-import-atelier-article.md`. Pour un dossier autonome, le champ `image` contient le nom local de la photo, par exemple `photo.jpg`.

---

## 1. Principe général

Un article KISSARI est rédigé comme un parcours éditorial structuré :

1. un bandeau d’ouverture avec catégorie, titre, chapeau et image ;
2. une introduction courte et forte ;
3. des sections H2 régulières ;
4. éventuellement un encadré rose de citation ;
5. éventuellement un encadré jaune pour une liste numérotée ;
6. éventuellement un encadré noir de conclusion ;
7. un bandeau automatique « A LIRE AUSSI » vers l’article suivant, ou un teaser éditorial non cliquable si aucun article suivant n’est encore publié.

Le template Hugo prend en charge automatiquement :

- le menu et le pied de page ;
- le bandeau d’ouverture ;
- la catégorie ;
- l’image principale ;
- la navigation vers l’article suivant ;
- le bandeau « A LIRE AUSSI » ;
- les dimensions et espacements généraux.

La rédaction doit donc fournir uniquement les métadonnées et le contenu éditorial structurés ci-dessous.

---

## 2. Fichier et slug

Créer un fichier :

```text
content/blog/<jj-mm-aaaa>-<slug>/index.md
```

Règles du slug :

- minuscules uniquement ;
- mots séparés par des tirets ;
- sans accent ;
- sans espace ;
- stable après publication.

Exemple :

```text
content/blog/29-10-2026-marketing-formation-avant-postes-engagement/index.md
```

---

## 3. Front matter Hugo obligatoire

Utiliser ce bloc YAML au début du fichier :

```yaml
---
title: "Titre exact de l’article"
slug: "titre-exact-de-l-article"
description: "Chapeau affiché dans le bandeau d’ouverture et les cartes du blog."
author: "Prénom NOM"
date: 2026-01-01
publishDate: 2026-01-01
lastmod: 2026-01-01
categories:
  - "categorie-id"
tags:
  - "tag-principal"
  - "tag-secondaire"
image: "image-principale.png"
featured: false
featured_order:
draft: false
source_document: "Nom du document source.docx"
next_teaser:
---
```

### 3.1. Règles des champs

| Champ | Règle |
|---|---|
| `title` | Titre éditorial exact. Ne pas le modifier pour des raisons de mise en page. |
| `slug` | Identifiant stable ASCII, en minuscules et avec tirets. |
| `description` | Chapeau court, complet et relu. Il apparaît dans le bandeau. |
| `author` | Nom affiché si nécessaire dans les données, même si le template ne le répète pas sous la frise. |
| `date` | Date d’écriture. |
| `publishDate` | Date effective de publication. Ne pas l’inventer. Peut rester vide si inconnue. |
| `lastmod` | Date de dernière modification éditoriale. Peut rester vide si inconnue. |
| `categories` | Identifiant de catégorie ASCII, par exemple `jusdecerveau`. |
| `tags` | Identifiants ASCII stables, minuscules, avec tirets. |
| `image` | Nom de la photo locale dans le dossier de l’article. Les anciens chemins `images/blog/...` restent compatibles. Cartes cadrées en haut, voir `08-blog-rails.md`. Le template génère `alt=""` pour ces images décoratives. |
| `featured` | `true` ou `false`, indépendamment de la chronologie. |
| `featured_order` | Nombre uniquement si l’article est featured. |
| `draft` | `true` par défaut dans l’Atelier ; `false` pour un article validé et prêt à publier. La date `publishDate` doit être atteinte. |
| `source_document` | Nom du document source permettant la traçabilité éditoriale. |
| `next_teaser` | Texte optionnel du bandeau bleu lorsqu’aucun article suivant réel n’est publié. Le teaser n’est pas cliquable. |

### 3.2. Catégories et tags

Affichage de la catégorie :

```text
#Jusdecerveau
```

Identifiant source :

```yaml
categories:
  - "jusdecerveau"
```

Ne jamais utiliser dans les tags :

- accents ;
- espaces ;
- `#` ;
- majuscules variables ;
- variantes synonymes non documentées.

---

## 4. Structure Markdown du corps de l’article

Ordre recommandé :

```markdown
**Introduction éditoriale forte.**

> **Citation ou baseline courte.**

## Première section

Paragraphe de développement.

## Deuxième section

Paragraphe de développement.

{{< callout color="yellow" title="Une partition en trois temps" label="Une partition en trois temps" >}}
1. **Avant**, texte de l’étape.
2. **Pendant**, texte de l’étape.
3. **Après**, texte de l’étape.
{{< /callout >}}

## Section suivante

Paragraphe de développement.

{{< callout color="black" title="Conclusion forte ou message de positionnement" label="Message clé" >}}
Texte de conclusion ou appel éditorial.
{{< /callout >}}
```

Le corps de l’article ne doit pas contenir :

- le menu ;
- le pied de page ;
- le bandeau d’ouverture ;
- le nom de l’auteur répété sous la frise ;
- le chapeau répété sous la frise ;
- le bandeau « A LIRE AUSSI » ;
- une navigation manuelle précédent/suivant ;
- des libellés techniques comme « Encadré jaune » ou « Encadré noir » ;
- du Lorem ipsum ;
- « Article à venir » ;
- des liens Obsidian `[[...]]` dans le contenu Hugo.

---

## 5. Règles typographiques

### 5.1. Introduction

Le premier paragraphe du corps est l’introduction, sans titre « Introduction ».

```markdown
**Face aux difficultés à mobiliser les apprenants, une conviction s’est imposée : ...**
```

Rendu attendu :

- Poppins ;
- bold ;
- 30 px ;
- `#000000` ;
- espace après : 40 px ;
- alignement à gauche.

Ne pas créer de H2 pour le mot « Introduction ».

### 5.2. Paragraphes courants

- Poppins ;
- 22 px ;
- `#000000` ;
- espace après : 30 px ;
- phrases courtes et paragraphes lisibles ;
- éviter les blocs de texte inutilement longs.

### 5.3. Sections

Utiliser un H2 Markdown :

```markdown
## Une vision en avance de phase
```

Rendu attendu :

- H2 ;
- Poppins bold ;
- 44 px ;
- `#000000` ;
- espace après : 44 px.

### 5.4. Mise en gras

Utiliser le Markdown standard :

```markdown
**expression ou phrase à mettre en évidence**
```

Le gras doit être réservé :

- aux idées fortes ;
- aux formulations validées par la rédaction ;
- aux passages explicitement signalés dans la maquette ou le document source.

Ne pas mettre automatiquement tout un paragraphe en gras, sauf pour l’introduction ou un encadré qui le demande explicitement.

---

## 6. Encadré rose — citation ou baseline

**VALIDÉ / VERROUILLÉ — 30 octobre 2026.** Visuel `guillemets.png` en tête, texte en dessous, hauteur `1.75cap`, proportions conservées. Application globale au site et à l’aperçu Atelier (version intégrée et autonome, image embarquée). Toute modification de ce contrat nécessite une nouvelle demande explicite. Les cadres jaunes/noirs et les contenus rédactionnels restent inchangés.

Syntaxe :

```markdown
> **C’est dans l’art de façonner l’envie que naissent les apprentissages appelés à durer.**
```

Rendu attendu :

- fond rose ;
- coins arrondis ;
- texte Poppins bold ;
- picto graphique en haut à gauche ;
- texte aligné à gauche sous le picto ;
- picto séparé du bord gauche selon la maquette ;
- pas de saut de ligne artificiel après le texte ;
- fermeture de l’encadré juste après la citation.

Ne pas écrire le picto dans le Markdown. Il est généré par le CSS à partir de `static/images/blog/guillemets.png`, sans modifier le texte de l’Atelier. Le visuel décoratif ouvre le cadre, puis le titre éventuel et le corps éditorial restent en dessous dans le flux normal. Hauteur : `1.75cap` (1,75 fois la hauteur d’une capitale ; repli `1.25em`), proportions conservées. Ce rendu s’applique aux citations Markdown historiques et aux shortcodes `callout color="pink"`, sans modifier les cadres jaunes ou noirs.

Ne pas ajouter de libellé technique avant la citation.

---

## 7. Encadré jaune — liste numérotée

Utiliser le shortcode :

```markdown
{{< callout color="yellow" title="Une partition en trois temps" label="Une partition en trois temps" >}}
1. **Avant**, il s’agit de susciter l’envie : faire découvrir l’offre, donner du sens à la formation, montrer ses bénéfices concrets et donner envie d’y consacrer du temps.
2. **Pendant**, l’enjeu est de maintenir l’engagement : proposer une expérience stimulante, favoriser les interactions, valoriser les progrès et encourager la participation active.
3. **Après**, l’objectif est de prolonger la dynamique : faciliter la mise en pratique sur le terrain, encourager le partage d’expériences et ancrer les nouvelles pratiques dans le quotidien.
{{< /callout >}}
```

Rendu attendu :

- fond jaune ;
- coins arrondis ;
- titre de mise en avant, hors hiérarchie des titres ;
- espace après le titre : 44 px ;
- texte Poppins bold, 24 px, `#000000` ;
- numéros `01`, `02`, `03` ;
- numéros dans des cercles blancs ;
- cercles positionnés à gauche ;
- texte occupant la largeur disponible de l’encadré ;
- retour à la ligne normal sur plusieurs lignes ;
- aucun picto de citation rose.

Ne pas écrire manuellement `01`, `02`, `03` dans le texte : la numérotation est générée par CSS à partir de la liste ordonnée.

---

## 8. Encadré noir — message final

Utiliser le shortcode :

```markdown
{{< callout color="black" title="Vos formations méritent mieux qu’un mail à J-7." label="Message clé" >}}
C’est cette conviction qui anime aujourd’hui KISSARI : faire en sorte que les formations ne soient pas seulement conçues, déployées et financées… mais surtout suivies, vécues et mises en pratique !
{{< /callout >}}
```

Rendu attendu :

- fond `#000000` ;
- coins arrondis ;
- titre de mise en avant hors hiérarchie, Poppins bold, 44 px, `#fbec88` ;
- espace après le titre : 30 px ;
- texte Poppins bold, 24 px, `#ffffff` ;
- espace inférieur : 30 px ;
- le corps est rendu dans un conteneur `.article-callout__body` afin que le texte blanc reste stylable et accessible ;
- aucun picto de citation.

- une note de bas de page s’écrit avec la syntaxe Markdown `[^1]` et `[^1]: texte` ;
- le renvoi et le marqueur visuel de la note s’affichent comme `*` via CSS, tout en conservant les liens sémantiques de renvoi et de retour ;
- une note ne doit pas être simulée avec un astérisque littéral dans le texte de la citation.

## 9. Bandeau « A LIRE AUSSI »

Ne pas rédiger ce bandeau dans le Markdown.

Le template Hugo le génère automatiquement à partir de l’article suivant dans la chronologie de la catégorie. Si aucun article suivant n’existe, un teaser peut être fourni dans le front matter :

```yaml
next_teaser: "Avec le marketing learning, va y avoir de l’action !"
```

Le teaser est visuel et non cliquable tant qu’aucune page correspondante n’existe.

Règles de rendu :

- fond bleu ;
- largeur maximale : 1920 px ;
- hauteur indicative : 500 px ;
- libellé `A LIRE AUSSI` ou `ARTICLES SUIVANT :` en Poppins majuscules, 24 px, noir ;
- libellé aligné à 74 px du bord gauche ;
- titre aligné à 148 px du bord gauche ;
- titre visuel hors hiérarchie, Poppins bold, 88 px, noir ;
- élément droit aligné à 74 px du bord droit lorsque le bandeau est lié ;
- titre cliquable uniquement lorsqu’un article réel existe ;
- pas de faux lien ni de fausse page article.

La navigation n’est donc pas écrite à la main dans le fichier Markdown, à l’exception du champ optionnel `next_teaser`.

---

## 10. Checklist avant intégration Hugo

### Métadonnées

- [ ] `title` exact et validé ;
- [ ] `slug` ASCII stable ;
- [ ] `description` rédigée et relue ;
- [ ] `date`, `publishDate` et `lastmod` séparées ;
- [ ] aucune date inventée ;
- [ ] catégorie ASCII correcte ;
- [ ] tags ASCII, minuscules et séparés par des tirets ;
- [ ] image existante et validée ;
- [ ] image décorative avec `alt=""` généré par le gabarit ; vérifier le cadrage des visages dans la carte ;
- [ ] source documentaire indiquée.

### Corps éditorial

- [ ] introduction sans titre « Introduction » ;
- [ ] introduction entièrement en gras si la maquette le demande ;
- [ ] premier paragraphe à 30 px ;
- [ ] paragraphes courants à 22 px ;
- [ ] titres de sections en H2 ;
- [ ] titres H2 à 44 px ;
- [ ] espaces entre les blocs respectés ;
- [ ] passages en gras explicitement validés ;
- [ ] encadrés utilisant le shortcode `callout` ;
- [ ] notes de bas de page utilisant `[^1]` plutôt qu’un astérisque littéral ;
- [ ] aucune indication technique visible ;
- [ ] aucun doublon de chapeau ou d’auteur.

### Vérification technique

Depuis la racine du projet :

```bash
hugo --minify --cleanDestinationDir --destination /tmp/maversionkissari-build
```

Puis contrôler :

- absence d’erreur Hugo ;
- page blog en HTTP 200 ;
- page article en HTTP 200 ;
- image présente ;
- encadrés présents ;
- bandeau lié ou teaser non cliquable conforme au front matter ;
- absence de Lorem ipsum ;
- absence de « Article à venir » ;
- rendu visuel vérifié sur desktop et mobile.

---

## 11. Gabarit vierge copiable

```markdown
---
title: "[Titre exact]"
slug: "[slug-ascii-stable]"
description: "[Chapeau court affiché dans le bandeau d’ouverture]"
author: "[Prénom NOM]"
date: YYYY-MM-DD
publishDate:
lastmod:
categories:
  - "[categorie-id]"
tags:
  - "[tag-principal]"
  - "[tag-secondaire]"
image: "[image-existante].png"
featured: false
featured_order:
draft: false
source_document: "[Document source]"
next_teaser:
---

**[Introduction éditoriale forte, sans titre, en une ou deux phrases.]**

> **[Citation ou baseline courte.]**

## [Première section]

[Paragraphe de 22 px.]

## [Deuxième section]

[Paragraphe de 22 px avec les passages importants en gras.] 

{{< callout color="yellow" >}}
## [Titre de la liste numérotée]

1. **Avant**, [texte].
2. **Pendant**, [texte].
3. **Après**, [texte].
{{< /callout >}}

## [Section suivante]

[Paragraphe de 22 px.]

{{< callout color="black" title="Titre final fort" label="Message clé" >}}
[Conclusion en blanc, bold, 24 px.]
{{< /callout >}}
```

---

## 12. Règle de prudence éditoriale

Le template ne doit pas être utilisé pour inventer :

- des dates ;
- des auteurs ;
- des citations ;
- des formulations présentées comme historiques ;
- des images ;
- des liens ;
- des éléments de preuve.

En cas d’information manquante, laisser le champ vide ou signaler explicitement le point à valider avant publication.

---

## 13. Règles d’accessibilité sanctuarisées

Ces règles sont obligatoires pour toute nouvelle page article et toute modification de template.

### Hiérarchie

- un seul `<h1>` par page : le titre de l’article ;
- les sections éditoriales utilisent les `<h2>` ;
- le bandeau final « A LIRE AUSSI » utilise un élément visuel non hiérarchique, pas un second `<h1>` ;
- les titres visuels des encadrés utilisent un paragraphe stylé, pas un `<h1>`, `<h2>` ou `<h3>` ;
- l’ordre des titres ne doit pas être sauté.

### Images

- l’image du personnage dans le bandeau est décorative et doit avoir `alt=""` ;
- la frise décorative doit avoir `alt=""` ;
- aucun texte éditorial ne doit être intégré dans une image ;
- le logo conserve un texte alternatif utile lorsqu’il fonctionne comme lien vers l’accueil.

### Liens et clavier

- le titre du bandeau final est un lien vers l’article suivant ;
- le lien doit rester compréhensible lorsqu’il est lu hors contexte ;
- tout lien et tout contrôle doit être atteignable au clavier ;
- tout élément recevant le focus doit disposer d’un indicateur visuel clairement perceptible ;
- le contrôle clavier avec `Tab` doit être vérifié avant chaque publication.

### Ordre de lecture

Le DOM doit suivre l’ordre visuel et éditorial :

```text
menu → bandeau article → frise → introduction → contenu → encadrés → A LIRE AUSSI → pied de page
```

Cette séquence est sanctuarisée pour toutes les pages article.

### Contraste

Les couleurs choisies par le demandeur sont conservées. Elles ne doivent pas être modifiées automatiquement pour des raisons de conformité graphique.

Un éventuel écart aux recommandations WCAG doit être signalé explicitement avant publication, sans changement automatique de la palette.

### Contrôle avant publication

Vérifier systématiquement :

- un seul `<h1>` ;
- hiérarchie H1/H2 cohérente ;
- encadrés hors hiérarchie de titres ;
- `alt=""` sur les images décoratives ;
- lien « A LIRE AUSSI » correct ;
- navigation complète au clavier ;
- focus visible ;
- absence de débordement à 320 px ;
- ordre DOM logique ;
- rendu visuel desktop et mobile.
