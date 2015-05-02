import hashlib
import itertools

from src.midiutil import MidiFile3 as MidiFile

import identijingle.constants


BASS_START = len(identijingle.constants.BLUES_CODES) // 4
MELODY_START = len(identijingle.constants.BLUES_CODES) // 2


def rng(byte_string):
    for window in itertools.permutations(byte_string, 4):
        num = 0
        for bits, item in enumerate(window):
            num += (item << (bits * 8))

        yield num


class JingleFromHash(object):
    def __init__(self, data):
        if isinstance(data, str):
            hasher = hashlib.new("sha512")
            hasher.update(data.encode("utf-8"))
            data = hasher.digest()

        self._rng = rng(data)

    def get_number(self):
        return next(self._rng)

    def notes_from_hash(self):
        for note in range(3):
            note = self.get_number() % 12
            length = (self.get_number() % 2.) / 2
            yield (identijingle.constants.BLUES_CODES[MELODY_START + note],
                   length)

    def save_midi(self, out_midi):
        midi_data = MidiFile.MIDIFile(1)
        midi_data.addTempo(0, 0, 60)

        note_time = 0.0
        for note, length in self.notes_from_hash():
            print (note, length)
            midi_data.addNote(0, 0, note, note_time, 1.0 + length, 120)
            note_time += 1.0 + length

        with open(out_midi, 'wb') as out_midi_handle:
            midi_data.writeFile(out_midi_handle)
