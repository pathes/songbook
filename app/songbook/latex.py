# -*- coding: utf-8 -*-
from re import sub
from .templatetags.latex_escape import latex_escape

LATEX = {
    'verse_token': '\zwrotka',
    'chorus_token': '\\refren',
    'verse_end_token': '\koniec',
    'chorus_end_token': '\koniec',
    'chords_token': '\chwyty',
}


class SongState:
    Nothing, Verse, Chorus = list(range(3))


def accidentals(str):
    return sub(
        r'([a-zA-Z]+)b',
        r'\1♭',
        sub(
            r'([a-zA-Z]+)#',
            r'\1♯',
            str(str)
        )
    )

def parse_song_content(song_content):
    result = []
    last_state = SongState.Nothing
    current_state = SongState.Nothing

    # Append last empty line to guarantee Nothing state on end.
    song_content += '\n'

    for line in song_content.split('\n'):
        last_state = current_state
        # Determining current state of the song
        is_empty = line.strip() == ''
        if is_empty:
            current_state = SongState.Nothing
        else:
            is_indented = line[0] == '\t' or line[:2] == '  '
            if is_indented:
                current_state = SongState.Chorus
            else:
                current_state = SongState.Verse

        # Adding necessary tokens if needed
        if current_state != last_state:
            if last_state == SongState.Verse:
                result.append(LATEX['verse_end_token'])
            elif last_state == SongState.Chorus:
                result.append(LATEX['chorus_end_token'])

            if current_state == SongState.Verse:
                result.append(LATEX['verse_token'])
            elif current_state == SongState.Chorus:
                result.append(LATEX['chorus_token'])

        # Side comments
        if current_state == SongState.Nothing:
            continue
        try:
            comment_index = line.index('|')
            result.append(
                latex_escape(line[:comment_index].strip()) +
                LATEX['chords_token'] +
                '{' +
                latex_escape(accidentals(line[comment_index+1:].strip())) +
                '}\n'
            )
        except ValueError:
            result.append(latex_escape(line.strip()) + ' ' + LATEX['chords_token'] + '{}\n')

    return '\n'.join(result)
