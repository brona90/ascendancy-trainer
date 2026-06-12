"""Shared helpers for the Ascendancy trainer exercises.

Everything on this site lives in DROP D (D2 A2 D3 G3 B3 E4) — string 6
is tuned a whole step down, so its open-string MIDI value is 38.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tab import n, c, r, render_tab            # noqa: F401, E402
from fretboard import chord_strip, scale_box   # noqa: F401, E402


# Drop D open-string MIDI values — keep in sync with OPEN_MIDI in render.py.
OPEN_MIDI = {6: 38, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}


# ── One-finger power chords (drop D, strings 6-5-4) ──────────────────
# Shape arrays are ordered low-to-high string (6 → 1) for chord_box.
PC_ROLES = {6: 'R', 5: '5', 4: 'R'}

D5_SHAPE  = [0, 0, 0, None, None, None]
E5_SHAPE  = [2, 2, 2, None, None, None]
F5_SHAPE  = [3, 3, 3, None, None, None]
G5_SHAPE  = [5, 5, 5, None, None, None]
A5_SHAPE  = [7, 7, 7, None, None, None]
BB5_SHAPE = [8, 8, 8, None, None, None]
C5_SHAPE  = [10, 10, 10, None, None, None]

# The same chords as (string, fret) note lists for tab/chord events.
D5  = [(6, 0), (5, 0), (4, 0)]
E5  = [(6, 2), (5, 2), (4, 2)]
F5  = [(6, 3), (5, 3), (4, 3)]
G5  = [(6, 5), (5, 5), (4, 5)]
A5  = [(6, 7), (5, 7), (4, 7)]
BB5 = [(6, 8), (5, 8), (4, 8)]
C5  = [(6, 10), (5, 10), (4, 10)]


def audio_from_bars(bars, bpm=100, gain=0.45, strum=False):
    """Turn tab bars into a playable sequence dict.

    strum=True → chord events play with a tiny strum offset.
    strum=False → chord events sound together (a pick stab).
    """
    seq = []
    for bar in bars:
        for ev in bar:
            kind = ev[0]
            if kind == 'note':
                _, s, f, opts = ev
                seq.append({"string": s, "fret": f, "dur": opts.get('dur', 0.5)})
            elif kind == 'chord':
                _, notes, opts = ev
                if notes:
                    key = 'strum' if strum else 'chord'
                    seq.append({key: notes, "dur": opts.get('dur', 0.5)})
            elif kind == 'rest':
                _, opts = ev
                seq.append({"rest": True, "dur": opts.get('dur', 0.5)})
    return {"type": "sequence", "notes": seq, "bpm": bpm, "gain": gain}


def tab_card(num, title, role, bars, labels=None, caption='', bpm=100,
             bars_per_line=4, width=900, chords=None, strum=False, gain=0.45):
    """Standard card: optional chord strip + rendered tab + audio."""
    tab_svg = render_tab(bars, chord_labels=labels, bars_per_line=bars_per_line,
                         width=width)
    strip = chord_strip(chords) if chords else ''
    return {
        "num": num, "title": title, "role": role,
        "body": strip + tab_svg, "caption": caption,
        "audio": audio_from_bars(bars, bpm=bpm, strum=strum, gain=gain),
    }
