"""Parse pasted ASCII guitar tab into engraved-SVG tab (tab.render_tab).

The full-song page used to dump the raw ASCII into a <pre>. This reads each
six-line staff "system" the way a player does — frets per string per column,
bar lines, palm-mute brackets, ghost/let-ring parens, hammer/pull/slide/bend
marks — and emits the same note/chord events every other page hand-writes, so
it renders as proper notation.

Fidelity contract (this is a learning tool — see the song page's note):
  * Fret numbers and which string they sit on are read EXACTLY from the source.
  * Rhythm is inferred from horizontal spacing, then each bar is normalised to
    four beats — playback timing is therefore approximate, never authoritative.
  * Techniques we can read unambiguously (PM, ghost notes, hammer-ons,
    pull-offs, slides, bends) are kept; ones that need prose (tap 'T', tremolo
    'TP', vibrato squiggles drawn on their own line, repeat counts) are left
    out of the engraving rather than guessed at.

Anything we can't parse cleanly raises ParseError so the caller can fall back
to the verbatim ASCII for that section — we never show invented notes.
"""

import re

from tab import n, c, render_tab  # noqa: F401


class ParseError(Exception):
    """Raised when a system can't be parsed faithfully — trigger ASCII fallback."""


# A staff line starts with a bar line (optionally a tuning letter before it),
# carries several dashes, and — crucially — has NO spaces: real tab strings are
# solid runs of dashes/frets, while the PM / chord / "Gtr II" annotation lines
# that sit between stacked staves use spaces to align text. That single rule
# keeps a leading-'|' PM line ("|   PM----|  PM----|") from being swallowed
# into the staff above it.
def is_staff_line(line):
    s = line.strip()
    if ' ' in s or s.count('-') < 3:
        return False
    return s.startswith('|') or bool(re.match(r'^[A-Ga-g]\|', s))


# One fret event on a single string. Captures, in priority order:
#   (12)       ghost / let-ring               -> group 'g'
#   12 b14 r12 fretted note, optional bend + release
#   x          dead / muted note
# Putting the bend target inside the match means '14' in '12b14' is consumed
# here and not re-read as a separate note.
_TOKEN_RE = re.compile(
    r'\((?P<g>\d+)\)'
    r'|(?P<f>\d+)(?:b(?P<bt>\d+)(?:r(?P<br>\d+))?)?'
    r'|(?P<x>x)'
)

# Connector characters that sit between two fret events.
_AFTER = {'h': 'hammer_to', 'p': 'pull_to',
          's': 'slide_up', 'S': 'slide_up', '/': 'slide_up', '\\': 'slide_down'}


def _pm_spans(pm_line):
    """Column ranges a 'PM…|' bracket covers, e.g. 'PM----|' -> [(start, end)]."""
    spans = []
    for m in re.finditer(r'PM', pm_line):
        start = m.start()
        bar = pm_line.find('|', m.end())
        end = bar if bar != -1 else m.end() + 10
        spans.append((start, end))
    return spans


def _bar_bounds(staff, width):
    """Columns that act as bar lines — where most strings carry a '|'."""
    cols = [col for col in range(width)
            if sum(1 for s in staff if s[col] == '|') >= 4]
    bounds = []
    for col in cols:
        if bounds and col - bounds[-1] <= 1:
            bounds[-1] = col          # collapse '||' clusters to one boundary
        else:
            bounds.append(col)
    return bounds


def _scale_durations(gap_cols):
    """Turn inter-note column gaps into beat durations summing to 4 per bar."""
    if not gap_cols:
        return []
    total = sum(gap_cols)
    if total <= 0:
        return [4.0 / len(gap_cols)] * len(gap_cols)
    return [g * 4.0 / total for g in gap_cols]


def _parse_bar(staff, lo, hi, pm_spans):
    """Read one bar [lo, hi) of a six-line staff into ordered events."""
    # Collect every fret event with its column and per-note technique opts.
    notes = []   # (col, string_num, fret_or_x, opts)
    for si in range(6):
        sn = si + 1
        line = staff[si]
        seg = line[lo:hi]
        for m in _TOKEN_RE.finditer(seg):
            col = lo + m.start()
            opts = {}
            if m.group('x') is not None:
                fret = 'x'
            elif m.group('g') is not None:
                fret = int(m.group('g'))
                opts['ghost'] = True
            else:
                fret = int(m.group('f'))
                if m.group('bt'):
                    opts['bend_to'] = int(m.group('bt'))
                if m.group('br'):
                    opts['release_to'] = int(m.group('br'))
            # Slide INTO this note from a leading '/' or '\'.
            pre = line[col - 1] if col > 0 else ''
            if pre == '/':
                opts['slide_into_dir'] = 'up'
            elif pre == '\\':
                opts['slide_into_dir'] = 'down'
            # Connector to the NEXT note (hammer/pull/slide) from the char after.
            after = line[lo + m.end()] if lo + m.end() < len(line) else ''
            if after in _AFTER:
                opts[_AFTER[after]] = True
            # Palm mute if this column sits under a PM bracket.
            if any(a <= col < b for a, b in pm_spans):
                opts['pm'] = True
            notes.append((col, sn, fret, opts))

    if not notes:
        return []

    # Group simultaneous notes (same column ± 1) into chords.
    notes.sort(key=lambda t: t[0])
    groups = []   # (col, [(sn, fret, opts), ...])
    for col, sn, fret, opts in notes:
        if groups and col - groups[-1][0] <= 1:
            groups[-1][1].append((sn, fret, opts))
        else:
            groups.append((col, [(sn, fret, opts)]))

    # Durations from the gaps between successive group columns; the final
    # group runs to the bar's end.
    cols = [g[0] for g in groups]
    gaps = [cols[i + 1] - cols[i] for i in range(len(cols) - 1)]
    gaps.append(max(1, hi - cols[-1]))
    durs = _scale_durations(gaps)

    events = []
    for (col, members), dur in zip(groups, durs):
        if len(members) == 1:
            sn, fret, opts = members[0]
            events.append(n(sn, fret, dur, **opts))
        else:
            # Chord: keep hammer/pull/slide/ghost/pm if shared; pm matters most.
            shared = {}
            if any(o.get('pm') for _, _, o in members):
                shared['pm'] = True
            if all(o.get('ghost') for _, _, o in members):
                shared['ghost'] = True
            events.append(c([(sn, fret) for sn, fret, _ in members], dur, **shared))
    return events


def _chord_labels_for(bars_cols, chord_line):
    """Pick a chord name (from the header line) for each bar by column overlap."""
    if not chord_line:
        return None
    tokens = []   # (col, name)
    # 'N.C.' (no chord) is matched only so it can be skipped — we don't label
    # bars with it. Real chord names are kept.
    CH = re.compile(
        r'N\.C\.|[A-G](?:#|b)?(?:\+?5|maj7|m7|sus[24]?|aug|dim|add\d+|m|7|9|6|\+)?'
        r'(?:/[A-G](?:#|b)?)?')
    for m in CH.finditer(chord_line):
        name = m.group()
        if name == 'N.C.':
            continue
        # Skip D.S./D.C. navigation markers (start with a chord letter).
        if chord_line[m.end():m.end() + 2] in ('.S', '.C'):
            continue
        tokens.append((m.start(), name))
    if not tokens:
        return None
    labels = []
    for lo, hi in bars_cols:
        pick = ''
        for col, name in tokens:
            if lo <= col < hi:
                pick = name
                break
        labels.append(pick)
    return labels if any(labels) else None


def parse_system(staff, pm_line='', chord_line=''):
    """Parse one six-line staff into (bars, labels, note_count).

    Raises ParseError if the staff doesn't look parseable.
    """
    if len(staff) != 6:
        raise ParseError(f'system has {len(staff)} lines, expected 6')
    width = max(len(s) for s in staff)
    staff = [s.ljust(width) for s in staff]
    pm_line = (pm_line or '').ljust(width)
    pm_spans = _pm_spans(pm_line)

    bounds = _bar_bounds(staff, width)
    if not bounds:
        raise ParseError('no bar lines found')

    # Regions between consecutive boundaries, plus any trailing content.
    regions = [(bounds[i] + 1, bounds[i + 1]) for i in range(len(bounds) - 1)]
    if bounds[-1] + 1 < width:
        regions.append((bounds[-1] + 1, width))

    bars, bars_cols = [], []
    for lo, hi in regions:
        evs = _parse_bar(staff, lo, hi, pm_spans)
        if evs:
            bars.append(evs)
            bars_cols.append((lo, hi))
    # An all-dashes staff is a resting guitar (e.g. the second voice that drops
    # out for a bar) — legitimately empty, not a parse failure. Return empty and
    # let the caller skip it.
    labels = _chord_labels_for(bars_cols, chord_line)
    note_count = sum(len(b) for b in bars)
    return bars, labels, note_count


def _voices_from_lines(lines):
    """Find the six-line staff voices (with PM / chord / label context) in a
    block of lines, top to bottom. Raises ParseError on a bad staff run."""
    voices = []
    i = 0
    while i < len(lines):
        if not is_staff_line(lines[i]):
            i += 1
            continue
        j = i
        while j < len(lines) and is_staff_line(lines[j]):
            j += 1
        run = lines[i:j]
        if len(run) % 6 != 0:
            raise ParseError(f'staff run of {len(run)} lines (not a multiple of 6)')

        # Context = the non-blank, non-staff lines directly above this run.
        ctx = []
        k = i - 1
        while k >= 0 and lines[k].strip() and not is_staff_line(lines[k]):
            ctx.append(lines[k])
            k -= 1
        ctx.reverse()
        pm = next((ln for ln in reversed(ctx) if 'PM' in ln), '')
        chords = next((ln for ln in ctx if _looks_like_chords(ln)), '')
        label = ''
        for ln in ctx:
            gm = re.search(r'Gtrs?\s+[IVX]+(?:\s*,\s*[IVX]+)*', ln)
            if gm:
                label = gm.group().strip()
                break

        for s in range(0, len(run), 6):
            voices.append({
                'staff': run[s:s + 6],
                'pm': pm if s == 0 else '',
                'chords': chords if s == 0 else '',
                'label': label,
            })
        i = j
    return voices


def split_groups(body):
    """Split a section into measure-groups (separated by blank lines), each a
    list of stacked voices. Blank lines delimit consecutive passages of the
    song; a single '|' / 'Gtr II' line only separates the voices inside one."""
    chunks, cur = [], []
    for ln in body.split('\n'):
        if ln.strip() == '':
            if cur:
                chunks.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        chunks.append(cur)
    groups = [vs for vs in (_voices_from_lines(c) for c in chunks) if vs]
    if not groups:
        raise ParseError('no staff systems found')
    return groups


def _looks_like_chords(line):
    # Chord header lines sit above the staff: no bar lines, no lowercase
    # (rejects 'Gtr'/'PM'/'TP'), and carry a chord-letter token.
    if '|' in line or any(c.islower() for c in line):
        return False
    return bool(re.search(r'[A-G](?:#|b)?', line))


def _voice_tracks(groups):
    """Turn the parsed measure-groups into per-guitar tracks of (bars, labels).

    The common voices — those present in every group — are deinterleaved so
    each guitar's bars run continuously across the whole section (group 1's
    Gtr I + group 2's Gtr I + …); that's what lets them lay out four bars to a
    line like real notation. Any extra voice that only some (taller) groups
    carry — e.g. a lead line that enters for one passage — is kept as its own
    track in reading order rather than forced into an alignment that isn't real.
    """
    counts = [len(g) for g in groups]
    height = min(counts) if counts else 0
    tracks = []
    if len(groups) >= 2 and height >= 1:
        for k in range(height):
            mbars, mlabels, label = [], [], ''
            for g in groups:
                bars, labels, _ = parse_system(g[k]['staff'], g[k]['pm'], g[k]['chords'])
                mbars += bars
                mlabels += (labels or [''] * len(bars))
                if not label and g[k]['label']:
                    label = g[k]['label']
            tracks.append((mbars, mlabels, label))
        for g in groups:                      # extra voices in taller groups
            for k in range(height, len(g)):
                bars, labels, _ = parse_system(g[k]['staff'], g[k]['pm'], g[k]['chords'])
                tracks.append((bars, labels or [''] * len(bars), g[k]['label']))
        return tracks
    for g in groups:
        for v in g:
            bars, labels, _ = parse_system(v['staff'], v['pm'], v['chords'])
            tracks.append((bars, labels or [''] * len(bars), v['label']))
    return tracks


def render_section(body, bars_per_line=4):
    """Engrave a whole section body as a stacked score + audio.

    Returns (html, audio_dict, together_dict) or raises ParseError.

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
    tracks = [t for t in _voice_tracks(split_groups(body)) if t[0]]
    if not tracks:
        raise ParseError('no notes parsed')

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
    for r in range(n_rows):
        lo = r * bars_per_line
        staves = []
        for vi, (bars, labels, label) in enumerate(tracks):
            chunk = bars[lo:lo + bars_per_line]
            if not chunk:
                continue
            start = bases[vi] + sum(len(b) for b in bars[:lo])
            staves.append(render_tab(
                chunk,
                chord_labels=labels[lo:lo + bars_per_line],
                bars_per_line=bars_per_line,
                width=row_w,
                beat_unit=4,
                title=label or None if r == 0 else None,
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
    data-i the voice's first note carries. Each voice's bars are normalised to
    four beats, so notes on the same beat across guitars line up; we collect
    every onset, emitting one chord (all strings sounding there) plus the
    data-i of every contributing note so the player can light them all at once.
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
    """Append one audio slot per rendered note/chord, in render order.

    Ghosts (let-ring) and dead 'x' notes become silent rests so the array stays
    index-aligned with the engraved notes while not re-triggering held strings.
    """
    for bar in bars:
        for ev in bar:
            kind = ev[0]
            if kind == 'note':
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
