# Prépublication KISSARI

## Publication autorisée et déploiement limité à main

Le domaine de production est `https://kissari.com/`. Les DNS restent une opération séparée et coordonnée.

- `.github/workflows/kissari-pages.yml` est l'unique workflow actif : il contrôle et construit toutes les branches prévues, puis déploie uniquement `main` si tous les contrôles réussissent.
- Les branches `atelier/**`, `recette/**` et les PR ne déploient pas. Le résultat de recette est archivé 7 jours.
- Les permissions globales restent en lecture ; seul le job `deploy` reçoit `pages: write` et `id-token: write`.
- La reconstruction des articles arrivés à échéance est programmée toutes les quinze minutes ; GitHub peut retarder les runs.
- L’ancien modèle inactif `deployment/kissari-pages.yml` a été transféré dans le dépôt privé `Marguerite-by-Kissari/atelier-ecriture`. Ne pas l’activer en parallèle du workflow public.
- L'environnement `github-pages` doit autoriser uniquement la branche `main`, sans approbation obligatoire par publication.

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
5. Valider un premier déploiement et son SHA ; vérifier le routage du domaine par une résolution locale de diagnostic, puis donner le feu vert à la bascule DNS.
6. Après propagation DNS, vérifier le certificat de `kissari.com` et `www.kissari.com` et imposer HTTPS. Ne pas annoncer HTTPS opérationnel avant cette vérification.
7. Tester les redirections, les branches `atelier/**`, les échecs de build et la reconstruction programmée. Le cron GitHub n'offre pas une ponctualité garantie à la minute.
