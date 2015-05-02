from src.midiutil import MidiFile3

import identijingle.constants


def chunk_bytestring(bs):
    for index in range(0, len(bs), 4):
        yield bs[index:index+4]


class JingleFromHash(object):
    @classmethod
    def chord_for_bye(cls, byte):
        num1 = (byte >> 6) & 3
        num2 = num1 + ((byte >> 4) & 3) + 1
        num3 = num2 + ((byte >> 2) & 3) + 1
        num4 = num3 + (byte & 3) + 1

        return tuple(identijingle.constants.BLUES_CODES[16] + num for num in (num1, num2, num3, num4))

    @classmethod
    def jingle_from_hash(cls, bytestring):
        for chunk in chunk_bytestring(bytestring):
            chord = cls.chord_for_byte(chunk[0])
