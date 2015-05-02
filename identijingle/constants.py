import itertools

NOTES_BY_NAME = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BLUES_NOTES = ["C", "D", "D#", "E", "G", "A"]
OCTAVES = list(range(11))

CODES_BY_NOTE = {
    "{0}{1}".format(note_name, octave): index
    for index, (octave, note_name) in enumerate(itertools.product(OCTAVES, NOTES_BY_NAME))
    if index <= 127
}

BLUES_CODES = [CODES_BY_NOTE["{0}{1}".format(note, octave)]
               for (octave, note) in itertools.product(OCTAVES, NOTES_BY_NAME)
               if "{0}{1}".format(note, octave) in CODES_BY_NOTE and note in BLUES_NOTES]
