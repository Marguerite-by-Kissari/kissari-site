# M15 — Rubrique éditoriale du blog et atelier d’écriture

## Statut et gouvernance

**Amendement du 15 novembre 2026 : Eric autorise explicitement l’intégration de M15 dans la racine de référence et le remplacement des anciennes sources du dépôt GitHub.** Les restrictions historiques d’isolement ci-dessous décrivent la phase prototype ; elles n’interdisent plus cette intégration. Les tests restent isolés et ne publient rien. Aucun bouton Git/SSH, workflow distant ou planificateur n’est ajouté dans ce lot. Les cases historiques de recette ne sont pas cochées rétroactivement.

Proposition approuvée pour **spécification et prototype testable** le 12 novembre 2026. Ce document est le contrat du prototype, pas une acceptation de son rendu. M15 reste non cochée jusqu’à validation utilisateur. Source : note Obsidian « M15 - Proposition technique - Rubrique éditoriale du blog ».

- Site validé : `/mnt/datas/01-dev/web/maversionkissari`.
- Implémentation de test isolée : `livrables/prototype-M15/site/`.
- HTML portable et mode d’emploi : `livrables/prototype-M15/`.
- Seuls les documents de spécification/suivi sont écrits dans les emplacements canoniques. Aucun changement fonctionnel du site validé, aucun déploiement distant.

## Contrat fonctionnel

- **M15-F01** Ajouter au même atelier deux onglets accessibles : « Écrire un article » et « Rubrique du blog ». Préserver le formulaire, le brouillon et l’export ZIP d’article existants. M26 reste exclu.
- **M15-F02** Le titre est libre, sans préfixe imposé, sur une ligne ; 1–100 points de code Unicode après trim. Conserver casse, accents et apostrophes. Aperçu pendant la saisie sans remplacement du champ ni perte de focus.
- **M15-F03** Afficher les articles publiables du catalogue réel ; recherche, sélection sans doublons, ordre explicite par boutons Monter/Descendre/Retirer. Ne pas changer les catégories ou les textes d’articles.
- **M15-F04** L’interrupteur désactive le bloc sans effacer la sélection. Rendre la rubrique seulement si enabled=true et au moins une référence est publiable. Une sélection vide ne réaffiche jamais tous les articles.
- **M15-F05** La rubrique réutilise le composant de cartes et ses styles, sous l’ID technique stable `editorial`. Elle apparaît dans Tout voir, pas dans les filtres de catégorie. « À la une » reste indépendant. Tous les éléments validés antérieurement sont préservés.
- **M15-F06** Le titre alimente H2 et libellés accessibles des flèches ; texte échappé, jamais HTML interprété.

## Données et formats

- **M15-D01** Autorité unique : `data/blog_editorial.json` avec exactement `schema_version:1`, `title:string`, `enabled:boolean`, `article_paths:string[]`. L’ordre du tableau est l’ordre des cartes. Références = URL canoniques relatives des articles, pas titres ou chemins des fichiers Markdown.
- **M15-D02** Le prototype reprend « Zoom sur nos idées » et sélectionne les trois articles Marketing Learning, dans l’ordre Action ! → Pourquoi… → Avant-postes… . L’ancien `zoom_title` n’est plus actif dans la copie. Aucun UUID ni modification des articles nécessaire.
- **M15-D03** Le catalogue Hugo `/blog/catalogue-editorial.json` expose exactement les métadonnées publiques nécessaires : version, date de génération, configuration, empreinte SHA-256 des octets du fichier canonique et articles publiables (URL/titre/catégorie/date). Exclure explicitement brouillons et publications futures, même dans un build d’aperçu.
- **M15-D04** Export des réglages : `{schema_version:1, base_config_sha256:<64 hex>, changes:{...}}`. Changes contient seulement les champs modifiés parmi title/enabled/article_paths ; titre normalisé avant comparaison. Aucun export sans changement.
- **M15-D05** Ne pas transporter la configuration globale dans le ZIP des articles. Changer le titre seul n’exporte que title. Préserver les champs globaux non modifiés et les métadonnées M22–M25.

## État navigateur et portabilité

- **M15-U01** Sauvegarde globale distincte : `kissari-blog-editorial-draft-v1`. Ne pas lire/écraser le contenu du brouillon d’article pour piloter la rubrique. Anciennes sauvegardes article inchangées.
- **M15-U02** Afficher provenance et génération du catalogue. HTTP : actualisation même origine ; si brouillon modifié, proposer le chargement sans écraser silencieusement. Local : aucun fetch automatique ; instantané embarqué + import JSON explicite.
- **M15-U03** Les boutons de sauvegarde/réouverture/import/export sont explicites. Confirmer avant de remplacer une édition locale modifiée. Signaler les erreurs de stockage et JSON. Aucun service externe.
- **M15-U04** La version servie et le HTML portable sont produits depuis le même HTML source, mêmes CSS/JS et même catalogue ; le fichier portable fonctionne en file://. Aperçu textuel des vraies cartes, sans images distantes nécessaires.
- **M15-U05** Les références devenues indisponibles restent visibles dans la sélection avec avertissement. Pour une sélection nouvellement modifiée, refuser les références inconnues ; pour un titre seul, conserver les anciennes références et prévenir. Le site filtre les références non publiables sans substitution.

## Import local contrôlé

- **M15-I01** `scripts/import-blog-editorial.py EXPORT.json` prévisualise seulement ; `--apply` autorise la modification de la configuration **de la copie contenant ce script**. L’utilisateur peut transmettre le JSON à Jarvis. Le navigateur ne publie ni n’écrit dans le dépôt.
- **M15-I02** Valider taille/JSON strict (doublons de clés rejetés), version/types/titre/chemins/doublons/listes blanches. Empreinte de base différente : refus sans modification, pas de forçage.
- **M15-I03** Recalculer le catalogue publiable à l’import ; ne pas faire confiance à l’ancien snapshot pour une nouvelle sélection. Aucun chemin de sortie fourni par l’export.
- **M15-I04** Sous verrou local, sauvegarder la configuration antérieure par empreinte, écrire atomiquement, vérifier un build isolé, journaliser. Échec du build : restaurer les octets antérieurs ; pas de publication. Retour explicite « enregistré, non publié ».

## Construction et livrables

`build-editorial-prototype.py` : build Hugo intermédiaire normal vers un répertoire de travail → catalogue → fabrication autonome depuis un HTML maintenable → copie identique du portable et de la version servie → build final. Aucun buildDrafts/buildFuture de livraison. Le serveur `scripts/serve-editorial-preview.py` sert le résultat du prototype et une API de test locale en boucle locale uniquement ; il n’est pas un serveur de publication.

## Amendement autorisé — test connecté et publication future

- **M15-C01** Ajouter « Tester sur le site » aux deux onglets. Capturer les réglages ou le même ZIP article que l’export, puis les envoyer au service local de même origine, jamais à une API de publication.
- **M15-C02** Construire une copie jetable des sources : aucune application dans la configuration ou les articles du prototype de référence. Garder une seule construction à la fois et limiter les prévisualisations actives ; répertoires temporaires dans le cache scratch.
- **M15-C03** Valider le contrat, les types, les chemins et l’empreinte actuelle. ZIP limité, deux fichiers seulement, aucun chemin libre, aucune collision d’URL ou écrasement d’un article existant. Les médias de test sont des images raster identifiées.
- **M15-C04** Vérifier le vrai HTML : titre, sélection, ordre, libellés accessibles ; construire puis exécuter les contrôles de navigation, des relations M22–M25 et des gabarits/notes. Restituer un rapport et des liens vers le site réel du test. Ne jamais annoncer un succès sur la seule foi d’un aperçu de formulaire.
- **M15-C05** Service limité à `127.0.0.1`, hôte contrôlé (y compris aperçu), POST d’origine identique avec nonce de session, taille bornée et JSON strict. Aucun CORS permissif, shell libre, Git/push/apply/deploy, ni source du projet servie par HTTP. Les erreurs ne peuvent pas modifier les sources de référence.
- **M15-C06** En file:// : zéro connexion automatique, édition/export maintenus, test désactivé et lien explicite vers l’atelier connecté. Un serveur HTTP statique seul ne suffit plus pour le test Hugo.
- **M15-C07** Ajouter une heure de publication ; convertir le couple date/heure Paris vers un ISO 8601 avec décalage explicite. Préserver la sauvegarde des anciens brouillons (heure par défaut 09:00). Rejeter les heures inexistantes/ambiguës à un changement d’heure.
- **M15-C08** Un article `draft: true` reste exclu. Un article validé avec date future reste absent du build public ; le test crée un aperçu privé avec les flags appropriés, et pour un article futur validé vérifie sa présence après échéance par `hugo --clock`. Ces flags sont interdits dans la future production.
- **M15-C09** Le prototype peut préparer l’article futur et prouver son comportement, mais **ne programme aucun job distant**. L’automatisation GitHub et les deux circuits PR/sans PR sont spécifiés dans [13 — Pilotage GitHub](13-atelier-github-publication-planifiee.md), pas connectés par ce lot.
- **M15-C10** L’état testé est celui capturé au clic, avec son rapport horodaté. Une modification ultérieure nécessite un nouveau test ; ce service ne comporte de toute façon aucun bouton de publication.

## Recette d’acceptation

- **M15-T01** Tests unitaires import : titre seul, sélection/ordre, disabled, JSON/clé/version/type/hash erronés, doublons, titre vide/long/multiligne, chemin dangereux, inconnu, ancien état, écriture atomique/sauvegarde et conflit après un premier import.
- **M15-T02** Builds réels : titre libre, ordre des trois cartes, labels accessibles, ID stable, zéro sélection et disabled absents, sélection partiellement/tout indisponible, HTML littéral échappé, absence de brouillons/futurs du catalogue.
- **M15-T03** Navigateur : vrai clic/frappe avec maintien du focus ; recherche/sélection ; boutons d’ordre ; sauvegarde/réouverture ; import d’état ; export JSON réellement téléchargé ; refus des entrées invalides ; filtrage et flèches du blog.
- **M15-T04** Chaîne complète : télécharger un titre modifié dans l’atelier → import dry-run puis apply dans la copie → reconstruire → vérifier le H2 réel du blog. Revenir au scénario de départ avant livraison.
- **M15-T05** File:// : ouvrir le portable, éditer, sauvegarder/réouvrir et télécharger le vrai JSON sans serveur ; aucun réseau caché. Tester aussi l’export ZIP d’article pour non-régression.
- **M15-T06** Rendu ordinateur/mobile (390/960/1280/1920 et grand écran), titre long/accents/apostrophes, pas de débordement de l’onglet. Tests antérieurs : menus, héros, notes et liens M22–M25.
- **M15-T08** Vrais clics dans les deux onglets → API → Hugo → contrôles → lien de prévisualisation ; vérifier aussi mauvais titre produit par le gabarit, conflit, requête étrangère, nonce invalide, hôte forgé, ZIP dangereux, fichier portable et cinq largeurs.
- **M15-T09** Export d’article futur avec heure/fuseau, absence publique avant date (page/listes/RSS/sitemap/catalogue), aperçu privé, présence après simulation de date ; sauvegarde/réouverture de l’heure et rejet des transitions horaires invalides.
- **M15-T07** Empreintes des sources fonctionnelles du site validé inchangées ; cases utilisateur inchangées ; versions portable/servie identiques ; livrer URL locale, chemin absolu HTML et procédure.

## Découpage d’exécution

1. Tests import/config en échec, validation et importateur, tests verts.
2. Configuration + sortie catalogue + rendu Hugo, builds et cas vide/ordre.
3. Onglets et état éditorial autonome, tests navigateur et export réel.
4. Chaîne d’import complète et non-régressions, captures, manuel et suivi à valider.

L’intégration du prototype dans le site validé exige une nouvelle acceptation de l’utilisateur. Les commandes du prototype ne modifient jamais cette racine par défaut.
