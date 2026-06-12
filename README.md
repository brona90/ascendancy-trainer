# Ascendancy Trainer

**Live site: https://brona90.github.io/ascendancy-trainer/**

A standalone, offline-capable practice app for learning **"Ascendancy"
by Trivium** on guitar — drop D setup, gallop picking, riff vocabulary,
the D minor scale map, harmonized twin leads, lead techniques, and a
song roadmap + daily routine for assembling the real thing. Built as a
Progressive Web App so it installs from Safari to the iOS home screen
and runs without a network.

Black, blood-red, and grey theme; light practice-paper cards with an
artsy blood-drip top edge. Tap any card to play it back through a
Karplus-Strong synth (tuned to **drop D** — the low string sounds at
D2); the diagram dots and the matching tab notes light up in time with
the audio.

> **Note on content:** the eight skill pages are original etudes written
> for practice. The **Full song** page is different: it engraves the
> structured tab in `src/song.json` (every guitar part, with exact
> durations, rests, ties and techniques — nothing inferred) as proper
> notation so a student can learn the actual piece section by section.

## Pages

- **Drop D tuning** — ear-tuning checks, the one-finger power chord,
  and a slide drill through the song's chord positions.
- **Gallop picking** — straight 8ths → gallop → reverse gallop →
  gallop with chord punches. The song's rhythmic engine.
- **Riff vocabulary** — four original etudes in the song's dialect:
  pedal point, chromatic crawl, breakdown stabs, clean arpeggios.
- **D minor scale map** — natural minor + pentatonic in three boxes,
  remapped for drop D (the open 6th string is the root).
- **Full neck** — the same D minor across the whole fretboard, the three
  boxes joined into one; a full-neck climb, the scale on the dropped 6th
  string, and every root located.
- **Harmonized thirds** — the twin-guitar skill: one melody, both
  voices, then stacked dyads.
- **Lead toolkit** — legato cells, tremolo picking, bends/vibrato,
  and the alternate-picked run.
- **Song roadmap** — section-by-section architecture, the
  chunk→ladder→seams→assemble method, and how to work with the
  official tab.
- **Full song** — the complete piece, engraved section by section from
  `src/song.json` with every guitar part stacked like a score, tempo /
  meter / guitar-count chips, per-guitar playback and a full-band
  Together mix.
- **Daily routine** — a 30-minute lap through everything, ending
  inside the actual song.

## Build

```bash
python3 build.py
```

Outputs `index.html`, one `<slug>.html` per exercise,
`manifest.webmanifest`, `sw.js`, `icon.svg`, and `apple-touch-icon.png`
into the repo root. Every page is fully self-contained — inline CSS,
base64-embedded Fraunces font, inline SVG for every diagram and tab —
and works straight off a static host.

Requires Python 3 and ImageMagick (`magick` or `convert`) with an SVG
delegate (librsvg) to rasterise the icon. The icon is a required build
product — if it can't be rasterised, `build.py` exits non-zero.

## Install on iOS

1. Host the folder anywhere static (or GitHub Pages) and open it in
   mobile Safari.
2. Tap the share icon → **Add to Home Screen**.
3. The app installs with the ember icon, launches standalone, and works
   offline thanks to the service worker.

## Features

- **Drop D audio engine** — Karplus-Strong plucked synth; string 6
  sounds a whole step down, like your guitar should
- **Lit notes** — chord-box dots, scale-box dots, and tab numbers flash
  ember-orange as their notes sound
- **Metronome drives everything** — one bpm slider controls every
  playback; the tempo-ladder method on the roadmap page is built on it
- **Loop** — modal Loop button cycles off → ∞ → 4× → 2× and persists
- **Fullscreen modal** — click any card; ← / → or swipe to navigate
- **Print stylesheet** — tabs and diagrams print cleanly

## Layout

```
seanSong/
├── build.py                       # discovers exercises, emits the site
├── src/
│   ├── render.py                  # shared template, CSS, JS, audio synth
│   ├── fretboard.py               # chord-box and scale-box SVG (drop D names)
│   ├── tab.py                     # tab notation SVG
│   ├── songjson.py                # structured tab JSON → engraved notation (full-song page)
│   ├── song.json                  # the song's tab data, engraved by the song page
│   ├── songtab.py                 # stacked-score layout (+ legacy ASCII-tab parser)
│   ├── font_regular.b64 / font_italic.b64
│   └── exercises/
│       ├── _common.py             # shared drop-D helpers (not a page)
│       ├── tuning.py  gallop.py  riffs.py  dminor.py  fullneck.py
│       ├── harmony.py leads.py   roadmap.py song.py   routine.py
└── (built) index.html, <slug>.html × 10, manifest.webmanifest,
    sw.js, icon.svg, apple-touch-icon.png
```

## Adding an exercise

1. Drop a new file into `src/exercises/<slug>.py` exporting an
   `EXERCISE` dict (use any existing file as a template; import shared
   helpers from `_common.py`).
2. Run `python3 build.py`.
