# Prépublication KISSARI

## État volontairement non publié

Le domaine de production prévu est `https://kissari.com/`. La présence de cette URL dans les sources ne publie rien et ne modifie pas le DNS.

- `.github/workflows/kissari-pages.yml` réalise uniquement les contrôles, la construction et l'archivage privé du résultat (7 jours).
- Il n'a ni job de déploiement, ni permission `pages: write` / `id-token: write`, ni reconstruction programmée.
- `deployment/kissari-pages.yml` demeure un modèle de publication inactif. Ne pas l'activer en parallèle : au lancement, faire évoluer le workflow unique après accord d'Éric.
- GitHub Pages, la visibilité publique du dépôt et les DNS nécessitent un feu vert distinct.

## Vérifier le candidat

```bash
python3 scripts/test-production-config.py
python3 scripts/test-editorial-config.py
python3 scripts/build-production.py --destination "$HOME/kissari-recette-public"
```

La construction utilise Hugo Extended 0.154.5, exclut les brouillons et les articles futurs par défaut, vérifie la navigation, retire `atelier-article/`, ajoute le SHA de source dans `deployment.json`, puis contrôle les liens et ressources internes, les URL canoniques, le sitemap et robots.txt.

Le sitemap expose uniquement les pages rendues, pas l'atelier. Le fichier robots.txt autorise l'indexation de production et annonce le sitemap. Une prévisualisation privée doit être protégée par le réseau ou une authentification et envoyer `X-Robots-Tag: noindex` ; robots.txt n'est pas un contrôle d'accès.

## Contrôles avant passage en public

- Examiner toutes les branches et tout l'historique pour les secrets et éléments confidentiels. Une analyse automatisée réduit le risque, elle ne garantit pas l'absence de secret.
- Les sources des outils éditoriaux, spécifications et articles futurs deviennent lisibles dans un dépôt public même quand elles sont absentes du site construit.
- Vérifier les accès des éditrices avec leurs identités propres, et non le compte administrateur.
- Ne pas confondre un push, un build réussi et une publication.

## Passage en production, après validation

1. Confirmer le candidat et le contrôle de confidentialité.
2. Rendre le dépôt public seulement sur accord.
3. Configurer Pages et l'environnement `github-pages` limité à `main`.
4. Faire évoluer le workflow unique en réutilisant les mêmes contrôles et la même construction. La configuration de production doit conserver `https://kissari.com/`, pas une URL locale ou un domaine invalide.
5. Valider un premier déploiement, son SHA et son certificat ; effectuer ensuite la bascule DNS coordonnée.
6. Tester les redirections, les branches `atelier/**`, les échecs de build et la reconstruction programmée. Le cron GitHub n'offre pas une ponctualité garantie à la minute.
