# Le style

Ce kit reproduit la structure des stories de Nik Setting, un créateur dont les séquences convertissent parce qu'elles ressemblent à des stories faites à la main sur le téléphone, pas à des visuels d'outil. Cherche son compte sur Instagram et regarde ses stories avant de faire la tienne. Puis dépose 3 à 5 captures de stories que tu aimes dans `pictures/references/` : c'est ça que Claude regarde, le texte ci-dessous ne remplace pas le fait de voir.

## Les 8 règles

1. **La photo est en plein cadre.** Une photo de toi ou de ton décor remplit toute la story, assombrie pour que le texte passe. Pas de bande, pas de fond noir vide.

2. **La preuve est posée dessus, en carte.** La capture (un dashboard, un compteur, un message reçu) est réduite et posée sur la photo, coins arrondis, ombre douce. La photo raconte, la carte prouve.

3. **4 à 7 blocs de texte par slide, empilés en colonne.** Alignés à gauche, collés les uns aux autres, en haut du cadre. Chaque bloc fait une à deux lignes de 8 à 15 mots. C'est un raisonnement qui se déroule, pas un slogan.

4. **Le bloc noir, texte blanc.** C'est le bloc natif Instagram. On le garde partout, sauf pour le mot-clé du CTA qui passe en bloc rouge.

5. **Une annotation rouge par slide de preuve.** Un ovale irrégulier autour du chiffre, une flèche courbe qui part du texte et va le chercher dans la carte. Tracé main, pas géométrique.

6. **Le chiffre entouré est visible à l'écran.** Si tu écris « 194 personnes », le 194 est dans la capture et le cercle tombe dessus. Jamais un chiffre qui n'existe que dans le texte.

7. **Chaque slide finit en suspens.** « à une condition… », « voilà ce qu'il a sorti… ». La suivante reprend là où elle s'arrête. Quatre slides, une seule phrase.

8. **Rien d'autre.** Pas d'en-tête, pas de logo, pas de pagination, pas de signature. Une story native n'a que du texte posé sur une image.

## La composition d'une slide de preuve

```
┌──────────────────────────────┐
│  photo assombrie (plein cadre)│
│                               │
│  ■ bloc 1                     │  ← colonne de blocs, x=72, à partir de y≈330
│  ■ bloc 2                     │
│  ■ bloc 3, en suspens…        │
│                               │
│   ┌────────────────────┐      │
│   │  capture en carte  │◯     │  ← inset(), le cercle sur le chiffre
│   └────────────────────┘ ↑    │
│                          │    │  ← la flèche part du bloc du dessous
│  ■ ce que ça prouve      ┘    │
│                               │
└──────────────────────────────┘
```

## Ce qui rate, et qu'on a déjà raté

- deux blocs par slide au lieu de cinq : ça tourne au slogan, le modèle argumente
- deux grappes de texte éloignées, une en haut et une en bas, au lieu d'une coulée
- une capture seule sur fond noir : ça sent l'outil
- un chiffre annoncé dans le texte et un cercle sur autre chose
- deux slides qui disent la même chose : on coupe, quatre slides suffisent
- une photo écartée parce qu'elle est claire : on assombrit au rendu avec `dim`, on ne trie pas sur la lumière

## Les photos

Ce qu'il faut dans `pictures/moi/` : des scènes, pas des poses. Toi au bureau, en déplacement, dans un lieu. Décentré ou petit dans le cadre, avec une grande zone calme pour le texte. Verticales de préférence, mais une horizontale bien composée se recadre. Claire ou sombre, peu importe : le rendu assombrit.
