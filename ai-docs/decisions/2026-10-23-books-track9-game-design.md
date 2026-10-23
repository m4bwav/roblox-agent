# Decision: game design before code, in roblox-agent-workflow

Date: 2026-10-23. Status: accepted.

## Context

roblox-agent's skills covered code quality and verification only. A request for a new game or a gameplay feature went straight to Luau, and the checks skill said a human playtest was owed without saying what it should look for. The owner's book-learnings pass (Rogers, *Level Up!*, 3rd ed.) proposed a game-design reference for this plugin.

## Rulings

- B1. The material goes in one on-demand reference, `skills/roblox-agent-workflow/references/game-design.md`, not in a sixth skill. A new skill would add a description that every session loads; the workflow skill already triggers on "writing Luau for a Roblox game".
- B2. The new step is Step 1 of roblox-agent-workflow, and the old Steps 1 to 8 moved to 2 to 9. Design has to come before code to be any use, and nothing outside the repository's own logs cited the old step numbers (searched the sibling plugins).
- B3. Engine defaults are given as values read from the API reference on 2026-10-23, with the instruction to read the place's own `StarterPlayer` and `Workspace` values. The reference says `CharacterUseJumpPower` defaults to true; places made from current Studio templates may differ, which is why the place wins.
- B4. Character height and width are measured in the playground (`GetExtentsSize`) rather than stated, because the units page gives only 1 stud = 28 cm and no character size.
- B5. The one-pager is written for a new experience only; a single feature gets a short feature card, and bug fixes and reviews skip the step. Otherwise every small request would grow paperwork.
- B6. The checks and studio skills link the reference's playtest section rather than repeating it; roblox-agent-studio's SKILL.md sits at its 2,500-token green line, so its new line is one sentence and an older sentence was shortened to stay green.
- B7. No new script or measured check: everything here is a planning rule. The proof is eval cases (a written one-pager and a metrics module that other code requires; a playtest answer covering both the break-it pass and the human questions).

## Rejected

- Copying the book's beat chart and attack matrix in full: they suit a level-based game, and most Roblox experiences are multiplayer rounds or obbies. The encounter card and the multiplayer-map rules cover what applies.
- Stating Roblox numbers from memory: the skill's own Step 2 forbids it.

Related: [../INDEX.md](../INDEX.md)
