# 01 — Landing page desktop : spécification et inventaire graphique

## Périmètre strict

Cette spécification couvre **une unique landing page en français** annonçant l’arrivée du futur site KISSARI. Elle ne définit ni les pages internes, ni une stratégie éditoriale, ni un blog, ni une newsletter, ni des parcours utilisateurs additionnels.

**Cible de travail actuelle : desktop uniquement.** La maquette source est pensée sur une largeur de référence de 1920 px. Les déclinaisons tablette et mobile seront spécifiées dans un lot ultérieur, après validation complète du desktop.

## Sources graphiques autorisées

Racine obligatoire des assets :

```text
/mnt/datas/obsidian-vault/10-Projets/20-Sociétés/10-KISS-ARI/site-web-hugo/KISSARI V1/KISSARI V1
```

Tous les chemins ci-dessous sont relatifs à cette racine. Les sources dans le vault restent immuables ; l’implémentation emploie des copies locales traçables.

## Typographie desktop

| Zone | Texte visible | Police | Taille de référence |
|---|---|---|---:|
| Header | navigation | Poppins Bold | 20 pt |
| Hero | `Bienvenue` | Poppins Bold | 20 pt |
| Hero | `Le nouveau site arrive` | Poppins ExtraBold | 95 pt |
| Hero | `En attendant` | Poppins Regular | 30 pt |
| Manifeste | `Notre manifeste` | Poppins Regular | 30 pt |
| Manifeste | `Bousculer` | Poppins ExtraBold | 95 pt |
| Manifeste | `Pour de bonnes raisons` | Poppins ExtraBold | 60 pt |
| Manifeste | texte courant | Poppins Regular | 25 pt |
| Manifeste | phrase CTA | Poppins ExtraBold | 25 pt |
| Expertises | surtitre | Poppins Regular | 30 pt |
| Expertises | `KISSARI` / `4 façons` | Poppins ExtraBold | 83 pt |
| Expertises | grand titre | Poppins ExtraBold | 95 pt |
| Expertises | sous-titre | Poppins ExtraBold | 45 pt |
| Expertises | texte courant | Poppins Regular | 25 pt |
| Expertises | chiffres | Poppins Regular | 20 pt |
| Footer | textes | Poppins Bold | 20 pt |

Fichiers de police : `../../Poppins/Poppins-Regular.ttf`, `../../Poppins/Poppins-Bold.ttf`, `../../Poppins/Poppins-ExtraBold.ttf`, `../../Poppins/Poppins-SemiBold.ttf` depuis la racine `KISSARI V1/KISSARI V1` vers le dossier parent `site-web-hugo/Poppins/`.

## Ordre d’affichage desktop

1. Header noir
2. Hero sur fond clair
3. Frise `Separation visuel.png`
4. Manifeste sur fond clair
5. Bloc expertises / quatre cartes
6. Footer — **différé**, non spécifié en détail à ce stade

## Header

- Espace : bande pleine largeur, hauteur cible 115 px.
- Fond : noir `#000001`.
- Logo obligatoire : `Livrables/Header/Logo blanc KISSARI.png` — 147×150 px — position gauche, `z-index: 10`.
- Navigation : plan texte `z-index: 10` ; aucun comportement, lien ou destination supplémentaire n’est défini par ce document.

## Hero

- Espace : fond `#F8F8F5`, hauteur cible 1 350 px ; contenu réparti en zone texte gauche et composition graphique droite.
- Zone texte : colonne gauche ; `z-index: 20`, toujours au-dessus du fond uniquement.
- La composition graphique occupe la moitié droite du bloc ; tous les éléments restent dans son conteneur.

| z-index | Asset | Dimensions source | Espace / position desktop | Règle de superposition |
|---:|---|---:|---|---|
| 0 | fond CSS | — | bloc hero complet | arrière-plan |
| 10 | `Livrables/Bloc 01/Cercle bleu.png` | 823×823 px | cercle principal, moitié droite | second plan graphique |
| 20 | `Livrables/Bloc 01/Femme.png` | 915×1742 px | personnage assis rouge, zone droite | au-dessus du cercle bleu |
| 30 | logo / textures centrales | **à identifier parmi les assets fournis avant implémentation** | centre de la composition | premier plan : recouvre partiellement le cercle bleu |
| 40 | `Livrables/Bloc 01/Pictogramme.png` | 396×315 px | bord droit du cercle | à cheval entre le cercle bleu et son extérieur |
| 50 | `Livrables/Bloc 01/Surlignage rose.png` | 843×58 px | repère rose du titre | au-dessus du texte/visuel concerné |

Règle impérative : le logo/les textures centrales sont au **premier plan** ; le cercle bleu est au **second plan**. Aucun nouvel élément graphique ne doit être inventé pour combler l’asset central tant que son fichier exact n’est pas identifié dans les sources.

## Séparateur

| z-index | Asset | Dimensions source | Espace / position desktop | Règle |
|---:|---|---:|---|---|
| 0 | `Livrables/Separation visuel.png` | 4345×339 px | pleine largeur, entre hero et manifeste | bande continue, sans espace latéral |

## Manifeste

- Espace : fond clair, hauteur cible 2 300 px ; texte à gauche, illustration à droite.
- Zone texte : `z-index: 20`.
- Illustration : conteneur droit, `z-index: 10`.

| z-index | Asset | Dimensions source | Espace / position desktop | Règle |
|---:|---|---:|---|---|
| 0 | fond CSS | — | bloc manifeste complet | arrière-plan |
| 10 | `Livrables/Bloc 02/Femme jaune + logo.png` | 1749×1970 px | moitié droite | un seul calque ; ne pas découper/recomposer les éléments inclus |
| 20 | texte manifeste | — | moitié gauche | au-dessus du fond ; hors emprise de l’image |
| 30 | `Livrables/Bloc 02/Bouton jaune.png` | 1275×1650 px | selon la position de la maquette | calque graphique distinct, au-dessus de l’illustration si chevauchement |

## Expertises

- Espace : fond clair, hauteur cible 2 300 px.
- En-tête en deux colonnes :
  - gauche : `KISSARI`, `votre partenaire`, `transformation ...` ;
  - droite : `... ou “4 façons`, `de vous faire aimer`, `toutes les matières.”`.
- Les points de suspension sont des fragments à reprendre strictement depuis le matériau fourni ; aucun complément éditorial n’est apporté ici.
- Cartes en grille 2×2 ; les cartes sont **statiques et non cliquables**. Aucun lien, bouton, flèche ou `En savoir plus`.

| Carte | z-index 0 : fond | z-index 10 : personnage | z-index 20 : pictogramme | z-index 30 : numéro/texte | Espace desktop |
|---|---|---|---|---|---|
| 01 | `Livrables/Bloc 03/Fond bleu.png` — 1707×1707 px | `Livrables/Bloc 03/Feme nuage.png` — 976×1409 px | `Livrables/Bloc 03/Icone 1.png` — 164×155 px | texte fourni | quadrant haut gauche |
| 02 | `Livrables/Bloc 03/Fond jaune.png` — 1707×1707 px | `Livrables/Bloc 03/Femme baguette.png` — 938×1016 px | `Livrables/Bloc 03/Icone 2.png` — 155×166 px | texte fourni | quadrant haut droit |
| 03 | `Livrables/Bloc 03/Fond violet.png` — 1707×1707 px | `Livrables/Bloc 03/Homme ballon.png` — 943×1212 px | `Livrables/Bloc 03/Icone 3.png` — 136×138 px | texte fourni | quadrant bas gauche |
| 04 | `Livrables/Bloc 03/Fond vert.png` — 1707×1707 px | `Livrables/Bloc 03/Femme cheveux.png` — 875×1076 px | `Livrables/Bloc 03/Icone 4.png` — 164×164 px | texte fourni | quadrant bas droit |

Règle de plan des cartes : fond → personnage → pictogramme → texte. Le personnage ne recouvre jamais le numéro ni le texte.

## Footer

Le footer est reporté après finalisation du gros du desktop. Il ne fait l’objet d’aucune spécification graphique, éditoriale ou technique dans ce lot.

## Inventaire graphique complet disponible

| Asset non encore placé ci-dessus | Dimensions source | Statut dans ce lot |
|---|---:|---|
| `Livrables/Header/Logo blanc KISSARI.png` | 147×150 px | utilisé dans header |
| tous les assets `Bloc 01`, `Bloc 02`, `Bloc 03` et le séparateur | voir tableaux | assignés à une zone desktop |
| `SPECS SITE KISSARI V1.rtf` | document | référence typographique/structurelle, non affiché |

## Critères d’acceptation du lot desktop

- La landing respecte l’ordre des six zones défini ci-dessus.
- Chaque asset placé possède un chemin source, une dimension, un espace desktop et, lorsque nécessaire, un plan `z-index`.
- La police est Poppins locale avec les poids/taille indiqués.
- Les cartes expertise ne sont pas interactives.
- Aucun comportement tablette/mobile ni contenu/structure de footer n’est implémenté ou jugé dans ce lot.
