# Spécification 16 — Publication autonome, dépôt unique

## Statut et décision

Architecture validée par Eric le 15 novembre 2026 ; **implémentation à réaliser**. Ce lot ne change que la documentation et les schémas, pas le code applicatif, les accès ou le déploiement.

Cette spécification supplante les options de gouvernance et d’architecture des spécifications 13/14 : pas de second dépôt éditorial, de collecte inter-dépôts, de clé technique supplémentaire, de GitHub App obligatoire ni de PR approuvée par les webmasters pour les deux propriétaires.

## 1. Cible

- Dépôt existant : `Marguerite-by-Kissari/kissari-site` ; branche de publication proposée `main`.
- Virginie et Christelle : deux comptes nominatifs, deux clés SSH personnelles, Write sur ce même dépôt. Administrateurs : accès conservés, clé non partagée.
- L’écriture des propriétaires n’est pas limitée par GitHub aux seuls articles : confiance assumée, filtrage éditorial dans le connecteur seulement.
- Un seul fichier `.github/workflows/kissari-pages.yml` à préparer : contrôles, build Hugo et déploiement Pages ; plusieurs jobs et types d’événements possibles dans ce fichier.
- Push `main` déclenche la chaîne directement. Aucun import/commit robot et aucune clé humaine requise dans Actions pour un déploiement standard.
- Le workflow bloque le déploiement en cas d’échec, pas l’arrivée du commit sur `main`. Corriger/revert si nécessaire ; le site précédent doit rester disponible.

## 2. Poste et atelier

- Atelier M15 conservé ; pas de refonte des gabarits, blocs, catégories ou notes validés.
- Connecteur local lancé à la demande, loopback et même origine ; Git/agent SSH système. Jamais de secret dans le navigateur/export ou de terminal web libre.
- Partial clone + sparse checkout : fichiers de l’article/rubrique sélectionnés, métadonnées Git et objets différés. Pas de promesse « aucun clone » ni de cache complet téléchargé sans accord.
- Maintenir l’index des fichiers non matérialisés ; staging explicitement limité pour ne jamais effacer le reste du site.
- Opérations : état, actualisation, réouverture, aperçu local, diff, publication/programmation, gestion de conflit, restauration par nouveau commit.
- Reprise d’articles existants sans perte : décider la persistance de l’état structuré source ou un import Markdown réellement supporté. Préserver slug/URL/dossier, médias et métadonnées M22–M25 ; refuser une conversion silencieusement destructrice.
- Le service actuel `scripts/serve-editorial-preview.py` ne fait pas de Git et refuse actuellement un article déjà existant : extension à concevoir/tester, pas une capacité disponible.
- Réglages de rubrique : intégrer le patch de `data/blog_editorial.json` avec diff, contrôle de base et confirmation séparée.

## 3. Tests et publication

- Enregistrement local/export : sans publication.
- Aperçu local : rendu d’atelier, pas équivalent à un build Hugo complet.
- Test Hugo distant optionnel : branche `atelier/<identité>/<article>` dans le même dépôt ; même workflow, aucun déploiement depuis cette branche, pas de PR requise.
- Publier : validation locale, confirmation du contenu exact, commit ciblé puis push fast-forward sur `main` ; checks/build de la révision courante puis Pages si succès.
- Refuser le push si la base a changé et ne peut être réappliquée sans ambiguïté ; conserver le brouillon ; pas de force-push.
- SSH ne lit pas l’API des checks privés : V1 avec liens GitHub authentifiés et messages honnêtes. Un suivi automatique complet nécessite une authentification API distincte à approuver, pas un secret embarqué.
- « Publié » uniquement après déploiement et lecture du site avec marqueur de SHA/revision, pas après le seul push ou un HTTP 200 générique.
- Permissions minimales par job, pas de credentials persistés dans le build ; Pages/OIDC pour le seul job de déploiement et seulement sur la branche/événement autorisés.
- Épingler Hugo/actions examinées ; empêcher un déploiement ancien d’écraser le dernier état autorisé. Production sans brouillons, futurs, état source de l’atelier, rapports privés ou catalogue privé.

## 4. Programmation et confidentialité

- Après recette du circuit immédiat : ajouter `schedule` et relance manuelle au même fichier workflow. Pas de deuxième workflow/serveur/cron local.
- `draft` indépendant de la date ; `Europe/Paris` résolu vers un instant explicite ; pas de `--buildDrafts`/`--buildFuture` en production.
- Programmer n’est effectif qu’après push sur la branche publiée et vérification du schedule actif. Heure d’éligibilité, pas SLA à la seconde.
- Dépôt public : textes futurs et branches de test lisibles. Sources privées/aperçus privés nécessitent configuration et offre adaptées, à vérifier ; une URL cachée Pages n’est pas une authentification.

## 5. Lots et responsabilités

1. **A — Inventaire : Jarvis**, informations Eric : visibilité/offre/Pages/règles, comptes/postes/OS, droits hérités et domaine. Aucun test de push exploratoire en production.
2. **B — Identités : Eric/Jarvis selon accès**, avec actes personnels des propriétaires : comptes, invitations et 2FA GitHub. Correction explicite d’Eric : Jarvis prépare les deux clés, Eric les transfère ; **Virginie/Windows et Christelle/macOS utilisent des clés sans phrase secrète**, directement, sans déverrouillage d’agent. Les ZIP personnels contiennent donc une clé privée directement utilisable : transfert privé seulement, aucun dépôt GitHub ni pièce jointe Discord. La fiche Marguerite contient les deux clés publiques complètes, jamais les privées.
3. **C — Connecteur : Jarvis** : Git léger, opérations structurées, contrôle local de sécurité, conflits et conservation du reste de l’index ; tests Git locaux, puis tests GitHub autorisés séparément.
4. **D — Atelier : Jarvis** : nouveaux contrôles, reprise d’articles, rubrique, états, test distant optionnel, mode offline, package/lanceur par OS ; validation UX avec les propriétaires.
5. **E — Workflow : Jarvis prépare**, activation distante après accord et droits disponibles ; configuration Pages et domaine par l’administrateur habilité.
6. **F — Recette : Jarvis + Eric + les deux propriétaires** : deux vraies publications, refus d’accès non autorisé, conflit, échec CI, révision publique et restauration.
7. **G — Programmation : Jarvis**, après recette immédiate et activation autorisée, même fichier workflow.
8. **H — Documentation : Jarvis** : installation par OS, premier accès GitHub, guide illustré des propriétaires, fiche réflexe une page, erreurs/conflits, guide administrateur, contrat API/format, versions et preuves.

Plan détaillé et cases d’exécution : `/mnt/datas/obsidian-vault/10-Projets/20-Sociétés/10-KISS-ARI/site-web-hugo/V1/Atelier - Plan de mise en oeuvre et responsabilités.md`.

Les guides applicatifs définitifs seront produits avec les écrans recettés, pas des boutons fictifs. Prévoir `docs/atelier/` pour les sources, `livrables/` ignoré pour le package et les preuves. Ne pas modifier notre clé, créer une invitation ou activer Pages au seul motif que l’architecture est validée.

## 6. Acceptation minimum

- Deux identités GitHub nominatives publient indépendamment sans approbateur webmaster.
- Compte non autorisé refusé ; accès administrateurs conservés ; aucun secret client ajouté à Actions.
- Poste léger mesuré, reste du site intact après commit d’un article ; conflits sans perte/force-push.
- Réouverture et modification d’un article existant sans perte de structure, URL ou métadonnées ; rubrique testée séparément.
- Test `atelier/**` sans mise en ligne ; échec CI sans déploiement ; source en échec clairement distinguée du site public précédent.
- Révision réellement servie vérifiée ; restauration persistante au prochain build.
- Programmation si livrée : absence avant échéance, présence après build/déploiement et brouillons exclus.
- Guide utilisateur et package correspondant aux OS réellement testés.

## État constaté avant ces modifications documentaires

Source locale au commit `ae2bc418231191014b06396395a69ee62c48cbe4`, Git propre ; remote SSH configuré vers le dépôt ci-dessus, M15 intégré. Aucun `.github/workflows` dans cette racine ou dans ce commit. Ce constat local ne certifie pas la visibilité, les droits, l’offre ou Pages à distance. Aucun nouveau code applicatif/workflow exécutable ni écriture distante dans le présent lot.
