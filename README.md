# Story Sequences Kit

Claude écrit, rend et publie tes séquences de stories Instagram et Facebook. Tu donnes un sujet et une preuve, tu valides deux fois, c'est en ligne.

Le style est celui des stories de Nik Setting : une photo de toi en fond, la preuve posée dessus en carte, du texte en blocs noirs, un cercle rouge sur le chiffre, un mot-clé à la fin qui déclenche un DM automatique.

## Ce qu'il te faut

- Claude Code ou Codex (le kit contient le skill pour les deux : `.claude/skills/` et `.agents/skills/`, et un `AGENTS.md`), avec un dossier de travail `content-os`
- PlugKit branché sur Claude par son serveur MCP, avec ton Instagram connecté (et ta Page Facebook si tu en as une). Essai gratuit sur plugkit.co
- 10 photos de toi, 3 stories que tu aimes, et une capture qui prouve ce que tu veux dire

## Installation (5 min)

1. Télécharge ce kit (bouton **Code → Download ZIP**, ou `git clone`). Tu obtiens un dossier `story-sequences-kit`. Glisse-le tel quel dans ton dossier `content-os`.
2. Ouvre `content-os` dans Claude Code et colle-lui :
   > Installe le kit stories : déplace tout le contenu de story-sequences-kit (y compris les fichiers cachés) à la racine de ce dossier, supprime le dossier vide, et lance `python3 stories/build_example.py` pour vérifier que le rendu marche. Montre-moi les 4 images.
3. Dépose tes images :
   - `pictures/references/` : 3 à 5 captures de stories dont tu aimes le rendu
   - `pictures/moi/` : tes photos (Claude les classe)
   - `pictures/screens/` : tes captures de preuve
4. Lance `/stories`.

## La commande

| Commande | Ce que ça fait |
|---|---|
| `/stories` | Te pose les questions qui manquent, écrit la séquence, la rend, te la montre, câble le mot-clé si besoin, et publie en story sur Instagram puis Facebook |

## Structure

```
stories/
  STYLE.md            le style, à lire avant tout
  deck.py             le renderer (1080x1920)
  build_example.py    le gabarit d'une séquence
  fonts/              les polices (licence OFL)
pictures/
  references/         les stories que tu aimes
  moi/                tes photos
  screens/            tes captures de preuve
out/                  les séquences rendues
```

Sur Mac le texte utilise Helvetica Neue, la police la plus proche de celle d'Instagram. Ailleurs, Hanken Grotesk prend le relais.

## Bloqué ?

Screenshot dans la communauté, on débloque.
