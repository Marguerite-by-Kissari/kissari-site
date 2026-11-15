# Intégration M15 et remplacement initial des sources GitHub

## Autorisation

Le 15 novembre 2026, Eric demande explicitement de remplacer les anciennes sources de `https://github.com/Marguerite-by-Kissari/kissari-site` par `/mnt/datas/01-dev/web/maversionkissari`, avec intégration M15. Le transport Git utilise la clé existante autorisée ; aucun force-push ni effacement d’historique.

## Périmètre de cette livraison

- Reprise des sources locales de référence, sans fusion des anciens gabarits distants.
- M15 intégré : onglets article/rubrique, titre et sélection ordonnée, catalogue, export des réglages, heure Paris de publication et test Hugo connecté local.
- Construction autonome M15 complète à travers `python scripts/build-atelier-standalone.py` ; livrable sous `livrables/atelier-editorial-kissari-autonome.html`.
- Le service de test garde ses rapports sous `livrables/test-reports/` et n’écrit ni article ni réglages dans la référence.
- Pas de formulaire de contact, de connecteur Git depuis l’interface, de workflow Pages, de changement DNS ou de planificateur dans ce lot. L’envoi des sources à GitHub ne certifie pas un déploiement public.
- `hugo.toml` conserve la configuration locale de référence ; domaine/baseURL/Pages seront traités au prochain lot, sans reprendre `unsafe = true` de l’ancien dépôt.

## Sauvegardes hors dépôt

Dossier : `/mnt/datas/01-dev/web/kissari-migration-backups/20261115-141956/`.
- Clone complet `remote-before/` et `remote-before.bundle` : branche initiale main, révision `c9925937ac21a11ffda5f277d825f940e9b03ea6`.
- `local-before-M15.tar.gz` : sources locales et livrables avant intégration, sortie public régénérable exclue ; archive lue avec succès.
- L’historique distant reste parent du commit de remplacement. La licence Poppins OFL est conservée sous `static/fonts/OFL.txt`.

## Vérifications effectivement exécutées avant push

- Clé SSH reconnue par GitHub comme deploy key de `Marguerite-by-Kissari/kissari-site` ; lecture Git du dépôt réussie. Le titre administratif « groot access » n’a pas été vérifié via API, aucune session API gh active.
- Build normal et minifié Hugo 0.154.5 Extended réussis : 8 pages, catalogue de 5 articles.
- Syntaxe JS, tests des notes intégrées, compatibilité anciens brouillons et heure Paris/été-hiver : réussis.
- Tests configuration M15, builds titre/ordre/sélection vide/désactivation/texte échappé et exclusion des brouillons/futurs : réussis.
- Tests connectés avec vrais builds temporaires : réglage de rubrique, article futur privé et refus d’un gabarit produisant un mauvais titre : réussis.
- Tests HTTP négatifs : origine étrangère, absence origine/nonce, hôte forgé, conflit de version, JSON invalide/doublonné, ZIP dangereux et absence de route Git/publication : réussis.
- Non-régressions navigation M01–M05, liens M22–M25, contrôles visuels/notes M07–M09/M13–M14/M17–M20 et notes Hugo : réussis.
- Vraie interaction navigateur sur `http://127.0.0.1:1345/atelier-article/` : saisie du titre, focus conservé, aperçu immédiat, clic « Tester sur le site », résultat réussi et consultation du vrai blog temporaire dont le titre correspond. Aucun débordement horizontal détecté à la largeur testée. Capture d’écran indisponible sur cet essai (timeout du navigateur) : ne pas présenter une nouvelle recette visuelle exhaustive comme réalisée.
- Comparaison des sources préexistantes à la sauvegarde : seuls le front matter de la liste blog, son gabarit, le JS et le bundle de l’atelier changent dans les dossiers content/layouts/static ; les autres sources existantes (accueil, CSS, visuels, articles) sont inchangées.
- Fichiers livrables, public, caches, clés et environnements exclus de Git ; recherche de signatures de clés privées et jetons GitHub sans résultat. Ce contrôle ciblé n’est pas une certification de sécurité.

## Utilisation locale après intégration

```bash
python scripts/serve-editorial-preview.py --port 1345
```

Puis ouvrir `http://127.0.0.1:1345/atelier-article/`. Le service de test n’est pas exposé sur Internet. Le serveur historique du prototype sur 1335 n’a pas été arrêté ou modifié.

## Etats à ne pas confondre

M15 intégré et vérifié localement ne signifie pas encore publication autonome depuis l’atelier. La révision Git effectivement poussée et vérifiée à distance est consignée dans le rapport d’exécution hors dépôt et dans la restitution à Eric ; les contrôles Pages et l’URL publique sont un lot ultérieur.
