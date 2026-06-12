"""Song roadmap — how the sections fit, and how to woodshed them.

This page deliberately contains no transcription of the song. It maps
the song's architecture in broad strokes, ties each section to the
trainer page that builds its skill, and lays out the practice method
for assembling the whole thing from the official tab.
"""

UG_URL = "https://tabs.ultimate-guitar.com/tab/trivium/ascendancy-tabs-506693"


def _html(body):
    return ('<div style="font-size:0.95rem;line-height:1.6;'
            'color:var(--card-ink-soft);">' + body + '</div>')


def _link(href, text):
    return f'<a href="{href}" style="color:var(--accent-dark);font-weight:600;">{text}</a>'


SECTION_ROWS = [
    ("Intro · 1–16", "Twin octave leads over the F#5→D5 gallop",
     "harmony.html", "Harmonized thirds", "gallop.html", "Gallop picking"),
    ("Verses · 17–32 / 57–72", "Palm-muted F# pedal gallop, the E#→F# leading-tone move, C#5 punches",
     "gallop.html", "Gallop picking", "riffs.html", "Riff vocabulary"),
    ("Pre-choruses · 33–48 / 73–88 / 177–192", "Syncopated stabs, both guitars in thirds",
     "riffs.html", "Riff vocabulary", "harmony.html", "Harmonized thirds"),
    ("Choruses · 49–56 / 89–104", "F#5→D5 — the home barre to the open dropped string",
     "tuning.html", "Power chords", "fsharp.html", "F# minor map"),
    ("Break · 105–112", "Open-string legato figure (0h7) — the song drops to a single line",
     "leads.html", "Legato builders", "riffs.html", "Riff vocabulary"),
    ("Break verse · 113–128", "The verse gallop returns over the break's open-string figure",
     "riffs.html", "Riff vocabulary", "gallop.html", "Gallop picking"),
    ("Solo · 129–144", "High register, taps up to frets 18–19",
     "leads.html", "Lead toolkit", "fullneck.html", "Full-neck map"),
    ("Bridge · 145–160", "Tremolo-picked chord walk — F#5–G#5–A5–G#5",
     "leads.html", "Tremolo picking", "gallop.html", "Picking endurance"),
    ("Duet · 161–176", "Twin guitars in diatonic thirds",
     "harmony.html", "Harmonized thirds", "fsharp.html", "F# minor map"),
    ("Final chorus · 193–228", "Thirty-six bars — everything at once; stamina is the skill",
     "routine.html", "Daily routine", "gallop.html", "Endurance drills"),
]


def section_table():
    rows = []
    for name, desc, h1, t1, h2, t2 in SECTION_ROWS:
        rows.append(
            '<div style="display:grid;grid-template-columns:11.5rem 1fr;gap:0.75rem;'
            'padding:0.65rem 0;border-bottom:1px solid var(--card-line);align-items:baseline;">'
            f'<div style="font-weight:700;color:var(--card-ink);font-style:italic;">{name}</div>'
            f'<div>{desc}<br><span style="font-size:0.85rem;">Train it: '
            f'{_link("./" + h1, t1)} · {_link("./" + h2, t2)}</span></div>'
            '</div>'
        )
    return '<div style="margin-top:0.5rem;">' + ''.join(rows) + '</div>'


WOODSHED_STEPS = """
<ol style="margin:0.25rem 0 0;padding-left:1.3rem;">
  <li style="margin:0.45rem 0;"><strong>Chunk it.</strong> Mark the section
  boundaries in the tab (intro, verse, chorus…). Name each riff — Riff A,
  Riff B — and learn them as separate vocabulary words, not one long
  sentence.</li>
  <li style="margin:0.45rem 0;"><strong>Ladder each chunk.</strong> The
  song sits at ♩212, so the rungs are real numbers: 50% ≈ 106 → 70% ≈ 148
  → 85% ≈ 180 → 212. For the hardest chunks (verse gallop, solo, bridge
  tremolo) add a 60% ≈ 127 rung — the jump from 106 to 148 is too big to
  take in one step. A tempo is &ldquo;earned&rdquo; when you play the
  chunk three times in a row clean.</li>
  <li style="margin:0.45rem 0;"><strong>Loop the seams.</strong> Most
  breakdowns happen <em>between</em> sections. Practise the last bar of one
  chunk into the first bar of the next as its own exercise.</li>
  <li style="margin:0.45rem 0;"><strong>Assemble.</strong> Play sections in
  pairs, then halves, then the whole song at 85% (♩180) before ever
  attempting 212 end-to-end.</li>
  <li style="margin:0.45rem 0;"><strong>Play with the record.</strong> The
  final exam. The record doesn't slow down for you — your gallop endurance
  (and your drop-D tuning stability) gets exposed here.</li>
</ol>
"""

GET_THE_NOTES = f"""
<p>This trainer builds your <em>hands</em>; the note-for-note source lives
on this site now — the {_link("./song.html", "Full song page")} engraves the
whole 228-bar arrangement, section by section, with playback. The community
tab it was checked against is
{_link(UG_URL, "Ascendancy — Ultimate Guitar")} — useful as a second
opinion when something sounds off.</p>
<p>Reading checklist as you go through it:</p>
<ul style="margin:0.25rem 0 0;padding-left:1.3rem;">
  <li style="margin:0.35rem 0;"><strong>Confirm the tuning</strong> at the
  top of the tab (drop D) and tune before reading a single bar.</li>
  <li style="margin:0.35rem 0;"><strong>Tag the devices.</strong> For every
  riff, ask: pedal-point? gallop or reverse gallop? leading-tone move?
  syncopated stabs? tremolo walk? open-string legato? You drilled all of
  them here — name what you see.</li>
  <li style="margin:0.35rem 0;"><strong>Mark the twin-lead passages</strong>
  and decide which voice you're learning first (low voice first is easier —
  it usually carries the melody).</li>
  <li style="margin:0.35rem 0;"><strong>Check tab vs. record.</strong>
  Community tabs are good but not gospel — when ears and paper disagree,
  trust your ears (or compare another version of the tab).</li>
</ul>
"""


EXERCISE = {
    "slug": "roadmap",
    "order": 8,
    "section": "The Song",
    "title_one": "Song",
    "title_em": "roadmap",
    "eyebrow": "Putting It All Together",
    "eyebrow_short": "Roadmap",
    "subtitle": "The architecture, the method, and the official tab.",
    "intro_prose": """
      <p><em>Ascendancy</em> — the title track of Trivium's 2005 album — is
      a fast, riff-dense metalcore song: drop D, F# minor, ♩212, 228 bars
      of 4/4, screamed verses against sung choruses, twin-guitar harmonies,
      a proper solo, and a rhythm section that gallops nearly wall to wall.
      Note the split: the <em>tuning</em> is drop D but the <em>key</em> is
      F# minor — the root is the fret-4 barre, and the open D is the ♭6,
      not home. It's a lot of material, which is exactly why you don't
      learn it front-to-back like a book.</p>
      <p>You learn it like a <strong>building</strong>: identify the
      sections, train the skill each one demands (that's the rest of this
      site), learn each section's notes from the official tab, then weld
      the seams. This page is the site map for that process.</p>
    """,
    "intro_pills": [
        ("Tuning", "Drop D — D A D G B E. Re-check it every session."),
        ("Key", "F# minor — F# G# A B C# D E. The root is the fret-4 barre; the open D is the ♭6."),
        ("Tempo", "♩ = 212. Nobody starts there — the ladder is 106 → 148 → 180 → 212."),
    ],
    "sections": [
        {
            "heading": "The architecture",
            "blurb": "What each section of the song asks of you, and where on this site to train it before you read its bars from the tab.",
            "layout": "full",
            "cards": [
                {
                    "num": "Map",
                    "title": "Section by section",
                    "role": "Skill links into the rest of the trainer",
                    "body": _html(section_table()),
                    "caption": "Bar numbers verified against the engraved tab on the Full song page — open a section there to read its exact notes.",
                },
            ],
        },
        {
            "heading": "The woodshed method",
            "blurb": "How players actually get a song like this to full speed. The method matters more than the hours.",
            "layout": "full",
            "cards": [
                {
                    "num": "Method",
                    "title": "Chunk → ladder → seams → assemble",
                    "role": "The five-step plan",
                    "body": _html(WOODSHED_STEPS),
                    "caption": "The metronome on every page of this site drives every exercise's playback — set it to your current ladder rung and the whole trainer follows you.",
                },
            ],
        },
        {
            "heading": "Get the notes",
            "blurb": "This site trains the techniques; the tab supplies the transcription. Use them together.",
            "layout": "full",
            "cards": [
                {
                    "num": "Source",
                    "title": "Working with the official tab",
                    "role": "Read it like someone who already speaks the dialect",
                    "body": _html(GET_THE_NOTES),
                    "caption": "Hands from the trainer, notes from the tab, feel from the record.",
                },
            ],
        },
    ],
    "next_step": {
        "heading_one": "Make it a ",
        "heading_em": "habit",
        "heading_two": "",
        "body": "<p>A song this dense yields to consistency, not heroics. The <a href=\"./routine.html\" style=\"color:var(--accent);font-weight:600;\">daily routine</a> page turns everything on this site into a 30-minute loop you can run every day until the song is yours.</p>",
        "items": [
            ("Week 1–2", "Setup + gallop + riff etudes. Don't touch the tab yet except to read its structure."),
            ("Week 3–4", "Verse and chorus chunks from the tab at ♩106–148 (50–70%), scales and harmony pages in rotation."),
            ("Week 5+", "Solo section via the lead toolkit, seam loops, then full assembly at ♩180 (85%)."),
        ],
    },
    "closing": "Sections, seams, then the song. Brick by brick.",
}
