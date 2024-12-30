# NSFPlay seperate channel exporter
# 
# MIT No Attribution
# 
# Copyright 2021-2024 Persune
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

import os
import subprocess
import sys
import argparse
import pathlib

def inyansf_writesetting(setting, value):
    global args
    in_yansf_path = pathlib.PurePath(args.nsfplay_path).joinpath("plugins/in_yansf.ini")
    with open(in_yansf_path, "r") as inyansf:
        with open("buffer", "w") as inyansf_buffer:
            for line in inyansf:
                if setting in line:
                    inyansf_buffer.write(setting + value)
                else:
                    inyansf_buffer.write(line)
    # write temporary buffer to original config file
    with open("buffer", "r") as inyansf_bufferread:
        with open(in_yansf_path, "w") as inyansfwrite:
            for line in inyansf_bufferread:
                inyansfwrite.write(line)

def inyansf_readsetting(setting):
    global args
    in_yansf_path = pathlib.PurePath(args.nsfplay_path).joinpath("plugins/in_yansf.ini")
    with open(in_yansf_path, "r") as inyansf:
        for line in inyansf:
            if setting in line:
                return line.split("=", 1)[1]

def main(argv=None):
    global args
    parser=argparse.ArgumentParser(
        description="NSFPlay Channel Exporter by Persune",
        epilog="version beta 0.6")
    parser.add_argument("nsfplay_path", type=pathlib.Path, help="path to NSFPlay folder")
    parser.add_argument("inputnsf", type=pathlib.Path, help="NSF file input")
    parser.add_argument("nsftrack", type=int, help="Track of .nsf")
    parser.add_argument("wavlength", type=int, help="Length of .wav export in seconds")
    parser.add_argument("outputwav", type=pathlib.Path, help="WAV Export name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable output verbosity")
    parser.add_argument("-nch", "--n163channels", type=int, default=0, help="Specify number of N163 channels. Default is 0")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if args.verbose:
      print("Verbosity turned on")

    with open(args.inputnsf, "rb") as fo:

        #1. determine which expansion chips are enabled
        #1a. open .nsf, check header for expansion chips

        exp_byte = fo.read()[123]
                                # 76543210
                                # ||||||||
        bit_vrc6 = 0b00000001   # |||||||+--VRC6 audio
        bit_vrc7 = 0b00000010   # ||||||+---VRC7 audio
        bit_fds  = 0b00000100   # |||||+----FDS audio
        bit_mmc5 = 0b00001000   # ||||+-----MMC5 audio
        bit_n163 = 0b00010000   # |||+------N163 audio
        bit_s5b  = 0b00100000   # ||+-------S5B audio
                                # |+--------VT02+ audio (unsupported in NSFPlay)
                                # +---------unused
        chan_2a03 = {0: "PU1", 1: "PU2", 2: "TRI", 3: "NOI", 4: "DMC"}
        chan_fds = {5: "FDS"}
        chan_mmc5 = {6: "PU3", 7: "PU4", 8: "PCM"}
        chan_s5b = {9: "5B1", 10: "5B2", 11: "5B3"}
        chan_vrc6 = {12: "V1", 13: "V2", 14: "SAW"}
        chan_vrc7 = {15: "FM1", 16: "FM2", 17: "FM3", 18: "FM4", 19: "FM5", 20: "FM6"}
        chan_n163 = {21: "N1", 22: "N2", 23: "N3", 24: "N4", 25: "N5", 26: "N6", 27: "N7", 28: "N8"}
        chan_vrc7ex = {29: "FM7 ", 30: "FM8", 31: "FM9"}

        chan_list = chan_2a03

        #2. determine list of channels to mute/isolate

        print("Expansion audio:")


        if exp_byte & bit_fds:
            print("\tFDS detected.")
            chan_list += chan_fds
        elif exp_byte & bit_mmc5:
            print("\tMMC5 detected.")
            chan_list += chan_mmc5
        elif exp_byte & bit_s5b:
            print("\tS5B detected.")
            chan_list += chan_s5b
        elif exp_byte & bit_vrc6:
            print("\tVRC6 detected.")
            chan_list += chan_vrc6
        elif exp_byte & bit_vrc7:
            print("\tVRC7/OPLL detected.")
            chan_list += chan_vrc7 + chan_vrc7ex  
        elif exp_byte & bit_n163:
            print("\tN163 detected.")
            if args.n163channels < 1:
                print("\tError: 0 N163 channels specified.")
                sys.exit(1)
            elif args.n163channels > 8:
                print("\tError: more than 8 N163 channels specified.")
                sys.exit(1)
            for x in range(0, args.n163channels):
                chan_list.append(chan_n163[x])
        else:
            print("\tNo expansion audio detected.")

        #3. modify in_yansf.ini to isolate channel

        vol_off = "=0\n"
        vol_on  = "=128\n"
        oldLevels = []
        oldTime = ""

        # back up old settings
        oldTime = inyansf_readsetting("PLAY_TIME")

        for x in range(len(chan_list)):
            currentchannel = "CHANNEL_%s_VOL"%(str(list(chan_list.keys())[x]).zfill(2))
            oldLevels.append(inyansf_readsetting(currentchannel))

        if args.verbose:
            print("Saved levels: ",oldLevels)
            print("Saved playback length: ",oldTime)

        for x in range(len(chan_list)):
            channelname = str(chan_list[x]).zfill(2)
            channeliso = "CHANNEL_%s_VOL"%(str(list(chan_list.keys())[x]).zfill(2))

            # mute all channels except exported channel
            for y in range(len(chan_list)):
                # write temporary buffer file with modified volumes
                if x != y:
                    currentchannel = "CHANNEL_%s_VOL"%(str(list(chan_list.keys())[y]).zfill(2))
                    inyansf_writesetting(currentchannel, vol_off)
                    if args.verbose:
                        print("Muting", currentchannel)
            # unmute exported channel to be sure
            inyansf_writesetting(channeliso, vol_on)
            if args.verbose:
                print("Isolating", channeliso)

            inyansf_writesetting("PLAY_TIME", "=" + str(args.wavlength * 1000) + "\n")

            # 4. export each isolated track with specific parameters
            # nsfplay [nsf_filename] [wav_filename] [track] [milliseconds]
            # variable .wav length fixed in 2.6
            nsfplay_exe = pathlib.PurePath(args.nsfplay_path).joinpath("nsfplay.exe")
            cli_args = str(nsfplay_exe)+f" \"{args.inputnsf}\" \"{args.outputwav}_{channelname}.wav\" {args.nsftrack} {args.wavlength * 1000}"
            print("Exporting %s..."%channelname)
            if args.verbose:
                print(cli_args)
            subprocess.run(cli_args)

        #restore settings
        inyansf_writesetting("PLAY_TIME", "=" + oldTime)

        for x in range(len(chan_list)):
            currentchannel = "CHANNEL_%s_VOL"%(str(chan_list[x]).zfill(2))
            if args.verbose:
                print("Restoring", currentchannel)
            oldLevel = "=" + oldLevels[x]
            inyansf_writesetting(currentchannel, oldLevel)

        os.remove("buffer")
if __name__ == '__main__':
    main(sys.argv)