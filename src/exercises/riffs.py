"""Riff vocabulary — original etudes in the song's dialect.

These are NOT the song's riffs. They are practice etudes built from the
same devices — the fretted F♯ pedal point, chromatic low-string crawls,
syncopated break stabs, and clean arpeggiated chords — so that when you
read the real parts from the tab, your hands already speak the language.
"""

from _common import (n, c, r, tab_card, PC_ROLES, D5_SHAPE, FS5_SHAPE,
                     B5_SHAPE, CS5_SHAPE, D5, FS5, B5, CS5)


def chug(dur=0.5, accent=False):
    return n(6, 4, dur, pm=True, accent=accent)


def gallop(accent=True):
    # One beat of gallop: eighth + two sixteenths on the F# pedal.
    return [chug(0.5, accent), chug(0.25), chug(0.25)]


# ── Etude 1: pedal-point riff ────────────────────────────────────────
# Fretted F♯ pedal (string 6, fret 4) with chord punches dropped
# between the gallops — the verse engine of the song.
PEDAL_BARS = [
    gallop() + gallop() +
    [c(D5, 0.5, accent=True), chug(0.5), c(B5, 0.5, accent=True), chug(0.5)],
    gallop() + gallop() +
    [c(CS5, 1.0, accent=True), c(B5, 0.5, accent=True), chug(0.5)],
    gallop() + gallop() +
    [c(D5, 0.5, accent=True), chug(0.5), c(B5, 0.5, accent=True), chug(0.5)],
    [c(D5, 1.0, accent=True), c(CS5, 1.0, accent=True), c(FS5, 2.0, accent=True)],
]
PEDAL_LABELS = ['F♯ ped · D5 B5', '· C♯5 B5', '· D5 B5', 'D5 C♯5 F♯5']

PEDAL_CHORDS = [
    ('F♯5 — pedal', FS5_SHAPE, PC_ROLES),
    ('D5', D5_SHAPE, PC_ROLES),
    ('B5', B5_SHAPE, PC_ROLES),
    ('C♯5', CS5_SHAPE, PC_ROLES),
]


# ── Etude 2: chromatic low-string crawl ──────────────────────────────
# The thrash device: palm-muted single notes crawling down the low
# string a half-step at a time, resolving into the fretted F♯ pedal.
CHROMA_BARS = [
    [n(6, 7, 0.5, pm=True, accent=True), n(6, 7, 0.5, pm=True),
     n(6, 6, 0.5, pm=True), n(6, 6, 0.5, pm=True),
     n(6, 5, 0.5, pm=True, accent=True), n(6, 5, 0.5, pm=True),
     n(6, 4, 0.5, pm=True), n(6, 4, 0.5, pm=True)],
    [n(6, 3, 0.5, pm=True, accent=True), n(6, 3, 0.5, pm=True),
     chug(0.5, True), chug(0.5), chug(0.5), chug(0.5), chug(0.5), chug(0.5)],
    [n(6, 4, 0.5, pm=True, accent=True), n(6, 5, 0.5, pm=True),
     n(6, 6, 0.5, pm=True), n(6, 7, 0.5, pm=True),
     n(6, 6, 0.5, pm=True, accent=True), n(6, 5, 0.5, pm=True),
     n(6, 4, 0.5, pm=True), n(6, 3, 0.5, pm=True)],
    [n(6, 4, 4.0, accent=True)],
]
CHROMA_LABELS = ['A G♯ G F♯', 'E♯ → F♯ pedal', 'climb & fall', 'F♯ ring']


# ── Etude 3: syncopated break stabs ──────────────────────────────────
# Stabs and silence, mirroring the song's Break. The rests are the riff.
BREAK_BARS = [
    [c(FS5, 0.5, accent=True), r(0.5), r(0.5), c(FS5, 0.5, accent=True),
     r(0.5), c(FS5, 0.5, accent=True), c(D5, 0.5, accent=True), r(0.5)],
    [c(D5, 0.5, accent=True), r(0.5), c(D5, 0.5, accent=True), r(0.5),
     c(FS5, 0.5, accent=True), r(0.5), r(0.5), r(0.5)],
    [c(FS5, 0.5, accent=True), r(0.5), r(0.5), c(FS5, 0.5, accent=True),
     r(0.5), c(FS5, 0.5, accent=True), c(D5, 0.5, accent=True), r(0.5)],
    [c(D5, 0.5, accent=True), c(D5, 0.5), c(D5, 0.5, accent=True), c(D5, 0.5),
     c(FS5, 2.0, accent=True)],
]
BREAK_LABELS = ['F♯5 · F♯5 F♯5 D5', 'D5 D5 F♯5', 'F♯5 · F♯5 F♯5 D5', 'D5 → F♯5']

BREAK_CHORDS = [
    ('F♯5', FS5_SHAPE, PC_ROLES),
    ('D5', D5_SHAPE, PC_ROLES),
]


# ── Etude 4: clean arpeggio interlude ────────────────────────────────
# The song's dynamic trick: drop to clean, let chords ring, then slam
# back in. F♯m → D → E → F♯m, picked as broken chords.
FSM_ARP = [n(4, 4, 0.5), n(3, 2, 0.5), n(2, 2, 0.5), n(1, 2, 0.5),
           n(2, 2, 0.5), n(3, 2, 0.5), n(2, 2, 0.5), n(1, 2, 0.5)]
D_ARP   = [n(4, 0, 0.5), n(3, 2, 0.5), n(2, 3, 0.5), n(1, 2, 0.5),
           n(2, 3, 0.5), n(3, 2, 0.5), n(2, 3, 0.5), n(1, 2, 0.5)]
E_ARP   = [n(4, 2, 0.5), n(3, 1, 0.5), n(2, 0, 0.5), n(1, 0, 0.5),
           n(2, 0, 0.5), n(3, 1, 0.5), n(2, 0, 0.5), n(1, 0, 0.5)]
ARP_BARS = [FSM_ARP, D_ARP, E_ARP,
            [c([(4, 4), (3, 2), (2, 2), (1, 2)], 4.0, accent=True)]]
ARP_LABELS = ['F♯m', 'D', 'E', 'F♯m']

ARP_CHORDS = [
    ('F♯m', [None, None, 4, 2, 2, 2], {4: 'R', 3: 'b3', 2: '5', 1: 'R'}),
    ('D',   [None, None, 0, 2, 3, 2], {4: 'R', 3: '5', 2: 'R', 1: '3'}),
    ('E',   [None, None, 2, 1, 0, 0], {4: 'R', 3: '3', 2: '5', 1: 'R'}),
]


EXERCISE = {
    "slug": "riffs",
    "order": 3,
    "section": "Rhythm Engine",
    "title_one": "Riff",
    "title_em": "vocabulary",
    "eyebrow": "Etudes in the Song's Dialect",
    "eyebrow_short": "Riffs",
    "subtitle": "Pedal point, chromatic crawls, break stabs, clean interludes.",
    "intro_prose": """
      <p>These four etudes are <em>original practice riffs</em>, not the
      song — for the real parts, read the official tab. What they teach is
      the song's riff <strong>grammar</strong>: a galloping pedal on the
      fretted F♯ interrupted by chord punches, chromatic crawls on the low
      string, a break where the silence hits as hard as the stabs, and the
      clean, ringing passages that set up the next wall of distortion.</p>
      <p>Learn each etude from the tab below, loop the audio, and only
      then raise the tempo — the song lives at ♩=212, so every device has
      to be clean long before it's fast. Each one maps directly onto a
      section of the real song.</p>
    """,
    "intro_pills": [
        ("F♯ minor world", "The riffs orbit F♯ · A · B · C♯ · E — chord tones of F♯ minor — plus D (the ♭6) and G♯ (the 2) where the lines walk through them."),
        ("Dynamics", "Palm-muted tight vs. open and ringing. The contrast is the drama."),
    ],
    "sections": [
        {
            "heading": "Etude 1 — pedal point",
            "blurb": "The fretted low F♯ keeps galloping while chords flash above it. This is the single most important move in the song's rhythm playing.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 1", "F♯ pedal with chord punches",
                    "Gallops · pedal muted, punches open and accented",
                    PEDAL_BARS, PEDAL_LABELS,
                    "Two textures in one bar: <em>thump</em> (muted gallop on fret 4) and <em>bark</em> (open punch). The instant the chord sounds, your palm lifts; the instant it's done, the mute re-seats. <strong>The hardest move here is the C♯5 punch</strong> — your index finger leaves the pedal at fret 4 and the whole hand leaps to fret 11, then snaps back. Practise bar 2 alone, dead slow, eyes on fret 11's target before you jump; only re-join the loop when the leap lands without a flam.",
                    bars_per_line=2, width=900, chords=PEDAL_CHORDS, gain=0.5),
            ],
        },
        {
            "heading": "Etude 2 — chromatic crawl",
            "blurb": "Single palm-muted notes walking down the low string a half-step at a time — pure thrash DNA, and it shows up whenever the song wants menace.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 2", "Chromatic descent to the fretted pedal",
                    "Alternate picking · strict palm mute · accents mark the shifts",
                    CHROMA_BARS, CHROMA_LABELS,
                    "Note names, fret by fret: A (7) → G♯ (6) → <strong>G (5), the chromatic passing tone</strong> outside the key — it exists only to connect G♯ to F♯ — then F♯ (4), home. Bar 2 opens on <strong>E♯ (3) — the verse's leading tone, a half step under the root</strong>; the song itself leans on this note before resolving up into F♯. Fingering: one finger per fret, hand drifting down the neck. Bar 3 reverses the motion — climb up, fall back. Keep every note the same length; chromatic runs expose uneven picking instantly.",
                    bars_per_line=2, width=900, gain=0.5),
            ],
        },
        {
            "heading": "Etude 3 — break stabs",
            "blurb": "Syncopation straight from the song's Break: chords land off the grid and the gaps stay dead silent. Count out loud — this one is won or lost in the rests.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 3", "Syncopated break stabs",
                    "F♯5 / D5 stabs + dead silence · choke every rest with both hands",
                    BREAK_BARS, BREAK_LABELS,
                    "After each stab, kill the strings: fretting hand relaxes (without lifting), picking palm drops flat. The groove lives in how <em>black</em> the silences are. Tap your foot on quarters the whole way through — bar 4 piles the D5 hits up and resolves them into a ringing F♯5.",
                    bars_per_line=2, width=900, chords=BREAK_CHORDS, gain=0.5),
            ],
        },
        {
            "heading": "Etude 4 — clean interlude",
            "blurb": "The breath before the next assault. Broken chords, every note ringing into the next — the exact opposite of everything above.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 4", "Arpeggiated F♯m — D — E",
                    "Let ring · fingers stay planted on the chord shape",
                    ARP_BARS, ARP_LABELS,
                    "The key's three pillars, broken open. F♯m: F♯3 root (4,4) · A3 ♭3 (3,2) · C♯4 5th (2,2) · F♯4 octave (1,2). D: D3 root (4,0) · A3 5th (3,2) · D4 octave (2,3) · F♯4 3rd (1,2). E: E3 root (4,2) · G♯3 3rd (3,1) · B3 5th (2,0) · E4 octave (1,0). Plant the whole chord shape first, then pick through it — never assemble it note by note. Maximum sustain, minimum pick attack. Practising loud-to-quiet transitions (Etude 1 straight into this) trains the song's biggest dynamic moves.",
                    bars_per_line=2, width=900, chords=ARP_CHORDS, strum=False),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Now read the ",
        "heading_em": "real parts",
        "heading_two": "",
        "body": "<p>With these four devices under your fingers, open the official tab and start matching: which sections gallop on the F♯ pedal? Where does the E♯ leading tone appear? Which hits are the Break's stabs? The <a href=\"./roadmap.html\" style=\"color:var(--accent);font-weight:600;\">song roadmap</a> page walks the structure section by section.</p>",
        "items": [
            ("One etude a day", "Rotate them. Each one is a different hand skill; none substitutes for another."),
            ("Transitions", "Practise jumping between etudes without stopping — Etude 1 into 4 into 3. The song never gives you a reset bar."),
            ("Write one", "Compose your own 2-bar riff using the F♯ pedal + one chromatic move. If you can write in the dialect, you can read it fluently."),
        ],
    },
    "closing": "Learn the grammar, then read the song like a native.",
}
