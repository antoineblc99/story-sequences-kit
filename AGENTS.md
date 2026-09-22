# Story Sequences Kit — pour Codex (et tout agent qui lit AGENTS.md)

Ce kit est un skill : `.claude/skills/stories/SKILL.md` (copie identique pour Codex dans `.agents/skills/stories/SKILL.md`).
Quand l'utilisateur demande une séquence de stories, ou tape `/stories`, lis ce fichier et applique-le pas à pas : les questions,
le texte, le rendu, les deux validations, puis la publication via le serveur MCP PlugKit (`list_accounts`, `create_post` avec
`asStory`, `create_comment_automation` ou séquence sur le mot-clé). Rien ne part sans le « ok » de l'utilisateur sur le texte,
puis sur les images.

Prérequis : PlugKit branché en MCP (Claude Code : commande copiée depuis le dashboard PlugKit → MCP ; Codex : la même config
dans `~/.codex/config.toml`), Python 3 avec Pillow pour le rendu, les dossiers `pictures/` remplis comme le README l'explique.
