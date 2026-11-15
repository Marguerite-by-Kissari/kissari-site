# 04 — Langues et limites de contenu

## Périmètre de contenu

- La landing actuelle est française uniquement.
- Tous les textes doivent être repris strictement depuis les éléments fournis.
- Cette spécification ne propose, ne réécrit et ne complète aucun contenu éditorial.
- Les fragments non complets, notamment dans l’en-tête expertises, restent marqués comme fragments à valider ; ils ne sont pas complétés.

## Préparation multilingue sans contenu EN

La structure Hugo future doit permettre plusieurs langues, sans créer ni publier de version anglaise maintenant :

```text
content/
  fr/
    _index.md
  en/
    _index.md   # structure vide ou draft, aucun contenu à inventer
```

- La langue par défaut est `fr`.
- Les clés de contenu et routes doivent être conçues pour accepter un préfixe de langue.
- Aucun texte EN, traduction automatique, menu EN fonctionnel ou sélection de langue active n’est inclus dans le lot desktop français.

## Hors périmètre

- Pages internes, blog, newsletter, formulaire de contact, presse, projet, offres.
- Footer : reporté après validation du gros du desktop.
- Toute recommandation éditoriale ou de contenu.
