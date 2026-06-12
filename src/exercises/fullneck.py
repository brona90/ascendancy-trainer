"""Full neck — D minor up and down the whole fretboard, in drop D.

The scale-map page splits D minor into three boxes. This page does the
opposite: it shows the seven notes everywhere at once, so the boxes become one
connected neck. The map and the root diagram are computed straight from the
pitch of every fret — nothing is hand-placed — and the two playable runs are
checked against the scale at build time, so every dot and note is real.
"""

from _common import n, render_tab, scale_box, OPEN_MIDI
from fretboard import OPEN_STRING_PC


# Pitch class → its scale degree label in D natural minor (D E F G A B♭ C).
# D=2 E=4 F=5 G=7 A=9 B♭=10 C=0 (semitones from C).
SCALE_ROLE = {2: 'R', 4: '2', 5: 'b3', 7: '4', 9: '5', 10: 'b6', 0: 'b7'}


def _pc(string, fret):
    return (OPEN_STRING_PC[string] + fret) % 12


def neck_positions(max_fret, roots_only=False):
    """Every D-minor note (or just the roots) from the nut to `max_fret`."""
    out = []
    for string in range(1, 7):
        for fret in range(0, max_fret + 1):
            pc = _pc(string, fret)
            if pc not in SCALE_ROLE:
                continue
            if roots_only and pc != 2:
                continue
            out.append((string, fret, SCALE_ROLE[pc]))
    return out


def _assert_in_scale(notes, label):
    """Guard: refuse to ship a run that wanders out of D minor."""
    for s, f in notes:
        if _pc(s, f) not in SCALE_ROLE:
            raise ValueError(f'{label}: ({s},{f}) is not in D minor — refusing to invent a note')


FULL_MAP = neck_positions(15)
ROOT_MAP = neck_positions(15, roots_only=True)

# Full-neck climb in BOX ORDER: every marked note, grouped low → middle → high
# position (the three D-minor boxes joined into one), each box climbed by pitch.
# Built from FULL_MAP (which is computed from pitch), never hand-typed, so it
# touches every dot and still passes _assert_in_scale. Played ascending then
# descending (see _scale_tab). The fret bands partition 0–15, so the union is
# the whole map. Pitch-checked below.
_BOXES = ((0, 5), (6, 9), (10, 15))   # open · middle · 12th-position

def _box_order(positions):
    """Order every marked note box by box, low to high, ascending within each."""
    out = []
    for lo, hi in _BOXES:
        band = sorted(((s, f) for (s, f, _r) in positions if lo <= f <= hi),
                      key=lambda sf: (OPEN_MIDI[sf[0]] + sf[1], sf[0]))
        out.extend(band)
    return out


FULL_RUN = _box_order(FULL_MAP)

# D minor on the dropped 6th string alone — one octave, open to the 12th. The
# drop-D party trick: because the low string is tuned to D, the whole scale
# lays out in order along just that one string.
LOW_STRING = [(6, f) for f in (0, 2, 3, 5, 7, 8, 10, 12)]   # D E F G A B♭ C D

# The seven roots, low to high, as a navigation drill.
ROOT_RUN = [(s, f) for (_, s, f) in sorted(
    {(OPEN_MIDI[s] + f, s, f) for (s, f, _) in ROOT_MAP})]

for _label, _seq in (('full-run', FULL_RUN), ('low-string', LOW_STRING),
                     ('root-run', ROOT_RUN)):
    _assert_in_scale(_seq, _label)


def _scale_tab(notes, bars_per_line=4):
    """Asc + desc as eighth-note tab, split into bars of eight."""
    full = notes + notes[:-1][::-1]
    events = [n(s, f, dur=0.5) for s, f in full]
    bars = [events[i:i + 8] for i in range(0, len(events), 8)]
    return render_tab(bars, bars_per_line=bars_per_line, width=900,
                      show_bar_numbers=False)


def _map_card(num, title, role, positions, fret_range, notes, caption,
              box_width=980, box_height=220):
    body = scale_box(positions, fret_range, title=title,
                     width=box_width, height=box_height)
    body += _scale_tab(notes)
    return {"num": num, "title": title, "role": role,
            "body": body, "caption": caption,
            "audio": {"type": "scale", "notes": [[s, f] for s, f in notes]}}


EXERCISE = {
    "slug": "fullneck",
    "order": 5,
    "section": "Scales",
    "title_one": "Full",
    "title_em": "neck",
    "eyebrow": "One Scale, Every Fret",
    "eyebrow_short": "Full neck",
    "subtitle": "D minor across the whole fretboard — the three boxes joined into one.",
    "intro_prose": """
      <p>The <a href="./dminor.html" style="color:var(--accent);font-weight:600;">scale map</a>
      page learns D minor as three boxes. This page erases the walls between
      them: here are the same seven notes —
      <strong>D&nbsp;·&nbsp;E&nbsp;·&nbsp;F&nbsp;·&nbsp;G&nbsp;·&nbsp;A&nbsp;·&nbsp;B♭&nbsp;·&nbsp;C</strong>
      — laid out from the open strings to the 15th fret, all at once.</p>
      <p>The goal is to stop thinking in positions and start seeing one
      connected neck, so a phrase can start anywhere and find its way home.
      Play the full-neck climb — all the way up to the top and back down — to
      feel the boxes link into one, learn the scale along the <em>dropped 6th
      string</em>, then chase the root all over the fretboard.</p>
    """,
    "intro_pills": [
        ("Same seven notes", "D (R) · E (2) · F (♭3) · G (4) · A (5) · B♭ (♭6) · C (♭7)"),
        ("Why it matters", "The solo and twin leads roam the whole neck — boxes alone won't keep up."),
    ],
    "sections": [
        {
            "heading": "The neck as one map",
            "blurb": "Every D-minor note from the nut to the 15th fret. The filled accents are the roots (D). Tap <strong>▶</strong> on any card and the matching dots light up as it plays — set the speed with the metronome and climb slowly.",
            "layout": "full",
            "cards": [
                _map_card(
                    "Map", "The whole neck",
                    "D natural minor · open to the 15th fret",
                    FULL_MAP, (0, 15), FULL_RUN,
                    "Don't memorise this as a picture — use it as a reference while you play. The run climbs the neck box by box: the whole open position first, then the middle box, then the 12th-position box, each one ascending, then the whole thing back down. Every marked note lights up, so you can watch the three boxes link into one connected neck."),
                _map_card(
                    "1 string", "Up the dropped string",
                    "D minor along string 6 · open to the 12th",
                    [(6, f, SCALE_ROLE[_pc(6, f)]) for f in range(0, 13)
                     if _pc(6, f) in SCALE_ROLE],
                    (0, 12), LOW_STRING,
                    "Because string 6 is tuned down to D, the entire scale lies in order along that one string — open is the root, the 12th fret is the root an octave up. A perfect way to hear the intervals and to learn where every note sits without a single position shift."),
                _map_card(
                    "Roots", "Find every root",
                    "Every D on the neck · the home note",
                    ROOT_MAP, (0, 15), ROOT_RUN,
                    "Just the D's. Knowing where home is anywhere on the neck is what lets you land a phrase. Play them low to high, then try to jump to any root without counting frets — string 6 and string 4 share their roots (the drop-D mirror), string 1 fret 10 is the high anchor."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "From the neck to the ",
        "heading_em": "music",
        "heading_two": "",
        "body": "<p>One connected neck is the foundation the lead playing stands on. Take it into the <a href=\"./harmony.html\" style=\"color:var(--accent);font-weight:600;\">harmonized thirds</a> and <a href=\"./leads.html\" style=\"color:var(--accent);font-weight:600;\">lead toolkit</a> pages — both run straight up these notes — and then to the song's <a href=\"./song.html\" style=\"color:var(--accent);font-weight:600;\">solo and duel</a>.</p>",
        "items": [
            ("Climb slow", "Full-neck run with the metronome, one clean pass up and back down. Raise the tempo only when it's spotless."),
            ("One string", "Play the scale along string 6 with your eyes closed — name each note out loud as you land it."),
            ("Root tag", "Improvise in D minor and force every phrase to end on a root, using a different root location each time."),
            ("Join the boxes", "Start a run in the open box and let it climb into the 12th-fret box without stopping. One neck, not three rooms."),
        ],
    },
    "closing": "Three boxes, one fretboard — the whole neck in D minor.",
}
