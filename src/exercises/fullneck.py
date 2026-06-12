"""Full neck — F# minor up and down the whole fretboard, in drop D.

The scale-map page splits F# minor into three boxes. This page does the
opposite: it shows the seven notes everywhere at once, so the boxes become one
connected neck. The map and the root diagram are computed straight from the
pitch of every fret — nothing is hand-placed — and every playable run is
checked against the scale at build time, so every dot and note is real.
"""

from _common import n, r, render_tab, scale_box, audio_from_bars, OPEN_MIDI
from fretboard import OPEN_STRING_PC
from fsharp import BOX_OPEN, BOX_MID, BOX_HIGH


# Pitch class → its scale degree label in F# natural minor (F# G# A B C# D E).
# F#=6 G#=8 A=9 B=11 C#=1 D=2 E=4 (semitones from C).
SCALE_ROLE = {6: 'R', 8: '2', 9: 'b3', 11: '4', 1: '5', 2: 'b6', 4: 'b7'}


def _pc(string, fret):
    return (OPEN_STRING_PC[string] + fret) % 12


def neck_positions(max_fret, roots_only=False):
    """Every F#-minor note (or just the roots) from the nut to `max_fret`."""
    out = []
    for string in range(1, 7):
        for fret in range(0, max_fret + 1):
            pc = _pc(string, fret)
            if pc not in SCALE_ROLE:
                continue
            if roots_only and pc != 6:
                continue
            out.append((string, fret, SCALE_ROLE[pc]))
    return out


def _assert_in_scale(notes, label):
    """Guard: refuse to ship a run that wanders out of F# minor."""
    for s, f in notes:
        if _pc(s, f) not in SCALE_ROLE:
            raise ValueError(f'{label}: ({s},{f}) is not in F# minor — refusing to invent a note')


FULL_MAP = neck_positions(16)
ROOT_MAP = neck_positions(16, roots_only=True)

# Full-neck climb in BOX ORDER: the three boxes from the scale-map page joined
# into one run, each box climbed by pitch and played up then back down (see
# _scale_tab). The fret bands (0,6) / (7,11) / (12,16) align exactly to the
# boxes. Two honesty notes, stated rather than hidden: the middle band has no
# D3 (it lives back at (5,5) / open string 4), and the top band has no G#3
# (it sits at (5,11), below the band). The runs skip those pitches — the map
# above still shows every location. Pitch-checked below.
_BANDS = ((0, 6, BOX_OPEN), (7, 11, BOX_MID), (12, 16, BOX_HIGH))


def _box_updown():
    """Scale up and down once per box, climbing the neck low → high.

    Within each box the notes are sorted by pitch — which, in a fret band, is
    essentially low string to high — deduped where a box voices the same pitch
    on two strings, then played ascending and back down. Concatenating the
    three boxes walks the whole neck the way you'd actually practise it: run
    the box up and down, shift up, run the next box, and so on.
    """
    out = []
    for lo, hi, box in _BANDS:
        band, seen = [], set()
        for midi, s, f in sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _r) in box}):
            if not (lo <= f <= hi):
                raise ValueError(f'box note ({s},{f}) outside band {lo}-{hi}')
            if midi in seen:
                continue
            seen.add(midi)
            band.append((s, f))
        out.extend(band)
        out.extend(band[-2::-1])     # back down, without repeating the top note
    return out


FULL_RUN = _box_updown()

# F# minor on the dropped 6th string alone — one octave, root to root. The
# drop-D twist: the open string is the b6 (D), NOT the root, so the octave
# runs fret 4 to fret 16 along just that one string.
LOW_STRING = [(6, f) for f in (4, 6, 7, 9, 11, 12, 14, 16)]   # F# G# A B C# D E F#

# The nine roots, low to high, as a navigation drill.
ROOT_RUN = [(s, f) for (_, s, f) in sorted(
    {(OPEN_MIDI[s] + f, s, f) for (s, f, _) in ROOT_MAP})]

for _label, _seq in (('full-run', FULL_RUN), ('low-string', LOW_STRING),
                     ('root-run', ROOT_RUN)):
    _assert_in_scale(_seq, _label)


def _scale_bars(notes, prebuilt=False):
    """Eighth-note tab events in bars of exactly 4.0 beats (the last bar is
    padded with rests). By default the notes play up then back down; pass
    prebuilt=True when `notes` already includes the descent."""
    full = notes if prebuilt else notes + notes[:-1][::-1]
    events = [n(s, f, dur=0.5) for s, f in full]
    bars = [events[i:i + 8] for i in range(0, len(events), 8)]
    bars[-1].extend(r(dur=0.5) for _ in range(8 - len(bars[-1])))
    return bars


def _map_card(num, title, role, positions, fret_range, notes, caption,
              box_width=980, box_height=220, prebuilt=False):
    body = scale_box(positions, fret_range, title=title,
                     width=box_width, height=box_height)
    bars = _scale_bars(notes, prebuilt=prebuilt)
    body += render_tab(bars, bars_per_line=4, width=900,
                       show_bar_numbers=False)
    return {"num": num, "title": title, "role": role,
            "body": body, "caption": caption,
            "audio": audio_from_bars(bars)}


EXERCISE = {
    "slug": "fullneck",
    "order": 5,
    "section": "Scales",
    "title_one": "Full",
    "title_em": "neck",
    "eyebrow": "One Scale, Every Fret",
    "eyebrow_short": "Full neck",
    "subtitle": "F♯ minor across the whole fretboard — the three boxes joined into one.",
    "intro_prose": """
      <p>The <a href="./fsharp.html" style="color:var(--accent);font-weight:600;">scale map</a>
      page learns F♯ minor as three boxes. This page erases the walls between
      them: here are the same seven notes —
      <strong>F♯&nbsp;·&nbsp;G♯&nbsp;·&nbsp;A&nbsp;·&nbsp;B&nbsp;·&nbsp;C♯&nbsp;·&nbsp;D&nbsp;·&nbsp;E</strong>
      — laid out from the open strings to the 16th fret, all at once.</p>
      <p>The goal is to stop thinking in positions and start seeing one
      connected neck, so a phrase can start anywhere and find its way home.
      Play the full-neck climb — all the way up to the top and back down — to
      feel the boxes link into one, learn the scale along the <em>dropped 6th
      string</em> (where the open string is the ♭6 and the root waits at
      fret&nbsp;4), then chase the root all over the fretboard.</p>
    """,
    "intro_pills": [
        ("Same seven notes", "F♯ (R) · G♯ (2) · A (♭3) · B (4) · C♯ (5) · D (♭6) · E (♭7)"),
        ("Why it matters", "The solo and twin leads roam the whole neck at ♩=212 — boxes alone won't keep up."),
    ],
    "sections": [
        {
            "heading": "The neck as one map",
            "blurb": "Every F♯-minor note from the nut to the 16th fret. The filled accents are the roots (F♯). Tap <strong>▶</strong> on any card and the matching dots light up as it plays — set the speed with the metronome and climb slowly; the song's ♩=212 is the destination, not the starting point.",
            "layout": "full",
            "cards": [
                _map_card(
                    "Map", "The whole neck",
                    "F♯ natural minor · open to the 16th fret",
                    FULL_MAP, (0, 16), FULL_RUN,
                    "Don't memorise this as a picture — use it as a reference while you play. The run climbs the open box up and down, shifts to the middle box, then the 12th-position box. Two gaps, named not hidden: the middle box has no D3 — after C♯3 at string 6, fret 11 the run jumps to E3, because D3 lives back at string 5, fret 5 — and the top box has no G♯3, which sits below it at string 5, fret 11. The map shows every location; reach outside a box when a line needs those notes.",
                    prebuilt=True),
                _map_card(
                    "1 string", "Up the dropped string",
                    "F♯ minor along string 6 · fret 4 to fret 16",
                    [(6, f, SCALE_ROLE[_pc(6, f)]) for f in (4, 6, 7, 9, 11, 12, 14, 16)],
                    (4, 16), LOW_STRING,
                    "The whole scale in order along one string — but mind the drop-D twist: the open string is the ♭6 (D), not the root. Home is fret 4, and the octave is fret 16: frets 4 · 6 · 7 · 9 · 11 · 12 · 14 · 16. A perfect way to hear the intervals and learn where every note sits without a single position shift."),
                _map_card(
                    "Roots", "Find every root",
                    "Every F♯ on the neck · the home note",
                    ROOT_MAP, (0, 16), ROOT_RUN,
                    "Just the F♯'s — nine of them up to the 16th fret: (6,4) low, then (4,4) · (5,9) · (6,16) all the same F♯3, then (1,2) · (2,7) · (3,11) sharing F♯4, with (4,16) beside them and (1,14) on top. Strings 6 and 4 share their root frets (the drop-D mirror). Play them low to high, then jump to any root without counting frets."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "From the neck to the ",
        "heading_em": "music",
        "heading_two": "",
        "body": "<p>One connected neck is the foundation the lead playing stands on. Take it into the <a href=\"./harmony.html\" style=\"color:var(--accent);font-weight:600;\">harmonized thirds</a> and <a href=\"./leads.html\" style=\"color:var(--accent);font-weight:600;\">lead toolkit</a> pages — both run straight up these notes — and then to the song's <a href=\"./song.html\" style=\"color:var(--accent);font-weight:600;\">solo and duel</a>.</p>",
        "items": [
            ("Climb slow", "Full-neck run with the metronome, one clean pass up and back down. The song wants ♩=212 eventually — raise the tempo only when the current one is spotless."),
            ("One string", "Play the scale along string 6 from fret 4 with your eyes closed — name each note out loud as you land it."),
            ("Root tag", "Improvise in F♯ minor and force every phrase to end on a root, using a different root location each time — there are nine."),
            ("Join the boxes", "Start a run in the open box and let it climb into the 12th-position box without stopping. One neck, not three rooms."),
        ],
    },
    "closing": "Three boxes, one fretboard — the whole neck in F♯ minor.",
}
