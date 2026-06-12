"""Riff vocabulary — original etudes in the song's dialect.

These are NOT the song's riffs. They are practice etudes built from the
same devices — open-D pedal point, chromatic low-string runs, syncopated
breakdown stabs, and clean arpeggiated chords — so that when you read
the real parts from the tab, your hands already speak the language.
"""

from _common import (n, c, r, tab_card, PC_ROLES, D5_SHAPE, F5_SHAPE,
                     G5_SHAPE, A5_SHAPE, C5_SHAPE, D5, F5, G5, A5, BB5, C5)


def chug(dur=0.5, accent=False):
    return n(6, 0, dur, pm=True, accent=accent)


# ── Etude 1: pedal-point riff ────────────────────────────────────────
# Open-D pedal with chord stabs dropped between the chugs.
PEDAL_BARS = [
    [chug(0.5, True), chug(0.5), c(F5, 0.5, accent=True), chug(0.5),
     chug(0.5), chug(0.5), c(G5, 0.5, accent=True), chug(0.5)],
    [chug(0.5, True), chug(0.5), c(A5, 0.5, accent=True), chug(0.5),
     chug(0.5), chug(0.5), c(C5, 0.5, accent=True), c(BB5, 0.5, accent=True)],
    [chug(0.5, True), chug(0.5), c(F5, 0.5, accent=True), chug(0.5),
     chug(0.5), chug(0.5), c(G5, 0.5, accent=True), chug(0.5)],
    [c(F5, 1.0, accent=True), c(G5, 1.0, accent=True), c(D5, 2.0, accent=True)],
]
PEDAL_LABELS = ['D ped · F5 G5', '· A5 C5 B♭5', '· F5 G5', 'F5 G5 D5']

PEDAL_CHORDS = [
    ('D5 — pedal', D5_SHAPE, PC_ROLES),
    ('F5', F5_SHAPE, PC_ROLES),
    ('G5', G5_SHAPE, PC_ROLES),
    ('A5', A5_SHAPE, PC_ROLES),
    ('C5', C5_SHAPE, PC_ROLES),
]


# ── Etude 2: chromatic low-string run ────────────────────────────────
# The thrash device: palm-muted single notes crawling chromatically on
# the dropped string, resolving back to the open pedal.
CHROMA_BARS = [
    [n(6, 5, 0.5, pm=True, accent=True), n(6, 5, 0.5, pm=True),
     n(6, 4, 0.5, pm=True), n(6, 4, 0.5, pm=True),
     n(6, 3, 0.5, pm=True, accent=True), n(6, 3, 0.5, pm=True),
     n(6, 2, 0.5, pm=True), n(6, 2, 0.5, pm=True)],
    [n(6, 1, 0.5, pm=True, accent=True), n(6, 1, 0.5, pm=True),
     chug(0.5, True), chug(0.5), chug(0.5), chug(0.5), chug(0.5), chug(0.5)],
    [n(6, 0, 0.5, pm=True, accent=True), n(6, 1, 0.5, pm=True),
     n(6, 2, 0.5, pm=True), n(6, 3, 0.5, pm=True),
     n(6, 5, 0.5, pm=True, accent=True), n(6, 3, 0.5, pm=True),
     n(6, 2, 0.5, pm=True), n(6, 1, 0.5, pm=True)],
    [n(6, 0, 4.0, accent=True)],
]
CHROMA_LABELS = ['G F♯ F E', 'E♭ → D pedal', 'climb & fall', 'D ring']


# ── Etude 3: syncopated breakdown ────────────────────────────────────
# Stabs and silence. The rests are the riff.
BREAK_BARS = [
    [c(D5, 0.5, accent=True), r(0.5), r(0.5), c(D5, 0.5, accent=True),
     r(0.5), c(D5, 0.5, accent=True), c(F5, 0.5, accent=True), r(0.5)],
    [c(G5, 0.5, accent=True), r(0.5), c(F5, 0.5, accent=True), r(0.5),
     c(D5, 0.5, accent=True), r(0.5), r(0.5), r(0.5)],
    [c(D5, 0.5, accent=True), r(0.5), r(0.5), c(D5, 0.5, accent=True),
     r(0.5), c(D5, 0.5, accent=True), c(F5, 0.5, accent=True), r(0.5)],
    [c(G5, 0.5, accent=True), c(G5, 0.5), c(F5, 0.5, accent=True), c(F5, 0.5),
     c(D5, 2.0, accent=True)],
]
BREAK_LABELS = ['D5 · D5 D5 F5', 'G5 F5 D5', 'D5 · D5 D5 F5', 'G5 F5 → D5']


# ── Etude 4: clean arpeggio interlude ────────────────────────────────
# The song's dynamic trick: drop to clean, let chords ring, then slam
# back in. Dm → B♭ → C → Dm, picked as broken chords.
DM_ARP = [n(4, 0, 0.5), n(3, 2, 0.5), n(2, 3, 0.5), n(1, 1, 0.5),
          n(2, 3, 0.5), n(3, 2, 0.5), n(2, 3, 0.5), n(1, 1, 0.5)]
BB_ARP = [n(5, 1, 0.5), n(4, 3, 0.5), n(3, 3, 0.5), n(2, 3, 0.5),
          n(3, 3, 0.5), n(4, 3, 0.5), n(3, 3, 0.5), n(2, 3, 0.5)]
C_ARP  = [n(5, 3, 0.5), n(4, 2, 0.5), n(3, 0, 0.5), n(2, 1, 0.5),
          n(3, 0, 0.5), n(4, 2, 0.5), n(3, 0, 0.5), n(2, 1, 0.5)]
ARP_BARS = [DM_ARP, BB_ARP, C_ARP,
            [c([(4, 0), (3, 2), (2, 3), (1, 1)], 4.0, accent=True)]]
ARP_LABELS = ['Dm', 'B♭', 'C', 'Dm']

ARP_CHORDS = [
    ('Dm', [None, None, 0, 2, 3, 1], {4: 'R', 3: '5', 2: 'R', 1: 'b3'}),
    ('B♭', [None, 1, 3, 3, 3, None], {5: 'R', 4: '5', 3: 'R', 2: '3'}),
    ('C',  [None, 3, 2, 0, 1, 0],   {5: 'R', 4: '3', 3: '5', 2: 'R', 1: '3'}),
]


EXERCISE = {
    "slug": "riffs",
    "order": 3,
    "section": "Rhythm Engine",
    "title_one": "Riff",
    "title_em": "vocabulary",
    "eyebrow": "Etudes in the Song's Dialect",
    "eyebrow_short": "Riffs",
    "subtitle": "Pedal point, chromatic runs, breakdown stabs, clean interludes.",
    "intro_prose": """
      <p>These four etudes are <em>original practice riffs</em>, not the
      song — for the real parts, read the official tab. What they teach is
      the song's riff <strong>grammar</strong>: a galloping open-D pedal
      interrupted by chord punches, chromatic crawls on the low string,
      breakdowns where the silence hits as hard as the stabs, and the
      clean, ringing passages that set up the next wall of distortion.</p>
      <p>Learn each etude from the tab below, loop the audio, and only
      then raise the tempo. Every device here maps directly onto a section
      of the real song.</p>
    """,
    "intro_pills": [
        ("D minor world", "The riffs orbit D · F · G · A · C · B♭ — chord tones of D minor."),
        ("Dynamics", "Palm-muted tight vs. open and ringing. The contrast is the drama."),
    ],
    "sections": [
        {
            "heading": "Etude 1 — pedal point",
            "blurb": "The open low D keeps galloping while chords flash above it. This is the single most important move in the song's rhythm playing.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 1", "Open-D pedal with chord stabs",
                    "Eighths · pedal muted, stabs open and accented",
                    PEDAL_BARS, PEDAL_LABELS,
                    "Two textures in one bar: <em>thump</em> (muted pedal) and <em>bark</em> (open stab). The instant the chord sounds, your palm lifts; the instant it's done, the mute re-seats. When this is clean, double-time the pedal notes into sixteenths.",
                    bars_per_line=2, width=900, chords=PEDAL_CHORDS, gain=0.5),
            ],
        },
        {
            "heading": "Etude 2 — chromatic crawl",
            "blurb": "Single palm-muted notes walking down the dropped string a half-step at a time — pure thrash DNA, and it shows up whenever the song wants menace.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 2", "Chromatic descent to the open pedal",
                    "Alternate picking · strict palm mute · accents mark the shifts",
                    CHROMA_BARS, CHROMA_LABELS,
                    "Fingering: one finger per fret, hand drifting down the neck. Bar 3 reverses the motion — climb up, fall back. Keep every note the same length; chromatic runs expose uneven picking instantly.",
                    bars_per_line=2, width=900, gain=0.5),
            ],
        },
        {
            "heading": "Etude 3 — breakdown stabs",
            "blurb": "Syncopation: chords land off the grid and the gaps stay dead silent. Count out loud — this one is won or lost in the rests.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 3", "Syncopated breakdown",
                    "Stabs + dead silence · choke every rest with both hands",
                    BREAK_BARS, BREAK_LABELS,
                    "After each stab, kill the strings: fretting hand relaxes (without lifting), picking palm drops flat. The groove lives in how <em>black</em> the silences are. Tap your foot on quarters the whole way through.",
                    bars_per_line=2, width=900, gain=0.5),
            ],
        },
        {
            "heading": "Etude 4 — clean interlude",
            "blurb": "The breath before the next assault. Broken chords, every note ringing into the next — the exact opposite of everything above.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Etude 4", "Arpeggiated Dm — B♭ — C",
                    "Let ring · fingers stay planted on the chord shape",
                    ARP_BARS, ARP_LABELS,
                    "Plant the whole chord shape first, then pick through it — never assemble it note by note. Maximum sustain, minimum pick attack. Practising loud-to-quiet transitions (Etude 1 straight into this) trains the song's biggest dynamic moves.",
                    bars_per_line=2, width=900, chords=ARP_CHORDS, strum=False),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Now read the ",
        "heading_em": "real parts",
        "heading_two": "",
        "body": "<p>With these four devices under your fingers, open the official tab and start matching: which sections gallop on the pedal? Where does the chromatic crawl appear? Which hits are breakdown stabs? The <a href=\"./roadmap.html\" style=\"color:var(--accent);font-weight:600;\">song roadmap</a> page walks the structure section by section.</p>",
        "items": [
            ("One etude a day", "Rotate them. Each one is a different hand skill; none substitutes for another."),
            ("Transitions", "Practise jumping between etudes without stopping — Etude 1 into 4 into 3. The song never gives you a reset bar."),
            ("Write one", "Compose your own 2-bar riff using the pedal + one chromatic move. If you can write in the dialect, you can read it fluently."),
        ],
    },
    "closing": "Learn the grammar, then read the song like a native.",
}
