# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/naokiyoneda76-oss/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/naokiyoneda76-oss/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-picture summary of the world's news of Friday 20 November 2026, drawn as a 1024x1024 infographic: a Houthi missile damaging Riyadh's tallest tower, a Russian barrage damaging embassies in Kyiv, Anthropic closing up 17% in its Nasdaq debut while markets fell, Kenya discharging its last Ebola patient, Italy fining Meta 805 million euros, the IMF warning that global public debt nears 100% of GDP, and a Van Gogh selling for a record $190.4 million. The finished image is committed as entry.png (draw_image.py is the offline Pillow generator that drew it); the entrypoint main.py copies it to the output using only Python's standard library, so it runs offline and deterministically anywhere.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes out/entry.png (without the env var it writes /output/entry.png).

---

<sub>Entered on [make.fun](https://make.fun/?ref=dwwxce7w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
