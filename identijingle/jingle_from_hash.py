import hashlib

from src.midiutil import MidiFile3 as MidiFile

import identijingle.constants


BASS_START = len(identijingle.constants.BLUES_CODES) // 4
MELODY_START = len(identijingle.constants.BLUES_CODES) // 2


def chunk_bytestring(bs):
    for index in range(0, len(bs), 4):
        yield bs[index:index+4]


def chunk_bits(bs, bit_count=8):
    mask = sum(1 << bc for bc in range(bit_count))
    bits_here= 0
    bit_total = 0
    never_yielded = True
    for byte in bs:
        bit_total = (bit_total << 8) + byte
        bits_here += 8
        if bits_here >= bit_count:
            yield (bit_total >> (bits_here - bit_count)) & mask
            never_yielded = False
            bits_here -= bit_count
            bit_total &= mask
    if (bits_here - bit_count) >= 0:
        yield (bit_total >> (bits_here - bit_count)) & mask
        never_yielded = False
    if never_yielded:
        yield bit_total

class JingleFromHash(object):
    @classmethod
    def chord_for_byte(cls, byte):
        num1 = (byte >> 6) & 3
        num2 = num1 + ((byte >> 4) & 3) + 1
        num3 = num2 + ((byte >> 2) & 3) + 1
        num4 = num3 + (byte & 3) + 1

        return tuple(identijingle.constants.BLUES_CODES[BASS_START + num] for num in (num1, num2, num3, num4))

    @classmethod
    def melody_for_bytes(cls, bytestring):
        old_length = 2
        for note in chunk_bits(bytestring, 6):
            length, key = 2 ** (note & 3), note >> 2
            if length == 1:
                length = old_length
            old_length = length
            yield (length, key)

    @classmethod
    def jingle_from_hash(cls, bytestring):
        for chunk in chunk_bytestring(bytestring):
            chord = cls.chord_for_byte(chunk[0])
            melody = cls.melody_for_bytes(chunk[1:])

            yield (chord, melody)

    @classmethod
    def jingle_from_data(cls, data_stream):
        if isinstance(data_stream, str):
            data_stream = data_stream.encode("utf-8", "replace")

        hasher = hashlib.new("sha512")
        hasher.update(data_stream)

        return cls.jingle_from_hash(hasher.digest())

    @classmethod
    def midi_from_data(cls, data, out_midi):
        midi_data = MidiFile.MIDIFile(1)
        midi_data.addTempo(0, 0, 120)
        note_time = 0.0
        for measure, measure_data in enumerate(cls.jingle_from_data(data)):
            chord, note_data = measure_data

            for note in chord:
                midi_data.addNote(0, 0, note, note_time, 4.0, 100)

            for note in note_data:
                length, key = note
                midi_data.addNote(0, 0, identijingle.constants.BLUES_CODES[MELODY_START + key], note_time, 1. / length, 127)
                note_time += 1. / length

        with open(out_midi, 'wb') as out_midi_handle:
            midi_data.writeFile(out_midi_handle)
