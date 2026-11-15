# Atelier — pilotage GitHub et publication différée

## Statut et périmètre

Demande utilisateur du 12 novembre 2026 : rendre accessibles dans l’atelier les opérations Git/GitHub nécessaires au pilotage éditorial, avec deux circuits, avec ou sans pull request, et permettre une publication future.

**Actualisation :** GitHub Pages et le transport Git par clé SSH sont désormais demandés. Voir `14-plan-atelier-publication-ssh-github-pages.md` pour le plan d’actions et la frontière entre atelier local, SSH et API GitHub. La GitHub App ci-dessous reste une ancienne proposition, pas une architecture imposée. Aucun dépôt ou accès distant n’a été connecté par cette actualisation.

**Spécifications initiales de l’évolution GitHub, pas une connexion déjà réalisée.** Le dépôt, la branche de publication et les comptes autorisés restent à identifier avant toute écriture distante. L’hébergement cible est maintenant GitHub Pages.

Le test connecté local et la date/heure de publication sont déjà prototypés dans `livrables/prototype-M15/site/`. Aucun push, PR, workflow distant, secret GitHub ou déploiement n’est créé par ce lot. M15 reste soumis à recette utilisateur.

## 1. Architecture retenue comme proposition

- Conserver Hugo pour le site public statique.
- Conserver un atelier unique : articles, rubrique éditoriale et tableau de pilotage de publication.
- Ajouter un connecteur de confiance à GitHub, de préférence une GitHub App limitée au dépôt choisi, avec sessions utilisateur authentifiées et droits explicites.
- Ne jamais incorporer de clé privée, secret d’application ou jeton permanent dans le HTML autonome, les exports ou le stockage navigateur. Les autorisations du connecteur ne remplacent pas celles des personnes.
- Garder le portable pour rédiger hors ligne et préparer des exports ; les fonctions GitHub et publication exigent une connexion. Pas de terminal à utiliser par les rédacteurs.
- Ne pas fabriquer un terminal Git généraliste dans l’interface : couvrir le pilotage éditorial, pas exposer `force push`, suppression de dépôt, règles de sécurité ou commandes arbitraires.

## 2. Opérations accessibles depuis l’interface

### Contexte et synchronisation

- Se connecter/se déconnecter ; afficher identité, droits, dépôt, branche et environnement cible.
- Lire l’état réel du dépôt ; actualiser la version de base et les contenus sans écraser un brouillon local.
- Créer/rouvrir/modifier un article ; conserver son slug, son URL, son identité et les métadonnées inconnues, notamment `next_article` et `next_banner_empty` des lots M22–M25.
- Charger les réglages éditoriaux actuels et le catalogue, y compris l’état privé des articles programmés pour le tableau de pilotage. Ne pas exposer ce catalogue privé sur le site public.
- Afficher les fichiers modifiés, le diff lisible, la version de référence et le message de commit ; filtrer strictement les chemins autorisés côté connecteur.

### Historique et contrôles

- Sauvegarder une version sur une branche de travail ; distinguer brouillon navigateur, brouillon enregistré sur GitHub et contenu publié.
- Créer une branche éditoriale et afficher sa cible ; actualiser/résoudre un conflit sans forçage ni perte silencieuse.
- Lancer les tests et une prévisualisation sur une révision identifiée, afficher progression, erreurs, résumé des checks et liens vers les logs GitHub.
- Invalider l’accord de publication si le contenu ou la base change après le test. Vérifier le SHA exact, et les règles GitHub applicables, au moment d’intégrer.
- Consulter l’historique des commits et restaurer via un nouveau commit de rétablissement. Pas de réécriture de l’historique partagé.

### Pilotage de la mise en ligne

- Choisir le circuit autorisé : « Soumettre pour validation » ou « Publier sans PR ».
- Voir/ouvrir/actualiser une PR, demander une relecture, consulter ses retours, la corriger, la fermer ou la fusionner selon les droits et checks.
- Lancer, suivre ou relancer un workflow de test/déploiement connu, sans permettre de fournir une commande libre.
- Afficher le SHA intégré, le SHA effectivement déployé, l’URL, le statut de déploiement et le contrôle HTTP final.
- Un commit, une PR fusionnée ou un workflow démarré ne suffisent pas à afficher « Publié ». Ce statut exige un déploiement réussi et une lecture de contrôle du site cible.
- Exposer une restauration contrôlée : rétablissement versionné des sources et déploiement cohérent. Un simple retour à un ancien artefact ne doit pas être annulé par la reconstruction suivante.

## 3. Option A — avec pull request

Parcours : rédaction → branche éditoriale → commit → tests/prévisualisation → PR → relecture/corrections → fusion autorisée → déploiement ou attente de la date future.

### Avantages

- Relecture avant intégration ; responsabilités et échanges tracés.
- Changements de plusieurs rédacteurs mieux isolés.
- Protections de branche et checks requis naturellement compatibles.
- Facile à généraliser à des contributeurs occasionnels ; publication future prévalidable bien avant l’échéance.

### Inconvénients

- Étape supplémentaire et attente si un relecteur indépendant est exigé.
- Gestion des conflits, PR abandonnées et corrections après retour.
- Davantage d’états à expliquer dans l’interface ; potentiellement des exécutions CI supplémentaires.
- Une PR n’est pas un coffre-fort : si le dépôt ou la prévisualisation est public, son contenu peut être lisible avant publication.

## 4. Option B — sans pull request

Parcours proposé : rédaction → commit candidat isolé → mêmes tests/prévisualisation → confirmation d’un éditeur autorisé → intégration sans PR de la révision contrôlée sur la branche de publication → déploiement ou attente de la date future.

« Sans PR » ne signifie ni sans Git, ni sans historique, ni sans test. Le candidat peut être validé sur une branche technique avant un avancement fast-forward de la branche cible ; si la base change, refuser et retester. Ne pas pousser un contenu non vérifié sur la branche de publication pour ensuite seulement constater l’échec.

### Avantages

- Parcours court pour une personne de confiance ou un petit groupe.
- Pas de dépendance à la disponibilité d’un relecteur.
- Même historique Git, même contrôles techniques et même capacité de rétablissement.

### Inconvénients

- Pas de seconde lecture humaine imposée : une erreur éditoriale peut passer malgré une CI verte.
- Droits d’intégration plus sensibles ; erreurs et conflits plus directement exposés.
- Politique de branche à concevoir expressément. Si GitHub exige une PR sans exception applicable, cette option doit être désactivée, pas contourner silencieusement la règle.
- Le déploiement ne doit jamais utiliser un vieux résultat de test ni un artefact d’une autre révision.

### Recommandation

**Avec PR par défaut ; sans PR réservé au rôle d’éditeur/publieur habilité.** Le choix doit rester dans l’atelier et être contraint par les droits réels, pas seulement par l’état visuel d’un bouton. Les deux circuits partagent les mêmes validations et la même chaîne de déploiement.

## 5. Publication future

### Contrat de contenu et interface

- Choisir une date et une heure en `Europe/Paris`. Stocker `publishDate` en ISO 8601 avec décalage explicite ; conserver le fuseau métier dans le pilotage. Gérer heure d’été/hiver ; refuser une heure inexistante ou ambiguë plutôt que choisir silencieusement.
- Deux décisions distinctes : **brouillon** (`draft: true`) ou **validé** (`draft: false`) ; date future = pas encore publiable. Un brouillon ne doit jamais paraître automatiquement à son échéance.
- Distinguer « en attente de validation », « programmation prête », « échéance dépassée/en attente de génération », « déploiement en cours », « publié » et « échec ».
- Une programmation n’est armée que lorsque le contenu validé est sur la branche effectivement utilisée par la chaîne de publication et que le déclencheur automatique est opérationnel.
- Avec PR : fusionner le contenu validé avant la date future. La PR non fusionnée reste en attente d’approbation ; atteindre sa date n’autorise jamais sa fusion automatique.
- Sans PR : intégrer le contenu validé avant la date future, après checks et confirmation autorisée.
- Modifier la programmation ou la suspendre doit produire un changement versionné ; désactiver la publication via retour à l’état brouillon, pas seulement un drapeau local.

### Déclenchement et déploiement

Hugo génère un site statique : **mettre une date future ne crée pas d’horloge dans le site déjà publié**. Une reconstruction puis un déploiement réussis sont indispensables après l’échéance.

Proposition : GitHub Actions sur intégration, déclenchement manuel et contrôle périodique, par exemple toutes les quinze minutes décalées du début d’heure (`7,22,37,52 * * * *`, sans fuseau de cron explicitement défini, donc UTC). La date de l’article reste un instant avec décalage explicite. Aucun workflow de ce type n’est installé par le prototype.

- Le workflow programmé doit exister sur la branche par défaut et y exécute son événement `schedule`. Aligner la branche de publication ou configurer explicitement le checkout et les contrôles d’autorité si elle diffère.
- Ne jamais utiliser `--buildFuture` ou `--buildDrafts` pour produire l’artefact de production.
- Exclure les contenus non publiables des pages, listes, RSS, sitemap et catalogue public. Les prévisualisations futures/brouillons doivent être privées.
- Tester à date simulée avant et après l’échéance, puis déployer atomiquement seulement un artefact valide ; empêcher qu’un ancien workflow publie après un plus récent.
- Échec de build/déploiement : conserver le site antérieur, signaler le retard et permettre la relance depuis l’interface.
- L’heure choisie est une heure d’éligibilité, pas une garantie à la seconde : GitHub documente des retards possibles et même des jobs perdus sous forte charge. Le délai nominal dépend de la périodicité, puis du temps de build et de déploiement. Si une heure stricte est requise, prévoir un ordonnanceur dédié et une surveillance.
- GitHub peut désactiver le planning d’un dépôt public inactif depuis 60 jours : afficher la santé réelle du déclencheur et alerter, pas seulement conserver une case « planifié ».

### Confidentialité

Si le dépôt source est public, le texte d’un article futur reste lisible dans Git, même si Hugo ne l’affiche pas. Pour un véritable embargo, utiliser des sources privées et des aperçus authentifiés. Un site public n’impose pas un dépôt source public.

## 6. Recette du futur connecteur GitHub

- Même contenu accepté via PR ou sans PR : même résultat ; absence des droits : refus serveur.
- Révision modifiée après test, base concurrente, conflit, checks rouges ou protection incompatible : intégration bloquée.
- Création puis modification d’un article existant : URL et métadonnées de navigation conservées.
- Publication future : absence avant échéance (page/listes/RSS/sitemap/catalogue), présence après génération à l’échéance ; brouillon toujours absent.
- Fuseau Paris été/hiver et heures ambiguës/inexistantes ; report/annulation de programmation ; PR non fusionnée à l’échéance.
- Panne/retard Actions, relance, dernier déploiement connu et restauration versionnée.
- Aucun statut « publié » avant déploiement réussi et contrôle HTTP de la bonne révision.
- Aucun jeton dans les exports/HTML/logs ; périmètre de chemins et opérations autorisés vérifié côté serveur ; contenu d’aperçu non public par défaut.

## 7. Décisions restant à prendre avant connexion réelle

URL du dépôt ; privé/public ; branche par défaut et branche de publication ; hébergement ; comptes/rôles ; règle de relecture et personnes pouvant publier sans PR ; périodicité et retard acceptable ; destination et confidentialité des aperçus.

## Sources officielles consultées

- [GitHub — Pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub Actions — schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), documentation relue le 12 novembre 2026 : branche par défaut, retards/jobs perdus, fuseau UTC par défaut ou option IANA, intervalle minimal et inactivité des dépôts publics.
- [Hugo — front matter](https://gohugo.io/content-management/front-matter/) ; comportement local vérifié avec de vrais builds et `--clock` dans les tests du prototype, pas déduit d’un simple aperçu.
