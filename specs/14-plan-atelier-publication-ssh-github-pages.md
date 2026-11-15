# Plan d’actions — Atelier Kissari, Git SSH et GitHub Pages

## Statut et décisions

Plan préparé le 15 novembre 2026. Aucun développement applicatif, initialisation Git, accès SSH distant, push, création de dépôt, changement de clé, workflow distant ou déploiement n’est effectué par ce document.

Instructions du propriétaire du projet :
- Hébergement cible : GitHub Pages, site Hugo statique.
- Publication Git par clé SSH autorisée ; reprendre le principe Git local → push → GitHub Actions → Pages utilisé pour les sites de Stéphane Bouquet et Gabriel.
- Aucune clé privée dans une page web, un export ou le stockage du navigateur.
- Formulaire de contact/prestataire tiers : décision suspendue à la validation du propriétaire du site. Hors de ce lot.
- Préparer les actions avant de développer. Les gabarits et sections validés ne sont pas à retoucher.

Ce plan amende la proposition d’architecture de `13-atelier-github-publication-planifiee.md` : GitHub Pages est désormais choisi ; une GitHub App n’est pas un prérequis pour le transport Git par SSH. Les invariants de relecture, d’intégrité des révisions, de confidentialité et de publication future de cette spécification demeurent applicables.

## 1. Etat constaté en lecture seule

- Racine à conserver : `/mnt/datas/01-dev/web/maversionkissari` ; `hugo.toml` présent, aucun `.git` ni `.github` à cette racine au contrôle. Aucun remote Kissari ne peut donc être déduit de ce répertoire.
- Atelier de référence : `static/atelier-article/`, constructeur du portable `scripts/build-atelier-standalone.py`, contrat d’import `specs/10-import-atelier-article.md`.
- Prototype M15 isolé : `livrables/prototype-M15/site/` ; éditeur, réglages de rubrique, tests Hugo connectés et publication future préparatoire. Lire `livrables/prototype-M15/LIRE-MOI.md` avant toute reprise. M15 n’est pas validé/intégré par le présent plan.
- Le service M15 `scripts/serve-editorial-preview.py` écoute localement selon sa documentation et ne comporte pas de publication Git. Son extension éventuelle doit rester séparée du fonctionnement de test sans écriture dans la référence.
- Deux clés publiques candidates Kissari existent : `id_ed25519_jarvis_kissari_agent.pub` et `kissariagent.pub`. Seules leurs empreintes ont été consultées ; existence locale ≠ autorisation distante ni permission sur le bon dépôt. Aucune clé privée lue, testée, générée ou copiée.
- Référence Stéphane, inspection locale : dépôt `stephane-web/sb-portfolio`, remote via alias SSH dédié ; workflows de contrôle Hugo en PR et build/artefact/déploiement Pages présents.
- Référence Gabriel, inspection locale : `gab-web`, remote SSH vers `IamGonna/webSite`. La copie locale du workflow `deploy-gab.yml` contient encore le déploiement VPS historique, alors que l’historique de conversation rapporte une migration Pages réussie. Ne pas la recopier comme configuration Pages actuelle ; référence distante à relire si nécessaire avant réemploi.

Les constats locaux ne certifient pas l’état actuel des dépôts distants.

## 2. Architecture proposée

```text
Poste d’un rédacteur/publieur habilité
  Atelier dans un navigateur
       ↓ requêtes locales contrôlées
  Pont local, démarré à la demande
       ├─ copie de travail Git du seul dépôt Kissari
       ├─ prévisualisations Hugo temporaires
       └─ Git / agent SSH du poste
                    ↓ push SSH
                 GitHub
                    ↓ Actions : contrôles puis build Hugo
                 Artefact public
                    ↓ déploiement officiel Pages
              Site public statique
```

- Aucun serveur éditorial public, PHP, base de données ou port de publication exposé sur Internet.
- Un HTML servi par Pages ne peut pas utiliser directement la clé SSH du poste. Le navigateur ne devient pas client Git SSH par ajout d’un bouton.
- Atelier connecté : servir l’interface et les actions locales sur la même origine, en boucle locale seulement. Un site distant ne doit pas pouvoir appeler le pont par CORS permissif.
- Atelier autonome : conserver édition, sauvegarde et export hors ligne ; aucune fausse promesse de push sous `file://`.
- Le pont est du logiciel local à maintenir et tester, mais pas un service permanent exposé : lancement à la demande, arrêt explicite, pas de daemon/port réseau ajouté par défaut. Le poste doit être équipé de Git, SSH et Hugo.
- Les contenus privés et brouillons restent hors des artefacts Pages, y compris les catalogues, rapports et aperçus.

## 3. Lot A — cadrer dépôt, rôles et accès

Actions :
- Identifier le propriétaire GitHub, l’URL exacte du dépôt, sa visibilité, la branche par défaut et la branche de publication.
- Identifier les postes/OS qui exécuteront l’atelier connecté, les comptes rédacteurs et publieurs, et le modèle de relecture (PR ou intégration directe autorisée).
- Confirmer la clé déjà autorisée et son périmètre. Préférer une clé dédiée au dépôt/poste ; ne pas réutiliser une clé de Stéphane ou Gabriel.
- Définir le domaine public et `baseURL`. Pour un dépôt source privé, vérifier l’offre GitHub permettant Pages avant d’affirmer que cette combinaison est disponible.
- Contrôles distants ultérieurs, en lecture seule et sur la seule cible autorisée : identité SSH avec l’alias fixé, puis `git ls-remote` du dépôt. Ne pas accepter aveuglément une nouvelle empreinte hôte ; vérifier l’empreinte GitHub officielle si nécessaire.

Important : l’authentification SSH réussie ne prouve pas à elle seule le droit d’écriture au dépôt. Un test de push ne doit pas servir de simple découverte non autorisée.

Critère : fiche dépôt/branche/URL/identité/clé et droits renseignée, accès en lecture confirmé ; droits d’écriture et politique de branche documentés, aucun contenu publié.

## 4. Lot B — établir une source Git propre, sans perte

Actions :
- Faire un inventaire et une sauvegarde non destructive de la racine actuelle et du prototype M15.
- Déterminer si l’on rattache la racine à un dépôt existant ou si un dépôt doit être créé. Comparer les sources dans une copie séparée avant import ; pas de remplacement forcé d’un dépôt distant existant.
- Préparer un `.gitignore` qui exclut caches, fichiers locaux, logs, secrets, clés, brouillons privés non destinés au dépôt et builds `public/`/`resources/` selon le contrat de génération. Ne pas supprimer ces répertoires du disque par principe.
- Définir explicitement quels contenus, assets et réglages éditoriaux sont versionnés. Exclure les prototypes, QA et livrables non nécessaires du site public.
- Choisir la reprise M15 après recette explicite ; ne pas promouvoir toute la copie isolée au rang de source sans comparaison.
- Ajouter un alias SSH propre au dépôt avec identité imposée, seulement si nécessaire et après identification de la bonne clé.

Critère : diff d’import lisible, sources et prototype préservés, aucun secret dans les fichiers/index/historique à pousser, build local reproductible. Aucun push à cette étape.

## 5. Lot C — chaîne de contrôles et déploiement Pages

Préparer les workflows dans une copie de travail/branche dédiée :
- Contrôle sur branche éditoriale ou PR : validation métadonnées et chemins, JS, tests de l’atelier, build Hugo et contrôles des pages générées.
- Version Hugo explicitement fixée à la version réellement validée ; ne pas reprendre aveuglément `latest` des anciens workflows. Actions tierces examinées et épinglées à une révision approuvée.
- Build public normal, jamais `--buildDrafts` ni `--buildFuture`. Empêcher brouillons, catalogue privé et rapports de test de rejoindre l’artefact.
- Déploiement avec les actions officielles Pages ; permissions minimales par job : lecture des sources pour le build ; `pages: write` et `id-token: write` seulement pour le job de déploiement nécessaire.
- Aucun secret SSH de poste nécessaire dans Actions pour déployer l’artefact Pages.
- Régler Pages sur « GitHub Actions », puis domaine/HTTPS après accord. L’activation et le premier push sont des actions distantes distinctes à autoriser.
- Gérer concurrence et révisions : ne pas laisser un ancien build remplacer une publication plus récente ; associer l’artefact au SHA source vérifié.

Critère : préparation locale vérifiée, puis après autorisation seulement, vrai contrôle CI, vrai déploiement Pages et lecture HTTP du site de la bonne révision. Les résultats distants ne doivent jamais être simulés dans l’atelier.

## 6. Lot D — pont local Git SSH, périmètre réduit

Etendre/réutiliser les primitives sûres du prototype, pas un terminal web générique :
- Serveur lié uniquement à `127.0.0.1` ; contrôle Host, Origin et jeton de session local anti-CSRF, refus des origines étrangères et du rebinding ; requêtes de mutation en POST. Aucun secret permanent dans le HTML ou `localStorage`.
- Dépôt, remote et branche autorisés fixés par configuration locale de confiance ; ne pas accepter leurs valeurs arbitraires du navigateur.
- Liste blanche de chemins éditoriaux ; validation des noms, slugs, types/taille des images, archives, liens symboliques et traversées de répertoires. Pas de modification de `.github/`, scripts, hooks ou config de sécurité via une soumission d’article.
- Git appelé par arguments structurés, jamais par commande shell issue d’un champ. Pas de force-push, reset destructif, suppression de branche distante ni modification globale de Git/SSH.
- Verrou par copie de travail et contrôle SHA de base pour éviter deux publications concurrentes ; pas de merge/pull automatique qui écrase des modifications locales.
- Préparer les candidats/tests dans des copies temporaires maîtrisées ; conserver les brouillons et les changements non liés.
- Clé/agent SSH exclusivement côté poste ; demande de déverrouillage locale si nécessaire. Ne jamais demander sa passphrase dans le formulaire web.
- Aucun hook d’un dépôt non approuvé ni exécution de contenu soumis comme script. Les changements de templates/scripts/workflows restent un circuit de maintenance distinct.

Limite de sécurité : la liste blanche du pont limite ses fonctions, pas le pouvoir cryptographique de la clé. Une clé SSH ayant écriture au dépôt peut avoir un périmètre plus large que les chemins éditoriaux. Documenter les protections de branche, les droits effectifs et le risque en cas de compromission du poste ; ne pas présenter une deploy key comme limitée nativement à `content/blog/`.

Critère : tests de refus, origine étrangère, commandes/chemins interdits, conflit, dépôt inattendu, clé absente et doublon ; aucune écoute publique ni perte de fichier.

## 7. Lot E — commandes éditoriales dans l’atelier

Parcours visible proposé :
1. « Actualiser depuis GitHub » : état/base distante sans écrasement du brouillon.
2. Rédiger/rouvrir un article ou régler la rubrique ; conserver l’URL et les métadonnées existantes.
3. « Tester sur le site » : vrai aperçu Hugo isolé lié au contenu courant.
4. « Voir les modifications » : résumé/diff, fichiers, branche et révision ; avertissement sur les images remplacées.
5. « Enregistrer une version » : commit candidat limité aux fichiers explicitement sélectionnés, sans inclure les changements d’une autre opération.
6. « Envoyer pour validation » ou « Publier » selon les droits et le circuit choisi ; confirmation de la cible et de la révision.
7. Etats distincts : local, enregistré, envoyé à GitHub, en validation, intégré, build, déploiement, vérification publique, échec.
8. Historique et « Rétablir une version » via un nouveau commit, sans réécriture partagée.

Circuit avec PR recommandé lorsque la relecture est exigée. Le circuit direct doit tester le candidat AVANT de faire avancer la branche de publication, refuser une base distante modifiée et retester. Il doit être désactivé si les protections imposent une PR sans exception explicitement autorisée.

Frontière SSH/API : SSH permet fetch/push, pas les appels API de création/fusion de PR, interrogation privée des checks ou déclenchement `workflow_dispatch`. Pour le premier lot, proposer des liens GitHub explicites pour les opérations non disponibles. Si le pilotage intégral depuis l’atelier est retenu, authentification API distincte sur le poste (session `gh`/jeton de portée minimale ou autre mécanisme approuvé), jamais embarquée dans le navigateur. Ne pas ajouter cette authentification par surprise.

Critère : vrai clic utilisateur → tests du même état → commit/push de la bonne révision → statut honnête. Pas de transfert manuel de ZIP requis dans le fonctionnement connecté normal ; l’export reste un secours.

## 8. Lot F — publication planifiée, après le circuit simple

- Conserver `draft` indépendant de la date/heure Paris ; stocker un instant explicite, gérer été/hiver et heures ambiguës/inexistantes.
- Intégrer les articles validés futurs sur la branche de publication avant échéance ; une PR non fusionnée ne devient pas autorisée par sa date.
- Ajouter reconstruction périodique et possibilité manuelle dans Actions ; vérifier la documentation actuelle de `schedule`, branche cible, limites et inactivité avant de fixer le YAML.
- L’ordinateur du rédacteur peut être éteint après intégration : le déclenchement se fait chez GitHub.
- L’heure est une échéance d’éligibilité, pas une garantie à la seconde. Signaler retard/échec et permettre une relance contrôlée.
- Tester l’absence avant échéance dans page/listes/RSS/sitemap/catalogue public, présence après build/déploiement, brouillons toujours absents et reprogrammation/suspension versionnées.
- Si le dépôt est public, les articles futurs y sont lisibles : pas d’embargo réel sans sources privées et aperçus protégés.

Critère : simulations Hugo avant/après puis essai réel explicitement autorisé, scheduler contrôlé et preuve de la publication en ligne. Pas de cron local ni serveur permanent ajouté pour compenser silencieusement.

## 9. Recette et ordre d’exécution

- [ ] A — Dépôt, poste(s), clé autorisée et droits identifiés.
- [ ] B — Sauvegarde, comparaison des sources, politique Git et reprise M15 décidées.
- [ ] C — Workflows préparés et vérifiés, puis activation distante expressément autorisée.
- [ ] D — Pont local sécurisé et tests négatifs.
- [ ] E — Atelier connecté testé de bout en bout sur branche/dépôt de recette.
- [ ] F — Programmation et restauration vérifiées après validation du circuit immédiat.
- [ ] Recette visuelle et fonctionnelle utilisateur ; aucune case d’acceptation M15 cochée automatiquement.

Ne pas développer tous les lots en même temps. Première tranche conseillée : A + B, préparation C sans déployer, et validation du parcours avant implémentation D/E. Puis publication d’une révision de recette autorisée, contrôle HTTP et essai de restauration. Programmer les articles seulement après cette base fiable.

## 10. Informations nécessaires pour démarrer la connexion

1. URL exacte du dépôt GitHub Kissari et branche cible ; dépôt déjà existant ou à créer, visibilité.
2. Quelle clé Kissari est déjà autorisée sur ce dépôt, et sous quelle forme (clé de compte ou deploy key) ? Ne fournir aucune clé privée en conversation.
3. Quel(s) poste(s) et OS utiliseront les rédacteurs ? Publication depuis leur propre poste ou seulement depuis le poste d’Eric ?
4. PR obligatoire, ou publication directe réservée à certains publieurs ? L’autorisation API pour automatiser le suivi/PR reste une décision distincte du transport SSH.
5. Domaine final et besoin de confidentialité des brouillons/aperçus.

## Sources locales inspectées

- `specs/10-import-atelier-article.md`
- `specs/13-atelier-github-publication-planifiee.md`
- `livrables/prototype-M15/LIRE-MOI.md`
- Workflows locaux Stéphane : `.github/workflows/hugo-check.yml`, `static.yml`.
- Workflow local Gabriel : `.github/workflows/deploy-gab.yml` (historique VPS, non réutilisable tel quel pour Pages).

Ce document prépare des opérations ; il ne constitue pas un relevé de tests ou de connexion distante réalisés.
