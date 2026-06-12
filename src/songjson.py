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

from tab import n, c, r, render_tab

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


def render_tracks(tracks, bars_per_line=4):
    """Engrave per-guitar tracks of (bars, labels, label) as a stacked score.

    Returns (html, audio_dict, together_dict).

    Layout is a real score: the guitars are stacked and aligned, four bars to a
    row, then the next four bars in the row below — so you read all the parts
    that sound together (e.g. the solo's two rhythm guitars under the lead) the
    way the original tab stacks them. Every stave shares one pixels-per-bar so a
    note is the same size everywhere, and rows scroll sideways on a narrow
    screen rather than being squeezed.

    `audio` plays the parts one guitar at a time (each guitar's whole part in
    order) and its note indices line up with the engraved tab-notes' data-i, so
    the playhead lights the right note. `together` layers all the guitars on one
    timeline (the full band) and carries, per beat, the data-i of every note
    that sounds there, so it lights them all at once across the stacked staves.
    """
    # Per-voice base index (track-major) — this is the order `audio` plays in
    # and the data-i each voice's notes carry, regardless of the row layout.
    bases, acc = [], 0
    for bars, _labels, _label in tracks:
        bases.append(acc)
        acc += sum(len(b) for b in bars)

    # One pixels-per-bar for the whole section keeps bars aligned across the
    # stacked staves and notes a uniform size; denser sections get more room.
    densest = max((len(b) for bars, _l, _lab in tracks for b in bars), default=4)
    bar_width = max(220, min(360, densest * 17))
    row_w = bars_per_line * bar_width
    n_rows = max((len(bars) + bars_per_line - 1) // bars_per_line
                 for bars, _l, _lab in tracks)

    rows_html = []
    for row in range(n_rows):
        lo = row * bars_per_line
        staves = []
        for vi, (bars, labels, label) in enumerate(tracks):
            chunk = bars[lo:lo + bars_per_line]
            if not chunk:
                continue
            start = bases[vi] + sum(len(b) for b in bars[:lo])
            staves.append(render_tab(
                chunk,
                chord_labels=labels[lo:lo + bars_per_line] if labels else None,
                bars_per_line=bars_per_line,
                width=row_w,
                beat_unit=4,
                title=label or None if row == 0 else None,
                show_bar_numbers=False,
                note_seq_start=start,
                fixed_px=True,
            ))
        if staves:
            rows_html.append('<div class="song-row">' + ''.join(staves) + '</div>')

    seq = []
    for bars, _labels, _label in tracks:
        _extend_audio(seq, bars)
    audio = {"type": "sequence", "notes": seq, "gain": 0.42} if seq else None
    together = (_together_sequence(list(zip(bases, (t[0] for t in tracks))))
                if len(tracks) > 1 else None)
    return '<div class="song-staves">' + ''.join(rows_html) + '</div>', audio, together


def _together_sequence(base_bars):
    """Layer every voice on one timeline so the section plays as a full band.

    `base_bars` is a list of (base_index, bars) per voice — base_index is the
    data-i the voice's first note carries. Notes on the same beat across
    guitars line up; we collect every onset, emitting one chord (all strings
    sounding there) plus the data-i of every contributing note so the player
    can light them all at once.
    """
    onsets = {}   # beat -> {'sf': [(s,f)...], 'idx': set()}
    for base, bars in base_bars:
        beat, k = 0.0, base
        for bar in bars:
            for ev in bar:
                dur = ev[-1].get('dur', 0.5)
                members = []
                if ev[0] == 'note':
                    _, s, f, o = ev
                    if not o.get('ghost') and isinstance(f, int):
                        members = [(s, f)]
                elif ev[0] == 'chord':
                    _, notes, o = ev
                    if not o.get('ghost'):
                        members = [(s, f) for s, f in notes if isinstance(f, int)]
                if members:
                    m = onsets.setdefault(round(beat, 3), {'sf': [], 'idx': set()})
                    m['sf'].extend(members)
                    m['idx'].add(k)
                beat += dur
                k += 1
    if not onsets:
        return None
    times = sorted(onsets)
    out = []
    for i, b in enumerate(times):
        dur = max(0.12, (times[i + 1] if i + 1 < len(times) else b + 1.0) - b)
        seen, uniq = set(), []
        for sf in onsets[b]['sf']:
            if sf not in seen:
                seen.add(sf)
                uniq.append([sf[0], sf[1]])
        out.append({"chord": uniq, "dur": dur, "idx": sorted(onsets[b]['idx'])})
    return {"type": "sequence", "notes": out, "gain": 0.4}


def _extend_audio(seq, bars):
    """Append one audio slot per rendered event, in render order.

    Ghosts (ties / let-ring) become silent rests so the array stays
    index-aligned with the engraved notes while not re-triggering held
    strings. Explicit rest events get a slot too — render_tab advances
    data-i on every event, so the audio array must as well.
    """
    for bar in bars:
        for ev in bar:
            kind = ev[0]
            if kind == 'rest':
                seq.append({"rest": True, "dur": ev[-1].get('dur', 0.5)})
            elif kind == 'note':
                _, s, f, opts = ev
                dur = opts.get('dur', 0.5)
                if opts.get('ghost') or not isinstance(f, int):
                    seq.append({"rest": True, "dur": dur})
                else:
                    seq.append({"string": s, "fret": f, "dur": dur})
            elif kind == 'chord':
                _, notes, opts = ev
                dur = opts.get('dur', 0.5)
                playable = [(s, f) for s, f in notes if isinstance(f, int)]
                if opts.get('ghost') or not playable:
                    seq.append({"rest": True, "dur": dur})
                else:
                    seq.append({"chord": playable, "dur": dur})


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
