# M10 / M11 — Documents du pied de page

## Périmètre autorisé

Intégration locale des deux PDF fournis par Eric : M10 mentions légales et M11 remplacement du lien CGV par RGPD. Aucune réécriture des documents, aucune certification juridique, aucun changement des autres lots.

## Sources et destinations

Originaux dans le dossier Obsidian V1, laissés intacts :
- `corrections-finale/Mentions_légales_par_KISSARI.pdf` → `static/documents/Mentions_légales_par_KISSARI.pdf` (4 pages).
- `corrections-finale/RGPD.pdf` → `static/documents/RGPD.pdf` (2 pages).

Liens via `relURL` dans les gabarits accueil, liste blog, article et contact. Nouvel onglet/fenêtre demandé par Eric : `target="_blank"`, `rel="noopener noreferrer"`, sans attribut download imposé. URLs PDF versionnées par SHA-256 pour invalider le cache lors du remplacement. Le navigateur choisit entre onglet et fenêtre ; le site d’origine reste ouvert. « Nous contacter », les menus, les styles et la signature restent inchangés. L’aperçu connecté construit les mêmes gabarits et embarque les deux ressources ; aucun footer juridique dupliqué dans l’atelier autonome.

`data/legal_documents.json` conserve les empreintes réelles des PDF reçus. Après une future version approuvée, recopier le fichier et actualiser ce manifeste explicitement, puis reconstruire ; modifier l’original Obsidian ne modifie pas automatiquement l’asset du site.

## Vérifications effectuées

- `hugo --minify --destination livrables/contact-recette/site --baseURL http://127.0.0.1:18820/`
- `python scripts/test-legal-documents.py livrables/contact-recette/site` : liens des huit pages, empreintes, absence de CGV dans les footers, vrai aperçu connecté et ressources PDF de cet aperçu.
- Navigation, page contact et tests d’aperçu connecté existants réussis.
- HTTP 200/application/pdf et empreintes identiques après récupération des deux PDF.
- Clic réel mentions légales et activation clavier RGPD ; document.contentType application/pdf.
- Pieds de page contrôlés à 1920/390 px pour accueil, blog, article et contact, sans débordement des liens du footer.
- Les retours à la ligne du contenu de contact sont hors de ce lot ; CSS inchangée.

## État de validation

Implémenté et testé ; rendu utilisateur à valider. Cases M10/M11 laissées décochées, toutes les autres lignes de checklist préservées. Captures et rapports dans `livrables/recette-M10-M11/` et le dossier V1 `assets-recettage/lot-M10-M11/`. Aucun push, activation Pages ou déploiement public.
