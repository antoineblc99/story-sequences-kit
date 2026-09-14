# Le style par défaut

Le kit part de la structure des stories de Nik Setting, un créateur dont les séquences convertissent parce qu'elles ressemblent à des stories faites à la main sur le téléphone, pas à des visuels d'outil. Cherche son compte sur Instagram et regarde ses stories.

C'est un point de départ. Dépose 3 à 5 captures de stories que tu aimes dans `pictures/references/`, et Claude s'aligne sur elles, pas sur ce texte.

## Ce qui ne bouge pas

- **La preuve est une capture.** Un dashboard, un compteur, un message reçu. Une photo raconte, elle ne prouve rien.
- **Ce qu'on entoure est visible.** Si le texte dit « 194 », le 194 est dans la capture et le cercle tombe dessus.
- **Deux validations.** Le texte, puis les images. Rien ne part sans.

## Ce qui marche bien

- **Une photo de toi en plein cadre**, assombrie pour que le texte passe, plutôt qu'un fond noir vide.
- **La capture posée dessus en carte**, coins arrondis, ombre douce. La photo raconte, la carte prouve.
- **Des blocs de texte empilés en colonne**, alignés à gauche, une à deux lignes chacun. Un raisonnement qui se déroule, pas un slogan.
- **Le bloc noir, texte blanc**, celui d'Instagram. Le mot-clé du CTA en bloc rouge, pour qu'il saute aux yeux.
- **Une annotation rouge** par slide de preuve : un ovale tracé main autour du chiffre, une flèche qui part du texte.
- **Chaque slide finit en suspens** et la suivante reprend là où elle s'arrête.
- **Pas d'en-tête ni de pagination** : une story native n'a que du texte sur une image. Si tu veux ta signature, mets-la, c'est ta story.

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

## Ce qui rate

- une capture seule sur fond noir : ça sent l'outil
- un chiffre annoncé dans le texte et un cercle sur autre chose
- deux slides qui disent la même chose : on coupe
- une photo écartée parce qu'elle est claire : on assombrit au rendu avec `dim`

## Les photos

Des scènes, pas des poses : toi au bureau, en déplacement, dans un lieu. Décentré ou petit dans le cadre, avec une zone calme pour le texte. Claire ou sombre, peu importe.
