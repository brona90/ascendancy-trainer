"""Full song — the complete piece, broken into section cards to learn.

The song lives as structured tab data in src/song.json (exact rhythm:
durations, rests, ties, techniques — see songjson.py). Each section
becomes a card engraved as proper notation with stacked guitar staves,
chips for tempo / meter / guitar count / bar range, per-guitar playback
and a full-band Together mix.
"""

import songjson


def _chip(text, kind=""):
    cls = "song-tag" + (f" song-tag-{kind}" if kind else "")
    return f'<span class="{cls}">{text}</span>'


def _meta_row(sec, tempo, timesig):
    n_g = sec["n_guitars"]
    chips = [
        _chip(f'♩ {tempo}', "tempo"),
        _chip(timesig),
        _chip(f'{n_g} guitar' + ('s' if n_g != 1 else '')),
        _chip(f'bars {sec["lo"] + 1}–{sec["hi"]}'),
    ]
    return '<div class="song-meta">' + ''.join(chips) + '</div>'


def build_sections():
    data = songjson.load()
    tempo = data['meta'].get('tempo')
    timesig = data['meta'].get('timeSignature', '4/4')
    cards = []
    for i, sec in enumerate(songjson.section_cards(data), 1):
        n_g = sec["n_guitars"]
        card = {
            "num": f"§{i}",
            "title": sec["title"],
            "role": (f'{n_g} guitar' + ('s' if n_g != 1 else '')
                     + f' · {sec["hi"] - sec["lo"]} bars'),
            "body": _meta_row(sec, tempo, timesig) + sec["html"],
        }
        if sec["audio"]:
            card["audio"] = sec["audio"]
        if sec["together"]:
            card["audio_together"] = sec["together"]
        cards.append(card)
    return [{
        "heading": "The song, section by section",
        "blurb": "The whole song, in playing order, engraved from a "
                 "structured tab — durations, rests and ties are exact, not "
                 "inferred. Each card stacks every guitar that plays in that "
                 "section; tap it to read fullscreen, hit <strong>▶</strong> "
                 "to hear the parts one guitar at a time, or "
                 "<strong>Together</strong> for the full band — the notes "
                 "light up as they sound. Set the speed with the metronome "
                 "(bottom-right) and slow anything down until it's clean. "
                 "When a part fights you, the skill that builds it is one "
                 "click away on the <a href=\"./roadmap.html\" "
                 "style=\"color:var(--accent);font-weight:600;\">roadmap</a>.",
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
      actually built from — <em>intro, verses, pre-choruses, choruses, the
      break, the solo, the bridge and the twin-lead duet</em>. Each card
      carries that section's tab with every guitar part stacked like a real
      score, plus tempo, meter and a play button.</p>
      <p>Learn it one card at a time: play a section back, slow it down with
      the metronome until your hands keep up, then speed it up. The lit notes
      show you where you are. The full song runs at ♩212 — nobody starts
      there; the tempo ladder on the roadmap is how you arrive.</p>
    """,
    "intro_pills": [
        ("How to use it", "Pick a section, play it slow, repeat it, speed it up. Then join it to the next."),
        ("Drop D", "Every fret here is in drop D — the low string sounds a D. Tune up before you start."),
        ("Two guitars", "Most sections stack Gtr I and Gtr II. Learn your part first, then flip on Together to hear how they interlock."),
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
