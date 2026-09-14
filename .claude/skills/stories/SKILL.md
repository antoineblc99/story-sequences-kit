---
name: stories
description: Crée une séquence de stories Instagram (4 slides) dans le style Nik Setting, la rend en images, et la publie en story sur Instagram et Facebook via PlugKit. Use quand l'utilisateur lance /stories, dit "une séquence stories sur X", ou veut transformer une preuve (capture, chiffre) en stories.
---

# Stories

Une séquence stories, c'est 4 slides qui se lisent comme une seule phrase : qui parle → ce qui s'est passé → la preuve → le mot-clé. Tu écris, tu rends, tu publies. L'utilisateur valide deux fois, jamais moins.

Lis `stories/STYLE.md` avant de commencer. C'est le style, il ne se discute pas.

## Étape 0 — vérifie ce qu'il te faut

- `pictures/references/` contient au moins 3 stories que l'utilisateur aime. Vide ? Demande-lui d'y déposer 3 à 5 captures de stories dont il aime le rendu, puis ouvre-les : c'est ta référence visuelle, pas le texte de STYLE.md.
- `pictures/moi/` contient ses photos (10 minimum, sombres ou claires peu importe, on assombrit au rendu). Vide ? Demande-lui d'en déposer, et classe-les en sous-dossiers par scène (`bureau/`, `voyage/`, `sport/`…) avec des noms parlants.
- `pictures/screens/` contient la capture qui prouve ce qu'il va dire. Il n'y en a pas ? Demande-la, elle est obligatoire.
- PlugKit est branché : `list_accounts` renvoie son Instagram (et sa Page Facebook s'il en a une). Sinon, leçon 1.9 d'abord.
- `voice/voice.md` est rempli. Sinon `/ma-voix` d'abord.

## Étape 1 — les 5 questions, à l'oral

Ne génère rien avant d'avoir les réponses. Pose-les d'un coup, il répond en vrac :

1. À qui il parle ? Un seul profil.
2. Ce que cette personne doit se dire après la dernière slide, en une phrase.
3. La scène vraie : où il était, ce qu'il a vu arriver. S'il n'y en a pas, on s'en passe.
4. La preuve, une seule : quel chiffre, sur quelle capture.
5. Le mot-clé du CTA, et ce que la personne reçoit en le tapant.

## Étape 2 — le copy

4 slides, une idée par slide, dans sa voix (`voice/voice.md`). Règles dures :

- minuscules, phrases courtes, 8 à 15 mots par bloc, une à deux lignes par bloc
- chaque slide finit en suspens et la suivante reprend là où elle s'arrête
- le chiffre qu'on entoure en rouge est visible sur la capture, jamais seulement dans le texte
- pas de superlatif, pas de promesse de résultat, pas de chiffre non vérifié
- slide 4 : « réponds MOT. » puis ce qu'il reçoit
- jamais de tiret cadratin

Montre le copy avec, pour chaque slide, la photo ou la capture prévue et ce que tu entoures. **Attends son ok.** S'il dit « c'est pas logique » ou « trop long », c'est que deux slides disent la même chose : coupe.

## Étape 3 — le rendu

Copie `stories/build_example.py` en `stories/build.py`, remplace les textes et les chemins, garde la composition :

- photo de `pictures/moi/` en plein cadre, assombrie : `shot(photo, dim=0.3 à 0.45)` sans `height`
- la capture posée dessus en carte : `inset(capture, x, y, w)`
- les blocs empilés en colonne en haut à gauche, un bloc par ligne
- une annotation rouge par slide de preuve, qui va chercher le chiffre dans la carte : `circle()` + `arrow()`
- le CTA : la ligne du mot-clé en bloc rouge (`fill=MARKER`), le reste en bloc noir
- aucun en-tête, aucun logo, aucune pagination

`python3 stories/build.py` écrit `out/AAAA-MM-JJ-titre/slide-1.jpg` à `slide-4.jpg`. Ouvre-les, vérifie que le cercle tombe sur le chiffre, puis montre-les. **Attends son ok.**

## Étape 4 — la publication

Avant d'envoyer, vérifie qu'une automation répond au mot-clé sur ses stories : `list_sequences` doit montrer une séquence `story_reply` active sur ce mot. Sinon, propose `install_playbook` avec le playbook `story-lead-magnet` (mot-clé, lien, texte du DM), montre le DM rendu, et installe seulement s'il dit oui. Une story publiée sans automation, c'est des réponses qui tombent dans le vide.

Puis, slide par slide, dans l'ordre :

1. `create_media_upload` avec le nom du fichier, envoie les octets avec `curl -T slide-N.jpg "<uploadUrl>"`.
2. `create_post` avec `asStory: true`, `publishNow: true`, `mediaItems: [{url: <mediaUrl>}]`, `accountIds` = son Instagram. Pas de `content`, une story n'a pas de légende.
3. Attends que `get_post` dise `published` avant la slide suivante, puis 60 secondes de plus : Meta refuse deux stories créées coup sur coup.

Instagram fini, recommence les 4 slides sur sa Page Facebook s'il en a une de connectée. JPEG uniquement.

## Étape 5 — le retour

Dis-lui ce qui est parti, où, et rappelle le mot-clé. Si son board existe, ajoute-y la séquence en « posté ».
