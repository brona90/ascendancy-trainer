"""Shared HTML template + glue.

`build_page(ex)` takes an exercise dict and writes <slug>.html.
`build_index(exs)` writes the landing index.html.
"""

import base64
import html
import json
import os
import time


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.dirname(os.path.abspath(__file__))


# ─────────────────────────────────────────────────────────────────────────────
# Icon
# ─────────────────────────────────────────────────────────────────────────────

ICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2a0709"/>
      <stop offset="1" stop-color="#070608"/>
    </linearGradient>
    <radialGradient id="hot" cx="50%" cy="42%" r="48%">
      <stop offset="0" stop-color="rgba(199,30,42,0.22)"/>
      <stop offset="100%" stop-color="rgba(199,30,42,0)"/>
    </radialGradient>
    <radialGradient id="ember" cx="35%" cy="32%" r="80%">
      <stop offset="0" stop-color="#ffe9d6"/>
      <stop offset="0.35" stop-color="#c81e2a"/>
      <stop offset="0.78" stop-color="#dc2626"/>
      <stop offset="1" stop-color="#5f0f0a"/>
    </radialGradient>
    <radialGradient id="emberRing" cx="50%" cy="50%" r="50%">
      <stop offset="0.7" stop-color="rgba(199,30,42,0)"/>
      <stop offset="0.92" stop-color="rgba(199,30,42,0.55)"/>
      <stop offset="1" stop-color="rgba(199,30,42,0)"/>
    </radialGradient>
  </defs>
  <!-- Rounded blackened background -->
  <rect width="180" height="180" rx="36" fill="url(#bg)"/>
  <!-- Top heat glow -->
  <rect width="180" height="180" rx="36" fill="url(#hot)"/>
  <!-- Vertical strings — the leftmost is the dropped D -->
  <g stroke="rgba(244,200,180,0.42)" stroke-linecap="round">
    <line x1="40" y1="36" x2="40" y2="160" stroke-width="2.0"/>
    <line x1="64" y1="36" x2="64" y2="160" stroke-width="1.6"/>
    <line x1="88" y1="36" x2="88" y2="160" stroke-width="1.3"/>
    <line x1="112" y1="36" x2="112" y2="160" stroke-width="1.1"/>
    <line x1="136" y1="36" x2="136" y2="160" stroke-width="0.9"/>
  </g>
  <!-- Horizontal frets -->
  <g stroke="rgba(248,113,113,0.20)" stroke-width="1">
    <line x1="32" y1="56" x2="148" y2="56"/>
    <line x1="32" y1="84" x2="148" y2="84"/>
    <line x1="32" y1="112" x2="148" y2="112"/>
    <line x1="32" y1="140" x2="148" y2="140"/>
  </g>
  <!-- Muted power-chord dots -->
  <g fill="#9a6555">
    <circle cx="64" cy="98" r="5.5"/>
    <circle cx="88" cy="98" r="5.5"/>
    <circle cx="112" cy="71" r="5.5"/>
  </g>
  <!-- HERO: the open dropped-D string, molten with glow ring -->
  <circle cx="40" cy="98" r="30" fill="url(#emberRing)"/>
  <circle cx="40" cy="98" r="19" fill="url(#ember)" stroke="#ffd9b8" stroke-width="0.8"/>
  <!-- Eyebrow -->
  <text x="90" y="22" font-family="Georgia, serif" font-style="italic" font-weight="600"
        font-size="11" fill="#e8c4b0" text-anchor="middle" letter-spacing="3.5">DROP D</text>
  <!-- Lower label -->
  <text x="90" y="172" font-family="Georgia, serif" font-style="italic" font-weight="700"
        font-size="13" fill="#c81e2a" text-anchor="middle" letter-spacing="2">ASCENDANCY</text>
</svg>'''

ICON_DATA_URI = 'data:image/svg+xml;base64,' + base64.b64encode(ICON_SVG.encode()).decode()


# fosterthecode brand icon (from ftc-icon.svg) — inlined verbatim so the page
# stays offline-self-contained. Its colours are intentionally left untouched
# (the brand green) even though the site theme is black + blood red.
FTC_ICON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="26" height="26" aria-hidden="true">
  <rect width="200" height="200" rx="40" fill="#0A1A0E"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#1a3320" stroke-width="1.5"/>
  <circle cx="100" cy="100" r="68" fill="none" stroke="#1a3320" stroke-width="1.5"/>
  <circle cx="100" cy="100" r="48" fill="none" stroke="#1a3320" stroke-width="1.5"/>
  <g transform="translate(62, 14)">
    <polygon points="34,10 10,62 58,62" fill="#22C55E"/>
    <polygon points="34,36 6,90 62,90" fill="#16A34A"/>
    <polygon points="34,62 2,122 66,122" fill="#15803D"/>
    <rect x="28" y="122" width="11" height="28" rx="2" fill="#22C55E" opacity="0.7"/>
    <text x="19" y="108" font-family="'Courier New', monospace" font-size="17" fill="#86EFAC" opacity="0.95" font-weight="700">&lt;/&gt;</text>
  </g>
</svg>'''


# Blood-drip card decoration. A repeating tile (drips of varying length hanging
# off a top band) rendered as an SVG data URI so it ships inline/offline. Baked
# in deep blood red to match the theme; tiled along each card's top edge in CSS.
DRIP_TILE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="220" height="70" viewBox="0 0 220 70">
  <defs>
    <linearGradient id="bd" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#9e0b14"/>
      <stop offset="0.5" stop-color="#7a0a11"/>
      <stop offset="1" stop-color="#48060a"/>
    </linearGradient>
  </defs>
  <!-- top smear with an uneven, pooled lower edge -->
  <path fill="url(#bd)" d="M0 0 H220 V9 C205 13 192 8 178 11 C162 14 150 7 132 10
    C112 13 96 8 82 12 C64 16 50 8 36 11 C22 14 11 8 0 10 Z"/>
  <!-- drips of varying length and girth, with bulbous, gravity-heavy tips -->
  <g fill="url(#bd)">
    <path d="M22 9 C19 28 17 41 21 49 C23 53 29 53 31 49 C35 41 33 28 30 9 Z"/>
    <path d="M78 10 C76 19 75 25 79 30 C81 33 85 33 87 30 C91 25 90 19 88 10 Z"/>
    <path d="M132 9 C129 34 127 52 132 61 C134 65 140 65 142 61 C147 52 145 34 142 9 Z"/>
    <path d="M186 10 C184 21 183 28 187 34 C189 37 193 37 195 34 C199 28 198 21 196 10 Z"/>
  </g>
  <!-- detached falling droplets (teardrops, point up) -->
  <g fill="#7a0a11">
    <path d="M137 64 C134 67 134 70 137 70 C140 70 140 67 137 64 Z"/>
    <path d="M58 30 C56 32 56 34 58 34 C60 34 60 32 58 30 Z"/>
  </g>
  <!-- wet specular highlights -->
  <g fill="#d8565b" opacity="0.4">
    <ellipse cx="25" cy="24" rx="1.8" ry="8"/>
    <ellipse cx="136" cy="30" rx="2" ry="12"/>
    <ellipse cx="189" cy="20" rx="1.5" ry="6"/>
    <ellipse cx="81" cy="18" rx="1.4" ry="5"/>
  </g>
</svg>'''
DRIP_DATA_URI = 'data:image/svg+xml;base64,' + base64.b64encode(DRIP_TILE_SVG.encode()).decode()


def _site_footer():
    """Small 'built by fosterthecode' mark for the bottom of every page.

    The icon keeps its own brand colours (green) on purpose — the rest of the
    site is black + blood red, but this is a credit, not a themed element.
    """
    return (
        '<footer class="site-footer">'
        + FTC_ICON_SVG
        + '<span>built by <strong>fosterthecode</strong></span>'
        + '</footer>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Fonts (Fraunces variable font, woff2 base64-embedded)
# ─────────────────────────────────────────────────────────────────────────────

def _read_font(name):
    p = os.path.join(SRC, name)
    if os.path.exists(p):
        return open(p, encoding='utf-8').read().strip()
    return ''

FONT_REGULAR = _read_font('font_regular.b64')
FONT_ITALIC = _read_font('font_italic.b64')
# UnifrakturCook 700 — a blackletter display face for the titles and section
# headings, so the site reads like a metal record sleeve rather than a generic
# serif. Body, captions, pills and tab stay in Fraunces for legibility.
FONT_BLACKLETTER = _read_font('font_blackletter.b64')


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

PAGE_CSS = r'''
@font-face {
  font-family: 'Fraunces';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url(data:font/woff2;base64,__FONT_REGULAR__) format('woff2');
}
@font-face {
  font-family: 'Fraunces';
  font-style: italic;
  font-weight: 100 900;
  font-display: swap;
  src: url(data:font/woff2;base64,__FONT_ITALIC__) format('woff2');
}
@font-face {
  font-family: 'Blackletter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(data:font/woff2;base64,__FONT_BLACKLETTER__) format('woff2');
}
:root {
  /* Black + blood-red + grey. Light "paper" cards carry the notation. */
  --paper: #0b0b0d;             /* near-black */
  --paper-warm: #18181b;        /* dark grey panel */
  --ink: #ededee;               /* near-white */
  --ink-soft: #b6b5b8;          /* light grey */
  --sepia: #8a898d;             /* mid grey — muted text */
  --line: rgba(190, 30, 40, 0.22);   /* blood-red hairline */
  --card: #f2f1ef;              /* cool off-white — practice paper */
  --card-edge: rgba(20, 20, 23, 0.25);
  --card-ink: #1b1b1d;          /* near-black ink */
  --card-ink-soft: #5f5f64;     /* grey */
  --card-sepia: #8a8a8e;        /* grey */
  --card-line: rgba(20, 20, 23, 0.16);
  /* Blood-red accents for borders, numbers, structure */
  --accent: #d22730;            /* blood red */
  --accent-dark: #8f1219;       /* deep blood red */
  /* Em / "lit" highlight — blood red (was molten orange) */
  --sage: #cc2630;
  --sage-dark: #7e0d13;
}
* { box-sizing: border-box; }
html {
  background: var(--paper); scroll-behavior: smooth; scroll-padding-top: 5rem;
  /* Don't let iOS inflate fonts on rotation to landscape. */
  -webkit-text-size-adjust: 100%; text-size-adjust: 100%;
}
/* Touch basics: no grey tap flash, and `manipulation` removes the
   double-tap-to-zoom gesture on tappables — rapid play/stop taps during
   practice must never zoom the page. */
button, a, .card, input[type=range] {
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
input[type=range] { accent-color: var(--accent-dark); }
body {
  margin: 0;
  background:
    radial-gradient(ellipse 90% 55% at 50% 0%, rgba(199, 30, 42, 0.08), transparent 75%),
    radial-gradient(ellipse 70% 50% at 15% 100%, rgba(214, 64, 74, 0.10), transparent 65%),
    var(--paper);
  color: var(--ink);
  font-family: 'Fraunces', 'Iowan Old Style', Charter, Georgia, 'Times New Roman', serif;
  font-variation-settings: 'opsz' 14, 'SOFT' 20, 'WONK' 0;
  font-weight: 400;
  line-height: 1.6;
  min-height: 100vh;
  -webkit-text-size-adjust: 100%;
}
.page {
  max-width: 1180px; margin: 0 auto;
  /* Respect the iPhone notch / Dynamic Island and the home indicator
     (viewport-fit=cover lets content draw into these regions). */
  padding:
    calc(1.25rem + env(safe-area-inset-top)) calc(1.5rem + env(safe-area-inset-right))
    calc(5rem + env(safe-area-inset-bottom)) calc(1.5rem + env(safe-area-inset-left));
}

.topbar {
  display: flex; justify-content: space-between; align-items: center;
  gap: 1rem; margin-bottom: 2rem; padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(248, 113, 113, 0.12);
}
.home-link {
  font-variation-settings: 'opsz' 14, 'wght' 500;
  color: var(--accent-dark); text-decoration: none;
  font-size: 0.92rem; letter-spacing: 0.02em;
}
.home-link:hover { color: var(--accent); }
.ex-switch { display: flex; align-items: center; gap: 0.6rem; }
.ex-switch-label {
  font-variation-settings: 'opsz' 9, 'wght' 500;
  text-transform: uppercase; letter-spacing: 0.3em;
  font-size: 0.65rem; color: var(--sepia);
}
.ex-switch select {
  font-family: inherit; font-size: 0.92rem;
  font-variation-settings: 'opsz' 14, 'wght' 500;
  padding: 0.35rem 0.6rem; background: var(--card);
  border: 1px solid rgba(185, 28, 28, 0.4); border-radius: 4px;
  color: var(--card-ink); cursor: pointer;
}

.title-block {
  text-align: center; margin-bottom: 3rem; padding-bottom: 2.5rem;
  border-bottom: 1px solid var(--line);
}
.title-block .eyebrow {
  font-variation-settings: 'opsz' 9, 'wght' 500;
  text-transform: uppercase; letter-spacing: 0.4em; font-size: 0.72rem;
  color: var(--accent); margin: 0 0 1.25rem; padding-left: 0.4em;
}
.title-block h1 {
  font-family: 'Blackletter', 'Fraunces', serif; font-weight: 700;
  font-size: clamp(2.7rem, 9.5vw, 5.6rem); line-height: 1.02;
  letter-spacing: 0; margin: 0; color: var(--ink);
}
.title-block h1 em {
  font-style: normal; color: var(--sage);
  text-shadow: 0 0 30px rgba(199, 30, 42, 0.25);
}
.title-block .subtitle {
  font-style: italic;
  font-variation-settings: 'opsz' 18, 'wght' 400;
  color: var(--sepia); font-size: 1.15rem;
  margin: 1rem auto 0; max-width: 38ch;
}

.legend { display: grid; grid-template-columns: 1.4fr 1fr; gap: 2.5rem;
  align-items: start; margin-bottom: 2.5rem;
}
.legend.no-pills { grid-template-columns: 1fr; }
.legend-prose p { margin: 0 0 0.8rem; color: var(--ink-soft); max-width: 58ch; }
.legend-prose p:last-child { margin-bottom: 0; }
.legend-prose strong { font-variation-settings: 'opsz' 14, 'wght' 600; color: var(--ink); }
.legend-prose em { color: var(--sage); font-style: italic; }
.pills { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.pills .pill {
  background: var(--paper-warm); padding: 0.85rem 1rem;
  border-radius: 4px; border-top: 2px solid var(--accent);
}
.pills .pill h3 {
  font-variation-settings: 'opsz' 24, 'wght' 600, 'WONK' 1;
  font-style: italic; font-size: 1.05rem; margin: 0 0 0.15rem;
  color: var(--accent-dark);
}
.pills .pill p { margin: 0; font-size: 0.85rem; color: var(--ink-soft); line-height: 1.4; }
@media (max-width: 720px) {
  .legend { grid-template-columns: 1fr; gap: 1.5rem; }
}
@media (max-width: 480px) {
  .pills { grid-template-columns: 1fr; }
}

.cards {
  display: grid; gap: 1.25rem;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  margin: 0 0 2.5rem;
}
.cards.wide { grid-template-columns: repeat(auto-fill, minmax(520px, 1fr)); }
.cards.full { grid-template-columns: 1fr; }
/* A 520px minimum overflows phone viewports — collapse wide grids there. */
@media (max-width: 600px) {
  .cards.wide { grid-template-columns: 1fr; }
}
.card {
  background:
    /* Subtle "spot-lit from above" highlight at the top */
    radial-gradient(ellipse 80% 45% at 50% 0%, rgba(255, 255, 255, 0.55), transparent 70%),
    /* Slight warm-cream gradient body */
    linear-gradient(160deg, #fbfbfa 0%, var(--card) 35%, #ececeb 100%);
  color: var(--card-ink);
  padding: 1.5rem 1.3rem 1.2rem; border-radius: 10px;
  border: 1px solid var(--card-edge);
  box-shadow:
    /* tight inner-top highlight */
    0 1px 0 rgba(255, 255, 255, 0.7) inset,
    /* tight inner-bottom shadow for depth */
    0 -1px 0 rgba(0, 0, 0, 0.05) inset,
    /* contact shadow */
    0 1px 2px rgba(8, 8, 10, 0.35),
    /* lifted shadow with blue tint */
    0 12px 28px -6px rgba(8, 8, 10, 0.6),
    /* glow halo, gold-tinted */
    0 0 0 1px rgba(199, 30, 42, 0.04);
  cursor: pointer;
  transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 220ms cubic-bezier(0.22, 1, 0.36, 1);
  display: flex; flex-direction: column;
  position: relative;
  isolation: isolate;
}
/* Artsy blood drip hanging off the top edge */
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 70px;
  background-image: url("__DRIP_URI__");
  background-repeat: repeat-x;
  background-position: left top;
  background-size: 220px 70px;
  border-radius: 10px 10px 0 0;   /* match the card's top corners */
  opacity: 0.72;
  pointer-events: none;
  transition: opacity 220ms ease;
}
/* Inner border highlight (just inside the cream edge) */
.card::after {
  content: '';
  position: absolute;
  inset: 4px;
  border-radius: 7px;
  border: 1px solid rgba(20, 20, 23, 0.04);
  pointer-events: none;
  z-index: 0;
}
.card > * { position: relative; z-index: 1; }
/* Hover lift only on devices that actually hover — on touch it just makes
   taps feel sticky (the :hover state lingers after the finger leaves). */
@media (hover: hover) {
  .card:hover {
    transform: translateY(-4px);
    box-shadow:
      0 1px 0 rgba(255, 255, 255, 0.8) inset,
      0 -1px 0 rgba(0, 0, 0, 0.06) inset,
      0 2px 4px rgba(8, 8, 10, 0.4),
      0 22px 44px -8px rgba(8, 8, 10, 0.7),
      0 0 36px -6px rgba(199, 30, 42, 0.22),
      0 0 0 1px rgba(199, 30, 42, 0.1);
  }
  .card:hover::before { opacity: 0.82; }
}
/* Touch feedback instead: a quick press-down. */
@media (hover: none) {
  .card:active { transform: scale(0.988); }
}
.card:focus-visible { outline: 2px solid var(--sage); outline-offset: 4px; }
.card .key-num {
  font-style: italic;
  color: var(--accent-dark);
  font-size: 0.7rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-variation-settings: 'opsz' 9, 'wght' 600, 'WONK' 1;
  margin-bottom: 0.4rem;
  display: inline-block;
  font-style: normal;
}
.card .key-num::after {
  content: '';
  display: inline-block;
  vertical-align: middle;
  width: 1.4rem;
  height: 1px;
  background: var(--accent-dark);
  margin-left: 0.5rem;
  opacity: 0.4;
}
.card h3 {
  margin: 0.1rem 0 0.4rem;
  font-size: 1.25rem;
  font-variation-settings: 'opsz' 32, 'wght' 600, 'SOFT' 30;
  color: var(--card-ink);
  line-height: 1.2;
  letter-spacing: -0.005em;
}
.card .role {
  font-size: 0.88rem;
  color: var(--card-ink-soft);
  font-style: italic;
  margin: 0 0 0.8rem;
  font-variation-settings: 'opsz' 18, 'wght' 400;
}
.card svg { color: var(--card-ink); width: 100%; height: auto; display: block; }
.card svg.chord-box { max-width: 240px; margin: 0 auto; }

/* Tab-note "lit" — fires when the playhead reaches this note. */
.tab-note rect, .tab-note text {
  transition: fill 80ms ease;
}
.tab-note.lit text { fill: var(--sage-dark); font-weight: 800; }
.tab-note.lit rect { fill: rgba(199, 30, 42, 0.32); }
.tab-note.lit { filter: drop-shadow(0 0 6px var(--sage)); }

/* Fret-dot "lit" animation — fires whenever the app plays that note. */
.fret-dot {
  transform-box: fill-box;
  transform-origin: center;
  transition: filter 80ms ease;
}
.fret-dot.lit {
  animation: fret-pulse 0.7s cubic-bezier(0.22, 1, 0.36, 1);
}
.fret-dot.lit:not(.root-dot):not(.open-dot) {
  fill: var(--sage) !important;
}
.fret-dot.lit.root-dot {
  fill: var(--sage) !important;
}
.fret-dot.lit.open-dot {
  stroke: var(--sage) !important;
  stroke-width: 2.6 !important;
  fill: var(--sage) !important;
  fill-opacity: 0.35;
}
@keyframes fret-pulse {
  0%   { transform: scale(1);    filter: drop-shadow(0 0 0 transparent); }
  18%  { transform: scale(1.42); filter: drop-shadow(0 0 8px var(--sage)) drop-shadow(0 0 16px var(--sage)); }
  60%  { transform: scale(1.1);  filter: drop-shadow(0 0 4px var(--sage)); }
  100% { transform: scale(1);    filter: drop-shadow(0 0 0 transparent); }
}

/* Chord strip — small chord diagrams in line above tab charts.
   Items have a FIXED width so every diagram renders identical size, no matter
   how long the label text is. */
.chord-strip {
  display: flex; gap: 1.25rem; justify-content: center; align-items: flex-start;
  margin: 0.5rem auto 1.25rem; flex-wrap: wrap;
}
.chord-strip-item {
  text-align: center;
  flex: 0 0 140px;     /* fixed flex-basis = uniform width */
  width: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.chord-strip-label {
  font-style: italic;
  color: var(--accent-dark);
  font-variation-settings: 'opsz' 18, 'wght' 600, 'WONK' 1;
  margin: 0 0 0.4rem;
  font-size: 0.9rem;
  letter-spacing: 0.005em;
  line-height: 1.25;
  min-height: 2.5em;
  display: flex; align-items: flex-end; justify-content: center;
  text-align: center;
  padding-bottom: 0.15rem;
  border-bottom: 1px solid rgba(185, 28, 28, 0.15);
  width: 100%;
}
.chord-strip svg.chord-box {
  width: 130px;
  height: auto;
  display: block;
  max-width: 130px;
}

/* Slash chart — 12-bar form, fully responsive */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  margin: 1.5rem 0 0.75rem;
  border-top: 1.4px solid var(--card-ink);
  border-bottom: 1.4px solid var(--card-ink);
  border-right: 1.4px solid var(--card-ink);   /* right edge of the staff */
}
.chart-bar {
  border-left: 1.4px solid var(--card-ink);
  padding: 1.1rem 0.5rem 0.85rem;
  position: relative;
  text-align: center;
  min-height: 82px;
  display: flex; flex-direction: column; justify-content: center;
  transition: background 120ms ease;
  background-clip: padding-box;
}
.chart-bar:hover { background: rgba(185, 28, 28, 0.04); }
/* Final-bar decoration: a thick line tucked just inside the right edge of the
   last cell to mark "end of form" (the standard "thin + thick" final bar). */
.chart-bar-last { padding-right: 0.85rem; }
.chart-bar-last::after {
  content: '';
  position: absolute;
  top: 0; bottom: 0; right: 3px;
  width: 3px;
  background: var(--card-ink);
  pointer-events: none;
}
.chart-bar-num {
  position: absolute; top: 4px; left: 7px;
  font-size: 0.6rem; opacity: 0.42;
  font-style: italic;
  font-variation-settings: 'opsz' 9, 'wght' 500;
}
.chart-chord {
  display: block;
  font-size: 1.55rem;
  font-variation-settings: 'opsz' 48, 'wght' 600, 'SOFT' 40;
  color: var(--card-ink);
  line-height: 1.05;
  margin-bottom: 0.3rem;
  letter-spacing: -0.01em;
}
.chart-slashes {
  display: block;
  font-style: italic;
  opacity: 0.3;
  font-size: 1rem;
  letter-spacing: 0.5em;
  padding-left: 0.5em;
  color: var(--accent-dark);
}
@media (max-width: 640px) {
  .chart-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 380px) {
  .chart-grid { grid-template-columns: 1fr; }
  .chart-bar { min-height: 60px; }
}

/* Tab SVGs — allow horizontal scroll on narrow screens so they stay readable */
.card .tab-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0 -1rem;     /* let the scroll area reach card edges */
  padding: 0 1rem;
  min-width: 0;        /* CRITICAL: allow flex item to shrink below content */
  max-width: 100%;
  width: 100%;
}
.card .tab-scroll svg.tab,
.card .tab-scroll svg.tab-rich {
  min-width: 580px;    /* below this the notation is unreadable */
}
.card .tab-scroll::-webkit-scrollbar { height: 6px; }
.card .tab-scroll::-webkit-scrollbar-thumb { background: rgba(124, 27, 18, 0.25); border-radius: 3px; }
.card .tab-scroll::after {
  content: '';
  display: block;
  pointer-events: none;
}
/* Subtle scroll hint on narrow screens (exercise tabs still scroll;
   song-page bar columns wrap instead and need no hint). */
@media (max-width: 720px) {
  .card .tab-scroll {
    background:
      linear-gradient(to right, var(--card) 30%, transparent),
      linear-gradient(to right, transparent, var(--card) 70%) right,
      radial-gradient(farthest-side at left, rgba(199,30,42,0.15), transparent),
      radial-gradient(farthest-side at right, rgba(199,30,42,0.15), transparent) right;
    background-repeat: no-repeat;
    background-size: 28px 100%, 28px 100%, 14px 100%, 14px 100%;
    background-attachment: local, local, scroll, scroll;
  }
  .song-bar .tab-scroll { background: none; }
}

/* Also let chord-strip + cards shrink properly inside the page */
.card { min-width: 0; }
.chord-strip { min-width: 0; max-width: 100%; }
.card .caption { margin-top: 0.6rem; font-size: 0.85rem; color: var(--card-ink-soft); }
.card .caption em { color: var(--accent-dark); font-style: italic; font-weight: 600; }
.card .caption strong { color: var(--card-ink); font-variation-settings: 'opsz' 14, 'wght' 600; }

/* Play button on cards */
.card-play {
  position: absolute; top: 0.85rem; right: 0.85rem;
  width: 34px; height: 34px; border-radius: 17px;
  background: linear-gradient(135deg, var(--accent-dark), #7f1d1d);
  color: var(--card);
  border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem; line-height: 1;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.18) inset,
    0 2px 6px rgba(0, 0, 0, 0.28),
    0 0 0 2px rgba(185, 28, 28, 0.18);
  z-index: 2;
  transition: transform 140ms ease, box-shadow 140ms ease, background 140ms ease;
}
/* Finger-sized on touch screens (44px is the floor for comfortable taps). */
@media (pointer: coarse) {
  .card-play { width: 44px; height: 44px; border-radius: 22px; font-size: 1.1rem; }
}
.card-play:hover {
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  color: var(--paper);
  transform: scale(1.1);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.3) inset,
    0 4px 14px rgba(185, 28, 28, 0.5),
    0 0 0 3px rgba(214, 64, 74, 0.28);
}
.card-play.playing {
  background: linear-gradient(135deg, var(--sage), var(--sage-dark));
  color: var(--paper);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.25) inset,
    0 2px 10px rgba(140, 14, 20, 0.5),
    0 0 0 3px rgba(199, 30, 42, 0.28);
}
.card-play.playing::before { content: '■'; font-size: 0.78rem; }
.card-play:not(.playing)::before { content: '▶'; padding-left: 2px; }

.section-heading {
  margin: 3rem 0 0.85rem;
  font-family: 'Blackletter', 'Fraunces', serif; font-weight: 700;
  font-size: clamp(1.7rem, 3.4vw, 2.2rem);
  color: var(--ink);
  letter-spacing: 0;
  line-height: 1.15;
  position: relative;
  padding-left: 0.95rem;
}
.section-heading::before {
  content: '';
  position: absolute;
  left: 0; top: 0.5em; bottom: 0.35em;
  width: 3px;
  background: linear-gradient(180deg, var(--accent), var(--sage));
  border-radius: 2px;
}
.section-heading em {
  color: var(--sage); font-style: normal;
}
.section-blurb {
  color: var(--ink-soft); max-width: 62ch; margin: 0 0 1.75rem;
  padding-left: 0.95rem;
}
.section-blurb em { color: var(--sage); font-style: italic; }
.section-blurb strong { color: var(--ink); font-variation-settings: 'opsz' 14, 'wght' 600; }

.next-step {
  background: var(--paper-warm); padding: 2rem 1.75rem;
  border-radius: 6px; border-left: 3px solid var(--sage);
  margin: 3rem 0 0;
}
.next-step h2 {
  margin: 0 0 0.75rem; font-size: 1.7rem;
  font-family: 'Blackletter', 'Fraunces', serif; font-weight: 700;
  line-height: 1.15; color: var(--ink);
}
.next-step h2 em { color: var(--sage); font-style: normal; }
.next-step p { margin: 0 0 0.8rem; color: var(--ink-soft); }
.next-step p em { color: var(--sage); font-style: italic; }
.next-step p strong { color: var(--ink); font-variation-settings: 'opsz' 14, 'wght' 600; }
.next-step ul { margin: 0; padding-left: 1.2rem; color: var(--ink-soft); }
.next-step li { margin: 0.35rem 0; }
.next-step li strong { color: var(--accent); font-variation-settings: 'opsz' 14, 'wght' 600; }
.next-step li em { color: var(--sage); font-style: italic; }

.closing {
  text-align: center; margin: 3rem 0 0;
  font-style: italic; color: var(--sepia); font-size: 1.1rem;
}

/* Cross-link footer between exercises */
.ex-footer {
  display: flex; justify-content: space-between; gap: 1rem;
  margin: 3rem 0 0; padding-top: 1.5rem;
  border-top: 1px solid var(--line);
  font-size: 0.95rem;
}
.ex-footer a {
  color: var(--accent); text-decoration: none;
  font-variation-settings: 'opsz' 14, 'wght' 500;
}
.ex-footer a:hover { color: var(--sage); }
.ex-footer .ef-prev::before { content: '← '; opacity: 0.6; }
.ex-footer .ef-next::after { content: ' →'; opacity: 0.6; }
.ex-footer span.disabled { opacity: 0.3; color: var(--ink-soft); }

/* ── Fullscreen modal ─────────────────────────── */
.modal-backdrop {
  position: fixed; inset: 0; z-index: 50;
  background: rgba(8, 8, 10, 0.86);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: none; align-items: center; justify-content: center;
  /* pan-y lets a tall modal body scroll vertically on iOS while we still
     handle horizontal swipes for card navigation in JS. */
  touch-action: pan-y;
}
.modal-backdrop.open { display: flex; }
.modal-frame {
  background: var(--card); color: var(--card-ink);
  width: min(94vw, 1200px); max-height: 94vh;
  border-radius: 8px; padding: 2rem 2rem 1.5rem; position: relative;
  display: flex; flex-direction: column; overflow: auto;
}
.modal-frame svg { color: var(--card-ink); max-width: 100%; height: auto; }

/* Modal sizing — the modal IS the fullscreen experience. Make it feel
   appropriately big. Chord diagrams roughly double their card size; charts
   take the whole frame and the chord names grow a lot. */
#modal-body { margin: 0 auto; }
/* Standalone chord-shape diagram: ~470px wide (~2× card size). */
#modal-body > svg.fretboard.chord-box { max-width: 470px; margin: 0.75rem auto 0; }
/* Diagrams used in a chord-strip beside a chart/tab: about 1.5× card size. */
#modal-body .chord-strip { gap: 2rem; }
#modal-body .chord-strip svg.chord-box { width: 200px; max-width: 200px; }
#modal-body .chord-strip-item { flex: 0 0 220px; width: 220px; }
#modal-body .chord-strip-label { font-size: 1.05rem; }
/* Chart — full frame width, big chord names. */
#modal-body .chart-grid { margin-top: 2.25rem; }
#modal-body .chart-bar { min-height: 140px; padding: 1.6rem 0.6rem 1.2rem; }
#modal-body .chart-chord { font-size: clamp(2rem, 4vw, 2.6rem); }
#modal-body .chart-slashes { font-size: 1.3rem; letter-spacing: 0.6em; }
#modal-body .chart-bar-num { font-size: 0.78rem; top: 8px; left: 10px; }
/* Scale-box / tab — let them use more width and height. */
#modal-body svg.scale-box, #modal-body svg.tab, #modal-body svg.tab-rich {
  max-width: 100%; width: 100%;
}
/* …but song-page bar columns keep their own width — stretching every
   one-bar SVG to the frame would wreck the wrapped-score layout. */
#modal-body .song-bar svg.tab, #modal-body .song-bar svg.tab-rich {
  width: auto; max-width: 100%;
}
#modal-body .tab-scroll { margin: 1rem 0 0; }
#modal-body .caption {
  font-size: 1.05rem; margin-top: 1.2rem; max-width: 60ch; line-height: 1.55;
}

.modal-close {
  position: absolute; top: 0.6rem; right: 0.8rem;
  background: none; border: none; cursor: pointer;
  font-size: 1.7rem; color: var(--card-ink-soft); line-height: 1;
  /* Comfortable touch target. */
  width: 44px; height: 44px;
  display: flex; align-items: center; justify-content: center;
}
.modal-actions {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 1.25rem; gap: 0.75rem;
}
.modal-actions .left, .modal-actions .right { display: flex; gap: 0.5rem; align-items: center; }
.modal-actions button {
  background: var(--accent-dark); color: var(--card);
  border: none; border-radius: 4px;
  padding: 0.55rem 1.05rem; font-family: inherit; font-size: 1rem;
  cursor: pointer; font-variation-settings: 'opsz' 14, 'wght' 500;
  transition: background 120ms ease, color 120ms ease, border-color 120ms ease;
}
.modal-actions button:hover { background: var(--accent); color: var(--paper); }
.modal-actions button:disabled { opacity: 0.4; cursor: default; }
.modal-actions .modal-play.playing { background: var(--sage-dark); }

/* "Together" (full-band) button — outlined so it reads as a secondary action */
.modal-together {
  background: transparent !important;
  color: var(--card-ink-soft) !important;
  border: 1px solid rgba(143, 18, 25, 0.5) !important;
}
.modal-together:hover {
  background: rgba(143, 18, 25, 0.1) !important;
  color: var(--card-ink) !important;
}
.modal-together.playing {
  background: var(--sage-dark) !important;
  color: var(--card) !important;
  border-color: var(--sage-dark) !important;
}

/* Loop button — subtle by default, accented when active */
.modal-loop {
  background: transparent !important;
  color: var(--card-ink-soft) !important;
  border: 1px solid rgba(185, 28, 28, 0.25) !important;
  font-style: italic;
  padding: 0.5rem 0.9rem !important;
  min-width: 5rem;
}
.modal-loop:hover {
  background: rgba(185, 28, 28, 0.08) !important;
  color: var(--card-ink) !important;
}
.modal-loop.active {
  background: rgba(214, 64, 74, 0.22) !important;
  color: var(--accent-dark) !important;
  border-color: var(--accent-dark) !important;
  font-variation-settings: 'opsz' 14, 'wght' 600;
}
.modal-title {
  font-size: 1.45rem; margin: 0 0 0.4rem;
  font-variation-settings: 'opsz' 36, 'wght' 600;
}
.modal-role { font-style: italic; color: var(--card-ink-soft); margin: 0 0 1rem; }

/* Phone modal: the frame becomes the whole screen — no slivers of backdrop
   to mis-tap, full height for tall tabs, and the action bar pinned at the
   bottom where thumbs live. */
@media (max-width: 720px) {
  .modal-backdrop { align-items: stretch; justify-content: stretch; }
  .modal-frame {
    width: 100%;
    height: 100vh; height: 100dvh;   /* dvh tracks the iOS toolbar */
    max-height: none; border-radius: 0;
    padding: calc(1rem + env(safe-area-inset-top)) 1rem
             calc(0.6rem + env(safe-area-inset-bottom));
  }
  .modal-title { font-size: 1.2rem; padding-right: 3rem; /* clear the ✕ */ }
  .modal-close {
    top: calc(0.5rem + env(safe-area-inset-top));
    right: 0.5rem; font-size: 2rem;
  }
  /* Sticky action bar: stays in reach while the tab body scrolls under it.
     margin-top:auto keeps it at the bottom even when the body is short. */
  .modal-actions {
    position: sticky; bottom: 0; margin-top: auto;
    padding: 0.8rem 0 0.3rem;
    background: linear-gradient(to top, var(--card) 72%, transparent);
  }
  .modal-actions button { padding: 0.7rem 1rem; font-size: 1.02rem; }
  #modal-body .caption { font-size: 0.95rem; }
  #modal-body .chord-strip { gap: 1rem; }
  #modal-body .chord-strip svg.chord-box { width: 150px; max-width: 150px; }
  #modal-body .chord-strip-item { flex: 0 0 160px; width: 160px; }
  #modal-body .chart-bar { min-height: 90px; padding: 1.1rem 0.5rem 0.9rem; }
}

/* ── Metronome ────────────────────────────────── */
/* z-index sits ABOVE the modal backdrop (50) so the user can keep using
   the metronome while a card is open fullscreen. */
.metro {
  position: fixed; z-index: 70;
  bottom: calc(1rem + env(safe-area-inset-bottom));
  right: calc(1rem + env(safe-area-inset-right));
  display: flex; flex-direction: column; align-items: flex-end;
}
.metro-btn {
  background: var(--accent-dark); color: var(--card);
  width: 52px; height: 52px; border-radius: 26px;
  border: none; cursor: pointer; font-family: inherit;
  font-size: 1.05rem; font-style: italic; font-weight: 600;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
}
.metro-btn:hover { background: var(--accent); color: var(--paper); }
.metro-panel {
  display: none; flex-direction: column; gap: 0.5rem;
  background: var(--paper-warm); border: 1px solid var(--line);
  border-radius: 6px; padding: 0.75rem 0.9rem;
  margin-bottom: 0.5rem; min-width: 220px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}
.metro-panel.open { display: flex; }
.metro-panel label { font-size: 0.85rem; color: var(--ink-soft); display: flex; justify-content: space-between; }
.metro-panel input[type=range] { width: 100%; }
.metro-row { display: flex; gap: 0.45rem; }
.metro-row button {
  flex: 1; padding: 0.45rem; font-family: inherit; font-size: 0.85rem;
  background: var(--paper); color: var(--ink); border: 1px solid var(--line);
  border-radius: 4px; cursor: pointer;
}
.metro-row button.on { background: var(--sage); color: var(--paper); border-color: var(--sage); }
/* Touch devices: a 52px launcher is fine, but the controls inside the
   panel need real finger room — taller sliders and buttons. */
@media (pointer: coarse) {
  .metro-btn { width: 56px; height: 56px; border-radius: 28px; }
  .metro-panel { min-width: min(260px, calc(100vw - 2rem)); padding: 0.9rem 1rem; gap: 0.7rem; }
  .metro-panel input[type=range] { height: 32px; }
  .metro-row button { padding: 0.65rem 0.45rem; font-size: 0.92rem; }
}

/* ── Full-song page — section meta chips + framed tab sheet ─────────── */
/* Each song section mines its tab text for tempo / chords / guitar parts and
   shows them as chips, then frames the verbatim ASCII tab in a "tab sheet" so
   it reads as notation paper instead of a raw text dump. Lives here (not the
   page module) so it shares the card palette and the print rules below. */
.song-meta {
  display: flex; flex-wrap: wrap; gap: 0.4rem;
  margin: 0.1rem 0 0.85rem;
}
.song-tag {
  font-variation-settings: 'opsz' 9, 'wght' 600;
  font-size: 0.7rem; letter-spacing: 0.04em;
  color: var(--card-ink-soft);
  background: rgba(20, 20, 23, 0.045);
  border: 1px solid var(--card-line);
  border-radius: 999px; padding: 0.18rem 0.62rem;
  white-space: nowrap; line-height: 1.5;
}
.song-tag-chord {
  font-style: italic;
  font-variation-settings: 'opsz' 18, 'wght' 600, 'WONK' 1;
  color: var(--accent-dark);
  background: rgba(214, 64, 74, 0.16);
  border-color: rgba(185, 28, 28, 0.28);
  letter-spacing: 0.01em;
}
.song-tag-tempo {
  color: var(--card-ink);
  background: rgba(20, 20, 23, 0.06);
}
.song-tag-rep {
  color: var(--sage-dark);
  background: rgba(199, 30, 42, 0.14);
  border-color: rgba(140, 14, 20, 0.3);
}
.song-tab-sheet {
  margin: 0;
  border: 1px solid var(--card-line);
  border-left: 3px solid var(--accent-dark);
  border-radius: 6px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0) 36%),
    #f3f2f1;
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.6) inset;
  overflow: hidden;
}
.song-tab-sheet pre {
  margin: 0; padding: 0.85rem 0.95rem;
  overflow-x: auto; -webkit-overflow-scrolling: touch;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.78rem; line-height: 1.5;
  white-space: pre; color: var(--card-ink);
}
.song-tab-sheet pre::-webkit-scrollbar { height: 6px; }
.song-tab-sheet pre::-webkit-scrollbar-thumb {
  background: rgba(124, 27, 18, 0.25); border-radius: 3px;
}
/* Stacked engraved staves on the full-song page. Each stave is pinned to an
   exact pixel size by an inline style (render_tab fixed_px), so a note is the
   same size on every line; the scroll wrapper lets a wide stave scroll
   sideways on a narrow screen. min-width:0 is required to defeat the generic
   .tab-scroll min-width that would otherwise re-stretch a short stave. */
.song-staves { margin: 0.4rem 0 0; }
.song-legend {
  font-size: 0.78rem; font-style: italic; color: var(--card-ink-soft);
  margin: 0 0 0.5rem;
}
/* One flex column per bar, every guitar stacked inside it. Columns wrap to
   the viewport: a desktop fits several bars per row, a phone gets one
   full-width bar — NO horizontal scrolling anywhere on the song page. */
.song-bars {
  display: flex; flex-wrap: wrap;
  column-gap: 10px; row-gap: 1.1rem;
  align-items: flex-start;
}
.song-bar { flex: 0 1 auto; max-width: 100%; }
/* Inside a column the .tab-scroll wrapper is inert (nothing scrolls) and the
   SVG sizes to its width attribute, shrinking only if the column is wider
   than a small screen. */
.song-bar .tab-scroll { overflow-x: visible; margin: 0; padding: 0; min-width: 0; background: none; }
.song-bar svg.tab, .song-bar svg.tab-rich {
  min-width: 0; width: auto; max-width: 100%; height: auto; display: block;
}

/* Notation text — use the site's Fraunces rather than the browser default
   serif, so the engraved tab doesn't read as generic. Scoped to the music
   SVGs so it never touches the fosterthecode footer mark. */
svg.tab text, svg.tab-rich text, svg.fretboard text {
  font-family: 'Fraunces', 'Iowan Old Style', Charter, Georgia, serif;
  font-variation-settings: 'opsz' 14, 'wght' 600;
}

/* In the fullscreen modal the sheet has the whole frame — bump legibility. */
#modal-body .song-tab-sheet { margin-top: 0.5rem; }
#modal-body .song-tab-sheet pre { font-size: 0.92rem; padding: 1.1rem 1.2rem; }
#modal-body .song-meta { margin-bottom: 1rem; }

/* ── Site footer — "built by fosterthecode" ─────────────────────────── */
.site-footer {
  display: flex; align-items: center; justify-content: center;
  gap: 0.55rem;
  margin: 3.5rem 0 0;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--sepia);
  font-size: 0.82rem;
}
.site-footer svg { display: block; border-radius: 7px; flex: 0 0 auto; }
.site-footer span { font-style: italic; letter-spacing: 0.01em; }
.site-footer strong {
  font-style: normal; font-variation-settings: 'opsz' 14, 'wght' 600;
  color: var(--ink-soft);
}

/* ── Reduced motion ───────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}

/* ── Print ────────────────────────────────────── */
@media print {
  /* The dark theme's named colors would print near-white on white paper —
     remap the custom properties so every heading/blurb inherits printable ink. */
  :root {
    --ink: #111; --ink-soft: #333; --sepia: #444;
    --accent: #8f1219; --accent-dark: #6e0e14;
  }
  html, body { background: white; color: black; }
  .topbar, .metro, .modal-backdrop, .card-play, .ex-footer { display: none !important; }
  .card { background: white; box-shadow: none; border: 1px solid #aaa; break-inside: avoid; }
  .card svg { color: black; }
  .song-tab-sheet { border: 1px solid #aaa; border-left: 3px solid #888; background: white; }
  .song-tag { border-color: #bbb; color: #333; background: none; }
}
'''.replace('__FONT_REGULAR__', FONT_REGULAR).replace('__FONT_ITALIC__', FONT_ITALIC).replace('__FONT_BLACKLETTER__', FONT_BLACKLETTER).replace('__DRIP_URI__', DRIP_DATA_URI)


# ─────────────────────────────────────────────────────────────────────────────
# Page JS — audio synth + modal + metronome + service worker
# ─────────────────────────────────────────────────────────────────────────────

PAGE_JS = r'''
// ── Audio: Karplus-Strong plucked-string synth ───────────────────────
const Audio = (() => {
  let ctx = null;
  let master = null;     // master gain node — global stop / volume
  const activeSources = new Set();
  const bufferCache = new Map();
  const OPEN_MIDI = {6: 38, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64};  // DROP D: string 6 = D2
  function getCtx() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      master = ctx.createGain();
      master.gain.value = userVolume;   // respect any volume the user set pre-context
      // Soft compressor catches stacked overlaps so chords don't clip.
      const comp = ctx.createDynamicsCompressor();
      comp.threshold.value = -18;
      comp.knee.value = 18;
      comp.ratio.value = 6;
      comp.attack.value = 0.003;
      comp.release.value = 0.25;
      // Make-up gain AFTER the compressor — the compressor tames peaks, this
      // brings the overall level back up loud. This is most of the volume.
      const makeup = ctx.createGain();
      makeup.gain.value = 2.4;
      master.connect(comp);
      comp.connect(makeup);
      makeup.connect(ctx.destination);
    }
    // 'suspended' OR Safari's non-standard 'interrupted' (after a call/Siri
    // in a standalone PWA) — anything not running gets a resume nudge.
    if (ctx.state !== 'running') ctx.resume();
    return ctx;
  }
  function midiToHz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  function freqFor(stringNum, fret) {
    return midiToHz(OPEN_MIDI[stringNum] + (fret|0));
  }
  // Karplus-Strong, tuned for warm + quick-decaying tone.
  function makeBuffer(freq) {
    const c = getCtx();
    const sr = c.sampleRate;
    const period = Math.max(2, Math.round(sr / freq));
    // Flat per-sample decay; higher notes still die faster because the loop
    // filter runs once per (shorter) period. Total duration capped at ~1.4s.
    const decay = 0.992;
    const durSec = Math.min(1.4, 0.7 + 200 / freq);
    const N = Math.floor(sr * durSec);
    const buf = c.createBuffer(1, N, sr);
    const out = buf.getChannelData(0);
    // Initial buffer = quieter, pre-smoothed noise. This kills the harsh "click" attack.
    const delay = new Float32Array(period);
    for (let i = 0; i < period; i++) {
      delay[i] = (Math.random() * 2 - 1) * 0.45;
    }
    // Three smoothing passes — softens the pluck. Each pass is a true 2-tap
    // moving average over a snapshot, so it doesn't cascade as an in-place IIR.
    for (let pass = 0; pass < 3; pass++) {
      const prev = Float32Array.from(delay);
      for (let i = 0; i < period; i++) {
        delay[i] = (prev[i] + prev[(i + 1) % period]) * 0.5;
      }
    }
    // Process
    let pos = 0;
    for (let i = 0; i < N; i++) {
      const nextPos = (pos + 1) % period;
      const avg = (delay[pos] + delay[nextPos]) * 0.5 * decay;
      out[i] = delay[pos];
      delay[pos] = avg;
      pos = nextPos;
    }
    // Attack ramp (50 samples)
    const att = Math.min(80, N);
    for (let i = 0; i < att; i++) out[i] *= i / att;
    // Release ramp — last 15% fades to silence so successive notes don't pile.
    const rel = Math.floor(N * 0.15);
    for (let i = 0; i < rel; i++) {
      out[N - 1 - i] *= i / rel;
    }
    return buf;
  }
  function getBuffer(freq) {
    const key = freq.toFixed(2);
    if (!bufferCache.has(key)) bufferCache.set(key, makeBuffer(freq));
    return bufferCache.get(key);
  }
  function playAt(freq, when, gain=0.5, pan=0) {
    const c = getCtx();
    const src = c.createBufferSource();
    src.buffer = getBuffer(freq);
    // The delay line is an integer number of samples and its 2-tap loop
    // filter adds half a sample of group delay, so the buffer actually rings
    // at sr/(period + 0.5) — up to ~16 cents flat in the lead register.
    // Resample to the true pitch.
    const sr = c.sampleRate;
    const period = Math.max(2, Math.round(sr / freq));
    src.playbackRate.value = freq * (period + 0.5) / sr;
    const g = c.createGain();
    g.gain.setValueAtTime(gain, when);
    g.gain.exponentialRampToValueAtTime(0.0001, when + src.buffer.duration);
    src.connect(g);
    const lp = c.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.value = Math.min(6000, freq * 6);
    lp.Q.value = 0.5;
    g.connect(lp);
    if (c.createStereoPanner) {
      const p = c.createStereoPanner();
      p.pan.value = pan;
      lp.connect(p);
      p.connect(master);
    } else {
      lp.connect(master);
    }
    src._gainNode = g;          // for stopAll's per-source fade
    activeSources.add(src);
    src.onended = () => { activeSources.delete(src); };
    src.start(when);
    return src;
  }
  function pluck(stringNum, fret, when=null, gain=0.5) {
    const c = getCtx();
    const t = when ?? c.currentTime;
    return playAt(freqFor(stringNum, fret), t, gain);
  }
  function strum(shape, opts={}) {
    const c = getCtx();
    const t0 = (opts.when ?? c.currentTime) + 0.02;
    const gap = opts.gap ?? 0.032;
    const dir = opts.direction || 'down';
    const idxs = shape.map((f, i) => ({i, f, stringNum: 6 - i}))
                      .filter(x => x.f !== null && x.f >= 0);
    if (dir === 'up') idxs.reverse();
    idxs.forEach((x, k) => {
      const when = t0 + k * gap;
      pluck(x.stringNum, x.f, when, 0.40);
      if (opts.onNote) opts.onNote(x.stringNum, x.f, when);
    });
    return t0 + idxs.length * gap;
  }
  function playSequence(notes, bpm=80, opts={}) {
    const c = getCtx();
    const t0 = (opts.when ?? c.currentTime) + 0.04;
    const beat = 60 / bpm;
    let t = t0;
    notes.forEach((nv, idx) => {
      if (nv.rest) {
        // silence — still advance the playhead so tab-note idx stays in sync
        if (opts.onIndex) opts.onIndex(idx, t);
      } else if (nv.strum) {
        nv.strum.forEach((sf, i) => {
          const when = t + i * 0.015;
          pluck(sf[0], sf[1], when, opts.gain || 0.42);
          if (opts.onNote) opts.onNote(sf[0], sf[1], when, idx);
        });
        if (opts.onIndex) opts.onIndex(idx, t);
      } else if (nv.chord) {
        nv.chord.forEach((sf, i) => {
          const when = t + i * 0.004;
          pluck(sf[0], sf[1], when, opts.gain || 0.42);
          if (opts.onNote) opts.onNote(sf[0], sf[1], when, idx);
        });
        if (opts.onIndex) opts.onIndex(idx, t);
      } else if (nv.string !== undefined) {
        pluck(nv.string, nv.fret, t, opts.gain || 0.5);
        if (opts.onNote) opts.onNote(nv.string, nv.fret, t, idx);
        if (opts.onIndex) opts.onIndex(idx, t);
      }
      t += (nv.dur || 1) * beat;
    });
    return {endTime: t};
  }
  function playScaleAscDesc(notes, bpm=110, opts={}) {
    const dur = opts.dur || 0.5;        // beats per note (default = eighth)
    const seq = notes.map(([s, f]) => ({string: s, fret: f, dur}));
    const desc = [...seq].slice(0, -1).reverse();
    return playSequence([...seq, ...desc], bpm, opts);
  }
  let userVolume = 0.8;
  function setVolume(v) {
    userVolume = v;
    if (master && ctx) {
      master.gain.cancelScheduledValues(ctx.currentTime);
      master.gain.setValueAtTime(v, ctx.currentTime);
    }
  }
  function stopAll() {
    // Per-source fade-then-stop — master gain stays untouched so the next
    // playback is immediately audible.
    if (!ctx) return;
    const now = ctx.currentTime;
    activeSources.forEach(s => {
      try {
        if (s._gainNode) {
          s._gainNode.gain.cancelScheduledValues(now);
          s._gainNode.gain.setValueAtTime(s._gainNode.gain.value, now);
          s._gainNode.gain.linearRampToValueAtTime(0.0001, now + 0.03);
        }
        s.stop(now + 0.04);
      } catch (e) {}
    });
    activeSources.clear();
    document.querySelectorAll('.card-play.playing').forEach(b => b.classList.remove('playing'));
    ['modal-play', 'modal-together'].forEach(id => {
      const b = document.getElementById(id);
      if (b) b.classList.remove('playing');
    });
  }
  // Expose the master gain node so other sources (e.g. the metronome click)
  // route through the same volume control instead of straight to destination.
  function getMaster() { getCtx(); return master; }
  return {pluck, strum, playSequence, playScaleAscDesc, getCtx, getMaster, freqFor, stopAll, setVolume};
})();

// ── Tempo (single source of truth — the metronome bpm slider) ────────
// Every audio playback uses this — chord progressions, scales, licks,
// boogie, comping. Adjusting the metronome slider live-updates the tempo
// of future playbacks (current playback finishes at its scheduled tempo).
let currentBpm = parseInt(localStorage.getItem('ascendancy-bpm') || '80', 10);

// ── Loop control (off → ∞ → 4× → 2× → off) ───────────────────────────
// (Declared up here so the modal IIFE below can reference it at init time.)
const LOOP_CYCLE = [0, -1, 4, 2];
let loopMode = 0;
let loopRemaining = 0;
let loopTimer = null;
let loopCardEl = null;
try {
  const _saved = parseInt(localStorage.getItem('ascendancy-loop') || '0', 10);
  if (LOOP_CYCLE.indexOf(_saved) >= 0) loopMode = _saved;
} catch (e) {}

function loopLabel(m) {
  if (m === 0) return '↻ Loop';
  if (m === -1) return '↻ ∞';
  return '↻ ' + m + '×';
}
function setLoopMode(m) {
  loopMode = m;
  loopRemaining = m > 0 ? m : 0;
  try { localStorage.setItem('ascendancy-loop', loopMode); } catch (e) {}
  const btn = document.getElementById('modal-loop');
  if (btn) {
    btn.textContent = loopLabel(loopMode);
    btn.classList.toggle('active', loopMode !== 0);
  }
}
function cycleLoop() {
  const i = LOOP_CYCLE.indexOf(loopMode);
  setLoopMode(LOOP_CYCLE[(i + 1) % LOOP_CYCLE.length]);
}
function cancelLoop() {
  if (loopTimer) { clearTimeout(loopTimer); loopTimer = null; }
  loopCardEl = null;
  if (loopMode > 0) loopRemaining = loopMode;
}

// ── Modal: click any .card to open fullscreen ────────────────────────
(function() {
  const cards = Array.from(document.querySelectorAll('.card'));
  if (!cards.length) return;
  const backdrop = document.getElementById('modal-backdrop');
  const frame = backdrop.querySelector('.modal-frame');
  const titleEl = document.getElementById('modal-title');
  const roleEl = document.getElementById('modal-role');
  const bodyEl = document.getElementById('modal-body');
  const prevBtn = document.getElementById('modal-prev');
  const nextBtn = document.getElementById('modal-next');
  const closeBtn = document.getElementById('modal-close');
  const playBtn = document.getElementById('modal-play');
  let idx = -1;
  let lastTrigger = null;   // element to restore focus to when the modal closes

  function render() {
    if (typeof stopCard === 'function') stopCard();
    const c = cards[idx];
    titleEl.textContent = c.dataset.title || '';
    roleEl.textContent = c.dataset.role || '';
    bodyEl.innerHTML = '';
    // Clone every part of the card except elements already shown in the
    // modal header (key-num / h3 / role) and the inline play button.
    Array.from(c.children).forEach(child => {
      if (child.classList && (
            child.classList.contains('card-play') ||
            child.classList.contains('key-num') ||
            child.classList.contains('role') ||
            child.tagName === 'H3'
          )) return;
      bodyEl.appendChild(child.cloneNode(true));
    });
    prevBtn.disabled = idx <= 0;
    nextBtn.disabled = idx >= cards.length - 1;
    playBtn.style.display = c.dataset.audio ? 'inline-block' : 'none';
    playBtn.classList.remove('playing');
    const lb = document.getElementById('modal-loop');
    if (lb) {
      lb.style.display = c.dataset.audio ? 'inline-block' : 'none';
      lb.textContent = loopLabel(loopMode);
      lb.classList.toggle('active', loopMode !== 0);
    }
    const tb = document.getElementById('modal-together');
    if (tb) {
      tb.style.display = c.dataset.audioTogether ? 'inline-block' : 'none';
      tb.classList.remove('playing');
    }
  }
  let lockScrollY = 0;
  function open(i) {
    // Remember what triggered the modal so we can restore focus on close.
    lastTrigger = (document.activeElement && cards.includes(document.activeElement.closest('.card')))
      ? document.activeElement.closest('.card')
      : cards[i];
    idx = i; render(); backdrop.classList.add('open');
    // iOS Safari ignores body overflow:hidden (the page rubber-bands under
    // the backdrop) — pin the body instead and restore scroll on close.
    lockScrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${lockScrollY}px`;
    document.body.style.width = '100%';
    // Move focus into the dialog (the close button).
    closeBtn.focus();
  }
  function close() {
    if (typeof stopCard === 'function') stopCard();
    backdrop.classList.remove('open'); idx = -1;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo(0, lockScrollY);
    // Restore focus to the triggering card.
    if (lastTrigger && typeof lastTrigger.focus === 'function') lastTrigger.focus();
    lastTrigger = null;
  }

  // Focusable elements currently visible inside the modal frame.
  function modalFocusables() {
    return Array.from(frame.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )).filter(el => !el.disabled && el.offsetParent !== null);
  }
  // Trap Tab / Shift-Tab inside the modal frame while open.
  function trapTab(e) {
    if (e.key !== 'Tab') return;
    const f = modalFocusables();
    if (!f.length) { e.preventDefault(); return; }
    const first = f[0], last = f[f.length - 1];
    const active = document.activeElement;
    if (e.shiftKey) {
      if (active === first || !frame.contains(active)) { e.preventDefault(); last.focus(); }
    } else {
      if (active === last || !frame.contains(active)) { e.preventDefault(); first.focus(); }
    }
  }

  cards.forEach((c, i) => {
    c.addEventListener('click', (e) => {
      // Don't open modal when clicking the play button
      if (e.target.closest('.card-play')) return;
      open(i);
    });
    c.setAttribute('tabindex', '0');
    c.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        if (e.target.closest('.card-play')) return;
        e.preventDefault(); open(i);
      }
    });
  });
  prevBtn.addEventListener('click', () => { if (idx > 0) { idx--; render(); } });
  nextBtn.addEventListener('click', () => { if (idx < cards.length - 1) { idx++; render(); } });
  closeBtn.addEventListener('click', close);
  backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
  document.addEventListener('keydown', (e) => {
    if (!backdrop.classList.contains('open')) return;
    if (e.key === 'Tab') { trapTab(e); return; }
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft' && idx > 0) { idx--; render(); }
    else if (e.key === 'ArrowRight' && idx < cards.length - 1) { idx++; render(); }
    // Space = play/pause shortcut — but never steal it from a focused
    // control (a keyboard user pressing Space on Loop/Close expects THAT
    // button to activate).
    else if (e.key === ' ' && !e.target.closest('button, input, select, a')) {
      e.preventDefault(); playBtn.click();
    }
  });

  // Modal play (toggle)
  playBtn.addEventListener('click', () => {
    const c = cards[idx];
    if (!c.dataset.audio) return;
    if (playBtn.classList.contains('playing')) {
      stopCard();
      playBtn.classList.remove('playing');
      return;
    }
    Audio.stopAll();
    cancelLoop();
    cancelHighlights();
    playBtn.classList.add('playing');
    playCardWithLoop(c, [playBtn]);
  });

  // "Together" — play all of a section's guitar parts layered as a full band.
  const togetherBtn = document.getElementById('modal-together');
  if (togetherBtn) {
    togetherBtn.addEventListener('click', () => {
      const c = cards[idx];
      if (!c.dataset.audioTogether) return;
      if (togetherBtn.classList.contains('playing')) {
        stopCard();
        togetherBtn.classList.remove('playing');
        return;
      }
      Audio.stopAll();
      cancelLoop();
      cancelHighlights();
      playBtn.classList.remove('playing');
      togetherBtn.classList.add('playing');
      playTogetherWithLoop(c, togetherBtn);
    });
  }

  // Loop cycle button
  const loopBtn = document.getElementById('modal-loop');
  loopBtn.addEventListener('click', () => { cycleLoop(); });
  // Initialise label
  loopBtn.textContent = loopLabel(loopMode);
  loopBtn.classList.toggle('active', loopMode !== 0);

  // Open a card directly via URL hash (#card=N).
  function openFromHash() {
    const m = (location.hash || '').match(/card=(\d+)/);
    if (!m) return;
    const i = parseInt(m[1], 10);
    if (i >= 0 && i < cards.length) open(i);
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);

  // Swipe gestures in modal. Touches that start inside a horizontally
  // scrollable tab are the user READING the tab — never card navigation.
  let tx = null, ty = null;
  backdrop.addEventListener('touchstart', (e) => {
    if (e.target.closest('.modal-actions') || e.target.closest('button')
        || e.target.closest('.tab-scroll')) return;
    tx = e.touches[0].clientX;
    ty = e.touches[0].clientY;
  });
  backdrop.addEventListener('touchend', (e) => {
    if (tx === null) return;
    const dx = (e.changedTouches[0].clientX) - tx;
    const dy = (e.changedTouches[0].clientY) - ty;
    tx = null; ty = null;
    // Only treat as horizontal card-nav when the gesture is mostly horizontal —
    // a mostly-vertical swipe should scroll the (possibly tall) modal body.
    if (Math.abs(dx) <= Math.abs(dy)) return;
    if (Math.abs(dx) < 60) return;
    if (dx < 0 && idx < cards.length - 1) { idx++; render(); }
    else if (dx > 0 && idx > 0) { idx--; render(); }
  });
})();

// ── Card play buttons ────────────────────────────────────────────────
let currentPlayTimeout = null;

// ── Highlight scheduler (rAF, audio-clock-locked) ────────────────────
// Lighting the dots/tab-notes used to fire on a setTimeout timeline that
// drifts from the audio clock under tab-backgrounding and accumulates jitter
// over long sequences. Instead, a single rAF loop holds every pending
// highlight event {el, when, until} and, each frame, compares the live audio
// clock (Audio.getCtx().currentTime) against `when`/`until` to toggle `.lit`.
// Because it reads the audio clock — not wall time — it re-syncs exactly even
// after the tab was backgrounded (rAF pauses, but on resume the clock has
// advanced, so overdue notes light then immediately un-light correctly).
const HIGHLIGHT_LIT_SEC = 0.72;   // how long a note stays lit (was 720ms)
let highlightEvents = [];          // {el, when, until, lit}
let highlightRaf = null;

// Follow-along: while the song plays in the open modal, keep the bar that
// just lit scrolled into view (one scroll per bar, never per note).
let _lastFollowedBar = null;
function _followBar(el) {
  const backdrop = document.getElementById('modal-backdrop');
  if (!backdrop || !backdrop.classList.contains('open')) return;
  if (!el.closest('#modal-body')) return;
  const bar = el.closest('.song-bar');
  if (!bar || bar === _lastFollowedBar) return;
  _lastFollowedBar = bar;
  bar.scrollIntoView({block: 'nearest', behavior: 'smooth'});
}

function _highlightTick() {
  const ctx = Audio.getCtx();
  const now = ctx.currentTime;
  let anyPending = false;
  for (const ev of highlightEvents) {
    if (ev.done) continue;
    if (!ev.lit && now >= ev.when && now < ev.until) {
      // Audio clock has reached this note — light it.
      ev.el.classList.remove('lit');
      void ev.el.getBoundingClientRect();   // restart any CSS transition
      ev.el.classList.add('lit');
      ev.lit = true;
      _followBar(ev.el);
    }
    if (now >= ev.until) {
      // Note (and its lit window) has passed — un-light and retire.
      if (ev.lit) ev.el.classList.remove('lit');
      ev.done = true;
    } else {
      anyPending = true;
    }
  }
  if (anyPending) {
    highlightRaf = requestAnimationFrame(_highlightTick);
  } else {
    // Nothing left to do — drop the loop and clear the (all-retired) list.
    highlightRaf = null;
    highlightEvents = [];
  }
}

function _scheduleHighlight(el, when) {
  if (!el) return;
  highlightEvents.push({el, when, until: when + HIGHLIGHT_LIT_SEC, lit: false, done: false});
  if (highlightRaf === null) highlightRaf = requestAnimationFrame(_highlightTick);
}

function highlightDot(scopeEl, stringNum, fret, when) {
  if (!scopeEl) return;
  const dots = scopeEl.querySelectorAll(
    `circle.fret-dot[data-s="${stringNum}"][data-f="${fret}"]`
  );
  dots.forEach(dot => _scheduleHighlight(dot, when));
}

// Light up the tab-note at the given sequence index inside scopeEl.
function highlightTabNote(scopeEl, idx, when) {
  if (!scopeEl || idx == null) return;
  scopeEl.querySelectorAll(`.tab-note[data-i="${idx}"]`).forEach(el => {
    _scheduleHighlight(el, when);
  });
}

// Cancel every pending highlight: stop the rAF loop + clear all `.lit`.
function cancelHighlights() {
  if (highlightRaf !== null) { cancelAnimationFrame(highlightRaf); highlightRaf = null; }
  _lastFollowedBar = null;
  highlightEvents.forEach(ev => { if (ev.el) ev.el.classList.remove('lit'); });
  highlightEvents = [];
  document.querySelectorAll('circle.fret-dot.lit').forEach(d => d.classList.remove('lit'));
  document.querySelectorAll('.tab-note.lit').forEach(d => d.classList.remove('lit'));
}

// Mirror a highlight in the open modal body if it's showing the same content.
function mirrorHighlight(shape, isScaleBox, stringNum, fret, when) {
  const mb = document.getElementById('modal-body');
  if (!mb || !document.getElementById('modal-backdrop').classList.contains('open')) return;
  if (isScaleBox) {
    mb.querySelectorAll('svg.scale-box').forEach(box => highlightDot(box, stringNum, fret, when));
    return;
  }
  if (!shape) return;
  // Card with a chord-strip (form, shuffle, licks turnarounds) → scope to the
  // matching chord-strip-item so only the right chord box lights up.
  const box = findShapeBox(mb, shape);
  if (box) {
    highlightDot(box, stringNum, fret, when);
    return;
  }
  // No chord-strip in modal — the card is a standalone chord shape (e7_shapes,
  // a7_shapes, b7_shapes, ninth_chords). Light up the only chord box.
  highlightDot(mb, stringNum, fret, when);
}

// Find the chord-strip-item whose data-shape equals `shape`, or null.
function findShapeBox(cardEl, shape) {
  if (!cardEl || !shape) return null;
  const target = JSON.stringify(shape);
  const items = cardEl.querySelectorAll('.chord-strip-item');
  for (const item of items) {
    const itemShape = item.dataset.shape;
    if (!itemShape) continue;
    // Compare canonically — parse both and compare element-wise to avoid
    // whitespace/separator differences between Python and JS.
    try {
      const a = JSON.parse(itemShape);
      const b = JSON.parse(target);
      if (a.length === b.length && a.every((v, i) => v === b[i])) return item;
    } catch (e) {}
  }
  return null;
}

// Build a "scope" element for the highlight, given an audio data type.
// For chord/progression/comp: shape-matched chord-strip-item (only that one
// chord box lights up). For scale: scale-boxes only. For sequence: skip.
function highlightScopeFor(cardEl, dataType, shape) {
  if (dataType === 'chord' || dataType === 'progression' || dataType === 'comp') {
    return findShapeBox(cardEl, shape) || cardEl;   // fallback for cards without a strip
  }
  if (dataType === 'scale') {
    // Wrap all scale-boxes in a synthetic container by returning the cardEl
    // but the caller will scope by selecting only svg.scale-box dots.
    return cardEl;
  }
  return null;   // sequence: no fretboard light
}

function playCard(cardEl, onEnd) {
  const data = JSON.parse(cardEl.dataset.audio);
  const ctx = Audio.getCtx();
  let endT = ctx.currentTime;
  // Every tempo-based playback uses the metronome's current bpm so changing
  // the metronome live-changes how everything plays back.
  if (data.type === 'chord') {
    const target = findShapeBox(cardEl, data.shape) || cardEl;
    endT = Audio.strum(data.shape, {
      direction: data.direction || 'down',
      onNote: (s, f, when) => {
        highlightDot(target, s, f, when);
        mirrorHighlight(data.shape, false, s, f, when);
      },
    });
    endT += 0.9;
  } else if (data.type === 'scale') {
    const onNote = (s, f, when, idx) => {
      cardEl.querySelectorAll('svg.scale-box').forEach(box => {
        highlightDot(box, s, f, when);
      });
      mirrorHighlight(null, true, s, f, when);
      highlightTabNote(cardEl, idx, when);
      const mb = document.getElementById('modal-body');
      if (mb && document.getElementById('modal-backdrop').classList.contains('open')) {
        highlightTabNote(mb, idx, when);
      }
    };
    let seq;
    if (data.skip_desc) {
      // Already a complete pre-built sequence (each box does its own asc+desc).
      const dur = data.dur || 0.5;
      const evs = data.notes.map(([s, f]) => ({string: s, fret: f, dur}));
      seq = Audio.playSequence(evs, currentBpm, {onNote});
    } else {
      seq = Audio.playScaleAscDesc(data.notes, currentBpm, {onNote, dur: data.dur});
    }
    endT = seq.endTime + 0.4;
  } else if (data.type === 'sequence') {
    const onNote = (s, f, when, idx) => {
      highlightTabNote(cardEl, idx, when);
      // Also light the matching dot in any chord / scale diagram on the card so
      // the reference diagrams animate along with the tab (the chord strips
      // sit above a sequence-type tab and used to stay dark).
      highlightDot(cardEl, s, f, when);
      const mb = document.getElementById('modal-body');
      if (mb && document.getElementById('modal-backdrop').classList.contains('open')) {
        highlightTabNote(mb, idx, when);
        highlightDot(mb, s, f, when);
      }
    };
    const seq = Audio.playSequence(data.notes, currentBpm, {gain: data.gain || 0.5, onNote});
    endT = seq.endTime + 0.5;
  } else if (data.type === 'progression') {
    const beat = 60 / currentBpm;
    let t = ctx.currentTime + 0.1;
    data.bars.forEach(b => {
      const target = findShapeBox(cardEl, b.shape) || cardEl;
      Audio.strum(b.shape, {
        when: t, direction: 'down',
        onNote: (s, f, when) => {
          highlightDot(target, s, f, when);
          mirrorHighlight(b.shape, false, s, f, when);
        },
      });
      t += (b.beats || 4) * beat;
    });
    endT = t + 0.5;
  } else if (data.type === 'comp') {
    const beat = 60 / currentBpm;
    const t0 = ctx.currentTime + 0.1;
    data.hits.forEach(hit => {
      const target = findShapeBox(cardEl, hit.shape) || cardEl;
      Audio.strum(hit.shape, {
        when: t0 + (hit.beat || 0) * beat,
        direction: hit.direction || 'down',
        onNote: (s, f, when) => {
          highlightDot(target, s, f, when);
          mirrorHighlight(hit.shape, false, s, f, when);
        },
      });
    });
    const lastBeat = data.hits.length ? Math.max(...data.hits.map(h => h.beat || 0)) : 0;
    const totalBeats = data.duration || (lastBeat + 2);
    endT = t0 + totalBeats * beat + 0.4;
  }
  const ms = Math.max(0, (endT - ctx.currentTime) * 1000);
  if (currentPlayTimeout) clearTimeout(currentPlayTimeout);
  currentPlayTimeout = setTimeout(() => {
    currentPlayTimeout = null;
    if (onEnd) onEnd();
  }, ms);
}

// Play a section's layered "all guitars together" sequence (data-audio-together).
// Each moment carries the data-i of every note that sounds on that beat, so we
// light them all at once across the stacked staves (and the open modal).
function playTogether(cardEl, onEnd) {
  if (!cardEl.dataset.audioTogether) return;
  const data = JSON.parse(cardEl.dataset.audioTogether);
  const ctx = Audio.getCtx();
  const lightMoment = (moment, when) => {
    if (!moment || !moment.idx) return;
    const mb = document.getElementById('modal-body');
    const modalOpen = mb && document.getElementById('modal-backdrop').classList.contains('open');
    moment.idx.forEach(di => {
      highlightTabNote(cardEl, di, when);
      if (modalOpen) highlightTabNote(mb, di, when);
    });
  };
  const onIndex = (i, when) => lightMoment(data.notes[i], when);
  const seq = Audio.playSequence(data.notes, currentBpm, {gain: data.gain || 0.45, onIndex});
  const ms = Math.max(0, (seq.endTime - ctx.currentTime) * 1000 + 200);
  if (currentPlayTimeout) clearTimeout(currentPlayTimeout);
  currentPlayTimeout = setTimeout(() => { currentPlayTimeout = null; if (onEnd) onEnd(); }, ms);
}

// Loop-aware wrapper for Together, mirroring playCardWithLoop.
function playTogetherWithLoop(cardEl, btn) {
  loopCardEl = cardEl;
  if (loopMode > 0) loopRemaining = loopMode;
  function tick() {
    playTogether(cardEl, () => {
      const shouldLoop = (loopCardEl === cardEl) &&
        (loopMode === -1 || (loopMode > 0 && loopRemaining > 1));
      if (shouldLoop) {
        if (loopMode > 0) loopRemaining -= 1;
        loopTimer = setTimeout(tick, 250);
      } else {
        loopCardEl = null;
        if (loopMode > 0) loopRemaining = loopMode;
        if (btn) btn.classList.remove('playing');
      }
    });
  }
  tick();
}

function stopCard() {
  Audio.stopAll();
  if (currentPlayTimeout) { clearTimeout(currentPlayTimeout); currentPlayTimeout = null; }
  cancelLoop();
  cancelHighlights();
}

// Play with loop awareness: when playback ends, if loopMode is non-zero and
// the user hasn't stopped, re-play the same card.
function playCardWithLoop(cardEl, playingButtons, onEnd) {
  loopCardEl = cardEl;
  if (loopMode > 0) loopRemaining = loopMode;  // reset count when starting fresh
  function tick() {
    playCard(cardEl, () => {
      // Natural end. Check if we should loop.
      const shouldLoop = (loopCardEl === cardEl) && (
        loopMode === -1 ||
        (loopMode > 0 && loopRemaining > 1)
      );
      if (shouldLoop) {
        if (loopMode > 0) loopRemaining -= 1;
        loopTimer = setTimeout(tick, 250);
      } else {
        loopCardEl = null;
        if (loopMode > 0) loopRemaining = loopMode;
        playingButtons.forEach(b => b.classList.remove('playing'));
        if (onEnd) onEnd();
      }
    });
  }
  tick();
}

document.querySelectorAll('.card-play').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const card = btn.closest('.card');
    if (!card || !card.dataset.audio) return;
    if (btn.classList.contains('playing')) {
      stopCard();
      return;
    }
    // Stop any other playing button first.
    document.querySelectorAll('.card-play.playing').forEach(b => b.classList.remove('playing'));
    Audio.stopAll();
    cancelLoop();
    cancelHighlights();
    btn.classList.add('playing');
    playCardWithLoop(card, [btn]);
  });
});

// ── Metronome ────────────────────────────────────────────────────────
(function() {
  const btn = document.getElementById('metro-btn');
  const panel = document.getElementById('metro-panel');
  if (!btn) return;
  let schedTimer = null, nextNoteTime = 0, current = 0;
  const bpmInput = document.getElementById('metro-bpm');
  const bpmLabel = document.getElementById('metro-bpm-label');
  const startBtn = document.getElementById('metro-start');
  const tapBtn = document.getElementById('metro-tap');
  const subBtns = Array.from(document.querySelectorAll('.metro-sub'));
  let bpm = parseInt(localStorage.getItem('ascendancy-bpm') || '80', 10);
  let subdiv = parseInt(localStorage.getItem('ascendancy-sub') || '1', 10);
  let running = false;
  bpmInput.value = bpm;
  bpmLabel.textContent = bpm;
  subBtns.forEach(b => {
    if (parseInt(b.dataset.sub, 10) === subdiv) b.classList.add('on');
    b.addEventListener('click', () => {
      subBtns.forEach(x => x.classList.remove('on'));
      b.classList.add('on');
      subdiv = parseInt(b.dataset.sub, 10);
      localStorage.setItem('ascendancy-sub', subdiv);
    });
  });
  bpmInput.addEventListener('input', () => {
    bpm = parseInt(bpmInput.value, 10);
    currentBpm = bpm;             // sync the global so all playback follows
    bpmLabel.textContent = bpm;
    localStorage.setItem('ascendancy-bpm', bpm);
  });
  btn.addEventListener('click', () => { panel.classList.toggle('open'); });
  function click(time, accent) {
    const c = Audio.getCtx();
    const o = c.createOscillator();
    const g = c.createGain();
    o.frequency.value = accent ? 1500 : 950;
    g.gain.setValueAtTime(0.0001, time);
    g.gain.exponentialRampToValueAtTime(0.32, time + 0.001);
    g.gain.exponentialRampToValueAtTime(0.0001, time + 0.05);
    // Route through master so the volume slider affects the click too.
    o.connect(g); g.connect(Audio.getMaster() || c.destination);
    o.start(time); o.stop(time + 0.06);
  }
  function scheduler() {
    const c = Audio.getCtx();
    // 0.3s lookahead survives background-tab timer throttling (locked
    // phone screen mid-practice) at the cost of bpm changes applying a
    // beat or so late.
    while (nextNoteTime < c.currentTime + 0.3) {
      // Accent ONLY the bar's downbeat — `current` counts subdivision
      // ticks through a 4/4 bar (subdiv * 4 of them).
      const accent = (current % (subdiv * 4)) === 0;
      click(nextNoteTime, accent);
      nextNoteTime += 60.0 / bpm / subdiv;
      current = (current + 1) % (subdiv * 4);
    }
    schedTimer = setTimeout(scheduler, 25);
  }
  startBtn.addEventListener('click', () => {
    const c = Audio.getCtx();
    if (running) {
      running = false;
      clearTimeout(schedTimer);
      startBtn.textContent = 'Start';
      startBtn.classList.remove('on');
    } else {
      running = true;
      current = 0;
      nextNoteTime = c.currentTime + 0.05;
      scheduler();
      startBtn.textContent = 'Stop';
      startBtn.classList.add('on');
    }
  });
  let tapTimes = [];
  tapBtn.addEventListener('click', () => {
    const now = Date.now();
    tapTimes.push(now);
    tapTimes = tapTimes.filter(t => now - t < 2500);
    if (tapTimes.length >= 2) {
      const intervals = [];
      for (let i = 1; i < tapTimes.length; i++) intervals.push(tapTimes[i] - tapTimes[i-1]);
      const avg = intervals.reduce((a,b)=>a+b,0) / intervals.length;
      const newBpm = Math.round(60000 / avg);
      if (newBpm >= 40 && newBpm <= 240) {
        bpm = newBpm; currentBpm = newBpm;
        bpmInput.value = newBpm; bpmLabel.textContent = newBpm;
        localStorage.setItem('ascendancy-bpm', newBpm);
      }
    }
  });
  // Silence everything (audio + metronome)
  const silenceBtn = document.getElementById('metro-silence');
  silenceBtn.addEventListener('click', () => {
    if (typeof stopCard === 'function') stopCard();
    if (running) {
      running = false;
      clearTimeout(schedTimer);
      startBtn.textContent = 'Start';
      startBtn.classList.remove('on');
    }
  });
  // Volume control
  const volInput = document.getElementById('metro-vol');
  const volLabel = document.getElementById('metro-vol-label');
  const savedVol = parseInt(localStorage.getItem('ascendancy-vol') || '80', 10);
  volInput.value = savedVol;
  volLabel.textContent = savedVol;
  Audio.setVolume(savedVol / 100);
  volInput.addEventListener('input', () => {
    const v = parseInt(volInput.value, 10);
    volLabel.textContent = v;
    Audio.setVolume(v / 100);
    localStorage.setItem('ascendancy-vol', v);
  });
})();

// Global keyboard shortcut: ESC stops everything
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && typeof stopCard === 'function') {
    stopCard();
    const mb = document.getElementById('modal-backdrop');
    if (mb && !mb.classList.contains('open')) {
      // ESC outside the modal also stops audio
    }
  }
});

// Unlock the AudioContext on the user's very first interaction. iOS Safari
// refuses to make sound until a context is created (or resumed) inside a
// touch / click handler — this guarantees it gets one.
(function() {
  let unlocked = false;
  function unlock() {
    if (unlocked) return;
    try {
      const c = Audio.getCtx();
      if (c.state === 'suspended') c.resume();
      // A 1-sample silent buffer "primes" the audio system on iOS.
      const buf = c.createBuffer(1, 1, 22050);
      const src = c.createBufferSource();
      src.buffer = buf;
      src.connect(c.destination);
      src.start(0);
    } catch (e) {}
    unlocked = true;
    ['touchstart', 'touchend', 'mousedown', 'keydown', 'click'].forEach(ev => {
      document.removeEventListener(ev, unlock, true);
    });
  }
  ['touchstart', 'touchend', 'mousedown', 'keydown', 'click'].forEach(ev => {
    document.addEventListener(ev, unlock, true);
  });
})();

// ── Service worker ────────────────────────────────────────────────────
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./sw.js').catch(() => {});
}
'''


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _topbar(current_slug, exercises):
    options = ''.join(
        f'<option value="{html.escape(e["slug"], quote=True)}.html"{" selected" if e["slug"] == current_slug else ""}>'
        f'{html.escape(e["title_one"], quote=True)} {html.escape(e["title_em"], quote=True)}</option>'
        for e in exercises
    )
    return f'''<div class="topbar">
  <a class="home-link" href="./index.html">← All exercises</a>
  <div class="ex-switch">
    <span class="ex-switch-label">Exercise</span>
    <select onchange="if(this.value)window.location.href=this.value;">
      {options}
    </select>
  </div>
</div>'''


def _title_block(ex):
    # eyebrow / title_one / title_em / subtitle are plain text — escape at sink.
    return f'''<header class="title-block">
  <p class="eyebrow">{html.escape(ex["eyebrow"], quote=True)}</p>
  <h1>{html.escape(ex["title_one"], quote=True)} <em>{html.escape(ex["title_em"], quote=True)}</em></h1>
  <p class="subtitle">{html.escape(ex["subtitle"], quote=True)}</p>
</header>'''


def _legend(ex):
    prose = ex.get("intro_prose", "")
    pills = ex.get("intro_pills", [])
    if pills:
        pills_html = '<div class="pills">' + ''.join(
            f'<div class="pill"><h3>{label}</h3><p>{body}</p></div>'
            for label, body in pills
        ) + '</div>'
        return f'<section class="legend"><div class="legend-prose">{prose}</div>{pills_html}</section>'
    return f'<section class="legend no-pills"><div class="legend-prose">{prose}</div></section>'


def _card_html(c):
    title = c.get("title", "")
    role = c.get("role", "")
    body = c.get("body", "")
    caption = c.get("caption", "")
    num = c.get("num", "")
    audio = c.get("audio")
    together = c.get("audio_together")
    # title/role are plain text; escape them at the HTML sinks (attribute +
    # tight element contexts). body/caption are INTENTIONAL prose HTML — never escape.
    title_esc = html.escape(title, quote=True)
    role_esc = html.escape(role, quote=True)
    audio_attr = ''
    play_btn = ''
    # html.escape the JSON: today's payloads are numeric, but the first
    # string field an author adds must not be able to truncate the attribute.
    if audio:
        audio_attr = f' data-audio="{html.escape(json.dumps(audio), quote=True)}"'
        play_btn = (f'<button class="card-play" type="button" '
                    f'aria-label="Play {title_esc}"></button>' if title else
                    '<button class="card-play" type="button" aria-label="Play"></button>')
    # A second, optional sequence that layers all of a section's guitars so it
    # can be played as a full band (the modal exposes a "Together" button).
    if together:
        audio_attr += f' data-audio-together="{html.escape(json.dumps(together), quote=True)}"'
    return (
        f'<article class="card" data-title="{title_esc}" data-role="{role_esc}"{audio_attr}>'
        + play_btn
        + (f'<div class="key-num">{num}</div>' if num else '')
        + (f'<h3>{title_esc}</h3>' if title else '')
        + (f'<p class="role">{role_esc}</p>' if role else '')
        + body
        + (f'<p class="caption">{caption}</p>' if caption else '')
        + '</article>'
    )


def _cards(ex):
    sections_html = []
    for sect in ex.get("sections", []):
        heading = sect.get("heading", "")
        blurb = sect.get("blurb", "")
        layout = sect.get("layout", "auto")
        cards_html = ''.join(_card_html(c) for c in sect["cards"])
        layout_class = '' if layout == 'auto' else f' {layout}'
        sections_html.append(
            (f'<h2 class="section-heading">{heading}</h2>' if heading else '')
            + (f'<p class="section-blurb">{blurb}</p>' if blurb else '')
            + f'<section class="cards{layout_class}">' + cards_html + '</section>'
        )
    return '\n'.join(sections_html)


def _next_step(ex):
    ns = ex.get("next_step")
    if not ns:
        return ''
    items_html = ''
    if ns.get("items"):
        items_html = '<ul>' + ''.join(
            f'<li><strong>{label}.</strong> {body}</li>' for label, body in ns["items"]
        ) + '</ul>'
    body = ns.get("body", "")
    head = f'<h2>{ns.get("heading_one", "")}<em>{ns.get("heading_em", "")}</em>{ns.get("heading_two", "")}</h2>'
    return f'<aside class="next-step">{head}{body}{items_html}</aside>'


def _closing(ex):
    c = ex.get("closing")
    if not c:
        return ''
    return f'<p class="closing">{c}</p>'


def _ex_footer(ex, exercises):
    """Prev/next exercise links at the bottom of each page."""
    sorted_ex = sorted(exercises, key=lambda e: e.get('order', 999))
    idx = next((i for i, e in enumerate(sorted_ex) if e['slug'] == ex['slug']), None)
    if idx is None:
        return ''
    prev_html = '<span class="ef-prev disabled">First exercise</span>'
    next_html = '<span class="ef-next disabled">Last exercise</span>'
    if idx > 0:
        p = sorted_ex[idx - 1]
        prev_html = (f'<a class="ef-prev" href="./{p["slug"]}.html">'
                     f'{html.escape(p["title_one"])} {html.escape(p["title_em"])}</a>')
    if idx < len(sorted_ex) - 1:
        nxt = sorted_ex[idx + 1]
        next_html = (f'<a class="ef-next" href="./{nxt["slug"]}.html">'
                     f'{html.escape(nxt["title_one"])} {html.escape(nxt["title_em"])}</a>')
    return f'<nav class="ex-footer">{prev_html}{next_html}</nav>'


def _modal_html():
    return '''<div class="modal-backdrop" id="modal-backdrop" role="dialog" aria-modal="true">
  <div class="modal-frame">
    <button class="modal-close" id="modal-close" aria-label="Close">×</button>
    <h2 class="modal-title" id="modal-title"></h2>
    <p class="modal-role" id="modal-role"></p>
    <div id="modal-body"></div>
    <div class="modal-actions">
      <div class="left">
        <button id="modal-prev">← Prev</button>
        <button id="modal-next">Next →</button>
      </div>
      <div class="right">
        <button id="modal-loop" class="modal-loop" aria-label="Loop playback (cycles off → ∞ → 4× → 2×)">↻ Loop</button>
        <button id="modal-together" class="modal-together" aria-label="Play all guitar parts together">▶ Together</button>
        <button id="modal-play" class="modal-play">▶ Play</button>
      </div>
    </div>
  </div>
</div>'''


def _metro_html():
    return '''<div class="metro">
  <div class="metro-panel" id="metro-panel">
    <label>Tempo <span id="metro-bpm-label">80</span> bpm</label>
    <input type="range" id="metro-bpm" min="40" max="240" value="80"/>
    <label>Volume <span id="metro-vol-label">80</span>%</label>
    <input type="range" id="metro-vol" min="0" max="100" value="80"/>
    <div class="metro-row">
      <button class="metro-sub" data-sub="1">♩</button>
      <button class="metro-sub" data-sub="2">♫</button>
      <button class="metro-sub" data-sub="3">3</button>
      <button class="metro-sub" data-sub="4">4</button>
    </div>
    <div class="metro-row">
      <button id="metro-start">Start</button>
      <button id="metro-tap">Tap</button>
    </div>
    <div class="metro-row">
      <button id="metro-silence" style="background:#b91c1c;color:#f5efe2;border-color:#b91c1c;">⏹ Silence all</button>
    </div>
  </div>
  <button class="metro-btn" id="metro-btn" aria-label="Metronome">♩</button>
</div>'''


PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Ascendancy Trainer</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="icon" type="image/svg+xml" href="{icon_data_uri}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Ascendancy">
<meta name="theme-color" content="#0b0b0d">
<style>{css}</style>
</head>
<body>
<main class="page">
{topbar}
{title_block}
{legend}
{cards}
{next_step}
{closing}
{ex_footer}
{site_footer}
</main>
{modal}
{metro}
<script>{js}</script>
</body>
</html>
'''


def build_page(ex, exercises):
    page_html = PAGE_TEMPLATE.format(
        title=html.escape(f'{ex["title_one"]} {ex["title_em"]}', quote=True),
        icon_data_uri=ICON_DATA_URI,
        css=PAGE_CSS,
        topbar=_topbar(ex["slug"], exercises),
        title_block=_title_block(ex),
        legend=_legend(ex),
        cards=_cards(ex),
        next_step=_next_step(ex),
        closing=_closing(ex),
        ex_footer=_ex_footer(ex, exercises),
        site_footer=_site_footer(),
        modal=_modal_html(),
        metro=_metro_html(),
        js=PAGE_JS,
    )
    out_path = os.path.join(ROOT, f'{ex["slug"]}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# Landing page
# ─────────────────────────────────────────────────────────────────────────────

# Index-only CSS kept as a separate raw (non-.format()) string so its literal
# `{` / `}` don't need brace-doubling. It's concatenated onto PAGE_CSS and passed
# as the {css} field below.
INDEX_CSS = r'''
.index-grid {
  display: grid; gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}
.index-card {
  background: var(--card); color: var(--card-ink);
  padding: 1.7rem 1.2rem 1.4rem; border-radius: 6px;
  border: 1px solid var(--card-edge);
  text-decoration: none; display: block;
  transition: transform 120ms, box-shadow 120ms;
  position: relative; isolation: isolate;
}
/* Blood drip off the top edge — same effect as the practice cards */
.index-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 64px;
  background: url("__DRIP_URI__") repeat-x left top;
  background-size: 220px 70px;
  border-radius: 6px 6px 0 0;
  opacity: 0.72;
  pointer-events: none;
  z-index: 0;
}
.index-card > * { position: relative; z-index: 1; }
.index-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.28); }
.index-card:hover::before { opacity: 0.85; }
.index-card .eyebrow {
  text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.62rem;
  color: var(--accent-dark); font-variation-settings: 'opsz' 9, 'wght' 600;
  margin: 0 0 0.5rem;
}
.index-card h2 {
  margin: 0 0 0.4rem; font-size: 1.5rem;
  font-family: 'Blackletter', 'Fraunces', serif; font-weight: 700;
  line-height: 1.1; color: var(--card-ink);
}
.index-card h2 em { color: var(--accent-dark); font-style: normal; }
.index-card p { margin: 0; font-size: 0.92rem; color: var(--card-ink-soft); line-height: 1.45; }
.section-title {
  margin: 2.5rem 0 1rem; color: var(--ink); font-size: 1.5rem;
  font-family: 'Blackletter', 'Fraunces', serif; font-weight: 700;
}
.section-title em { color: var(--sage); font-style: normal; }
.index-intro {
  max-width: 56ch; color: var(--ink-soft); margin: 0 auto 2.5rem;
  text-align: center; font-size: 1.05rem;
}
.index-intro em { color: var(--sage); font-style: italic; }
.install-tip {
  margin: 3rem auto 0; max-width: 60ch; padding: 1.25rem 1.5rem;
  background: var(--paper-warm); border-radius: 6px;
  border-left: 3px solid var(--accent); color: var(--ink-soft); font-size: 0.92rem;
}
.install-tip strong { color: var(--accent); font-variation-settings: 'opsz' 14, 'wght' 600; }
.install-tip em { font-style: italic; color: var(--sage); }
'''.replace('__DRIP_URI__', DRIP_DATA_URI)

# NOTE: INDEX_TEMPLATE is .format()-ed. The CSS now lives in INDEX_CSS (above) and
# is injected via {css}, so it needs NO brace-doubling. Only the literal braces in
# the inline <script> at the bottom still must be doubled ({{ }}).
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Ascendancy Trainer · Trivium in Drop D</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="icon" type="image/svg+xml" href="{icon_data_uri}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Ascendancy">
<meta name="theme-color" content="#0b0b0d">
<style>{css}</style>
</head>
<body>
<main class="page">
<header class="title-block">
  <p class="eyebrow">Trivium · Drop D · Practice Library</p>
  <h1>Ascendancy <em>Trainer</em></h1>
  <p class="subtitle">Every skill the title track demands, one exercise at a time.</p>
</header>
<p class="index-intro">
  A practice companion for learning <em>Ascendancy</em> by Trivium — drop D
  tuning, gallop picking, F# minor riff vocabulary, harmonized twin leads,
  and a section-by-section plan for assembling the song. Work these pages
  alongside the official tab: the tab tells you the notes, these exercises
  build the hands that play them.
</p>
{sections}
<div class="install-tip">
  <strong>Install on iOS:</strong> tap the share icon in Safari, then
  <em>Add to Home Screen</em>. Works offline once cached. Tap any card to play it back.
</div>
{site_footer}
</main>
<script>
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('./sw.js').catch(() => {{}});
}}
</script>
</body>
</html>
'''


def build_index(exercises):
    sections = {}
    for ex in exercises:
        sec = ex.get("section", "Other")
        sections.setdefault(sec, []).append(ex)

    sections_html = []
    section_order = ["Setup", "Rhythm Engine", "Scales", "Twin Leads", "The Song", "Practice"]
    ordered_sections = [s for s in section_order if s in sections] + [s for s in sections if s not in section_order]

    for sec_name in ordered_sections:
        items = sections[sec_name]
        items.sort(key=lambda e: e.get("order", 999))
        cards_html = []
        for ex in items:
            cards_html.append(
                f'<a class="index-card" href="./{html.escape(ex["slug"], quote=True)}.html">'
                f'<p class="eyebrow">{html.escape(ex.get("eyebrow_short", ex["eyebrow"]), quote=True)}</p>'
                f'<h2>{html.escape(ex["title_one"], quote=True)} <em>{html.escape(ex["title_em"], quote=True)}</em></h2>'
                f'<p>{html.escape(ex["subtitle"], quote=True)}</p></a>'
            )
        sections_html.append(
            f'<h2 class="section-title"><em>{html.escape(sec_name, quote=True)}</em></h2>'
            f'<section class="index-grid">{"".join(cards_html)}</section>'
        )

    index_html = INDEX_TEMPLATE.format(
        icon_data_uri=ICON_DATA_URI,
        css=PAGE_CSS + INDEX_CSS,
        sections='\n'.join(sections_html),
        site_footer=_site_footer(),
    )
    out_path = os.path.join(ROOT, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# Manifest + service worker + icon
# ─────────────────────────────────────────────────────────────────────────────

MANIFEST = {
    "name": "Ascendancy · Trivium Guitar Trainer",
    "short_name": "Ascendancy",
    "description": "Drop D trainer for Trivium's Ascendancy — gallops, riffs, scales, twin leads.",
    "start_url": "./index.html",
    "scope": "./",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#120d0d",
    "theme_color": "#0b0b0d",
    "icons": [
        {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any maskable"},
        {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml"},
    ],
}


# WARNING: SW_TEMPLATE is .format()-ed — every literal JS `{`/`}` below MUST be
# doubled (`{{`/`}}`). Only {ver} and {precache} are real format fields. (Left
# inline rather than extracted because the braces are interleaved with the only
# two substitutions; splitting it out is riskier than the brace-doubling.)
SW_TEMPLATE = '''const VERSION = '{ver}';
const CACHE = `ascendancy-${{VERSION}}`;
const PRECACHE = {precache};
self.addEventListener('install', (e) => {{
  // cache:'reload' bypasses the HTTP cache so a new SW version can't be
  // filled with stale responses (GitHub Pages serves max-age=600).
  e.waitUntil(caches.open(CACHE).then((c) =>
    c.addAll(PRECACHE.map((u) => new Request(u, {{cache: 'reload'}})))));
  self.skipWaiting();
}});
self.addEventListener('activate', (e) => {{
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
  ).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', (e) => {{
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  e.respondWith(
    caches.match(req, {{ignoreSearch: req.mode === 'navigate'}}).then((hit) => hit || fetch(req).then((resp) => {{
      if (resp && resp.status === 200 && resp.type === 'basic') {{
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
      }}
      return resp;
    }}).catch((err) => {{
      // Offline fallback is for page navigations only — an icon or manifest
      // request must not get an HTML body.
      if (req.mode === 'navigate') return caches.match('./index.html');
      throw err;
    }}))
  );
}});
'''


def build_assets(exercises):
    with open(os.path.join(ROOT, 'icon.svg'), 'w', encoding='utf-8') as f:
        f.write(ICON_SVG)
    with open(os.path.join(ROOT, 'manifest.webmanifest'), 'w', encoding='utf-8') as f:
        json.dump(MANIFEST, f, indent=2)
    precache = ['./', './index.html'] + [f'./{e["slug"]}.html' for e in exercises] + [
        './manifest.webmanifest', './apple-touch-icon.png', './icon.svg'
    ]
    sw = SW_TEMPLATE.format(ver=f'v{int(time.time())}', precache=json.dumps(precache))
    with open(os.path.join(ROOT, 'sw.js'), 'w', encoding='utf-8') as f:
        f.write(sw)
