---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Un skill, c'est un dossier avec un SKILL.md : écris tes consignes une fois, Claude Code les applique tout seul."
destination: tiktok
aspect: 1080x1920
language: fr
audience: "créateurs et développeurs qui utilisent Claude Code, débutants sur les skills"
length: 52s
angle: how-to
voice: "ff_siwis (Kokoro, voix française dynamique)"
---

## Intent

Vidéo TikTok verticale qui explique comment créer des skills dans Claude Code : ce qu'est un skill,
où le ranger, le fichier SKILL.md et son en-tête (name, description), les fichiers d'appui,
et comment l'utiliser (automatiquement ou avec /nom-du-skill). Demande de l'utilisateur, mot pour mot :
« une vidéo qui parle des skills, sur comment créer des skills, sur Claude Code […] avec une voix off,
dynamique, avec des effets en motion design professionnel […] avec des flottants ». L'utilisateur
laisse les choix à Claude (« je pense que toi ») → run autonome.

## Customizations

- Voix off d'homme en français (demande précédente de l'utilisateur).
- Motion design professionnel et dynamique, éléments flottants (cartes, fichiers, icônes qui flottent en douceur).

## Notes

- Faits vérifiés dans la doc officielle code.claude.com/docs/en/skills :
  `~/.claude/skills/<nom>/SKILL.md` (perso), `.claude/skills/<nom>/SKILL.md` (projet),
  frontmatter `name` + `description`, la description décide quand Claude charge le skill,
  invocation manuelle `/<nom>`, fichiers d'appui dans le même dossier, SKILL.md < 500 lignes.
- Pas de HeyGen ni de Hugging Face dans cet environnement : voix Piper locale, musique et SFX générés localement (host audio).
