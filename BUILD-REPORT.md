# Build report — news-image-20261120 v3 ("The Daily Globe", 20 Nov 2026)

## What was built

Fresh implementation, written from a design description (not a copy of
the v2/v5 renderers): a single self-contained `main.py` (PIL + DejaVu)
that renders a 1024×1024 front page. Structure follows the winning
pattern seen on the live leaderboard: front-page newspaper, many
stories, date-checked, drawn illustrations, UTC timeline, per-region
grouping, day-in-figures strip.

- 45 stories: 3 leads + 8 map places + 7 regions + 24 grid + 3 ticker.
- 3 drawn lead illustrations, all redrawn for this edition: the Dnipro
  at night (bridge spans + blast burst), a falling ANT price line
  ($111.50 open → $97.17 close → $88.91 day-two close), a cyclone
  spiral over the Odisha coast with wind arrows.
- Dark world map with 16 land polygons (Greenland, Madagascar, Borneo,
  New Guinea, Sumatra, Cuba, Iceland added over v5), a seeded stipple
  ocean, a graticule, and 8 pins spread so no two circles overlap
  (minimum centre distance 18 px).
- UTC timeline (5 moments, clock times grounded in source timestamps),
  day-in-figures strip (110+, $88.91, 300,000+, 100,000).
- Faint seeded paper grain over the page (deterministic).

## What changed vs v2 — and why (the 94.2401% ceiling)

v1 and v2 scored an identical 94.2401%. Two different images landing
on the exact same rate to the millionth means both lost the same games
against the same strong house/reference images: same structural
weaknesses, not bad luck. The fixes in v3 target the judge's criteria
in order:

1. **Faithfulness (criterion 4) — v2 contained checkable errors.**
   - Riyadh: v2 said defences shot the Houthi missile down. Reporting
     on 20 Nov says the missile DAMAGED the PIF tower. Corrected.
   - Cyber chief: v2 said the White House "taps Kirsten Davies".
     The news of the day was the FIRING of Sean Cairncross, confirmed
     by Trump on Friday; Davies takes over. Corrected.
   - Egypt's $2.3bn IMF deal: announced 18 Nov, not 20 Nov. Dropped.
   - "FEMA bed bugs", "Macron hosts Harris", "Telus/BCE bid", "Trump
     asks justices over EPA grants" — carried in v2 but not verifiable
     against 20 Nov reporting. Dropped, replaced with verified items
     (Pete Rose pardon, Comancheros/'Ndrangheta sanctions, Texas
     execution, Kharkiv hospital strike, Georgia mourning, Sudan gold
     mine strike, Haiti, Nigeria, South Africa crime stats, Suneung
     cheating, Sikh plot sentencing, Meta €805m fine, GTA VI $2.3bn).
   - Date traps avoided: Venezuela–US deal, Senegal boat, Bukele third
     term, Denmark–Greenland pact, Shenzhen summit, ICJ ruling are all
     19 Nov, not 20 Nov — excluded as stories of their own (Shenzhen
     appears only as background in the Kyiv lead).
2. **Selection and breadth (criterion 2)** — seven regions instead of
   six (Oceania restored with the M5.6 New Caledonia quake); leads are
   the three most consequential genuine 20-Nov stories (Kyiv barrage,
   the AI market rout, Akvan landfall).
3. **Craft/readability (criteria 3, 5)** — v2's lead decks overflowed
   into their source lines and region headlines ran out of their boxes
   (same defect class v5 found on first render). v3 shortens every deck
   and region headline to fit, verified visually at full size and in
   map/region crops. Lead illustrations are richer (night skyline +
   blast, price line with markers, spiral + coastline + arrows).

## Verification (local, 21 Nov 2026 ~02:00 WIB)

- `python3 main.py` run twice + grader mode
  `MAKEFUN_OUTPUT_DIR=/tmp/v3_out2 python3 -P -s main.py`: byte-identical
  output every time.
  sha256 `3859615f08e0ed498f2ebd03bf6cd1caa23f8eabddd9c824bcff6b2bdc1c5105`
  (168,762 bytes).
- Dimensions 1024×1024 RGB — under the 1 MiB limit.
- Visual check of the rendered PNG: masthead, leads, map, timeline,
  figures, regions, grid, ticker and footer all legible at 1024px.
  Three defects found on first render and fixed: lead decks overflowing
  into source lines (decks shortened, deck type 12 pt), region-box
  headlines running out of their boxes (headlines shortened to two
  lines, boxes deepened to 694), and map pins clustered/overlapping in
  Europe (nudges recomputed from projected coordinates, min separation
  18 px; pins are schematic — at this scale a nudge of a few pixels is
  several degrees — but no two circles overlap and every number reads).
- All 45 stories listed with verification source and date in
  `STORIES.md`, including a "Deliberately NOT used" section.

## Repo gates

- Repo: https://github.com/AndryXSad/news-image-20261120-v3
- Commit: `90e4a0b29462f08bfd8a268cb0cf0f59244736d0` (2 commits)
- README carries the 3 live make.fun badges (competition, rank,
  reward) — both badge URLs return HTTP 200.
- About homepage: https://make.fun/bounty/news-image-20261120;
  topic: `makefun`.
- LICENSE: first push carried the SPDX line on top and GitHub's API
  returned `NOASSERTION` (same flag v5 hit). Rewrote as the canonical
  MIT text starting with "MIT License"; `gh api
  repos/AndryXSad/news-image-20261120-v3/license` now returns
  `{"license": "MIT", "name": "MIT License"}`.

## Recording note (for the coordinator)

`makefun record` does NOT apply to this competition: it refused to
start (HTTP 400 — "news-image-20261120 does not take recorded
transcripts: its entries upload their transcripts (a bundle or loose
files) as the requirements say"). This competition takes transcript
uploads with the submission instead. No recording id exists. The
builder session for the bundle is the Muse app session
`8b59421f-4b6b-4acb-ad0c-59ed78df2bd9`, stored under
`~/agents/agent-8b59421f-4b6b-4acb-ad0c-59ed78df2bd9/` — the
coordinator should bundle from that session directory. All build files
(`main.py`, `entry.png`, `STORIES.md`, `README.md`, `LICENSE`) were
written fresh by the agent in this session; nothing was copied from
the v2/v5 repositories (no clone of either was made).

## Self-judging vs the live top-50 bar

Live leaderboard, 21 Nov 2026 ~08:10 WIB: 12,603 entries. Rank 1 at
99.2057%; rank 50 (the bar) at 98.8744%; v2 sits at 94.2401%
(rank #8,210). The bar moved up from ~98.77% yesterday.

Honest estimate: v3 is strictly stronger than v2 — the factual errors
are gone, selection is broader (7 regions), and nothing overflows —
so it should score above 94.2401%. How far above is unknowable from
here: the provisional rate is measured against fixed house images, and
the jump from 94% to 98.9% means winning games v2 lost, most of them
against the strongest reference images. The remaining gap is craft:
v3 is still a flat drawn-only page (168 KB) while the top entries run
286–743 KB with visibly richer rendering, and the map is still a
coarse hand-drawn outline with schematic pins. I estimate v3 lands
roughly in the 95–97% range — better than v2, plausibly in the top
few thousand, but NOT plausibly clearing the 98.8744% top-50 bar.
The one thing I cannot verify locally is how the judge weighs the
corrected facts; if the judge's reference images are weak on
faithfulness, the correction alone could be worth more than my
estimate. But on the evidence I have, top-50 is unlikely.

## Submission status

NOT SUBMITTED. The coordinator decides. One slot remains (day cap 3,
2 entries made). Recommendation: **submit** — the slot is the last
one, the entry is strictly better than both live entries, the deadline
is 22 Nov 07:00 WIB, and there is no further build iteration planned
that could use the slot better. The honest expectation is a better
provisional rate than 94.2401%, not a prize. If the coordinator would
rather hold the slot for a different approach (e.g. a richer rendered
image), that is a legitimate call — but no such build exists today.
