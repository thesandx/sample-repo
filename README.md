# sample-repo

This is just a sample repository.

It contains **no source code** — it was created to test the local repo → GitHub
push workflow, following the user's instructions exactly.

Nothing here is meant to be used or built.

## vivah.online reel-editing skill

`.claude/skills/vivah-reel-editor/` is a handover skill for Claude agents making Instagram reels
for vivah.online. Claude Code picks it up automatically from `.claude/skills/`. Start at
[`SKILL.md`](.claude/skills/vivah-reel-editor/SKILL.md), then run
`bash .claude/skills/vivah-reel-editor/scripts/setup.sh`.
No API keys live in this repo: the OpenRouter key comes from the `OPENROUTER_KEY` environment
variable, and every paid call needs Sandeep's approval first.
