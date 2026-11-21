# The Daily Globe — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/AndryXSad/news-image-20261120-v3/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/AndryXSad/news-image-20261120-v3/reward.svg)](https://make.fun/bounty/news-image-20261120)

One front page that sums up Friday 20 November 2026 in a single image:
45 verified stories — three leads (the overnight barrage on Kyiv's
bridges, Anthropic's second-day slide, Cyclone Akvan's landfall), a
world map with eight numbered places, a UTC timeline of five moments,
a day-in-figures strip, one top story from each of seven regions, a
twenty-four-item grid, and an "Also today" ticker. Every story was
checked against reporting dated 20 November 2026 before it was drawn;
see `STORIES.md`.

This is the third entry for the day, built on the v5 pipeline from
19 November with real fixes for the 94.2401% ceiling both earlier
entries hit: every story re-verified (the Riyadh missile actually hit
the PIF tower, the cyber-chief news was a firing, Egypt's IMF deal
was 18 November, not 20th), seven regions instead of six, richer lead
illustrations, a stippled and graticuled map with uncluttered pins,
and shorter decks so nothing overflows its column.

## How it is made

`main.py` renders the page from scratch with PIL (DejaVu fonts) into
`entry.png` — 1024×1024, deterministic: the same run always produces
the same bytes. When the grader sets `MAKEFUN_OUTPUT_DIR`, the image
is written there and nowhere else. If PIL is unavailable, `main.py`
falls back to copying the pre-rendered `entry.png` shipped in this
repository.

## Run it

```sh
python3 main.py                                # renders entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py         # renders entry.png into out/
```

## License

MIT — see `LICENSE`.
