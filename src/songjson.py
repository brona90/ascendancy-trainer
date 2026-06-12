"""Engrave the full song from src/song.json — a structured tab export.

Unlike the old ASCII pipeline, nothing here is inferred from horizontal
spacing: the JSON carries exact durations (dots and tuplets already
folded into the duration fraction), explicit rests, ties, hammer-ons /
pull-offs, slides, bends and per-beat palm mute. The engraving and the
playback both carry the source's actual rhythm.

Every guitar track must be in drop D (checked at load — a track in
another tuning would silently play wrong pitches through the shared
synth, so we refuse it loudly instead).

Shape of the JSON (see meta/schema inside the file):
  tracks[].measures[].voices[].beats[] — each beat has notes[], a
  duration [num, den] as a fraction of a whole note, and optional
  rest / palmMute / vibrato flags; each note has fret, string and
  optional tie / hp / slide / bend / vibrato / accentuated.

CAUTION — the schema text inside the JSON claims `string` is 1-indexed
(1 = highest), but the data is 0-indexed from the highest string: the
values run 0–5, and only the 0-indexed reading turns the song's 454
two-note dyads into perfect octaves (1-indexed makes them all major
sevenths) and its barre chords into drop-D power chords. We convert to
the app's 1-indexed strings here, in one place.
"""

import json
import os

from tab import n, c, r
from songtab import render_tracks

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SRC_DIR, 'song.json')

# The drop-D MIDI tuning every page (and the synth) assumes, string 1 → 6.
DROP_D_MIDI = [64, 59, 55, 50, 45, 38]

# Short stave titles per partId — the JSON's track names carry full
# player/gear credits ("Corey Beaulieu | Jackson USA Signature …").
_STAVE_TITLES = {
    1: 'Gtr I · Corey',
    2: 'Gtr II · Heafy',
    3: 'Gtr III · additional',
    4: 'Gtr IV · additional',
}


def load():
    with open(JSON_PATH, encoding='utf-8') as f:
        return json.load(f)


def _guitar_tracks(data):
    """The fretted-guitar tracks, in part order. Drops choir/drums/bass."""
    out = []
    for t in data['tracks']:
        if 'Guitar' not in (t.get('instrument') or ''):
            continue
        if t.get('tuningMidi') != DROP_D_MIDI:
            raise ValueError(
                f"track {t.get('partId')} ({t.get('name')!r}) is not in drop D: "
                f"{t.get('tuningMidi')}")
        out.append(t)
    return out


def _next_fret_same_string(flat, i, string):
    """Fret of the next sounding note on `string`, looking only at the
    immediately following beat — that's the note an hp/slide connects to."""
    if i + 1 >= len(flat):
        return None
    for nt in flat[i + 1][1].get('notes', []):
        if not nt.get('rest') and nt.get('string') == string:
            return nt.get('fret')
    return None


def _note_opts(nt, nxt_fret):
    """Per-note technique opts in tab.py's vocabulary."""
    o = {}
    if nt.get('tie'):
        # Tied = still ringing from the previous attack: engraved in parens,
        # and _extend_audio turns ghosts into silent slots so the string
        # isn't re-plucked.
        o['ghost'] = True
    if nt.get('vibrato') or nt.get('wideVibrato'):
        o['vibrato'] = True
    bend = nt.get('bend')
    if bend:
        # bend tone is in cents-of-a-fret-pair: 50 = half step, 100 = full.
        o['bend_to'] = nt['fret'] + max(1, round(bend.get('tone', 100) / 50))
    if nt.get('hp'):
        # The flag sits on the origin note; direction decides hammer vs pull.
        if nxt_fret is not None and nxt_fret < nt['fret']:
            o['pull_to'] = True
        else:
            o['hammer_to'] = True
    slide = nt.get('slide')
    if slide in ('shift', 'legato'):
        if nxt_fret is not None and nxt_fret < nt['fret']:
            o['slide_down'] = True
        else:
            o['slide_up'] = True
    elif slide == 'downwards':
        o['slide_down'] = True
    elif slide == 'below':
        o['slide_into_dir'] = 'up'
    elif slide == 'above':
        o['slide_into_dir'] = 'down'
    return o


def _track_bars(track, lo, hi):
    """Measures [lo, hi) of one track → list of bars of tab.py events.

    Every measure yields a bar — whole-bar rests included — so the stacked
    staves and the Together mix stay aligned across guitars.
    """
    flat = []   # (bar_index, beat) in playing order
    for bi, m in enumerate(track['measures'][lo:hi]):
        voices = m.get('voices') or [{}]
        for b in voices[0].get('beats', []):
            flat.append((bi, b))

    bars = [[] for _ in range(hi - lo)]
    for i, (bi, b) in enumerate(flat):
        num, den = b['duration']
        dur = round(4.0 * num / den, 4)
        notes = [x for x in b.get('notes', []) if not x.get('rest')]
        if b.get('rest') or not notes:
            bars[bi].append(r(dur))
            continue
        shared = {}
        if b.get('palmMute'):
            shared['pm'] = True
        if b.get('vibrato') or b.get('wideVibrato'):
            shared['vibrato'] = True
        if any(x.get('accentuated') for x in notes):
            shared['accent'] = True
        # Tied chord members are still ringing from the previous attack —
        # only the untied notes are struck. An all-tied beat becomes a ghost
        # (engraved in parens, silent slot in the audio).
        struck = [x for x in notes if not x.get('tie')]
        if not struck:
            shared['ghost'] = True
            struck = notes
        if len(struck) == 1:
            nt = struck[0]
            opts = _note_opts(nt, _next_fret_same_string(flat, i, nt['string']))
            opts.update(shared)
            bars[bi].append(n(nt['string'] + 1, nt['fret'], dur, **opts))
        else:
            bars[bi].append(c([(x['string'] + 1, x['fret']) for x in struck],
                              dur, **shared))
    # A measure with no beats at all (shouldn't happen, but stay aligned).
    for bar in bars:
        if not bar:
            bar.append(r(4.0))
    return bars


def _has_sound(bars):
    return any(ev[0] in ('note', 'chord') and not ev[-1].get('ghost')
               for bar in bars for ev in bar)


def section_cards(data=None, bars_per_line=4):
    """One dict per song section, in playing order:

      {title, lo, hi, n_guitars, html, audio, together}

    lo/hi are 0-based measure bounds [lo, hi); html/audio/together come from
    songtab.render_tracks (stacked staves, per-guitar playback, full-band mix).
    """
    data = data or load()
    guitars = _guitar_tracks(data)
    secs = data['meta']['sections']
    total = data['meta']['totalMeasures']
    cards = []
    for i, sec in enumerate(secs):
        lo = sec['measure']
        hi = secs[i + 1]['measure'] if i + 1 < len(secs) else total
        tracks = []
        for t in guitars:
            bars = _track_bars(t, lo, hi)
            if _has_sound(bars):
                title = _STAVE_TITLES.get(t['partId'], t.get('name') or 'Gtr')
                tracks.append((bars, None, title))
        if not tracks:
            continue
        html, audio, together = render_tracks(tracks, bars_per_line)
        cards.append({
            'title': sec['name'],
            'lo': lo,
            'hi': hi,
            'n_guitars': len(tracks),
            'html': html,
            'audio': audio,
            'together': together,
        })
    return cards
