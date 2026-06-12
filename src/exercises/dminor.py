"""D minor — the scale map for riffs and leads, in drop D.

Three boxes: the open drop-D position the riffs live in, the mid-neck
D minor pentatonic box where the song's lead lines breathe, and the
12th-position natural minor box for the high melodic material.
"""

from _common import n, render_tab, scale_box, OPEN_MIDI


# ── Box 1: open position, D natural minor (drop D) ───────────────────
# String 6 is the dropped D — the open string IS the root.
BOX_OPEN = [
    (6, 0, 'R'), (6, 2, '2'), (6, 3, 'b3'), (6, 5, '4'),
    (5, 0, '5'), (5, 1, 'b6'), (5, 3, 'b7'),
    (4, 0, 'R'), (4, 2, '2'), (4, 3, 'b3'),
    (3, 0, '4'), (3, 2, '5'), (3, 3, 'b6'),
    (2, 1, 'b7'), (2, 3, 'R'),
    (1, 0, '2'), (1, 1, 'b3'), (1, 3, '4'),
]

# ── Box 2: D minor pentatonic, frets 5–8 ─────────────────────────────
# Root on the 5th string fret 5. In drop D the 6th string mirrors the
# 4th string — same frets, one octave down.
BOX_PENT = [
    (6, 5, '4'), (6, 7, '5'),
    (5, 5, 'R'), (5, 8, 'b3'),
    (4, 5, '4'), (4, 7, '5'),
    (3, 5, 'b7'), (3, 7, 'R'),
    (2, 6, 'b3'), (2, 8, '4'),
    (1, 5, '5'), (1, 8, 'b7'),
]

# ── Box 3: 12th-position D natural minor ─────────────────────────────
BOX_HIGH = [
    (6, 10, 'b7'), (6, 12, 'R'), (6, 14, '2'),
    (5, 10, '4'), (5, 12, '5'), (5, 13, 'b6'),
    (4, 10, 'b7'), (4, 12, 'R'), (4, 14, '2'),
    (3, 10, 'b3'), (3, 12, '4'), (3, 14, '5'),
    (2, 11, 'b6'), (2, 13, 'b7'),
    (1, 10, 'R'), (1, 12, '2'), (1, 13, 'b3'), (1, 15, '4'),
]


def _ordered_for_play(positions):
    """Ascending by actual pitch, using the DROP D open-string values."""
    nps = sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _) in positions})
    return [[s, f] for _, s, f in nps]


def _build_scale_tab(notes):
    """Asc + desc as tab events, split into bars of 8 eighth notes."""
    desc = notes[:-1][::-1]
    full = notes + desc
    events = [n(s, f, dur=0.5) for s, f in full]
    bars = [events[i:i + 8] for i in range(0, len(events), 8)]
    return render_tab(bars, bars_per_line=4, width=900, show_bar_numbers=False)


def make_card(num, title, role, positions, fret_range, caption):
    body = scale_box(positions, fret_range, title=title)
    notes = _ordered_for_play(positions)
    tab_svg = _build_scale_tab(notes)
    return {"num": num, "title": title, "role": role,
            "body": body + tab_svg, "caption": caption,
            "audio": {"type": "scale", "notes": notes}}


EXERCISE = {
    "slug": "dminor",
    "order": 4,
    "section": "Scales",
    "title_one": "D minor",
    "title_em": "scale map",
    "eyebrow": "Riffs Low, Leads High",
    "eyebrow_short": "D minor",
    "subtitle": "Natural minor and pentatonic, mapped for drop D.",
    "intro_prose": """
      <p>The song's note pool is <strong>D natural minor</strong>:
      D&nbsp;·&nbsp;E&nbsp;·&nbsp;F&nbsp;·&nbsp;G&nbsp;·&nbsp;A&nbsp;·&nbsp;B♭&nbsp;·&nbsp;C.
      The riffs draw their chord roots from it, the harmonized leads run
      up and down it, and the solo carves shapes out of it. Inside it
      lives the simpler <strong>D minor pentatonic</strong>
      (D&nbsp;·&nbsp;F&nbsp;·&nbsp;G&nbsp;·&nbsp;A&nbsp;·&nbsp;C) — the safe skeleton when
      you're improvising fills.</p>
      <p>Drop D bends the usual shapes on one string only: everything on
      strings 5–1 is exactly where you learned it, but the 6th string is
      shifted up two frets — and now <em>mirrors the 4th string an octave
      down</em>. Box&nbsp;1 below makes that remapping a feature: the open
      6th string is the root.</p>
    """,
    "intro_pills": [
        ("Seven notes", "D (R) · E (2) · F (♭3) · G (4) · A (5) · B♭ (♭6) · C (♭7)"),
        ("Drop D rule", "Strings 5–1 unchanged. String 6: add 2 to every standard-tuning fret."),
    ],
    "sections": [
        {
            "heading": "Three boxes, low to high",
            "blurb": "Box 1 is riff country — where the rhythm parts live. Box 2 is the pentatonic core mid-neck. Box 3 is lead country, up at the 12th position where the harmonized melodies sit.",
            "layout": "full",
            "cards": [
                make_card("Box 1", "Open position — riff country",
                          "D natural minor · the dropped string is the root",
                          BOX_OPEN, (0, 5),
                          "Every riff note in the low register is in this box. Notice strings 6 and 4 share the same fret pattern — the drop-D mirror. Walk it ascending and descending until the ♭6 (B♭) and ♭7 (C) are as familiar as the root."),
                make_card("Box 2", "Pentatonic core — frets 5–8",
                          "D minor pentatonic · root on string 5, fret 5",
                          BOX_PENT, (5, 8),
                          "Five notes, no half-steps — the can't-miss skeleton for fills and the first stop when improvising over the song's chords. The two low-string dots show the drop-D mirror again: string 6 frets 5 and 7 are G and A, an octave under string 4."),
                make_card("Box 3", "12th position — lead country",
                          "D natural minor · root on strings 6, 4 and 1",
                          BOX_HIGH, (10, 15),
                          "The high register where twin-lead melodies and solo runs live. The root sits on string 1 fret 10, string 4 fret 12, and string 6 fret 12 — learn all three anchors so any phrase can find home."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Scales into ",
        "heading_em": "melodies",
        "heading_two": "",
        "body": "<p>A scale box is an alphabet, not a sentence. The song turns this alphabet into harmonized twin-guitar melodies — that's the next page: <a href=\"./harmony.html\" style=\"color:var(--accent);font-weight:600;\">harmonized thirds</a>. Keep the box positions under your fingers; the harmony lines run straight up them.</p>",
        "items": [
            ("3 min", "Box 1 ascending/descending with the metronome. Land on a root to finish."),
            ("3 min", "Box 2 the same — then improvise eight bars of fills using only its five notes."),
            ("3 min", "Box 3 — play it in triplets instead of eighths. Lead phrasing starts here."),
            ("Connect", "Walk Box 1 → Box 2 up the 5th string, Box 2 → Box 3 up the 3rd. One neck, not three rooms."),
        ],
    },
    "closing": "Seven notes, three boxes, every riff and lead in the song.",
}
