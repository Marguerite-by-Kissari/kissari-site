# Spécification — page d’accueil KISSARI

## 1. Statut et périmètre

Cette spécification décrit l’implémentation actuelle de la page unique Hugo de
`maversionkissari`. Elle sert de contrat de rendu et de document de reprise.

- **Source HTML :** `layouts/index.html`
- **Feuille de style source :** `static/css/site.css`
- **Assets :** `static/images/` et `static/favicons/`
- **Fontes :** `static/fonts/`
- **Génération :** Hugo

La page reprend uniquement les assets fournis. Aucun décor, personnage ou logo
n’est recréé en CSS.

## 2. Règle commune de stage

La composition suit deux régimes :

1. jusqu’à `1920px` de viewport, les éléments liés au bord utilisent le bord de
   la fenêtre ;
2. au-delà, les éléments liés au stage suivent un stage de `1920px` centré.

Les blocs qui doivent suivre le bord gauche utilisent donc un retrait de `40px`
jusqu’à `1920px`, puis `calc((100vw - 1920px) / 2 + 40px)`.

## 3. En-tête

- fond noir ;
- logo KISSARI fourni ;
- favicon : monogramme blanc seul issu de
  `favicons/kissari-monogramme-blanc-source.png` (libellé KISSARI retiré),
  sur fond transparent ; le navigateur applique donc son propre fond,
  sans pastille noire ajoutée ;
  versions livrées : `favicon.ico`, PNG `32 × 32` et `512 × 512`,
  et icône Apple `180 × 180` ;
- navigation principale, lien actif souligné en rose ;
- sélecteur de langue `FR / EN` ;
- focus clavier visible sur les liens.

## 4. Hero

### Contenu

- accroche, titre et texte fournis ;
- effet sous **« bientôt. »** réalisé avec deux pseudo-éléments roses décalés,
  placés derrière la ligne de base du mot ;
- panneau central KISSARI fourni, positionné à `x = 306px` dans le canevas
  visuel de `1024px`.

### Personnage rouge

Le personnage en maillot et son panneau sont indépendants du canevas central :

- collés au bord gauche de la fenêtre jusqu’à `1920px` ;
- collés au bord gauche du stage centré au-delà ;
- panneau aligné en bas sur la frise de transition ;
- à `1024px`, le sujet visible est calibré à environ `245px` de haut.

## 5. Frises de séparation

Les deux frises utilisent le même asset :
`images/separation-visuel-tight.png`.

Cet asset est le recadrage exact de la zone non transparente de
`separation-visuel.png` : `4001 × 133px`.

Critères de rendu :

- frise sur toute la largeur disponible jusqu’à `1920px` ;
- largeur maximale de `1920px`, centrée au-delà ;
- fond noir visible seulement dans les transparences intrinsèques de la frise ;
- aucune bande noire ajoutée sous la frise ;
- même markup et mêmes règles CSS entre Hero → Manifeste et Manifeste →
  Expertises.

## 6. Manifeste

- fond rose ;
- texte aligné à `40px` du bord gauche jusqu’à `1920px`, puis au même repère
  dans le stage centré ;
- largeur de liste jusqu’à `620px`, afin de garder les propositions sur une
  ligne lorsque la largeur disponible le permet ;
- illustration jaune/KISSARI alignée sur le bord droit de la fenêtre jusqu’à
  `1920px`, puis sur le bord droit du stage ;
- les trois lignes de liste restent libres de revenir à la ligne si l’écran ne
  permet pas leur affichage complet : aucun débordement forcé.

## 7. Expertises

### Repères

- le libellé **« CE QUI NOUS ANIME »** suit le même repère gauche que le
  Manifeste (`40px`, puis stage centré) ;
- entre `800px` et `1920px`, le bloc de titres occupe `70vw`, plafonné à
  `1344px` ;
- entre `800px` et `1920px`, la grille occupe `80vw`, plafonnée à `1536px`
  (10 points de largeur supplémentaires par rapport aux titres) ;
- sous `800px`, la grille reprend toute la largeur intérieure avec `40px` de
  retrait de chaque côté ; les titres utilisent une zone légèrement plus large
  et indépendante, afin de conserver les deux compositions de trois lignes ;
- bloc de titres et grille sont centrés horizontalement ;
- à partir de `800px`, la seconde colonne de titre commence exactement sur la
  séparation verticale des cartes 01 et 02, donc sur le bord gauche de la carte
  jaune ; à `1920px` et au-delà, ce repère est au centre du viewport ;
- à partir de `800px`, la première colonne de titre mesure
  `calc(35vw - 40px)` puis `632px` à partir de `1920px`, avec un espacement de
  `40px` ; sous `800px`, les titres utilisent `47% / 53%` et un espacement de
  `26px` ;
- la taille des titres desktop suit `clamp(47px, 3.6vw, 54px)`.

### Cartes

- grille `2 × 2`, coins externes arrondis ;
- assets de fond, personnage et pictogramme issus de `static/images/` ;
- chaque carte crée son contexte d’empilement avec `z-index: 1` ;
- la carte 01 porte la classe `first-card` et `z-index: 100` ;
- calques internes : fond `0`, personnage `10`, pictogramme `20`, texte `30`.

Cette structure évite qu’un élément interne de Transformer, Créer ou Faire
rayonner passe visuellement devant Imaginer.

## 8. Pied de page

- bande noire pleine largeur, hauteur minimale `114px` sur desktop ;
- logo KISSARI blanc fourni ;
- signature : « L’agence digitale qui vous fait aimer toutes les matières. » ;
- liens : Mentions légales, CGV, Nous contacter ;
- liens en rose au survol/focus et focus clavier visible ;
- sous `800px`, contenu et liens passent à la ligne.

Les routes légales sont déclarées dans le footer, mais leur contenu éditorial
n’est pas inclus dans ce prototype mono-page.

## 9. Hero du blog — repère commun

Le hero du blog (`layouts/blog/list.html`) conserve le visage, la main et la
frise dans le même conteneur décoratif `.blog-hero__visual`, ancré sur les
quatre bords du hero.

- le personnage et la frise sont tous deux ancrés à `bottom: 0` ;
- la frise conserve son épaisseur visuelle avec `scaleY(1.5)`, mais son
  origine de transformation est désormais `center bottom` ;
- la frise ne dépend plus d'un `bottom: clamp(...)` distinct ;
- le personnage est calé à `right: 8px` jusqu'au breakpoint mobile ;
- la relation main/visage/frise reste donc stable lors d'un zoom navigateur
  ou d'un changement de largeur équivalent.

Les trois éléments sont décoratifs (`aria-hidden`) : le contenu textuel du
hero reste indépendant et accessible.

## 10. Lisibilité du CSS

`static/css/site.css` est organisé en sections numérotées et commentées :

1. fondations ;
2. en-tête ;
3. hero ;
4. séparateurs ;
5. manifeste ;
6. expertises ;
7. grand écran ;
8. pied de page.

Convention de maintenance : une propriété par ligne, indentation à deux espaces,
ligne blanche entre les règles et commentaires documentant les règles de
positionnement ou d’empilement non triviales.

## 10. Vérifications requises

```bash
cd /mnt/datas/01-dev/web/maversionkissari
npx --yes prettier@3.5.3 --check static/css/site.css
hugo --minify --cleanDestinationDir --destination /tmp/maversionkissari-build
```

Contrôles visuels minimum :

- Hero à `1024px`, `1920px` et au-delà de `1920px` ;
- Manifeste à `1400px` et `2560px` ;
- Expertises à `1400px` et `1920px` ;
- footer à `1920px`.

## 11. Validation exécutée

Les contrôles suivants ont été exécutés sur cette version :

- formatage : `prettier --check static/css/site.css` ;
- génération : build Hugo minifié réussi ;
- Expertises à `565px` : grille intérieure de `485px`, marges de `40px`,
  titres mobiles en trois lignes et absence de chevauchement ;
- Expertises à `1400px` : grille de `1120px` (`80vw`), centrée de `x = 140px`
  à `x = 1260px` ; seconde colonne de titre et bord gauche de la carte jaune
  alignés à `x = 700px` ;
- footer contrôlé à `1920px`.

## 12. Hors périmètre

- publication, DNS et déploiement ;
- rédaction des pages Mentions légales, CGV et Contact ;
- modification du projet historique `/mnt/datas/01-dev/web/kissari`.
