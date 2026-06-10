# Working Notes

## Learner profile
- Same learner as `../playing-chords-blindly/` — read that workspace's NOTES and
  learning records before planning anything here.
- Commands: chord construction, inversions, common tones/glued fingers, parallel
  5th/8ve detection, leading-tone resolution, his own fingering rule
  (3-and-5 within a third; thumb takes any fourth; pinky-side fourth → middle
  note on finger 2). Plays I–V–vi–IV blind, both hands, B3–A4 box.
- He corrects teachers precisely and is right about it. Verify, then adopt.
  Third confirmed correction 2026-06-12: lesson 1's "glue two" overpromised
  glued FINGERS when the move only guarantees held KEYS (see learning-record
  0002 here). Renamed moves to hold two / hold one; "glue" is reserved for
  key+finger per the glossary. NEVER describe a move as gluing fingers —
  fingers come from the second pass (his fingering rule), and his ergonomic
  constraints (3–5 spans ≤ a 3rd) are hard constraints.

## Teaching stance for THIS workspace
- The skill is a *decision procedure*, so the feedback loop is
  **classify → derive → play → verify**: name the move before touching the keys,
  predict the shape, play it, check against the rules. (The prior workspace's
  eyes-closed loop is NOT the loop here — sight is fine; hesitation is the enemy.)
- Efficiency is a first-class goal: drill classification speed (root letters off
  a chart), not just correctness.
- ONE thing per lesson. Novelty budget goes to selection rules only — shapes,
  box, and fingering are reused from the prior workspace.

## Canonical worked example (lesson 1 — don't re-pick)
'50s progression C–Am–F–G ("Stand by Me changes"), key of C:
  RH (B3–A4 box):  C = C4·E4·G4 (1·3·5) · Am = C4·E4·A4 (1·2·5) ·
                   F = C4·F4·A4 (1·3·5) · G = B3·D4·G4 (1·2·5)
  LH bass roots:   C3 → A2 → F2 → G2 → C3 (every move ≤ a 4th; closes exactly)
  These are HIS four drilled shapes from the blind loop, in a new order.
  Per change: C→Am hold two (C glued on 1; E key stays, finger 3→2 = held-note-
  re-fingered, LR-0002 of prior workspace finally occurs in the wild; G→A on 5).
  Am→F hold two (C on 1, A on 5; E→F, finger 2 lifts, 3 lands).
  F→G mirror the bass (bass up a step, all three RH voices down: C→B on 1,
  F→D = 3 lifts/2 lands, A→G on 5). G→C hold one (G on 5; B→C leading tone on
  thumb; D→E = 2 lifts/3 lands).
  Verified four-voice clean: no parallel 5ths/8ves anywhere (incl. vs bass),
  root doubled throughout, leading tone resolves at G→C, loop closes on the
  exact starting voicing.

## Known issue discovered 2026-06-12 (drive lesson 2 with it)
The prior workspace's **both-hands** loop has parallel octaves AND fifths
against the bass at **G→Am** (bass G→A up a step while RH block-shifts up:
G–G4 → A–A4, G–D4 → A–E4). The 2026-06-10 re-voicing fixed RH-alone outer
voices (lesson 2 there was one hand); nobody re-checked after lesson 3 added
the bass. Told him in chat the day this workspace opened. V→vi is the textbook
exception (3rd of V up a step, double the 3rd of vi — MT21C 26.7), and the
strict answer in his box (RH C4+E4 only, doubled C as unison) drops to two
sounding RH keys — there are trade-offs to discuss, not a silent fix.
**Whether to update the drilled blind loop is HIS call.** Lesson 1 ends with a
derive-your-old-loop stretch drill that runs into exactly this wall, as the
cliffhanger into lesson 2.

## Deliberately not raised (only if he flags it)
- F→G in the '50s loop puts bass and top voice in an octave **by contrary
  motion** (F2–A4 → G2–G4). Acceptable in keyboard style and matches the
  textbook contrary-motion procedure; strict counterpoint sometimes frowns on
  it between outer voices. If he spots it, that's a great r/musictheory
  question — and evidence his eye is ahead of the curriculum.
- Parallel 4ths between upper voices (F→G has C–F → D–G... actually 4th→4th
  between RH voices 1–2 going down: C4–F4 → B3–D4 is a 4th→3rd; the up-shift
  WRONG version has them) — acceptable per MT21C 26.3; don't open the topic.

## Lesson arc (tentative)
1. ✅ The three moves — root interval → hold two / hold one / mirror the bass,
   plus the fingers second pass (added after his correction, LR-0002);
   '50s loop worked + name-the-move trainer. (lessons/0001 + reference/0001)
2. The deceptive change — V→vi as the one exception (leading tone up, doubled
   3rd); repair the old blind loop's G→Am; his decision what to adopt there.
3. Transfer — derive unseen progressions in C from charts (I–IV–vi–V,
   vi–IV–I–V, I–vi–ii–V introduces Dm), then a new key (G or F) where black
   keys join the shapes.
4. Choosing the STARTING shape — where to put the box; top-note (melody)
   considerations when comping under singing.
5. Bass inversions / slash chords (C/E, G/B) — true inversion selection in the
   bass; MT21C 26.8 is the source waiting in RESOURCES.
6. (If he wants) Taste: when pop deliberately breaks the rules — currently out
   of scope per MISSION.

## Admin
- Open lessons with: `xdg-open <path>.html`
- Glossary: promote introduced terms after he uses them in a session
  (watch for: mirror the bass, parallel trap, root interval).
- Community question still never asked (carried from prior workspace) — there's
  now a natural opening: the contrary-octave question above is genuinely
  community-worthy. Propose when it comes up, don't push.
