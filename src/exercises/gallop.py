"""Gallop picking — the rhythmic engine of Ascendancy.

Down-down-up on the open low D, palm-muted, at speed. Every heavy
section of the song runs on this motor (or its reverse). These drills
are progressive: straight eighths → gallop → reverse gallop → gallop
with chord punches.
"""

from _common import (n, c, tab_card, PC_ROLES, D5_SHAPE, F5_SHAPE, G5_SHAPE,
                     F5, G5)


def chug(dur=0.5, accent=False):
    """One palm-muted hit on the open low D."""
    return n(6, 0, dur, pm=True, accent=accent)


# ── Drill 1: straight eighths ────────────────────────────────────────
EIGHTHS_BAR = [chug(0.5, accent=(i % 4 == 0)) for i in range(8)]
EIGHTHS_BARS = [EIGHTHS_BAR, EIGHTHS_BAR]


# ── Drill 2: the gallop (eighth + two sixteenths) ────────────────────
def gallop_beat(accent=True):
    return [chug(0.5, accent=accent), chug(0.25), chug(0.25)]


GALLOP_BAR = sum([gallop_beat() for _ in range(4)], [])
GALLOP_BARS = [GALLOP_BAR, GALLOP_BAR]


# ── Drill 3: reverse gallop (two sixteenths + eighth) ────────────────
def rev_gallop_beat(accent=True):
    return [chug(0.25, accent=accent), chug(0.25), chug(0.5)]


REV_BAR = sum([rev_gallop_beat() for _ in range(4)], [])
REV_BARS = [REV_BAR, REV_BAR]


# ── Drill 4: gallop with chord punches ───────────────────────────────
# Three gallop beats on the pedal, then a power-chord punch on beat 4.
PUNCH_BARS = [
    gallop_beat() + gallop_beat(accent=False) + gallop_beat(accent=False)
    + [c(F5, 1.0, accent=True)],
    gallop_beat() + gallop_beat(accent=False) + gallop_beat(accent=False)
    + [c(G5, 1.0, accent=True)],
    gallop_beat() + gallop_beat(accent=False) + gallop_beat(accent=False)
    + [c(F5, 0.5, accent=True), c(G5, 0.5, accent=True)],
    [n(6, 0, 4.0, accent=True)],
]
PUNCH_LABELS = ['…F5', '…G5', '…F5 G5', 'D ring']

PUNCH_CHORDS = [
    ('D5 — the pedal', D5_SHAPE, PC_ROLES),
    ('F5 — fret 3', F5_SHAPE, PC_ROLES),
    ('G5 — fret 5', G5_SHAPE, PC_ROLES),
]


EXERCISE = {
    "slug": "gallop",
    "order": 2,
    "section": "Rhythm Engine",
    "title_one": "Gallop",
    "title_em": "picking",
    "eyebrow": "The Motor of the Song",
    "eyebrow_short": "Gallop",
    "subtitle": "Down-down-up on a palm-muted low D — the metalcore heartbeat.",
    "intro_prose": """
      <p>Strip the song to its skeleton and you'll find this: a palm-muted
      open low D played in a <strong>gallop</strong> — an eighth note
      followed by two sixteenths, <em>da-ga-da, da-ga-da</em>, like hooves.
      Trivium's fast rhythm playing alternates between the gallop and its
      mirror image, the <strong>reverse gallop</strong> (two sixteenths
      into an eighth), often inside the same riff.</p>
      <p>Pick it <em>down-down-up</em>. Anchor the heel of your picking
      hand on the strings just in front of the bridge — enough pressure to
      choke the ring, not enough to bend the pitch sharp. Start far slower
      than feels necessary. The gallop falls apart from the top down: it's
      clean at 90, sloppy at 120, and gone at 150 unless the slow reps
      were honest.</p>
    """,
    "intro_pills": [
        ("Picking", "Gallop = down-down-up. Reverse gallop = down-up-down. Never all downstrokes at speed."),
        ("Palm mute", "Heel of the hand at the bridge. The note should thump, not ring."),
    ],
    "sections": [
        {
            "heading": "Step 1 — straight eighths",
            "blurb": "Before subdividing, lock plain eighth notes to the click. Accent beats 1 and 3. Every note identical: same volume, same mute depth, same attack.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Drill 1", "Eighth-note chug on open D",
                    "All downstrokes · palm-muted · accents on 1 and 3",
                    EIGHTHS_BARS, None,
                    "Boring is the point. Two minutes of perfectly even chugging teaches your hand the mute depth and pick angle everything else is built on.",
                    bars_per_line=2, width=760, gain=0.5),
            ],
        },
        {
            "heading": "Step 2 — the gallop",
            "blurb": "One eighth + two sixteenths per beat: <em>DA-ga-da</em>. The accent lands on the eighth, picked with a downstroke, every beat.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Drill 2", "The gallop — four per bar",
                    "Eighth + two sixteenths · down-down-up · accent the front",
                    GALLOP_BARS, None,
                    "Count it &ldquo;<strong>1</strong>-and-a, <strong>2</strong>-and-a&rdquo;. The two sixteenths must be exactly even — the classic fault is rushing them into a flam. Loop this against the metronome and creep the tempo up 5&nbsp;bpm at a time.",
                    bars_per_line=2, width=760, gain=0.5),
            ],
        },
        {
            "heading": "Step 3 — the reverse gallop",
            "blurb": "Mirror image: two sixteenths + an eighth, <em>da-ga-DA</em>. This is the more thrash-flavoured cell, and the song mixes both freely.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Drill 3", "Reverse gallop — four per bar",
                    "Two sixteenths + eighth · down-up-down · accent beat-front",
                    REV_BARS, None,
                    "Harder than the forward gallop because the hand wants to rest <em>before</em> the long note, not after. If it lurches, halve the tempo and exaggerate the accent on the first sixteenth.",
                    bars_per_line=2, width=760, gain=0.5),
            ],
        },
        {
            "heading": "Step 4 — gallop with punches",
            "blurb": "Now the riff skill itself: keep the gallop running on the open pedal and land a power chord cleanly on beat 4 without breaking the motor.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Drill 4", "Pedal gallop + chord punches",
                    "Three gallop beats, chord on 4 · the verse-riff motion",
                    PUNCH_BARS, PUNCH_LABELS,
                    "The fretting hand jumps from nothing (open pedal) to a one-finger barre and back. <em>Release the palm mute for the chord</em> so it barks, then re-seat it instantly for the next gallop. Bar 3 doubles the punch rate — that's the harder move.",
                    bars_per_line=2, width=900, chords=PUNCH_CHORDS, gain=0.5),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Build the ",
        "heading_em": "tempo ladder",
        "heading_two": "",
        "body": "<p>Speed comes from accuracy compounded, not effort. Pick one drill per day and ladder it: clean for a full minute at one tempo earns +5&nbsp;bpm next time. Write your numbers down. When Drill 4 is clean at speed, the song's verse rhythm parts stop being scary — then go spell them out with the <a href=\"./riffs.html\" style=\"color:var(--accent);font-weight:600;\">riff vocabulary</a> page.</p>",
        "items": [
            ("Daily", "2 minutes of Drill 1 as a warm-up, always. Then your current ladder drill."),
            ("Honesty rule", "One flammed gallop = the minute doesn't count. Restart the clock."),
            ("Endurance", "The song holds this motor for minutes at a time. Once a drill is clean, double its duration before raising the tempo."),
        ],
    },
    "closing": "Da-ga-da, da-ga-da. The hooves that carry the whole song.",
}
