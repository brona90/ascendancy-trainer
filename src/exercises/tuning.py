"""Drop D — get in tune, then own the one-finger power chord.

Ascendancy (like most of the album it names) lives in drop D — but the
song's key is F# minor, with the home barre at fret 4. Before anything
else: tune the low E down a whole step and learn how that remaps the
bottom three strings.
"""

from _common import (n, c, tab_card, PC_ROLES, D5_SHAPE, FS5_SHAPE, GS5_SHAPE,
                     A5_SHAPE, B5_SHAPE, CS5_SHAPE, D5, FS5, GS5, A5, B5, CS5)


# ── Card 1: tuning check ─────────────────────────────────────────────
# Octave check (string 4 open vs string 6 open) + A check (string 6
# fret 7 vs string 5 open).
TUNING_BARS = [
    [
        n(4, 0, 1.0),                      # reference D3
        n(6, 0, 1.0),                      # target D2 — one octave down
        c([(6, 0), (4, 0)], 2.0),          # together: a pure octave, no beating
    ],
    [
        n(5, 0, 1.0),                      # open A
        n(6, 7, 1.0),                      # dropped string fret 7 = the same A
        c([(6, 7), (5, 0)], 2.0),          # unison check
    ],
]
TUNING_LABELS = ['Octave check', 'Unison check']


# ── Card 2: the one-finger power chord ───────────────────────────────
# The song's actual vocabulary: Ascendancy is in F# minor, and these six
# frets are every position the drills below touch.
PC_CHORDS = [
    ('D5 — open', D5_SHAPE, PC_ROLES),
    ('F♯5 — fret 4', FS5_SHAPE, PC_ROLES),
    ('G♯5 — fret 6', GS5_SHAPE, PC_ROLES),
    ('A5 — fret 7', A5_SHAPE, PC_ROLES),
    ('B5 — fret 9', B5_SHAPE, PC_ROLES),
    ('C♯5 — fret 11', CS5_SHAPE, PC_ROLES),
]
PC_BARS = [
    [c(D5, 2.0, accent=True), c(FS5, 2.0, accent=True)],
    [c(GS5, 2.0), c(A5, 2.0)],
    [c(B5, 2.0), c(CS5, 2.0)],
]
PC_LABELS = ['D5 · F♯5', 'G♯5 · A5', 'B5 · C♯5']


# ── Card 3: power-chord slide drill ──────────────────────────────────
# Walk the one-finger shape through the positions the song actually
# uses: up D5 → F♯5 → G♯5 → A5, leap to C♯5, walk back down, then run
# the bridge motion F♯5–G♯5–A5–G♯5 and park on home.
SLIDE_BARS = [
    [c(D5, 0.5, accent=True), c(D5, 0.5), c(FS5, 0.5, accent=True), c(FS5, 0.5),
     c(GS5, 0.5, accent=True), c(GS5, 0.5), c(A5, 0.5, accent=True), c(A5, 0.5)],
    [c(CS5, 0.5, accent=True), c(CS5, 0.5), c(A5, 0.5, accent=True), c(A5, 0.5),
     c(GS5, 0.5, accent=True), c(GS5, 0.5), c(FS5, 0.5, accent=True), c(FS5, 0.5)],
    [c(FS5, 0.5, accent=True), c(FS5, 0.5), c(GS5, 0.5), c(GS5, 0.5),
     c(A5, 0.5), c(A5, 0.5), c(GS5, 0.5), c(GS5, 0.5)],
    [c(FS5, 4.0, accent=True)],
]
SLIDE_LABELS = ['D5 F♯5 G♯5 A5', 'C♯5 A5 G♯5 F♯5', 'F♯5 G♯5 A5 G♯5', 'F♯5']


EXERCISE = {
    "slug": "tuning",
    "order": 1,
    "section": "Setup",
    "title_one": "Drop D",
    "title_em": "tuning",
    "eyebrow": "Setup · Tune Down First",
    "eyebrow_short": "Drop D",
    "subtitle": "One whole step down on the low string changes everything.",
    "intro_prose": """
      <p><em>Ascendancy</em> is played in <strong>drop D</strong>:
      D&nbsp;A&nbsp;D&nbsp;G&nbsp;B&nbsp;E. Only the 6th string moves — down a
      whole step from E to D. The payoff is huge: the bottom three strings
      become a <em>movable one-finger power chord</em>, which is what makes
      the fast riffing in this song physically possible, and the open low D
      gives the galloping pedal tone its growl.</p>
      <p>The song itself is in <strong>F&#9839; minor</strong> — fret 4 is
      <em>home</em>, the F&#9839;5 barre you'll live on. Tune by ear with
      the two checks below, or use a tuner. Then drill the one-finger
      shape until sliding between frets feels like pointing at a note.</p>
    """,
    "intro_pills": [
        ("Why drop D", "Power chords collapse to one finger — barre strings 6–4 at any fret."),
        ("Two ear checks", "String 6 open = string 4, one octave down. String 6 fret 7 = open A."),
    ],
    "sections": [
        {
            "heading": "Get in tune",
            "blurb": "Detune the low E slowly until the octave against the open D string stops &ldquo;beating&rdquo;. Then confirm: fret 7 on the dropped string should be the exact pitch of your open A.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Check", "Tuning checks — octave and unison",
                    "String 4 → string 6 octave · fret 7 → open A unison",
                    TUNING_BARS, TUNING_LABELS,
                    "Play the pairs slowly and listen for the slow &ldquo;wah-wah-wah&rdquo; of two pitches almost matching — tune until it disappears. <em>Always tune down past the note and come back up</em> so the string holds pitch under hard picking.",
                    bars_per_line=2, width=720),
            ],
        },
        {
            "heading": "The one-finger power chord",
            "blurb": "Barre your index finger flat across strings 6–5–4. That's the whole grip. Root, fifth, octave — every riff position in the song is this shape at a different fret.",
            "layout": "full",
            "cards": [
                tab_card(
                    "Shape", "The song's six positions",
                    "D5 open · F♯5 fret 4 · G♯5 fret 6 · A5 fret 7 · B5 fret 9 · C♯5 fret 11",
                    PC_BARS, PC_LABELS,
                    "These six frets — open, 4, 6, 7, 9, 11 — are where the song's rhythm parts live, and <strong>fret 4 (F&#9839;5) is home</strong>. Strike each chord once and let it ring. <strong>Mute strings 3–2–1</strong> with the underside of your barre finger.",
                    bars_per_line=3, width=900, chords=PC_CHORDS),
                tab_card(
                    "Drill", "Power-chord slide drill",
                    "Eighth notes · two hits per fret · one finger does all the work",
                    SLIDE_BARS, SLIDE_LABELS,
                    "Bar 1 starts on the <em>open</em> D5 — there's no finger to slide from, so just drop the barre on at fret 4; between the fretted shapes, keep light contact with the strings and don't lift off. Accent the first hit at each new fret, and <em>say the chord names aloud as you land them</em>. Bar 3 is the bridge walk — F&#9839;5, G&#9839;5, A5, G&#9839;5. Clean at 100&nbsp;bpm, this drill <em>is</em> the mobility the riffs need.",
                    bars_per_line=4, width=900),
            ],
        },
    ],
    "next_step": {
        "heading_one": "From shape to ",
        "heading_em": "engine",
        "heading_two": "",
        "body": "<p>Once the tuning is solid and the one-finger shape moves cleanly, the next bottleneck is the picking hand. Head to the <a href=\"./gallop.html\" style=\"color:var(--accent);font-weight:600;\">Gallop picking</a> page — it's the rhythmic engine of the entire song.</p>",
        "items": [
            ("Every session", "Re-check the octave before practising. Drop-tuned strings drift more than standard."),
            ("Grip check", "One finger, flat barre, thumb low behind the neck. If your hand aches, you're squeezing too hard."),
            ("Name the frets", "Say the chord names out loud while running the slide drill — D, F♯, G♯, A, B, C♯. The song's riffs are spelled from these."),
        ],
    },
    "closing": "One string down, one finger across. The doorway to the whole song.",
}
