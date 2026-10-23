# Game design before code (Roblox)

Read this when the request is a new experience or a gameplay feature: an obby, a tycoon, a combat round, a new map, enemies, a boss, a checkpoint system. It decides what gets built before any Luau is written, and what a playtest has to look for afterwards. The rules are adapted, in this plugin's words, from Scott Rogers, *Level Up! The Guide to Great Video Game Design* (3rd ed.), with Roblox's own design pages and engine defaults added. Engine values below were read from the API reference on 2026-10-23 (R-20261023-1); look them up again before you rely on them.

Roblox's design pages are worth one fetch when the user wants more depth on any of these: `https://create.roblox.com/docs/production/game-design/design-for-roblox.md`, `core-loops.md`, `onboarding.md` and `prototyping.md` in the same folder.

## 1. The one-pager comes first

For a new experience, write `docs/ONE-PAGER.md` in the user's repository and show it to them before writing gameplay code. One page, these headings:

| Heading | What goes there |
|---|---|
| Working title | A name that can change later. |
| Audience | Age range, and the Content Maturity label the experience expects (`https://create.roblox.com/docs/production/promotion/content-maturity.md`). |
| Core loop | One verb for what the player does most ("jump", "build", "fight", "trade"), then the short cycle around it (do, earn, upgrade, do again). |
| Session length | The target for one sitting. Roblox players can leave in a click and decide within minutes whether a game is for them, so the first fun moment comes early. |
| Selling points | About five things that make it worth playing. |
| Comparables | Two or three successful experiences it resembles, named. |
| Out of scope | What it will not do, so later requests can be checked against it. |

Keep it current. When a later request does not serve the core loop or contradicts "out of scope", say so in one line and let the user decide. A system the game will use fewer than three times is rarely worth building; reuse and reskin instead.

For a single feature in an existing game, skip the one-pager and write a short feature card instead (purpose, how it serves the core loop, numbers, how it will be tested).

## 2. Metrics live in one ModuleScript

Players judge distances by eye, so every gap, ledge and corridor should come from the character's numbers, and those numbers should not change once levels are built. Put them in one module (for example `ReplicatedStorage/Shared/Metrics.luau`) that both map-building code and character code read:

```luau
-- Read the current defaults from StarterPlayer before trusting these.
local Metrics = {
	WalkSpeed = 16,        -- studs/s, StarterPlayer.CharacterWalkSpeed default
	JumpHeight = 7.2,      -- studs, used when UseJumpPower is false
	JumpPower = 50,        -- used when UseJumpPower is true
	Gravity = 196.2,       -- studs/s^2, Workspace.Gravity default
	CorridorWidth = 0,     -- set from the measured character width (see below)
}
return Metrics
```

- Defaults read on 2026-10-23 from the `StarterPlayer`, `Humanoid` and `Workspace` class pages: `CharacterWalkSpeed` 16, `CharacterJumpHeight` 7.2 studs, `CharacterJumpPower` 50, `CharacterUseJumpPower` true, `CharacterMaxSlopeAngle` 89 degrees, `Workspace.Gravity` 196.2 studs/s², `Players.RespawnTime` 5 s, `SpawnLocation.Duration` (spawn ForceField) 10 s. A place may have changed any of them, so read the place's own `StarterPlayer` and `Workspace` values (Studio MCP `inspect_instance`, or the place file) and use those.
- Measure the character rather than assuming its size: in the playground, `character:GetExtentsSize()` gives height and width. Build corridors several character widths wide; first layouts always come out too cramped.
- Derive the jump numbers from the metrics, then confirm them by playtest: the longest gap a player clears at `WalkSpeed`, the highest ledge. Size obstacles a margin below those, never exactly at them.
- If the game changes movement (sprint, double jump, low gravity zones), add the new values to the same module and build the zones from them.

## 3. A playground place and owner-only debug commands

Before building real levels, make a test area: a separate place, or a `Playground` folder that is never published. It holds flat ground for movement, a row of gaps and ledges sized from the metrics, every hazard, and a spot where any enemy mix can be spawned on demand.

Debug commands (skip stage, invulnerable, grant item, grant currency, teleport to checkpoint) speed up every later test. They are also an exploit if they reach a live server:

- The server checks `player.UserId` against an owner list, never a client flag (Step 4 of the skill).
- Refuse them outside Studio unless the user explicitly wants them live: `RunService:IsStudio()` on the server, or a separate test place.
- Keep them in one module so they can be removed or audited in one place.

## 4. Enemy and encounter card

Fill one card per enemy type before scripting its AI: size, speed, health, attack and its tell, aggression range, and the role it plays. Rules:

- Speed, size and strength trade off. Small means fast and weak, big means slow and strong. Something both fast and strong feels unfair. A chaser should run slightly slower than `WalkSpeed` so retreating works.
- Every attack has a tell the player can read in time: a wind-up animation, a sound, a glow, a beam. Fast enemies pause between attacks.
- Roles, so groups are mixed rather than piled: chaser, shooter, guard (holds a spot), blocker (shield in front), flyer, bomber, patroller. Pairs that work: a blocker in front of a shooter, one big chaser with small fast ones, a guard on a door with a shooter above. Mixed groups make the player choose a target.
- Only one or two enemies attack the player at once, even in a big group. Cap simultaneous attackers in the AI, not just the total count.
- Enemies spawn out of sight or behind a spawner the player can see coming, never inside the player's reach.
- Health from hits: player health is the number of average hits they should survive times the average enemy damage; enemy health is the number of normal hits it should take.
- A boss is a readable pattern: an attack to learn, a big attack to survive, a clear vulnerable window, and shorter openings between, escalating over rounds. The arena is designed with the boss. The player lands the final hit, and a respawn should not reset the whole fight.

Introduce elements in order. Movement comes first, then one new mechanic repeated until it is understood, then a second, then both together. After that, a hazard over familiar moves, enemies alone, enemies with hazards, and finally a twist. Two or three new things per stage is plenty.

## 5. Multiplayer maps

Most Roblox experiences are multiplayer, so these matter more here than in single-player design:

- Simple, readable shapes. Team halves mirrored (or deliberately balanced) so neither side starts ahead.
- A visible middle ground between teams, and defensible points that can be seen on approach.
- Protected spawns: `SpawnLocation` per team (`TeamColor`, `Neutral` off), out of the sightlines of the enemy side, with the spawn ForceField (`Duration`) long enough that a spawning player can move before being hit. Spawn camping is the most common complaint.
- Landmarks visible from far away and at each exit, so players re-orient without a map.
- More than one route between any two key points.
- Ambient sounds that cannot be mistaken for player footsteps or weapons.

## 6. Fairness and restarts

- Death is quick and cheap: a short respawn (`Players.RespawnTime`), and nothing earned in that life is lost unless losing it is the game.
- Obby and stage checkpoints: a `SpawnLocation` or checkpoint part on flat ground, facing the direction of travel, away from hazards and enemy reach, saved the moment it is touched (server-side, per player).
- No death the player could not see coming: lethal drops look lethal, hazards look dangerous (red, spikes, fire), timing hazards run on a fixed pattern with a little leeway, and traps have a tell.
- If it looks reachable, it is reachable. Show out-of-bounds with visible walls, rocks or fences, not invisible barriers.
- Aim for challenge, never a target number of deaths. Help a struggling player by offering, not forcing: a skip after several failures, a checkpoint closer to the hard part.
- Mobile players are a large share of Roblox: check touch controls reach every action, and keep stages short enough to finish in a few minutes.

## 7. Playtest protocol

The skill's verification ladder ends with a playtest. Two parts:

**The agent's own Studio playtest** (roblox-agent-studio Step 4). Beyond "it runs", try to break it like a careless player would, using `execute_luau` on the server or client and reading `get_console_output`:

- Teleport the character backwards along the course and play stages out of order.
- Move it out of bounds, onto walls and roofs, under the map; check it is caught and respawned.
- Run past enemies to see whether they follow, get stuck, or pile up.
- Push every tuning value to its extremes (walk speed, enemy count, spawn rate) and see what breaks.
- Log each death with its position and cause to the console during the test; a list of positions is a cheap heat map of the unfair spots.

**The human playtest the reply hands over.** Give the user this checklist, because only a person can judge feel:

1. Set the questions before the session: can a new player find the goal, read the objective, finish the first stage, use the UI, on both desktop and a phone?
2. Watch a first-time player without helping. Record the screen if they agree.
3. Afterwards ask: what did you think the goal was? Where were you confused, frustrated or bored? How long did it feel? What felt unfair? Favourite and least favourite part? Would you play again?
4. Act on a problem when several players hit it. Suggestions can be ignored; the confusion behind them cannot.
