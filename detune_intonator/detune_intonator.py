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
import csv

VERSION = "0.2.0"

CLK_NTSC = 1789773
CLK_PAL = 1662607
CLK_VRC7 = 3579545

note_key_dict = {
    "c": 0,
    "c#": 1,
    "d": 2,
    "d#": 3,
    "e": 4,
    "f": 5,
    "f#": 6,
    "g": 7,
    "g#": 8,
    "a": 9,
    "a#": 10,
    "b": 11,
}

class chiptype(Enum):
    _2A03 = 0  # default
    _2A07 = auto()  # default
    _VRC6 = auto()
    _VRC7 = auto()
    _FDS = auto()
    _N163 = auto()

# limited to 12 tones per octave
class tunetype(Enum):
    _custom = 0
    _12tet = auto() # default
    _3_limit = auto()
    _5_limit = auto()
    _7_limit = auto()
    _meantone = auto()

intonation_dict = {
    "12tet": tunetype._12tet,
    "3_limit": tunetype._3_limit,
    "5_limit": tunetype._5_limit,
    "7_limit": tunetype._7_limit,
}

@dataclass
class tune_setting:
    type: tunetype = tunetype._12tet
    key: int = note_key_dict["a"]
    reference: float = 440.0
    N163_channels: int = 0



def note_to_reg_2A03_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    period = int(round((CLK_NTSC / (freq * 16.0)) - 1.0))
    return min(max(period, 0), 0x7FF)

def note_to_reg_2A07_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    period = int(round((CLK_PAL / (freq * 16.0)) - 1.0))
    return min(max(period, 0), 0x7FF)

def note_to_reg_VRC6_saw_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    freq = MIDI_num_to_freq(tunesetting, MIDI_num)
    period = int(round((CLK_NTSC / (freq * 14.0)) - 1.0))
    return min(max(period, 0), 0xFFF)

def note_to_reg_VRC7_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    oct = 5
    period = int(round((freq * 2**(19-oct)) / (CLK_VRC7 / 72.0)))
    return min(max(period, 0), 0x1FF)

def note_to_reg_FDS_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    period = int(round((freq * 65536.0 * 16) / CLK_NTSC))
    return min(max(period, 0), 0xFFF)

def note_to_reg_N163_period(tunesetting: tune_setting, freq: float, MIDI_num: int = None) -> int:
    period = int(round((freq * 15.0 * 262144.0 * tunesetting.N163_channels) / CLK_NTSC))
    return min(max(period, 0), 0x3FFFF)

def note_to_reg_period_delta(ref: tune_setting, tun: tune_setting, chip: chiptype, MIDI_num: int) -> int:
    freqref = 0.0
    freq = 0.0
    if chip == chiptype._VRC7:
        # there's only a single octave LUT for VRC7
        MIDI_note = MIDI_num % 12 + 48
        freqref = MIDI_num_to_freq(ref, MIDI_note)
        freq = MIDI_num_to_freq(tun, MIDI_note)
    else: 
        freqref = MIDI_num_to_freq(ref, MIDI_num)
        freq = MIDI_num_to_freq(tun, MIDI_num)

    delta = chiptype_dict[chip](ref, freqref, MIDI_num) - chiptype_dict[chip](tun, freq, MIDI_num)

    # invert delta for freq-based registers
    if chip == chiptype._VRC7 or chip == chiptype._FDS or chip == chiptype._N163:
            delta *= -1
    return delta

chiptype_dict = {
    chiptype._2A03: note_to_reg_2A03_period,
    chiptype._2A07: note_to_reg_2A07_period,
    chiptype._VRC6: note_to_reg_VRC6_saw_period,
    chiptype._VRC7: note_to_reg_VRC7_period,
    chiptype._FDS:  note_to_reg_FDS_period,
    chiptype._N163: note_to_reg_N163_period
}

def MIDI_num_to_12tet(tunesetting: tune_setting, MIDI_num: int) -> float:
    refnote = tunesetting.key+36 # FT notes are 2 octaves lower
    return tunesetting.reference * 2**((MIDI_num - refnote)/12)

def MIDI_num_to_just(tunesetting: tune_setting, MIDI_num: int) -> float:
    # get nearest root key frequency
    MIDI_oct = int(MIDI_num / 12)
    closest_key = ((MIDI_oct - 1) * 12) + tunesetting.key
    note_dist = MIDI_num - closest_key

    if (note_dist >= 12):
        closest_key += 12
        note_dist -= 12

    freq = MIDI_num_to_12tet(tunesetting, closest_key)

    # if MIDI_num is root key, return that
    if closest_key != MIDI_num:
        a, b = just_dict[tunesetting.type][note_dist]
        if a > 0 and b > 0:
            freq = freq * a / b
        else:
            tempset = tune_setting()
            freq = MIDI_num_to_freq(tempset, MIDI_num)

    return freq

def MIDI_num_to_meantone(tunesetting: tune_setting, MIDI_num: int) -> float:
    # TODO: meantone
    return MIDI_num_to_12tet(tunesetting, MIDI_num)

def MIDI_num_to_freq(tunesetting: tune_setting, MIDI_num: int) -> float:
    return tuner_dict[tunesetting.type](tunesetting, MIDI_num)

tuner_dict = {
    tunetype._12tet: MIDI_num_to_12tet,
    tunetype._custom: MIDI_num_to_just,
    tunetype._3_limit: MIDI_num_to_just,
    tunetype._5_limit: MIDI_num_to_just,
    tunetype._7_limit: MIDI_num_to_just,
    tunetype._meantone: MIDI_num_to_meantone
}

# pythagorean tuning from this table
# https://en.wikipedia.org/wiki/Just_intonation#Pythagorean_tuning
_3_lim_ratios = (
    (1.0, 1.0),
    (256.0,243.0),
    (9.0,8.0),
    (32.0,27.0),
    (81.0,64.0),
    (4.0,3.0),
    (729.0,512.0), # augmented 4th
    (3.0,2.0),
    (128.0,81.0),
    (27.0,16.0),
    (16.0,9.0),
    (243.0,128.0)
)

# 5-lim and 7-lim from this table
# https://en.wikipedia.org/wiki/Five-limit_tuning#The_just_ratios

# 5-lim asymmetric standard
_5_lim_ratios = (
    (1.0, 1.0),
    (16.0,15.0),
    (9.0,8.0),
    (6.0,5.0),
    (5.0,4.0),
    (4.0,3.0),
    (45.0,32.0), # augmented 4th
    (3.0,2.0),
    (8.0,5.0),
    (5.0,3.0),
    (9.0,5.0), # minor 7th
    (15.0,8.0)
)

_7_lim_ratios = (
    (1.0, 1.0),
    (15.0,14.0),
    (8.0,7.0),
    (6.0,5.0),
    (5.0,4.0),
    (4.0,3.0),
    (7.0,5.0), # augmented 4th
    (3.0,2.0),
    (8.0,5.0),
    (5.0,3.0),
    (7.0,4.0), # minor 7th
    (15.0,8.0)
)



def parse_argv(argv):
    parser=argparse.ArgumentParser(
        description="Intonation detune table generator for 0CC-FamiTracker",
        epilog="version " + VERSION)

    # output options
    parser.add_argument(
        "output",
        type=str,
        help="output .csv")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="print debug messages")
    parser.add_argument(
        "--intonation",
        choices=[
            "12tet",
            "3_limit",
            "5_limit",
            "7_limit",
        ],
        default="12tet",
        help="intonation type. default = \"12tet\"")
    parser.add_argument(
        "--intervals",
        nargs=24,
        metavar=(
            "n_0", "d_0",
            "n_1", "d_1",
            "n_2", "d_2",
            "n_3", "d_3",
            "n_4", "d_4",
            "n_5", "d_5",
            "n_6", "d_6",
            "n_7", "d_7",
            "n_8", "d_8",
            "n_9", "d_9",
            "n_10", "d_10",
            "n_11", "d_11"
        ),
        type=float,
        help="custom 12 tone interval ratio list, overrides default intonation settings.")
    parser.add_argument(
        "--key",
        choices=[
            "c",
            "c#",
            "d",
            "d#",
            "e",
            "f",
            "f#",
            "g",
            "g#",
            "a",
            "a#",
            "b",
        ],
        default="a",
        help="note to be designated as unison. default = \"a\"")
    parser.add_argument(
        "--reference",
        type=float,
        default=440.0,
        help="reference pitch for unison note. default = 440.0")
    parser.add_argument(
        "-nchan",
        "--n163-channels",
        type=int,
        default=0,
        help="N163 channel count. default = 0")
    return parser.parse_args(argv[1:])

DEBUG = True

def main(argv=None):
    global just_dict
    args = parse_argv(argv or sys.argv)

    # input: path to output, tuning type, tuning key, pitch reference
    # output: 97x6 .csv full of period offset values
    # chiptype, C-0 period offset, C#1 period offset, ... B-7 period offset
        # chiptype  value
        # 2A03      0
        # 2A07      1
        # VRC6 saw  2
        # VRC7      3
        # FDS       4
        # N163      5
    # for VRC7: since it has one octave LUT,
    # the values keep repeating every octave

    reference = tune_setting()
    tuner = tune_setting(
        type = intonation_dict[args.intonation],
        key = note_key_dict[args.key],
        reference=args.reference,
        N163_channels = args.n163_channels
    )

    # modified at runtime for custom interval sets
    _user_ratios = ()
    just_dict = {}

    if args.intervals is not None and len(args.intervals) % 2 == 0:
        tuner.type = tunetype._custom
        _user_ratios = tuple([ratio for ratio in zip(args.intervals[::2],args.intervals[1::2])])
    just_dict = {
        tunetype._custom: _user_ratios,
        tunetype._3_limit: _3_lim_ratios,
        tunetype._5_limit: _5_lim_ratios,
        tunetype._7_limit: _7_lim_ratios,
    }

    with open(args.output, "w", newline='') as detune_table:
        csv_file = csv.writer(detune_table, quoting=csv.QUOTE_NONNUMERIC)
        for chip in chiptype:
            csv_row = []
            csv_row.append(chip.value)
            for note in range(96):
                deltatune = note_to_reg_period_delta(reference, tuner, chip, note)
                csv_row.append(deltatune)
            csv_file.writerow(csv_row)

if __name__=='__main__':
    main(sys.argv)
