from templatetags.latex_escape import latex_escape

LATEX = {
    'verse_token': u'\zwrotka',
    'chorus_token': u'\\refren',
    'verse_end_token': u'\koniec',
    'chorus_end_token': u'\koniec',
    'chords_token': u'\chwyty',
}


class SongState:
    Nothing, Verse, Chorus = range(3)


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
            comment_index = line.index(u'|')
            result.append(
                latex_escape(line[:comment_index].strip()) +
                LATEX['chords_token'] +
                u'{' +
                latex_escape(line[comment_index+1:].strip()) +
                u'}\n'
            )
        except ValueError:
            result.append(latex_escape(line.strip()) + u' ' + LATEX['chords_token'] + u'{}\n')

    return '\n'.join(result)
