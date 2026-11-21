# LUMARIS — a place that isn't there

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Gillangzx/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Gillangzx/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

An entry for make.fun's **The Poster for a Place That Isn't There**: a travel
poster for an invented destination.

## The place

LUMARIS is a lakeside town that does not exist. At dusk its lagoon glows cyan
— the water itself is the light — and one white stone arch bridge crosses it,
the town's unmistakable signature. Warm windows cluster on the far shore
beneath a dark mountain ridge, and the sky runs indigo down to an amber band
at the horizon. The poster's whole promise is that glow: a swim in lit water
as the day ends.

The picture carries exactly one piece of text, the place's name, set large in
wide-tracked serif in the empty sky. There is no tagline, no quote, no rating,
nothing else to read.

## How it runs

`render.py` draws the poster by hand with Pillow and writes `entry.png`
(1024×1024, PNG). `main.ts` (Node 22, standard library only) copies that
committed image to the output directory, so the judge sees exactly the bytes
in this repository:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
```

## License

MIT — see LICENSE.
