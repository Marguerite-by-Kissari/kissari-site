# Intégrer un article exporté par l’Atelier

## Circuit recommandé

1. Ouvrir `/atelier-article/` (ou le fichier HTML autonome à jour).
2. Renseigner le contenu et choisir une image proposée ou charger une photo.
3. Choisir le statut : **Brouillon** par défaut, ou **Prêt à publier** après validation éditoriale.
4. Cliquer sur **Exporter le ZIP**, puis décompresser l’archive.
5. Copier le dossier complet dans `/mnt/datas/01-dev/web/maversionkissari/content/blog/`.
6. Vérifier le rendu local, puis générer le site. La mise en ligne reste une action séparée.

```text
content/blog/
└── 30-10-2026-titre-de-l-article/
    ├── index.md
    └── photo.jpg
```

Ne pas déposer le ZIP lui-même, ni ajouter un niveau de dossier intermédiaire.
Ne pas placer ce dossier directement dans `public/` : ce répertoire est généré.
Aucune copie séparée de la photo dans `static/` n’est nécessaire.

## Métadonnées et comportement

- Dossier nommé avec la date **d’export**, au format jj-mm-aaaa, suivie du titre normalisé.
- `index.md` contient un `slug` sans date : l’adresse est `/blog/titre-de-l-article/`.
- Le champ `image` est le nom local de la photo dans le dossier.
- Le gabarit article et les cartes résolvent les ressources locales Hugo ; les anciens chemins `images/blog/...` restent pris en charge.
- `date` est la date de création ; `publishDate` est la date de publication.
- Brouillon : `draft: true`, absent d’un build normal.
- Prêt à publier : `draft: false`, affiché si la date de publication est atteinte.
- Une date future exige une nouvelle génération à cette date ou après ; aucun planificateur de publication n’est installé par cette modification.
- La carte, la catégorie et la navigation sont générées par Hugo, sans ajout manuel de HTML.
- Le statut est conservé dans la sauvegarde navigateur ; une ancienne sauvegarde sans statut est rouverte en brouillon.

## Images et cartes du blog

Le même fichier image alimente le bandeau de l’article et les cartes. Les cartes utilisent un recadrage panoramique automatique ancré en haut (`object-fit: cover; object-position: center top`). Garder les visages et éléments importants vers le haut du visuel ; le bas peut être masqué selon la taille de fenêtre. Le fichier source reste inchangé.

Le grand aperçu de l’Atelier représente le **bandeau de l’article**, pas la carte de la liste. Vérifier cette dernière dans `/blog/` après intégration, sur ordinateur et mobile. Ne pas appliquer les dimensions des cartes au bandeau de l’article.

Le contrat responsive est décrit dans `08-blog-rails.md` : trois cartes complètes sur ordinateur, deux sur tablette, une carte principale sur mobile ; textes non tronqués et hauteur naturelle par rangée.

## Mettre des mots en gras

Sélectionner le texte dans l’introduction, un paragraphe, une liste, le texte d’un encadré ou une note, puis cliquer sur **G — Gras** à côté du champ. Le bouton ajoute `**texte**` ; le passage est immédiatement rendu en gras dans l’aperçu. Pour retirer le gras, sélectionner le même passage (avec ou sans ses doubles astérisques) et cliquer à nouveau. Sans sélection, un message demande de sélectionner des mots.

Les marqueurs Markdown restent visibles dans le champ de saisie. Ils sont conservés dans la sauvegarde navigateur et dans le ZIP ; Hugo génère un élément `<strong>` dans le corps de l’article. Les passages multilignes sont formatés ligne par ligne. Le HTML saisi reste échappé dans l’aperçu.

Cette commande concerne le contenu rédactionnel, pas les métadonnées (titre principal, chapeau, auteur) ni les titres d’encadrés, déjà stylés par le gabarit. Elle ne transforme pas l’Atelier en éditeur riche complet.

## Ajouter une note sur une sélection

Sélectionner un mot ou un passage dans l’introduction ou un champ de texte du corps, puis cliquer sur **\* — Note**, à côté de **G — Gras**. La fenêtre modale rappelle le passage et permet de saisir le texte de la note. **Enregistrer la note** ajoute un renvoi après le passage ; **Annuler** ou **Échap** ne change rien. Une sélection est obligatoire pour une nouvelle note.

Le champ affiche un identifiant Markdown `[^note-…]`, mais l’aperçu et le site affichent un astérisque cliquable, avec le texte de note en bas d’article et un lien de retour. Pour modifier une note, sélectionner son marqueur puis cliquer sur Note. Supprimer le marqueur du champ pour retirer le renvoi ; les définitions sans renvoi ne sont pas exportées.

Les notes sont conservées dans la sauvegarde navigateur et dans le ZIP. Les notes multilignes sont exportées avec l’indentation Markdown requise. Le bouton Note n’ajoute plus de bloc dans le flux ; les anciens blocs Note restent lisibles, éditables et exportables. Les titres/métadonnées ne reçoivent pas de nouvelle commande Note.

Les notes dans les cadres roses, jaunes et noirs sont résolues par `layouts/partials/callout-body.html`, avec identifiants isolés et report du texte en bas de l’article par `layouts/blog/single.html`. Le HTML brut reste désactivé : aucun assouplissement de sécurité du moteur Markdown.

Tests : `node scripts/test-atelier-inline-notes.cjs` et `python scripts/check-inline-notes-hugo.py`, plus test navigateur de sélection, modale, sauvegarde/réouverture et export ZIP réel.

## Titres de section

Dans chaque bloc « Titre », saisir le libellé dans le champ **Titre**, pas dans le texte complémentaire. L’export bloque les titres vides ou multilignes. Le Markdown attendu est `## Action n°1 : …` sur une seule ligne. Une ligne `##` vide suivie d’un paragraphe n’est pas un titre correct ; les anciennes archives doivent être contrôlées avant validation.

## Mise à jour d’un article

Même titre, même jour : le dossier exporté a le même nom. Ne pas fusionner ou écraser sans vérifier que c’est bien une mise à jour.
Un export un autre jour porte une autre date de dossier, mais garde le même slug si le titre ne change pas : **remplacer le dossier de l’article existant après sauvegarde, ne pas conserver les deux**.
Conserver le slug d’un article déjà publié même si son titre change, pour préserver son adresse.
Les anciennes archives ne sont pas converties automatiquement : réexporter avec le nouvel Atelier, ou adapter manuellement le fichier et le chemin image.

## Vérification locale

```bash
cd /mnt/datas/01-dev/web/maversionkissari
hugo server --bind 127.0.0.1 --port 1314 --disableFastRender
```

Ouvrir `http://127.0.0.1:1314/blog/` pour le site et `/atelier-article/` pour l’éditeur.
Pour examiner explicitement les brouillons : ajouter `--buildDrafts` (ne pas utiliser ce mode pour publier).

## Maintenance de l’Atelier autonome

Après modification de `static/atelier-article/app.js` ou `app.css`, régénérer le HTML autonome :

```bash
python scripts/build-atelier-standalone.py
```

Ne pas modifier uniquement les copies générées dans `public/`.
