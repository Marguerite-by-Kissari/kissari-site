# KISSARI — site public Hugo

Ce dépôt contient le site public : contenus, médias, gabarits Hugo, styles et scripts du site, ainsi que son workflow GitHub Pages.

**L’atelier d’écriture est désormais développé dans le dépôt privé [`Marguerite-by-Kissari/atelier-ecriture`](https://github.com/Marguerite-by-Kissari/atelier-ecriture).** Son interface, ses services locaux, ses générateurs, son installateur et sa documentation spécifique ont été transférés puis retirés de la branche courante de ce dépôt. Aucune réécriture de l’historique Git n’a été effectuée : les anciennes versions restent consultables.

## Contenus et rendu

- Accueil : `layouts/index.html`, styles `static/css/site.css`.
- Blog : `content/blog/`, gabarits `layouts/blog/`, médias d’articles et visuels sous `static/images/blog/`.
- Contact : page de contacts directs email/LinkedIn, sans formulaire d’envoi.
- Mentions légales et RGPD : PDF sous `static/documents/`, empreintes dans `data/legal_documents.json`.
- Contrats graphiques : `specs/001-homepage.md`, repères 1920 px, frises, Manifeste, Expertises et pied de page. Préserver les composants et textes validés.

## Lancer localement

Prérequis : Hugo Extended 0.154.5. Pour les tests, Python 3.11+ et Node.js ; Pillow pour certains contrôles de rendu.

Depuis ce clone :

```bash
hugo server --bind 127.0.0.1 --port 1314 --disableFastRender
```

Ouvrir <http://127.0.0.1:1314/> ou <http://127.0.0.1:1314/blog/>. L’interface `/atelier-article/` ne fait plus partie de ce dépôt.

## Articles et rubrique éditoriale

L’atelier privé continue de produire les articles pour **ce dépôt public**, pas pour son propre dépôt applicatif. Les articles validés vont dans `content/blog/` ; les réglages de rubrique restent dans `data/blog_editorial.json`. Le choix « Prêt à publier », le statut de brouillon et la date/heure de publication déterminent la visibilité au build.

Le catalogue JSON (`layouts/blog/list.editorialcatalog.json`) et ses contrats de validation (`scripts/editorial_config.py`, `test-editorial-config.py`, `test-editorial-build.py`) restent ici : ils servent les données du site et son intégration éditoriale, sans embarquer l’interface d’administration. Le guide de format `specs/09-template-redaction-article-blog.md` est partagé avec l’atelier.

Pour lancer l’atelier en développement, cloner les deux dépôts côte à côte et suivre le README du dépôt privé. Son lanceur assemble un espace de recette jetable sans modifier les sources de ce site.

## Contrôles et production

```bash
python3 scripts/test-production-config.py
python3 scripts/test-editorial-config.py
python3 scripts/test-editorial-build.py
python3 scripts/build-production.py --destination "$HOME/.hermes/cache/scratch/kissari-public-build"
```

La destination doit être un dossier de sortie dédié, jamais un dossier de sources. La construction vérifie la navigation, l’absence de l’atelier dans l’artefact public, les liens internes, les URL canoniques, le sitemap et robots.txt.

Le workflow actif `.github/workflows/kissari-pages.yml` contrôle puis déploie `main`. Les branches `atelier/**`, `recette/**` et les PR ne déclenchent pas de déploiement public. La reconstruction programmée toutes les quinze minutes rend les articles éligibles à leur échéance ; GitHub peut retarder les runs. Un commit envoyé n’est pas une preuve de mise en ligne.

Voir `deployment/PREPUBLICATION.md` pour les contrôles de publication. Le domaine de production reste `https://kissari.com/` ; aucune configuration DNS n’est modifiée par la séparation.

## Traçabilité et retour arrière

L’extraction part du commit `9450a145066c4477ed1a3fd89fe7b1cd4404302f`. Le code a été publié et relu dans le dépôt privé au commit `7b9d2ccecae868042ba9129d595d8fa155d77278` **avant** le retrait ici. Le manifeste d’empreintes est conservé dans `atelier-ecriture/docs/migration-manifest.json`.

Le retrait est un commit ordinaire et peut être annulé par revert après examen des changements ultérieurs. Aucun secret, clé privée ou package personnel ne doit être ajouté à l’un ou l’autre dépôt.
