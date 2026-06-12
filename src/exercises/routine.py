"""30-minute daily routine — one lap of the trainer.

A structured daily practice that touches every skill the song needs:
tuning check, gallop motor, riff vocabulary, scales, harmony, leads,
and a chunk of the real song from the tab.
"""


def _body(html_inner):
    return ('<div style="font-size:0.95rem;line-height:1.6;'
            'color:var(--card-ink-soft);">' + html_inner + '</div>')


def _link(href, text):
    return f'<a href="{href}" style="color:var(--accent-dark);font-weight:600;">{text}</a>'


EXERCISE = {
    "slug": "routine",
    "order": 10,
    "section": "Practice",
    "title_one": "Daily",
    "title_em": "routine",
    "eyebrow": "30 Minutes · One Lap of the Song",
    "eyebrow_short": "Routine",
    "subtitle": "Tune, gallop, riff, scale, harmonize, lead — then play the song.",
    "intro_prose": """
      <p>A song that runs at ♩212 is a physical adaptation as much as a
      mental one — and adaptations come from <em>daily</em> exposure, not
      weekend marathons. This lap touches every skill the song demands in
      thirty minutes. Run it once a day; the back ten minutes are where the
      actual song gets assembled, one chunk at a time.</p>
      <p>One tempo discipline rules the session: pick your ladder rung
      (♩106 → 148 → 180 → 212 — the metronome remembers it across every
      page), earn it clean, and only raise it tomorrow.</p>
    """,
    "intro_pills": [
        ("Tempo discipline", "One bpm per session, climbing toward ♩212. Clean three times in a row = +5 next session."),
        ("Daily beats long", "30 focused minutes daily beats 3 hours on Sunday. Every time."),
    ],
    "sections": [
        {
            "heading": "The 30-minute lap",
            "blurb": "In order — the warm-up earns you the riffs, the riffs earn you the leads, and the last block is always the song itself.",
            "layout": "wide",
            "cards": [
                {
                    "num": "0:00 → 2:00", "title": "Tune and warm up",
                    "role": "2 min · drop D check + fret-hand wake-up",
                    "body": _body(
                        '<p>' + _link('./tuning.html', 'Drop D page') + ': run both tuning '
                        'checks. Then wake the fret hand before any speed work — slow '
                        'chromatic squeezes (1-2-3-4 up one string, barely pressing) and a '
                        'few gentle finger stretches, then thirty seconds of slow one-finger '
                        'power-chord slides, eyes closed, listening for buzz.</p>'
                        '<p style="margin:0;"><strong>Goal:</strong> perfect octave, relaxed grip.</p>'),
                    "caption": "Drop-tuned strings drift and cold hands tear. Never skip either check.",
                },
                {
                    "num": "2:00 → 8:00", "title": "Gallop motor",
                    "role": "6 min · the rhythm engine, at your ladder tempo",
                    "body": _body(
                        '<p>' + _link('./gallop.html', 'Gallop page') + ': two minutes of '
                        'straight eighths, then your current drill (gallop, reverse gallop, '
                        'or punches) for four. Loop the card audio and lock to it.</p>'
                        '<p style="margin:0;"><strong>Rule:</strong> one flam = restart the minute. '
                        'But never grind through tension — tension at speed is how you get hurt; '
                        'shake the hand out between blocks, because speed grows from relaxed reps.</p>'),
                    "caption": "This is the song's engine. Build it warm every day.",
                },
                {
                    "num": "8:00 → 14:00", "title": "Riff vocabulary",
                    "role": "6 min · two etudes, contrast picked",
                    "body": _body(
                        '<p>' + _link('./riffs.html', 'Riffs page') + ': pick two etudes with '
                        'opposite characters — pedal point + breakdown, or chromatic + clean '
                        'arpeggios. Three clean passes each, then jump between them without '
                        'stopping.</p>'
                        '<p style="margin:0;">The jump <em>is</em> the exercise — the song never hands you a reset bar.</p>'),
                    "caption": "Rotate pairs through the week so all four etudes stay alive.",
                },
                {
                    "num": "14:00 → 18:00", "title": "Scale lap",
                    "role": "4 min · one box, three ways",
                    "body": _body(
                        '<p>' + _link('./fsharp.html', 'F# minor map') + ': one box per day. '
                        'Ascend/descend in eighths, then in triplets, then improvise eight '
                        'bars of fills inside it.</p>'
                        '<p style="margin:0;"><strong>Goal:</strong> land phrases on a root without hunting for it.</p>'),
                    "caption": "Box 1 Monday, Box 2 Tuesday, Box 3 Wednesday — repeat.",
                },
                {
                    "num": "18:00 → 22:00", "title": "Twin-lead skill",
                    "role": "4 min · alternate harmony and lead sessions",
                    "body": _body(
                        '<p>Alternate sessions. One session: ' + _link('./harmony.html', 'Harmonized thirds') + ' — '
                        'play one voice live against the other voice\'s looped audio.</p>'
                        '<p>Next session: ' + _link('./leads.html', 'Lead toolkit') + ' — one '
                        'builder, three clean passes, then once 5 bpm above comfort.</p>'
                        '<p style="margin:0;">Match phrasing exactly — twin leads die from sloppy vibrato, not wrong notes.</p>'),
                    "caption": "Melody hands and rhythm hands are different muscles. Train both.",
                },
                {
                    "num": "22:00 → 30:00", "title": "The song itself",
                    "role": "8 min · current chunk from the official tab",
                    "body": _body(
                        '<p>' + _link('./roadmap.html', 'Roadmap method') + ': open the '
                        'official tab to your current chunk. Three clean passes at your '
                        'ladder tempo, then loop the seam into the next section, then one '
                        'pass of everything you\'ve assembled so far.</p>'
                        '<p style="margin:0;"><strong>Finish</strong> by playing your best chunk along with the record — even if it\'s only eight bars.</p>'),
                    "caption": "End every session inside the actual song. That's the point of all of it.",
                },
            ],
        },
    ],
    "next_step": {
        "heading_one": "The weekly ",
        "heading_em": "rotation",
        "heading_two": "",
        "body": "<p>The lap is the day; here's the week:</p><ul style=\"color:var(--ink-soft);margin:0.5rem 0;padding-left:1.2rem;\"><li><strong>Mon–Fri</strong> — the full lap, rotating boxes, etude pairs, and alternating harmony/lead sessions</li><li><strong>Sat</strong> — double song time: 15+ minutes of chunks, seams, and assembly</li><li><strong>Sun</strong> — listen only. The record, twice: once for guitars, once for the drums your gallop locks to.</li></ul>",
        "items": [
            ("Log it", "One line per day: ladder bpm + current chunk. A month of lines is proof you're moving."),
            ("Record Fridays", "Phone video of your best chunk every Friday. Compare month over month."),
            ("Stuck rule", "Plateaued for a week? Drop 20 bpm for three days and rebuild. It works every time."),
        ],
    },
    "closing": "Thirty minutes a day until the song plays itself.",
}
