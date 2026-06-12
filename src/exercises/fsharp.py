"""F# minor — the scale map for riffs and leads, in drop D.

Three natural-minor boxes — open, middle (frets 7–11) and 12th position —
plus the F# minor pentatonic box at frets 4–7 where the song's lead lines
breathe. Everything anchors on string 6, fret 4: in drop D the open low
string is the b6 (D), not the root, so fret 4 is home.
"""

from _common import n, r, render_tab, scale_box, audio_from_bars, OPEN_MIDI


# ── Box 1: the open box, F# natural minor (drop D), frets 0–6 ────────
# The open 6th string is the b6 (D) — the root lives at fret 4. The
# ascent is fully gapless: 19 notes, D2 up to A4 without a hole.
BOX_OPEN = [
    (6, 0, 'b6'), (6, 2, 'b7'), (6, 4, 'R'), (6, 6, '2'),
    (5, 0, 'b3'), (5, 2, '4'), (5, 4, '5'),
    (4, 0, 'b6'), (4, 2, 'b7'), (4, 4, 'R'),
    (3, 1, '2'), (3, 2, 'b3'), (3, 4, '4'),
    (2, 2, '5'), (2, 3, 'b6'), (2, 5, 'b7'),
    (1, 2, 'R'), (1, 4, '2'), (1, 5, 'b3'),
]

# ── Box 2: middle box, frets 7–11 ────────────────────────────────────
# Roots at (5,9), (3,11) and (2,7). Ascending out of string 6 the b6
# (D3) is NOT in this box — it lives back at (5,5) / open string 4.
BOX_MID = [
    (6, 7, 'b3'), (6, 9, '4'), (6, 11, '5'),
    (5, 7, 'b7'), (5, 9, 'R'), (5, 11, '2'),
    (4, 7, 'b3'), (4, 9, '4'), (4, 11, '5'),
    (3, 7, 'b6'), (3, 9, 'b7'), (3, 11, 'R'),
    (2, 7, 'R'), (2, 9, '2'), (2, 10, 'b3'),
    (1, 7, '4'), (1, 9, '5'), (1, 10, 'b6'),
]

# ── Box 3: 12th position, frets 12–16 — Box 1 an octave up ───────────
# Roots at (6,16), (4,16) and (1,14). The 2 (G#3) below (5,12) sits
# outside the box, at (5,11) or (6,18).
BOX_HIGH = [
    (6, 12, 'b6'), (6, 14, 'b7'), (6, 16, 'R'),
    (5, 12, 'b3'), (5, 14, '4'), (5, 16, '5'),
    (4, 12, 'b6'), (4, 14, 'b7'), (4, 16, 'R'),
    (3, 13, '2'), (3, 14, 'b3'), (3, 16, '4'),
    (2, 12, '4'), (2, 14, '5'), (2, 15, 'b6'),
    (1, 12, 'b7'), (1, 14, 'R'), (1, 16, '2'),
]

# ── F# minor pentatonic, frets 4–7 (F# A B C# E) ─────────────────────
# Root on string 6, fret 4 — the same anchor as Box 1. In drop D the
# 6th string mirrors the 4th: same frets, one octave down.
BOX_PENT = [
    (6, 4, 'R'), (6, 7, 'b3'),
    (5, 4, '5'), (5, 7, 'b7'),
    (4, 4, 'R'), (4, 7, 'b3'),
    (3, 4, '4'), (3, 6, '5'),
    (2, 5, 'b7'), (2, 7, 'R'),
    (1, 5, 'b3'), (1, 7, '4'),
]


def _ordered_for_play(positions):
    """Ascending by actual pitch (drop-D open-string values), keeping one
    position per pitch — boxes can voice the same note on two strings."""
    out, seen = [], set()
    for midi, s, f in sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _) in positions}):
        if midi in seen:
            continue
        seen.add(midi)
        out.append((s, f))
    return out


def _updown_bars(notes):
    """Asc + desc as eighth-note tab events, in bars of exactly 4.0 beats
    (the last bar is padded with rests)."""
    full = notes + notes[:-1][::-1]
    events = [n(s, f, dur=0.5) for s, f in full]
    bars = [events[i:i + 8] for i in range(0, len(events), 8)]
    bars[-1].extend(r(dur=0.5) for _ in range(8 - len(bars[-1])))
    return bars


def make_card(num, title, role, positions, fret_range, caption):
    body = scale_box(positions, fret_range, title=title)
    bars = _updown_bars(_ordered_for_play(positions))
    body += render_tab(bars, bars_per_line=4, width=900, show_bar_numbers=False)
    return {"num": num, "title": title, "role": role,
            "body": body, "caption": caption,
            "audio": audio_from_bars(bars)}


EXERCISE = {
    "slug": "fsharp",
    "order": 4,
    "section": "Scales",
    "title_one": "F♯ minor",
    "title_em": "scale map",
    "eyebrow": "Riffs Low, Leads High",
    "eyebrow_short": "F♯ minor",
    "subtitle": "Natural minor and pentatonic, mapped for drop D.",
    "intro_prose": """
      <p>The song's note pool is <strong>F♯ natural minor</strong>:
      F♯&nbsp;·&nbsp;G♯&nbsp;·&nbsp;A&nbsp;·&nbsp;B&nbsp;·&nbsp;C♯&nbsp;·&nbsp;D&nbsp;·&nbsp;E.
      The riffs draw their chord roots from it, the harmonized leads run
      up and down it, and the solo carves shapes out of it. Inside it
      lives the simpler <strong>F♯ minor pentatonic</strong>
      (F♯&nbsp;·&nbsp;A&nbsp;·&nbsp;B&nbsp;·&nbsp;C♯&nbsp;·&nbsp;E) — the safe skeleton when
      you're improvising fills.</p>
      <p>Here's the big mental shift from standard-tuning F♯ minor: in
      drop D the open low string is the <em>♭6</em> (D), not the root —
      the root lives at <strong>string 6, fret 4</strong>. Anchor
      everything on that fret. It's also where the song's home power
      chord sits, so the scale and the riffs share the same landmark.</p>
    """,
    "intro_pills": [
        ("Seven notes", "F♯ (R) · G♯ (2) · A (♭3) · B (4) · C♯ (5) · D (♭6) · E (♭7)"),
        ("Drop D rule", "Strings 5–1 unchanged. String 6: add 2 to every standard-tuning fret — open is the ♭6, the root is at fret 4."),
    ],
    "sections": [
        {
            "heading": "Three boxes and a pentatonic, low to high",
            "blurb": "Box 1 is riff country — where the rhythm parts live. Box 2 is the middle of the neck, Box 3 is lead country at the 12th position, and the pentatonic box at frets 4–7 is the can't-miss core for fills.",
            "layout": "full",
            "cards": [
                make_card("Box 1", "Open box — riff country",
                          "F♯ natural minor · root at string 6, fret 4",
                          BOX_OPEN, (0, 6),
                          "Every riff note in the low register is in this box, and the ascent is fully gapless — 19 notes, D2 to A4, no holes. The open 6th string is the ♭6, not the root: home is fret 4, and strings 6 and 4 share the same fret pattern (the drop-D mirror). Walk it up and down until the ♭6 (D) and ♭7 (E) below the root feel as solid as the root itself."),
                make_card("Box 2", "Middle box — frets 7–11",
                          "F♯ natural minor · roots at (5,9), (3,11) and (2,7)",
                          BOX_MID, (7, 11),
                          "Honesty first: this box is not the whole scale. Ascending out of string 6, the ♭6 (D3) is missing — after C♯3 at string 6, fret 11 the run jumps straight to E3, because D3 lives back at string 5, fret 5 (or open string 4). Know the gap and reach back for it when a line needs it. F♯4 appears twice — (3,11) and (2,7) — so the run plays it once."),
                make_card("Box 3", "12th position — lead country",
                          "F♯ natural minor · roots at (6,16), (4,16) and (1,14)",
                          BOX_HIGH, (12, 16),
                          "Box 1 moved up an octave — same shape, twelve frets higher. The high register where twin-lead melodies and solo runs live; roots at string 6 fret 16, string 4 fret 16 and string 1 fret 14. One gap to name: the 2 (G♯3) below string 5, fret 12 sits outside the box — at (5,11) or (6,18) — so the run jumps F♯3 to A3. B4 appears twice, (3,16) and (2,12); the run plays it once."),
                make_card("Pent", "Pentatonic core — frets 4–7",
                          "F♯ minor pentatonic · root at string 6, fret 4",
                          BOX_PENT, (4, 7),
                          "Five notes, no half-steps — F♯ · A · B · C♯ · E, the first stop when improvising over the song's chords. Same anchor as Box 1: root at string 6, fret 4. The low-string dots show the drop-D mirror again — string 6 frets 4 and 7 are F♯ and A, an octave under string 4."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Scales into ",
        "heading_em": "melodies",
        "heading_two": "",
        "body": "<p>A scale box is an alphabet, not a sentence. The song turns this alphabet into harmonized twin-guitar melodies — that's the next page: <a href=\"./harmony.html\" style=\"color:var(--accent);font-weight:600;\">harmonized thirds</a>. Keep the box positions under your fingers; the harmony lines run straight up them.</p>",
        "items": [
            ("3 min", "Box 1 ascending/descending with the metronome — the song sits at ♩=212, so start way below it. Land on a root to finish."),
            ("3 min", "The pentatonic box the same — then improvise eight bars of fills using only its five notes."),
            ("3 min", "Box 3 — play it in triplets instead of eighths. Lead phrasing starts here."),
            ("Connect", "Walk Box 1 → Box 2 up the 5th string, Box 2 → Box 3 up the 3rd. One neck, not three rooms."),
        ],
    },
    "closing": "Seven notes, three boxes, every riff and lead in the song — anchored on fret 4.",
}
