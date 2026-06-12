"""Full song — the complete piece, broken into section cards to learn.

The song lives as one ASCII tab in src/song_tab.txt. Each section becomes a
card: it's engraved as proper notation (songtab → tab.render_tab) so it reads
and lights up like every other page, with the chords / tempo / guitar count
shown as chips. A section we can't engrave faithfully falls back to the exact
ASCII so the student never sees an invented note.
"""

import html
import os
import re

import songtab

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB_PATH = os.path.join(SRC_DIR, 'song_tab.txt')


# Bare (unbracketed) section headings are auto-detected too — a short line
# containing one of these words and no tab characters starts a new card.
# Covers the headings most published-style ASCII tabs use.
SECTION_WORDS = re.compile(
    r'(?i)\b(intro|outro|verse|chorus|pre-?chorus|bridge|solo|interlude|'
    r'duel|breakdown|refrain|riff)\b')


def _is_bare_heading(line):
    s = line.strip()
    return (0 < len(s) <= 40 and '|' not in s and '--' not in s
            and SECTION_WORDS.search(s))


def load_sections():
    """Parse song_tab.txt → [(title, text), ...]. '#' lines are ignored.

    Sections start at a [Bracketed] header OR a bare heading line like
    'Verse' / 'Pre-Chorus' / "Heafy's Solo".
    """
    if not os.path.exists(TAB_PATH):
        return []
    sections = []
    title = None
    lines = []

    def flush():
        body = '\n'.join(lines).strip('\n')
        if title is not None or body:
            sections.append((title or 'Song', body))

    def start(new_title):
        nonlocal title, lines
        if title is not None or any(s.strip() for s in lines):
            flush()
        title = new_title
        lines = []

    for line in open(TAB_PATH, encoding='utf-8').read().splitlines():
        if line.lstrip().startswith('#'):
            continue
        m = re.match(r'\s*\[(.+?)\]\s*$', line)
        if m:
            start(m.group(1))
        elif _is_bare_heading(line):
            start(line.strip())
        else:
            lines.append(line)
    flush()
    return [(t, b) for t, b in sections if b.strip()]


# ── ASCII-tab → playable sequence ────────────────────────────────────
# Heuristic parser: each character column ≈ one sixteenth note. A
# "system" is 6 consecutive staff lines (lines starting with '|' that
# carry at least a few dashes); the top line is string 1 (high E).
# Parenthesised numbers are ties/ghosts (already ringing) and 'x' is a
# mute — both are skipped. Stacked guitar parts play back-to-back.

def _is_staff_line(line):
    s = line.strip()
    return (s.startswith('|') or re.match(r'^[A-Ga-g]\|', s)) and s.count('-') >= 3


def _split_systems(body):
    systems, run = [], []
    for ln in body.splitlines():
        if _is_staff_line(ln):
            run.append(ln)
        else:
            if len(run) >= 6:
                systems.append(run[:6])
            run = []
    if len(run) >= 6:
        systems.append(run[:6])
    return systems


def _system_events(staff):
    notes = []
    for si, ln in enumerate(staff):
        for m in re.finditer(r'\d+', ln):
            col = m.start()
            if col > 0 and ln[col - 1] == '(':
                continue          # tie / let-ring — note already sounding
            fret = int(m.group())
            if fret > 24:
                continue          # annotation (e.g. a '4x' repeat), not a fret
            notes.append((col, si + 1, fret))
    if not notes:
        return []
    notes.sort()
    groups = []                   # columns within 1 char are one hit (chords)
    for col, s, f in notes:
        if groups and col - groups[-1][0] <= 1:
            groups[-1][1].append([s, f])
        else:
            groups.append((col, [[s, f]]))
    events = []
    for i, (col, sf) in enumerate(groups):
        dur = ((groups[i + 1][0] - col) * 0.25 if i + 1 < len(groups) else 1.0)
        dur = max(0.25, min(2.0, dur))
        if len(sf) == 1:
            events.append({"string": sf[0][0], "fret": sf[0][1], "dur": dur})
        else:
            events.append({"chord": sf, "dur": dur})
    return events


def section_audio(body):
    seq = []
    for staff in _split_systems(body):
        evs = _system_events(staff)
        if not evs:
            continue
        if seq:
            seq.append({"rest": True, "dur": 1.0})   # breath between systems
        seq.extend(evs)
    if not seq:
        return None
    return {"type": "sequence", "notes": seq, "gain": 0.45}


# ── Section metadata — surfaced as chips + a per-card subtitle ────────
# Each card used to carry an identical role + caption, so every section in
# the song looked the same. Instead we mine the tab text a guitarist already
# wrote above the staves — tempo (Q=…), time signature, chord symbols, how
# many guitar voices are stacked, and any repeat marks (4x / 8x) — and show
# them, so each card announces what it actually is.

_ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
_CHORD_RE = re.compile(
    r'N\.C\.|'
    r'[A-G](?:#|b)?(?:\+?5|maj7|m7|sus[24]?|aug|dim|add\d+|m|7|9|6|\+)?'
    r'(?:/[A-G](?:#|b)?)?'
)


def _chords_in(line):
    """Chord tokens on a header line, or [] if it isn't one.

    A chord line sits above the staff: no bar lines, no lowercase (which
    cleanly rejects 'Gtr', 'PM', 'TP', repeat 'x' marks). Navigation markers
    like D.S. / D.C. start with a chord letter but aren't chords — drop them.
    """
    if '|' in line or any(c.islower() for c in line):
        return []
    out = []
    for m in _CHORD_RE.finditer(line):
        name = m.group()
        if name == 'N.C.':
            continue   # "no chord" — don't surface it as a chord
        if line[m.end():m.end() + 2] in ('.S', '.C'):
            continue   # D.S. / D.C. dal-segno / da-capo marker, not a chord
        out.append(name)
    return out


def section_meta(body):
    """Mine display metadata from a section's tab text."""
    tempo = timesig = None
    guitars = set()
    repeats = []
    chords = []
    seen = set()
    for raw in body.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s:
            continue
        is_staff = _is_staff_line(line)
        if not is_staff:
            mt = re.search(r'Q\s*=\s*(\d+)', s)
            if mt:
                tempo = int(mt.group(1))
            mts = re.search(r'\b(\d+/\d+)\b', s)
            if mts:
                timesig = mts.group(1)
            for g in re.findall(r'Gtrs?\s+([IVX]+(?:\s*,\s*[IVX]+)*)', s):
                for r in re.findall(r'[IVX]+', g):
                    if r in _ROMAN:
                        guitars.add(_ROMAN[r])
            for r in re.findall(r'(?<!\d)(\d+)x\b', s):
                if r not in repeats:
                    repeats.append(r)
            for m in _chords_in(line):
                if m not in seen:
                    seen.add(m)
                    chords.append(m)
    return {
        "tempo": tempo,
        "timesig": timesig,
        "guitars": max(guitars) if guitars else None,
        "repeats": repeats,
        "chords": chords,
    }


def _chip(text, kind=""):
    cls = "song-tag" + (f" song-tag-{kind}" if kind else "")
    return f'<span class="{cls}">{html.escape(text)}</span>'


def _meta_row(meta):
    chips = []
    for ch in meta["chords"][:8]:
        chips.append(_chip(ch, "chord"))
    if meta["tempo"]:
        chips.append(_chip(f'♩ {meta["tempo"]}', "tempo"))
    if meta["timesig"]:
        chips.append(_chip(meta["timesig"]))
    if meta["guitars"]:
        n = meta["guitars"]
        chips.append(_chip(f'{n} guitar' + ('s' if n != 1 else '')))
    for r in meta["repeats"]:
        chips.append(_chip(f'×{r}', "rep"))
    if not chips:
        return ""
    return '<div class="song-meta">' + ''.join(chips) + '</div>'


def _role_for(meta):
    if meta["chords"]:
        head = ' → '.join(meta["chords"][:3])
        return head + (' …' if len(meta["chords"]) > 3 else '')
    if meta["guitars"]:
        n = meta["guitars"]
        return f'{n} guitar' + ('s' if n != 1 else '') + ' stacked'
    return 'Drop D riff'


def section_card(idx, title, body):
    meta = section_meta(body)
    # Engrave as notation when we can read it faithfully; otherwise show the
    # exact ASCII so a student never learns an invented note.
    together = None
    try:
        tab_html, audio, together = songtab.render_section(body)
    except songtab.ParseError:
        tab_html = ('<div class="song-tab-sheet"><pre>'
                    + html.escape(body) + '</pre></div>')
        audio = section_audio(body)
    card = {
        "num": f"§{idx}",
        "title": title,
        "role": _role_for(meta),
        "body": _meta_row(meta) + tab_html,
    }
    if audio:
        card["audio"] = audio
    if together:
        card["audio_together"] = together
    return card


def build_sections():
    sections = load_sections()
    if not sections:
        return []
    cards = [section_card(i + 1, t, b) for i, (t, b) in enumerate(sections)]
    return [{
        "heading": "The song, section by section",
        "blurb": "The whole song, in playing order. Each card shows one "
                 "section's chords, tempo and guitar parts — tap it to read "
                 "the tab fullscreen, or hit <strong>▶</strong> to hear it and "
                 "watch the notes light up. Set the speed with the metronome "
                 "(bottom-right) and slow anything down until it's clean. "
                 "Rhythm in playback is approximate — your ears and the "
                 "official tab are the final word. When a part fights you, the "
                 "skill that builds it is one click away on the "
                 "<a href=\"./roadmap.html\" style=\"color:var(--accent);"
                 "font-weight:600;\">roadmap</a>.",
        "layout": "full",
        "cards": cards,
    }]


EXERCISE = {
    "slug": "song",
    "order": 9,
    "section": "The Song",
    "title_one": "Full",
    "title_em": "song",
    "eyebrow": "Ascendancy · Drop D · Full Arrangement",
    "eyebrow_short": "Full song",
    "subtitle": "The complete piece, broken into sections you can learn one at a time.",
    "intro_prose": """
      <p>This is the whole song, in order, split into the sections it's
      actually built from — <em>intro, verse, pre-chorus, chorus, the
      bridges, the solo and the duel</em>. Each card carries that section's
      tab, its chords and tempo, and a play button.</p>
      <p>Learn it one card at a time: play a section back, slow it down with
      the metronome until your hands keep up, then speed it up. The lit notes
      show you where you are; the official tab is the source of truth for the
      fine detail.</p>
    """,
    "intro_pills": [
        ("How to use it", "Pick a section, play it slow, repeat it, speed it up. Then join it to the next."),
        ("Drop D", "Every fret here is in drop D — the low string sounds a D. Tune up before you start."),
    ],
    "sections": build_sections(),
    "next_step": {
        "heading_one": "Put the sections ",
        "heading_em": "together",
        "heading_two": "",
        "body": "<p>Once a section is clean on its own, assemble the song with the <a href=\"./roadmap.html\" style=\"color:var(--accent);font-weight:600;\">roadmap</a> method: chunk it, climb the tempo ladder, then practise the <em>seams</em> where one section hands off to the next. The metronome carries your tempo across every page.</p>",
        "items": [
            ("Start slow", "Drop the metronome until you can play a section with zero mistakes — then raise it a few bpm at a time."),
            ("Loop the hard bar", "Open a card fullscreen and use the loop button to drill the one bar that trips you."),
            ("Mind the seams", "The transitions between sections are their own skill. Practise the last bar of one into the first bar of the next."),
        ],
    },
    "closing": "Learn the sections, link the seams, and the song plays itself.",
}
