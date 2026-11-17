# Mobile — navigation partagée et accueil

Statut : validé par Eric (« Je valide, tu peux faire le push vers github avec commentaires sur les modifications effectuées »). Push sur main autorisé. Référence avant modifications : `0b2ec6bb1176fb241201ab44476849ad3af86f64`.

## Périmètre demandé

À moins de 800 px :

- Menu burger commun à l’accueil, au blog, aux articles et au contact. Logo du haut et indication FR / EN visibles. Les destinations et le contenu du menu restent inchangés ; aucune traduction anglaise ni fausse destination n’a été ajoutée.
- Accueil uniquement : panneau femme en maillot + logo/filigrane dessous masqué ; logo du menu et contenu réel de la vidéo conservés.
- Sous « En attendant… » : trait noir horizontal de 120 px, puis espace avant le lecteur vidéo. Texte et vidéo en flux normal, lecteur carré adapté à la largeur disponible, commandes natives utilisables. Après demande complémentaire d’Eric : icône de lecture bleue masquée sur mobile. À sa demande suivante, un espace de 24 px sépare le bas de la vidéo du bandeau de séparation. Icône desktop inchangée.

## Implémentation

- `static/css/mobile.css` : règles sous `max-width: 799px`, aucun changement du CSS desktop validé.
- `static/js/mobile-navigation.js` : disclosure non modale, bouton natif, `aria-controls`/`aria-expanded`, fermeture par lien, clic extérieur, Échap et changement de breakpoint. Focus restauré après Échap. Sans JavaScript les liens restent visibles.
- Partials partagés `mobile-navigation-head.html` / `mobile-navigation-toggle.html` appelés depuis les quatre gabarits existants.
- Test ajouté : `scripts/test-mobile-navigation.py`, vérification des huit pages du site réel construit.
- Test contact adapté strictement au seul bouton burger ; aucun retour du formulaire ni tolérance pour d’autres boutons d’envoi.

## Vérification réelle

- Navigateur : 320, 390, 425, 799 et 1920 px.
- À 1920 px : rectangles, affichage et tailles de police des neuf éléments mesurés (header, logo, navigation, langue, hero, copy, femme, vidéo, scène) identiques avant/après.
- À petite largeur : femme masquée, FR / EN visible, séparation entre texte et vidéo, burger ouvrable/fermable au clic et au clavier ; liens réels et fallback sans JS vérifiés. Pas de déclaration de conformité responsive globale des sections non concernées.
- Build Hugo, navigation générale, corrections des articles, PDF, contact et aperçu connecté : réussis ; contrôle syntaxique JS réussi.
- Preuves : `livrables/recette-mobile-accueil/` (`browser-verification.json`, `desktop-before.json`, `interactions.json`, captures).

## Présentation locale

- Aperçu mobile interactif : <http://127.0.0.1:18824/> (choix 320 / 390 / 425 px).
- Site : <http://127.0.0.1:1313/>.
- Aperçu ouvert dans Zen Browser sur le bureau ; titre de fenêtre relu : « Recette mobile KISSARI ».
- Avant validation, aucun commit ou push de ce lot. Intégration GitHub maintenant autorisée ; conservation des modifications de production déjà présentes sur main, y compris le workflow Pages. Les autres chantiers restent inchangés.
