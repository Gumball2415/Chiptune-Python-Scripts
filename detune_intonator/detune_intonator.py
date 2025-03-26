# intonation detune table generator for 0CC+ FamiTracker
# 
# MIT No Attribution
# 
# Copyright 2024 Persune
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



def freq_to_reg_period(chip_type: chiptype, freq: float, N163chan: int = None) -> int:
    convfunct = {
        chiptype._2A03: freq_to_reg_2A03_period,
        chiptype._VRC6: freq_to_reg_VRC6_period,
        chiptype._VRC7: freq_to_reg_VRC7_period,
        chiptype._MMC5: freq_to_reg_2A03_period,
        chiptype._FDS: freq_to_reg_FDS_period,
        chiptype._5B: freq_to_reg_5B_period,
    }
    return convfunct[chip_type](freq, N163chan)

def freq_to_reg_2A03_period(freq: float) -> int:
    period = 0
    return period

def freq_to_reg_VRC6_period(freq: float) -> int:
    period = 0
    return period

def freq_to_reg_VRC7_period(freq: float) -> int:
    period = 0
    return period

def freq_to_reg_FDS_period(freq: float) -> int:
    period = 0
    return period

def freq_to_reg_N163_period(freq: float, N163chan: int) -> int:
    period = 0
    return period

def freq_to_reg_5B_period(freq: float) -> int:
    period = freq_to_reg_2A03_period(freq) - 1
    return period

def MIDI_num_to_freq(tune_type: tunetype, MIDI_num: int, pitchref: float, key: int = None) -> float:
    convfunc = {
        tunetype._12tet: MIDI_num_to_12tet,
        tunetype._just: MIDI_num_to_just,
        tunetype._pythagorean: MIDI_num_to_pythagorean,
        tunetype._meantone: MIDI_num_to_meantone
    }
    return convfunc[tune_type](MIDI_num, pitchref, key)

def MIDI_num_to_12tet(MIDI_num: int, pitchref: float, key: int = None) -> float:
    freq: float = 0.0
    return freq

def MIDI_num_to_just(MIDI_num: int, pitchref: float, key: int) -> float:
    freq: float = 0.0
    return freq

def MIDI_num_to_pythagorean(MIDI_num: int, pitchref: float, key: int) -> float:
    freq: float = 0.0
    return freq

def MIDI_num_to_meantone(MIDI_num: int, pitchref: float, key: int) -> float:
    freq: float = 0.0
    return freq



def parse_argv(argv):
    parser=argparse.ArgumentParser(
        description="Just intonation detune table generator for 0CC+ FamiTracker",
        epilog="version " + VERSION)

    # output options
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="print debug messages")

    return parser.parse_args(argv[1:])

def main(argv=None):
    args = parse_argv(argv or sys.argv)
    # input: path to output, tuning type, tuning key, pitch reference
    # output: 12x8 .csv full of period values

if __name__=='__main__':
    main(sys.argv)
