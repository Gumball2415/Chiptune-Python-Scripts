# intonation detune table generator for 0CC+ FamiTracker
# 
# MIT No Attribution
# 
# Copyright 2025 Persune
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

import sys
import argparse
from enum import Enum, auto
from dataclasses import dataclass
import math

VERSION = "0.1.0"

class chiptype(Enum):
    _2A03 = auto()  # default
    _VRC6 = auto()
    _VRC7 = auto()
    _MMC5 = auto()
    _FDS = auto()
    _N163 = auto()
    _5B = auto()

# limited to 12 tones per octave
class tunetype(Enum):
    _12tet = auto() # default
    _just = auto()
    _pythagorean = auto()
    _meantone = auto()

class note(Enum):
    c = 0
    c_sh = auto()
    d = auto()
    d_sh = auto()
    e = auto()
    f = auto()
    f_sh = auto()
    g = auto()
    g_sh = auto()
    a = auto()
    a_sh = auto()
    b = auto()

note_key_dict = {
    "c": note.c,
    "c#": note.c_sh,
    "d": note.d,
    "d#": note.d_sh,
    "e": note.e,
    "f": note.f,
    "f#": note.f_sh,
    "g": note.g,
    "g#": note.g_sh,
    "a": note.a,
    "a#": note.a_sh,
    "b": note.b,
}

@dataclass
class tune_setting:
    chip: chiptype = chiptype._2A03
    type: tunetype = tunetype._12tet
    key: note = note.c
    reference: float = 440.0
    cpu_rate: int = 1789773
    N163_channels = 0



just_ratio_dict = {
    0: 1.0,
    1: 16.0/15.0,
    2: 9.0/8.0,
    3: 6.0/5.0,
    4: 5.0/4.0,
    5: 4.0/3.0,
    6: 45.0/32.0,
    7: 3.0/2.0,
    8: 8.0/5.0,
    9: 5.0/3.0,
    10: 9.0/5.0,
    11: 15.0/8.0,
}

def freq_to_reg_period(tune_setting: tune_setting, freq: float) -> int:
    convert_dict = {
        chiptype._2A03: freq_to_reg_2A03_period,
        chiptype._VRC6: freq_to_reg_VRC6_period,
        chiptype._VRC7: freq_to_reg_VRC7_period,
        chiptype._MMC5: freq_to_reg_2A03_period,
        chiptype._FDS: freq_to_reg_FDS_period,
        chiptype._5B: freq_to_reg_5B_period,
    }
    return convert_dict[tune_setting.chip](freq, tune_setting)

def freq_to_reg_2A03_period(tune_setting: tune_setting, freq: float) -> int:
    period = 0
    return period

def freq_to_reg_VRC6_period(tune_setting: tune_setting, freq: float) -> int:
    period = 0
    return period

def freq_to_reg_VRC7_period(tune_setting: tune_setting, freq: float) -> int:
    period = 0
    return period

def freq_to_reg_FDS_period(tune_setting: tune_setting, freq: float) -> int:
    period = 0
    return period

def freq_to_reg_N163_period(tune_setting: tune_setting, freq: float) -> int:
    period = 0
    return period

def freq_to_reg_5B_period(tune_setting: tune_setting, freq: float) -> int:
    return freq_to_reg_2A03_period(tune_setting, freq) - 1

def MIDI_num_to_freq(tune_setting: tune_setting, MIDI_num: int) -> float:
    convert_dict = {
        tunetype._12tet: MIDI_num_to_12tet,
        tunetype._just: MIDI_num_to_just,
        tunetype._pythagorean: MIDI_num_to_pythagorean,
        tunetype._meantone: MIDI_num_to_meantone
    }
    return convert_dict[tune_setting.type](tune_setting, MIDI_num)

def MIDI_num_to_12tet(tune_setting: tune_setting, MIDI_num: int) -> float:
    return 2**((MIDI_num - 69)/12) * tune_setting.reference

def MIDI_num_to_just(tune_setting: tune_setting, MIDI_num: int) -> float:
    # get nearest root key frequency
    closest_key_A = int(math.floor((MIDI_num / 12) - 1) * 12) + tune_setting.key.value
    closest_key_B = int(math.floor((MIDI_num / 12))  * 12) + tune_setting.key.value

    closest_key = 0

    # the nearest root key is determined by using the same note as the key, and the closest octave as the input note
    if abs(MIDI_num - closest_key_A) < abs(MIDI_num - closest_key_B):
        closest_key = closest_key_A
    else:
        closest_key = closest_key_B

    freq = MIDI_num_to_12tet(tune_setting, closest_key)

    # if MIDI_num is root key, return that
    if closest_key != MIDI_num:
        freq *= just_ratio_dict[MIDI_num - closest_key]
    return freq

def MIDI_num_to_pythagorean(tune_setting: tune_setting, MIDI_num: int) -> float:
    freq: float = 0.0
    return freq

def MIDI_num_to_meantone(tune_setting: tune_setting, MIDI_num: int) -> float:
    freq: float = 0.0
    return freq



def parse_argv(argv):
    parser=argparse.ArgumentParser(
        description="Intonation detune table generator for 0CC-FamiTracker",
        epilog="version " + VERSION)

    # output options
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="print debug messages")

    return parser.parse_args(argv[1:])

DEBUG = True

def main(argv=None):
    args = parse_argv(argv or sys.argv)
    if DEBUG:
        tuner = tune_setting(
            type = tunetype._just,
            key = note.a
        )
        MIDI_num_to_freq(tuner, 69)
    # input: path to output, tuning type, tuning key, pitch reference
    # output: 12x8 .csv full of period values

if __name__=='__main__':
    main(sys.argv)
