# KISSARI — sources Hugo et atelier éditorial

Sources locales de référence destinées au dépôt `Marguerite-by-Kissari/kissari-site`.
M15 est intégré à la demande d’Eric : rédaction d’article, réglage de rubrique,
export et test Hugo local. Le push des sources et le déploiement Pages sont deux étapes distinctes.
Ce premier remplacement n’installe aucun workflow de déploiement ni de publication depuis l’atelier.

## Sources
- Spécifications graphiques et textes fournis : `specs/001-homepage.md`
- Assets : copies locales des livrables KISSARI V1 et des fontes Poppins

## Documentation et contrat de rendu

- Spécification complète et critères de validation : `specs/001-homepage.md`
- HTML de la page : `layouts/index.html`
- CSS source commenté : `static/css/site.css`
- Blog et cartes compactes : `specs/08-blog-rails.md`
- Modèle de rédaction : `specs/09-template-redaction-article-blog.md`
- Export ZIP et intégration : `specs/10-import-atelier-article.md`

La spécification est le document de référence pour les repères 1920px, les
frises, le Manifeste, les Expertises et le pied de page. Elle inclut les règles
mobile/desktop du cadre Expertises : `80vw` sur desktop, grille centrée et
alignement du titre droit sur la carte jaune.

## Lancer localement

```bash
cd /mnt/datas/01-dev/web/maversionkissari
hugo server --bind 127.0.0.1 --port 1314 --disableFastRender
```

Puis ouvrir : <http://127.0.0.1:1314/>.

La page d’index des articles est disponible à <http://127.0.0.1:1314/blog/>. Les
articles sont issus des fichiers réels de `content/blog/`.

## Ajouter un article depuis l’Atelier

Voir [le mode d’emploi](specs/10-import-atelier-article.md) : exporter le ZIP,
décompresser le dossier dans `content/blog/`, puis régénérer le site.
Le choix « Prêt à publier » est nécessaire pour apparaître dans un build normal.

## Présentation du blog

- Trois cartes complètes au-dessus de 1100 px, deux de 701 à 1100 px, une carte principale sur mobile.
- Photos panoramiques cadrées en haut (`object-fit: cover; object-position: center top`). Préserver les visages dans la partie supérieure des images.
- Titres et chapeaux complets, hauteur naturelle homogène par rangée ; flèches et navigation clavier conservées.
- Les réglages des cartes ne modifient ni les photos sources ni la mise en page des articles.

## Atelier à utiliser

- Dans le site : <http://127.0.0.1:1314/atelier-article/>.
- Version autonome : `livrables/atelier-editorial-kissari-autonome.html`.
- Un bloc de section doit avoir un champ **Titre** renseigné sur une seule ligne ; l’export refuse les titres vides ou multilignes.
- Après modification des sources de l’Atelier, exécuter `python scripts/build-atelier-standalone.py` : ce point d’entrée reconstruit désormais M15, son catalogue et le livrable autonome complet, sans perdre l’onglet Rubrique ni l’heure de publication.
- Le grand aperçu de l’Atelier représente l’article, pas sa carte compacte dans la liste du blog.

## Vérifier un build de production local

```bash
hugo --minify --destination "$HOME/.hermes/cache/scratch/maversionkissari-build"
```

## Atelier M15 intégré

Pour les tests connectés (sans écriture dans les contenus de référence ni publication) :

```bash
python scripts/serve-editorial-preview.py --port 1345
```

Ouvrir `http://127.0.0.1:1345/atelier-article/`. Un serveur Hugo ou HTTP statique seul
ne fournit pas l’API de test. La version autonome garde l’édition et l’export hors ligne.
Les aperçus et rapports restent locaux dans le cache et `livrables/`, non versionnés.
Une date future ne déclenche pas encore de reconstruction automatique sur GitHub.

Les anciennes sources distantes sont remplacées par un commit ordinaire conservant
l’historique ; aucun force-push n’est requis. Le domaine, la configuration Pages et
les workflows de publication restent à traiter dans le lot suivant.
