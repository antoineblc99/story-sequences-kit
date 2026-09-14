# Stories

Ce dossier contient le système de séquences stories de l'utilisateur. Tu écris, tu rends, tu publies. Il valide.

## Structure
- `stories/STYLE.md` — le style des slides. À lire avant d'écrire ou de rendre une séquence.
- `stories/deck.py` — le renderer. `stories/build_example.py` — le gabarit à copier en `build.py`.
- `pictures/references/` — les stories que l'utilisateur aime. C'est la référence visuelle, à ouvrir avant chaque séquence.
- `pictures/moi/` — ses photos, classées par scène. Une photo sert de décor, elle ne prouve rien.
- `pictures/screens/` — ses captures de preuve. La preuve, c'est toujours une capture.
- `out/` — les séquences rendues, un dossier par date.

## Règles
- Une séquence commence par 5 questions à l'oral (skill `stories`), jamais par une génération.
- Le copy est validé avant tout rendu. Le rendu est validé avant toute publication. Deux ok, pas moins.
- Le chiffre entouré en rouge est visible sur la capture. Jamais un chiffre qui n'existe que dans le texte.
- Une photo n'est jamais écartée parce qu'elle est claire : on assombrit au rendu.
- Pas d'en-tête, pas de logo, pas de pagination sur une slide.
- Publication en story via PlugKit (`create_post` avec `asStory`), Instagram puis Facebook, une slide à la fois, 60 secondes entre deux.
- Avant de publier, une automation répond au mot-clé sur les stories (playbook `story-lead-magnet`). Sinon on l'installe d'abord.

## Workflow
sujet + preuve → `/stories` → 5 questions → copy (ok) → rendu (ok) → publié Instagram + Facebook → mot-clé → DM
