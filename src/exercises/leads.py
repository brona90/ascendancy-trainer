"""Lead toolkit — the techniques the solo section demands.

Four builders, all original: legato cells, tremolo picking, bends with
vibrato, and an alternate-picked scale run. Each isolates one hand
skill the song's lead playing leans on.
"""

from _common import n, tab_card


# ── Builder 1: legato cells (hammer-on / pull-off triplets) ──────────
# One triplet cell per beat, walking across the 7–11 box of the F# minor
# pentatonic.
LEGATO_BARS = [
    [n(1, 9, 1/3, hammer_to=12, accent=True), n(1, 12, 1/3, pull_to=9), n(1, 9, 1/3),
     n(2, 10, 1/3, hammer_to=12, accent=True), n(2, 12, 1/3, pull_to=10), n(2, 10, 1/3),
     n(3, 9, 1/3, hammer_to=11, accent=True), n(3, 11, 1/3, pull_to=9), n(3, 9, 1/3),
     n(4, 9, 1/3, hammer_to=11, accent=True), n(4, 11, 1/3, pull_to=9), n(4, 9, 1/3)],
    [n(4, 9, 1/3, hammer_to=11, accent=True), n(4, 11, 1/3, pull_to=9), n(4, 9, 1/3),
     n(3, 9, 1/3, hammer_to=11, accent=True), n(3, 11, 1/3, pull_to=9), n(3, 9, 1/3),
     n(2, 10, 1/3, hammer_to=12, accent=True), n(2, 12, 1/3, pull_to=10), n(2, 10, 1/3),
     n(3, 11, 1.0, vibrato=True)],
]
LEGATO_LABELS = ['Triplet cells down', 'and back · land on F#']

# ── Builder 2: tremolo picking ───────────────────────────────────────
# Accent ONLY the first sixteenth of each new pitch — that's the melody
# change the caption talks about.
TREM_BARS = [
    [n(1, 14, 0.25, accent=True)] + [n(1, 14, 0.25)] * 7
    + [n(1, 17, 0.25, accent=True)] + [n(1, 17, 0.25)] * 7,
    [n(1, 16, 0.25, accent=True)] + [n(1, 16, 0.25)] * 7
    + [n(1, 14, 0.25, accent=True)] + [n(1, 14, 0.25)] * 7,
]
TREM_LABELS = ['F# → A', 'G# → F#']

# ── Builder 3: bends and vibrato ─────────────────────────────────────
BEND_BARS = [
    [n(2, 12, 2.0, bend_to=14, accent=True),       # B bent a whole step to C#
     n(2, 10, 1.0),                                 # A
     n(2, 9, 1.0, vibrato=True)],                   # G#, wide vibrato
    [n(2, 12, 1.0, pre_bend=14, accent=True),       # pre-bend C#, release to B
     n(2, 10, 1.0),
     n(2, 9, 2.0, vibrato=True)],
    [n(1, 10, 1.0, slide_up=True), n(1, 12, 1.0),   # slide D→E
     n(1, 14, 2.0, bend_to=16, vibrato=True)],      # F# bent to G#, held with vibrato
    [n(1, 14, 4.0, vibrato=True)],                  # home: high F#
]
BEND_LABELS = ['Bend B→C#', 'Pre-bend & release', 'Slide + bend F#→G#', 'Land on F#']

# ── Builder 4: alternate-picked run ──────────────────────────────────
# Descending F# natural minor in sixteenths, high octave then low.
RUN_HI = [n(1, 14, 0.25, accent=True), n(1, 12, 0.25), n(1, 10, 0.25), n(1, 9, 0.25),
          n(2, 12, 0.25, accent=True), n(2, 10, 0.25), n(2, 9, 0.25), n(2, 7, 0.25)]
RUN_LO = [n(3, 11, 0.25, accent=True), n(3, 9, 0.25), n(3, 7, 0.25), n(3, 6, 0.25),
          n(4, 9, 0.25, accent=True), n(4, 7, 0.25), n(4, 6, 0.25), n(4, 4, 0.25)]
RUN_BARS = [
    RUN_HI + RUN_HI,
    RUN_LO + [n(4, 4, 0.25, accent=True), n(4, 6, 0.25), n(4, 7, 0.25), n(4, 9, 0.25),
              n(3, 6, 0.25, accent=True), n(3, 7, 0.25), n(3, 9, 0.25), n(3, 11, 0.25)],
    [n(3, 11, 4.0, vibrato=True)],
]
RUN_LABELS = ['High octave ×2', 'Low octave, turn', 'F# — hold']


EXERCISE = {
    "slug": "leads",
    "order": 7,
    "section": "Twin Leads",
    "title_one": "Lead",
    "title_em": "toolkit",
    "eyebrow": "Solo-Section Skills",
    "eyebrow_short": "Leads",
    "subtitle": "Legato, tremolo, bends, and the alternate-picked run.",
    "intro_prose": """
      <p>The song's solo and melodic breaks are built from four physical
      skills: <strong>legato</strong> (hammer-ons and pull-offs doing the
      work the pick doesn't), <strong>tremolo picking</strong> (one note,
      maximum density), <strong>bends with vibrato</strong> (the vocal,
      screaming notes), and <strong>alternate-picked scale runs</strong>
      (the fast descents that connect phrases).</p>
      <p>Each builder below isolates one skill inside the F# minor boxes
      you already know — the map's boxes sit at frets 0&ndash;6,
      7&ndash;11 and 12&ndash;16; the legato cells live in the 7&ndash;11
      box and the bends in the 12&ndash;16 box. None of them is the solo
      — they are the gym that makes the solo learnable from the tab.</p>
    """,
    "intro_pills": [
        ("All in F# minor", "Every builder lives in the boxes from the scale-map page."),
        ("Slow is fast", "The record sits at ♩=212 — start the tremolo and run ladders around ♩=110. Lead speed is cleanliness compounded; the metronome is the coach."),
    ],
    "sections": [
        {
            "heading": "Builder 1 — legato cells",
            "blurb": "Pick once, sound three notes: pick–hammer–pull triplets walking across the 7–11 pentatonic box. The pick hand rests; the fret hand does everything.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Legato", "Triplet cells across the box",
                    "Pick · hammer · pull — one pick stroke per beat",
                    LEGATO_BARS, LEGATO_LABELS,
                    "The hammered and pulled notes must be <em>as loud as</em> the picked one — snap the pull-off slightly sideways, don't just lift. Loop until the triplets are perfectly even, then move the cells up into the 12–16 box.",
                    bars_per_line=2, width=900),
            ],
        },
        {
            "heading": "Builder 2 — tremolo picking",
            "blurb": "Sixteenth notes on a single pitch, melody moving underneath the blur — the device behind the song's most intense sustained-melody moments.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Tremolo", "Tremolo melody — F# A G# F#",
                    "Strict down-up sixteenths · accent each new pitch",
                    TREM_BARS, TREM_LABELS,
                    "Tiny pick motion from the wrist, pick barely clearing the string. The accent marks where the melody note changes — that change must land <em>exactly</em> on the beat, not when your hand happens to get there. If your forearm burns, stop and shake it out — speed grows from relaxed reps, not from grinding through tension.",
                    bars_per_line=2, width=860),
            ],
        },
        {
            "heading": "Builder 3 — bends and vibrato",
            "blurb": "The vocal notes. A whole-step bend must hit the target pitch dead-on — check it constantly against the fretted note two frets up.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Bends", "Bend, pre-bend, slide — the scream kit",
                    "Whole-step bends · support fingers behind the bending finger",
                    BEND_BARS, BEND_LABELS,
                    "Bend with three fingers and wrist rotation, not one finger's strength. (The playback sounds the starting pitch only — <em>your</em> job is the pitch in the arrow.) Pre-bend: bend silently first, pick, then release. Vibrato comes from the same wrist motion as the bend, just smaller.",
                    bars_per_line=2, width=900),
            ],
        },
        {
            "heading": "Builder 4 — the alternate-picked run",
            "blurb": "Descending F# minor in sixteenths, two octaves. This is the connective tissue of every fast solo phrase in the genre.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Run", "Two-octave descent and turn",
                    "Strict alternate picking · accents on the string changes",
                    RUN_BARS, RUN_LABELS,
                    "Down-up without exception, even across string changes — that's what the accents test. The descent bottoms out at fret 4 on the D string: F#, the root, sitting exactly where the old open low D used to ring. Practise at half speed with a metronome and <em>never</em> let the last four notes of the bar rush — and if your picking forearm tightens up, stop and shake it out; relaxed reps are the only ones that compound. When it's clean, the turnaround bar teaches the ascent for free.",
                    bars_per_line=2, width=900),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Assemble the ",
        "heading_em": "solo",
        "heading_two": "",
        "body": "<p>With these four skills moving, the solo section in the official tab decomposes into things you already do: this run is Builder 4 starting on a different beat, that scream is Builder 3's bend with longer vibrato. Map each solo phrase to its builder, drill the builder, then learn the phrase. The <a href=\"./roadmap.html\" style=\"color:var(--accent);font-weight:600;\">roadmap</a> page slots this into the full-song plan.</p>",
        "items": [
            ("Rotate", "One builder per day alongside your rhythm work. Lead hands decay fast — touch them often."),
            ("Pitch check", "Record your bends. Flat bends are the #1 tell of an unfinished solo."),
            ("Tempo truth", "Log the bpm where each builder is truly clean. The gap between that and the record is your roadmap, not your shame."),
        ],
    },
    "closing": "Four skills, one gym. The solo is waiting at the end of it.",
}
