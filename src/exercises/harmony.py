"""Harmonized thirds — the twin-guitar signature.

Trivium's melodic identity is two guitars playing the same line a
diatonic third apart. This page builds that skill on an ORIGINAL
practice melody in F# minor: learn the low line, learn the high line,
then hear them stacked.
"""

from _common import n, c, tab_card


# ── The practice melody (Guitar 1) — one line up the B string ────────
# F# G# A B C# D C# B | A G# F#(hold). Single-string on purpose: you can
# SEE the scale steps, and the harmony line is the same walk two letters up.
GTR1_BARS = [
    [n(2, 7, 0.5, accent=True), n(2, 9, 0.5), n(2, 10, 0.5), n(2, 12, 0.5),
     n(2, 14, 0.5, accent=True), n(2, 15, 0.5), n(2, 14, 0.5), n(2, 12, 0.5)],
    [n(2, 10, 1.0, accent=True), n(2, 9, 1.0), n(2, 7, 2.0, vibrato=True)],
]
GTR1_LABELS = ['Gtr 1 — the line', 'resolve to F#']

# ── Guitar 2 — the same walk, a diatonic third above, on the E string ─
# A B C# D E F# E D | C# B A(hold)
GTR2_BARS = [
    [n(1, 5, 0.5, accent=True), n(1, 7, 0.5), n(1, 9, 0.5), n(1, 10, 0.5),
     n(1, 12, 0.5, accent=True), n(1, 14, 0.5), n(1, 12, 0.5), n(1, 10, 0.5)],
    [n(1, 9, 1.0, accent=True), n(1, 7, 1.0), n(1, 5, 2.0, vibrato=True)],
]
GTR2_LABELS = ['Gtr 2 — a 3rd up', 'resolve to A']

# ── Both together — dyads ────────────────────────────────────────────
DYAD_BARS = [
    [c([(2, 7), (1, 5)], 0.5, accent=True), c([(2, 9), (1, 7)], 0.5),
     c([(2, 10), (1, 9)], 0.5), c([(2, 12), (1, 10)], 0.5),
     c([(2, 14), (1, 12)], 0.5, accent=True), c([(2, 15), (1, 14)], 0.5),
     c([(2, 14), (1, 12)], 0.5), c([(2, 12), (1, 10)], 0.5)],
    [c([(2, 10), (1, 9)], 1.0, accent=True), c([(2, 9), (1, 7)], 1.0),
     c([(2, 7), (1, 5)], 2.0, vibrato=True)],
]
DYAD_LABELS = ['Stacked 3rds', 'F# + A']


def line_card(num, title, role, bars, labels, caption):
    return tab_card(num, title, role, bars, labels, caption,
                    bars_per_line=2, width=820)


EXERCISE = {
    "slug": "harmony",
    "order": 6,
    "section": "Twin Leads",
    "title_one": "Harmonized",
    "title_em": "thirds",
    "eyebrow": "The Twin-Guitar Sound",
    "eyebrow_short": "Harmony",
    "subtitle": "Two guitars, one melody, a diatonic third apart.",
    "intro_prose": """
      <p>That soaring two-guitar sound in the song's melodic sections is
      <strong>harmony in diatonic thirds</strong> — the Iron Maiden
      inheritance that Trivium built a career on. Guitar&nbsp;2 plays the
      <em>same melody</em> as Guitar&nbsp;1, but every note is moved two
      scale steps up <em>within F# minor</em>. The Duet section of the
      full song (bars 161&ndash;176 on the full-song page) is exactly
      this device, live: every simultaneous pair of notes in it is a
      minor or major third.</p>
      <p>&ldquo;Diatonic&rdquo; is the key word: the gap is sometimes a
      major third (two whole steps) and sometimes a minor third — whatever
      the scale provides. That shimmer of alternating interval colors is
      the sound. The practice melody below is an original line built for
      exactly this: learn both voices alone, then play the dyad version,
      then loop one voice on the site's audio and play the other live
      against it.</p>
    """,
    "intro_pills": [
        ("The rule", "Same melody, two scale steps up, staying inside F# minor."),
        ("The shimmer", "F#→A is minor 3rd, A→C# major 3rd, D→F# major… the mix is the magic."),
    ],
    "sections": [
        {
            "heading": "Voice 1 — the melody",
            "blurb": "A single-string walk up F# minor on the B string. Single-string on purpose: you can see every scale step your harmony partner will mirror.",
            "layout": "full",
            "cards": [
                line_card("Gtr 1", "The line — F# minor on the B string",
                          "F# G# A B C# D C# B · A G# F#",
                          GTR1_BARS, GTR1_LABELS,
                          "Memorise it as <em>letters</em>, not frets — F#, G#, A, B, C#, D — because the harmony line is the same letters shifted. Vibrato on the final F#."),
            ],
        },
        {
            "heading": "Voice 2 — a third above",
            "blurb": "Identical contour on the E string, every note two F#-minor steps higher. If you can sing voice 1 while playing voice 2, you own this.",
            "layout": "full",
            "cards": [
                line_card("Gtr 2", "The harmony — same walk, two steps up",
                          "A B C# D E F# E D · C# B A",
                          GTR2_BARS, GTR2_LABELS,
                          "Where Gtr 1 plays F#, you play A; where it plays G#, you play B. Same rhythm, same accents, same vibrato spot — twin leads only work when the two hands phrase identically."),
            ],
        },
        {
            "heading": "Both voices stacked",
            "blurb": "The two lines as dyads on adjacent strings — one guitar faking the twin-lead sound, and the proof of which thirds are major and which are minor.",
            "layout": "full",
            "cards": [
                line_card("Stack", "Dyads — hear the third change color",
                          "Two-finger shapes · watch the fret gap breathe",
                          DYAD_BARS, DYAD_LABELS,
                          "Look at the fret gaps: B-string 7 / E-string 5 is a <em>minor</em> third (F#+A); B-string 10 / E-string 9 is <em>major</em> (A+C#), and so is B-string 15 / E-string 14 (D+F#). The shape stretches and relaxes as the scale dictates. Play this against the metronome until the shape changes are invisible — and match the single lines' final vibrato on the closing dyad too."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Make it ",
        "heading_em": "twin",
        "heading_two": "",
        "body": "<p>Harmony practice is duo practice. Loop the Gtr&nbsp;1 card's audio and play Gtr&nbsp;2 live over it — then swap. Record yourself playing one voice on your phone and duet with the recording. When you reach the Duet at bars 161&ndash;176, you'll recognise the device instantly and only need to learn the notes. One caveat: on the record, twin-lead writers sometimes swap a third for a perfect 4th or 5th to fit the underlying chord — if the official tab disagrees with strict thirds somewhere, that's why.</p>",
        "items": [
            ("Transpose the trick", "Take any 4-note F#-minor phrase you like and harmonize it two steps up yourself. The skill is the rule, not this one melody."),
            ("Phrasing lock", "Bends, slides and vibrato must match between voices — practise the final vibrato of both lines at the same width and speed."),
            ("Ear training", "Sing the harmony while playing the melody. Painful at first, transformative after a week."),
        ],
    },
    "closing": "One melody, two voices, the sound that defines the record.",
}
