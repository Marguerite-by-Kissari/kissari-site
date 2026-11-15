# Page contact — première mise en forme

> **RÉVISION ACTIVE : coordonnées sans cadre + bloc rose permanent.** Groupe de deux lignes centré et sans soulignement, sans les libellés « email : » / « linkedin : ». Icônes email et LinkedIn alignées dans une même colonne, liens dans la colonne suivante : `contact@kissari.fr` et `KISSARI sur linkedin`. Destinations exactes `mailto:contact@kissari.fr` et `https://www.linkedin.com/company/kissari/home/`. Sous les liens, centrer horizontalement le bloc rose et réutiliser `bloc-rose.png` avec le titre « Votre message sera entre de bonnes mains ! », le délai de 48 h et le téléphone de la maquette ; tout le texte du bloc est centré. Ce bloc est affiché en permanence sur demande explicite ; il ne confirme aucune transmission. Aucun formulaire, bouton d’envoi, compteur ou JS de formulaire chargé. Hero/navigation/frise/footer inchangés. Build, tests de contact/navigation et recette navigateur desktop/mobile effectués ; acceptation graphique utilisateur encore ouverte.
>
Icône information ajoutée à côté de l’email : texte de confidentialité fourni reproduit à l’identique, disclosure natif au clic/clavier et survol ajouté en JavaScript local. Aucune correction juridique ni nouvelle logique de formulaire. Le texte mentionne toujours un formulaire et des astérisques : incohérence signalée, correction laissée à l’utilisateur.

> **Le reste du document archive la première passe de formulaire, désormais supplantée.** Ne pas réintroduire ses champs, son compteur ni son ancien aperçu de confirmation.

## Périmètre de cette passe

Demande : créer la page `/contact/` depuis les artefacts de `/home/groot/Téléchargements/aTrier/formulaire/Formulaire`, en respectant la maquette `Site KISSARI-Fomulaire.png` et les composants/canevas validés du site. Le montage fourni présente deux états d’une même page : formulaire puis confirmation. Ne pas les empiler avec deux pieds de page sur le site réel.

Cette passe est une **recette graphique locale**. Aucun push, déploiement, service tiers ou mail réellement envoyé. Les finitions catalogue/reprise d’articles/SEO de l’atelier restent ouvertes ; elles ne sont pas clôturées par la page contact.

## Sources et fidélité

- La maquette 4003 × 6299 est une référence, jamais une image de fond de la page complète.
- Utiliser les sept artefacts séparés : femme au glaçon, frise, champ, cadre du message, bouton, flèche, bloc rose.
- Garder les textes HTML, labels associés et vrais contrôles natifs ; aucune capture de texte ni faux champ en image.
- Réutiliser police Poppins, styles/header/footer existants et canevas centré plafonné à 1920 px. La navigation existante garde ses destinations ; ne pas inventer Nos offres/Nos projets pour reproduire des liens sans pages.
- Hero : `#CONTACT`, « Et si on brisait la glace ? », introduction et appel « Jetez-vous à l’eau et écrivez-nous ! » tels que lus sur la maquette.
- Formulaire de cette passe : Objet du message + Votre message, compteur de 600 mots, bouton jaune. Le champ email de réponse reste requis fonctionnellement par la demande antérieure mais n’est pas dessiné dans cette maquette ; ne pas le considérer supprimé du besoin. Prévoir son intégration avant raccordement réel.
- Confirmation : texte et numéro de téléphone de la maquette, sur le bloc rose, accessible dans un aperçu de recette séparé.

## Pas d’envoi fictif

Aucune configuration de destinataire/prestataire/action n’a été trouvée dans le dossier, ZIP ou message Discord contrôlés. Ne pas créer de compte ni choisir un endpoint à la place du propriétaire. Aucun destinataire ou secret SMTP dans le HTML.

- Le bouton ne doit déclencher aucun envoi ni afficher « message envoyé » pendant cette passe.
- Validation native, limite 600 mots et focus/erreur accessibles ; le contenu reste saisi lorsque l’envoi est indisponible.
- L’état de confirmation est un aperçu explicitement étiqueté « aucun message envoyé », pas le résultat d’un submit réussi.
- Sans JavaScript : aucun POST implicite de données et aucune fuite des champs en query string.

## Acceptation

- [ ] Vrai build Hugo, route contact, une H1 et un seul footer.
- [ ] Artefacts fournis copiés dans les assets du site et références valides.
- [ ] Desktop 1920 px, petit écran 390 px et large viewport >1920 : pas de débordement ; composants existants inchangés.
- [ ] Labels, saisie/focus, compteur, refus >600 mots et conservation du message exercés dans le navigateur.
- [ ] Aucun appel réseau d’envoi et aucune fausse confirmation après clic.
- [ ] État de confirmation visualisé séparément avec marqueur de recette visible.
- [ ] Livrer lien local et captures ; laisser les modifications visuelles à l’arbitrage suivant de l’utilisateur.
