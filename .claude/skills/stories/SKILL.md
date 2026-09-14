---
name: stories
description: Écrit, rend et publie une séquence de stories Instagram et Facebook via PlugKit, dans le style des références de l'utilisateur. Use quand l'utilisateur lance /stories, parle d'une séquence stories, ou veut transformer une preuve (une capture, un chiffre, un résultat) en stories.
---

# Stories

Une séquence stories, c'est 3 à 6 slides qui se lisent comme une seule phrase, avec une preuve au milieu et un mot-clé à la fin. Tu écris le texte, tu fais les images, tu publies. L'utilisateur valide deux fois : le texte, puis les images. Rien ne part sans ces deux ok.

`stories/STYLE.md` décrit le style par défaut. Si `pictures/references/` contient des stories, ce sont elles qui commandent : regarde-les avant d'écrire.

## Étape 0 — ce qu'il te faut

- PlugKit branché : `list_accounts` renvoie son Instagram, et sa Page Facebook s'il en a une. Sinon, leçon 1.9 d'abord.
- `voice/voice.md` rempli. Sinon `/ma-voix` d'abord.
- `pictures/moi/` avec ses photos. Vide ? Demande-lui d'en déposer une dizaine, classe-les par scène avec des noms parlants.
- `pictures/references/` avec des stories qu'il aime. Pas obligatoire, mais c'est ce qui rend le style vraiment sien.

## Étape 1 — comprendre ce qu'il veut

Ne génère rien tant que tu ne sais pas ces quatre choses : à qui la séquence parle, ce que cette personne doit faire à la fin, ce qui prouve ce qu'il avance, et ce qu'elle reçoit en tapant le mot-clé.

Il n'y a pas de liste de questions. Pars de ce qu'il t'a dit, et pose les questions qui manquent pour cette séquence-là, deux ou trois à la fois, à l'oral. Un lancement, un résultat client, une leçon apprise, une offre : chaque sujet appelle ses propres questions. Si une réponse est floue, reformule et fais valider. Si la preuve n'existe pas encore en capture, demande-la.

## Étape 2 — le texte

Écris la séquence dans sa voix (`voice/voice.md`), une idée par slide, et montre-la avec, pour chaque slide, la photo ou la capture prévue et ce que tu entoures en rouge.

Trois choses ne se négocient pas :
- ce qui est entouré est un chiffre ou un élément visible sur la capture, jamais quelque chose qui n'existe que dans le texte
- aucun chiffre non vérifié, aucune promesse de résultat
- jamais de tiret cadratin

Le reste (longueur des blocs, suspens, minuscules) est dans STYLE.md, c'est un défaut, pas un moule.

**Attends son ok sur le texte.** S'il dit « trop long » ou « pas logique », deux slides disent la même chose : coupe.

## Étape 3 — les images

Une fois le texte validé, et pas avant :

1. Choisis les images. La photo de fond vient de `pictures/moi/`, la preuve de `pictures/screens/`. S'il manque quelque chose pour cette séquence (une capture précise, une photo d'un lieu), demande-la : c'est souvent pertinent, jamais obligatoire.
2. Copie `stories/build_example.py` en `stories/build.py` et adapte-le : textes, chemins, position du cercle. La composition par défaut est dans STYLE.md.
3. Rends : `python3 stories/build.py` écrit `out/AAAA-MM-JJ-titre/slide-N.jpg`.
4. Ouvre chaque image, vérifie que le cercle tombe bien sur le chiffre, puis montre la séquence complète, dans l'ordre.

**Attends son ok sur les images.**

## Étape 4 — la publication

Avant d'envoyer quoi que ce soit, vérifie que le mot-clé a une réponse :
- `list_sequences` doit montrer une séquence `story_reply` active sur ce mot,
- son bouton doit pointer vers la ressource promise. Demande-lui le lien, ouvre-le, vérifie qu'il mène bien à ce que la story annonce. Une ressource pas encore créée, c'est une séquence à reporter.

Rien de tout ça ? Propose `install_playbook` avec le playbook `story-lead-magnet` (mot-clé, lien, texte du DM dans sa voix), montre le DM rendu, installe seulement s'il dit oui.

Puis, slide par slide, dans l'ordre :
1. `create_media_upload` avec le nom du fichier, envoie les octets avec `curl -T slide-N.jpg "<uploadUrl>"`.
2. `create_post` avec `asStory: true`, `publishNow: true`, `mediaItems: [{url: <mediaUrl>}]`, `accountIds` = son Instagram. Pas de `content`, une story n'a pas de légende.
3. Attends que `get_post` dise `published`, puis 60 secondes : Meta refuse deux stories créées coup sur coup.

Instagram fini, recommence sur sa Page Facebook s'il en a une de connectée. JPEG uniquement.

## Étape 5 — le retour

Dis-lui ce qui est parti, où, et rappelle le mot-clé. Si son board existe, ajoute-y la séquence.
