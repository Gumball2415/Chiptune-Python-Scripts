import os
import subprocess
import sys
import argparse

parser=argparse.ArgumentParser(
  description="NSFPlay Channel Exporter by Persune",
  epilog="version beta 0.2")
parser.add_argument("-i", "--inputnsf", type=str, help="NSF file input")
parser.add_argument("-o", "--outputwav", type=str, help="WAV Export name")
parser.add_argument("-t", "--nsftrack", type=int, help="Track of .nsf")
parser.add_argument("-l", "--wavlength", type=int, help="Length of .wav export in milliseconds")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable output verbosity")
args = parser.parse_args()

if args.verbose:
  print("Verbosity turned on")

fo = open(args.inputnsf, "rb")

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
chan_2a03 = [0, 1, 2, 3, 4]
chan_fds = [5]
chan_mmc5 = [6, 7, 8]
chan_s5b = [9, 10, 11]
chan_vrc6 = [12, 13, 14]
chan_vrc7 = [15, 16, 17, 18, 19, 20]
chan_n163 = [21, 22, 23, 24, 25, 26, 27, 28]
chan_vrc7ex = [29, 30, 31]
chan_list = chan_2a03

#2. determine list of channels to mute/isolate

print("Expansion audio:")
if exp_byte & bit_fds:
  print("FDS detected.")
  chan_list += chan_fds
if exp_byte & bit_mmc5:
  print("MMC5 detected.")
  chan_list += chan_mmc5
if exp_byte & bit_s5b:
  print("S5B detected.")
  chan_list += chan_s5b
if exp_byte & bit_vrc6:
  print("VRC6 detected.")
  chan_list += chan_vrc6
if exp_byte & bit_vrc7:
  print("VRC7 detected.")
  chan_list += chan_vrc7 + chan_vrc7ex  
if exp_byte & bit_n163:
  print("has N163")
  chan_list += chan_n163
else:
  print("no expansion audio detected")

#3. modify in_yansf.ini to isolate channel

vol_off = "=0\n"
vol_on  = "=128\n"

for x in chan_list:
  channelname = "CHANNEL_%s"%str(x).zfill(2)
  channeliso = channelname + "_VOL"
  
  #mute all channels
  for y in chan_list:
    # write temporary buffer file with modified volumes
    currentchannel = "CHANNEL_%s_VOL"%(str(y).zfill(2))
    inyansf = open("plugins/in_yansf.ini", "r")
    inyansf_buffer = open("buffer", "w")
    
    for line in inyansf:
      if currentchannel in line:
        inyansf_buffer.write(currentchannel + vol_off)
        if args.verbose:
          print("Muting", currentchannel)
      else:
        inyansf_buffer.write(line)
    inyansf.close()
    inyansf_buffer.close()

    # write temporary buffer to original config file
    inyansf_bufferread = open("buffer", "r")
    inyansfwrite = open("plugins/in_yansf.ini", "w")
    for line in inyansf_bufferread:
      inyansfwrite.write(line)
    inyansf_bufferread.close()
    inyansfwrite.close()

  #unmute exported channel
  inyansf = open("plugins/in_yansf.ini", "r")
  inyansf_buffer = open("buffer", "w")
  for line in inyansf:
    if channeliso in line:
      inyansf_buffer.write(channeliso + vol_on)
      if args.verbose:
        print("Isolating", channeliso)
    else:
      inyansf_buffer.write(line)
  inyansf.close()
  inyansf_buffer.close()
  # write temporary buffer to original config file
  inyansf_bufferread = open("buffer", "r")
  inyansfwrite = open("plugins/in_yansf.ini", "w")
  for line in inyansf_bufferread:
    inyansfwrite.write(line)
  inyansf_bufferread.close()
  inyansfwrite.close()
 
#4. export each isolated track with specific parameters
  # nsfplay [nsf_filename] [wav_filename] [track] [milliseconds]
  cli_args = "nsfplay.exe \"%s\" \"%s_%s.wav\" %i %i"%(args.inputnsf, args.outputwav, channelname, args.nsftrack, args.wavlength)
  print("Exporting %s..."%channelname)
  if args.verbose:
    print(cli_args)
  subprocess.run(cli_args)
  
#restore channel levels to 128
for x in chan_list:
  currentchannel = "CHANNEL_%s_VOL"%(str(x).zfill(2))
  inyansf = open("plugins/in_yansf.ini", "r")
  inyansf_buffer = open("buffer", "w")
  for line in inyansf:
    if currentchannel in line:
      inyansf_buffer.write(currentchannel + vol_on)
      if args.verbose:
        print("Restoring", currentchannel)
    else:
      inyansf_buffer.write(line)
  inyansf.close()
  inyansf_buffer.close()
  inyansf_bufferread = open("buffer", "r")
  inyansfwrite = open("plugins/in_yansf.ini", "w")
  for line in inyansf_bufferread:
    inyansfwrite.write(line)
  inyansf_bufferread.close()
  inyansfwrite.close()

os.remove("buffer")
fo.close()