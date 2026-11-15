# 02 — Système visuel desktop

## Périmètre

Ce document décrit le rendu desktop de la landing page uniquement. Il ne prescrit ni adaptation tablette/mobile, ni contenu éditorial supplémentaire, ni comportement de pages internes.

## Palette issue des références

| Jeton | Valeur | Zone observée |
|---|---:|---|
| `color.ink` | `#000001` | header, textes noirs, footer ultérieur |
| `color.paper` | `#F8F8F5` | hero, manifeste, expertises |
| `color.pink` | `#FEBAB8` / `#FB8BBF` | accents/surlignage ; valeur finale à confirmer sur la maquette source |
| `color.yellow` | `#FCEC89` / `#FFE96B` | bloc 02 et carte jaune ; valeur finale à confirmer sur la maquette source |
| `color.blue` | bleu de `Cercle bleu.png` / `Fond bleu.png` | hero et carte 01 |
| `color.green` | vert de `Fond vert.png` | carte 04 |
| `color.violet` | violet de `Fond violet.png` | carte 03 |

Aucune normalisation ou correction de couleur n’est appliquée dans ce lot : les PNG fournis restent la référence visuelle.

## Police

- Famille obligatoire : Poppins locale.
- Poids autorisés pour la landing : Regular, Bold, ExtraBold ; SemiBold seulement si un état d’interface déjà fourni le nécessite.
- Les tailles desktop par zone sont définies dans `01-homepage.md` et proviennent du RTF fourni.

## Composition desktop

- Largeur de référence : 1920 px.
- Les hauteurs de référence RTF sont : hero 1 350 px ; manifeste 2 300 px ; expertises 2 300 px ; header 115 px.
- Chaque section garde son propre contexte de superposition (`position: relative` / `isolation: isolate`) afin qu’aucun calque ne passe visuellement dans la section suivante.
- Les règles d’espace et de `z-index` sont exclusivement centralisées dans `01-homepage.md`.

## Compatibilité W3C

Aucune correction directe n’est prescrite par ces spécifications. Si une incompatibilité W3C ou accessibilité est constatée pendant une future implémentation, elle doit être documentée comme une **proposition** distincte, avec impact et alternative, avant toute modification.
