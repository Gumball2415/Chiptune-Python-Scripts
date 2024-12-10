# MML wavetable converter
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

import argparse
import os
from pathlib import Path

error_text = "error: "

# cmd parsing
parser = argparse.ArgumentParser(
    description="A crusty, no-interpolation wavetable converter. Converts mml wavetable data from one format to another.",
    epilog="version beta 0.1"
    )

parser.add_argument(
    "input_txt",
    help="input text file containing mml formatted wavetable data, seperated by line breaks.",
    type=Path)

parser.add_argument(
    "input_depth",
    help="input bit depth of wavetable data.",
    type=int)

parser.add_argument(
    "output_txt",
    help="output text file containing mml formatted wavetable data, seperated by line breaks.",
    type=Path)

parser.add_argument(
    "output_length",
    help="output wavelength of wavetable data.",
    type=int)

parser.add_argument(
    "output_depth",
    help="output bit depth of wavetable data.",
    type=int)

parser.add_argument(
    "-v", "--verbose",
    help="enable verbose debug messages",
    action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")



# functions
def bitshift ( integer: int, shift_value:int ):
    outvalue = 0;
    if (shift_value > 0):
        outvalue = integer << shift_value
    elif (shift_value < 0):
        outvalue = integer >> shift_value
    return outvalue;

def wavestretcher(
    input_wavedata,
    input_bitdepth,
    output_wavedata,
    output_wavelength,
    output_bitdepth,
    verbose):
    if verbose:
        debugtext = "input wavelength: " + str(len(input_wavedata)) + "\n"
        debugtext += "wave data: "
        for i in range(len(input_wavedata)):
            debugtext += str(input_wavedata[i]) + " ";
        print(debugtext)
        debugtext = "\n"
    
    # 2.1 convert amplitude to target bit depth
    temp_wavedata_x = []
    if verbose:
        debugtext += "bit shift: "
    for i in range(len(input_wavedata)):
        wavebit_translate = bitshift(int(input_wavedata[i]), int(output_bitdepth - input_bitdepth))
        temp_wavedata_x.append(int(wavebit_translate))
        
        if verbose:
            debugtext += str(temp_wavedata_x[i]) + " "
 
    if verbose:
        print(debugtext)
        debugtext = "\n"

    temp_wavedata_y = []
    
    # 2.2 convert wavelength to target wavelength
    wave_increment = (len(input_wavedata)/output_wavelength)
    if verbose:
        debugtext += "wave index increment: " + str(wave_increment)
        print(debugtext)
        debugtext = "\n"
        debugtext += "wave index: "
    
    # duplicate, or skip samples
    for i in range(output_wavelength):
        if verbose:   
            debugtext += str(int(i * wave_increment)) + " "
        temp_wavedata_y.append(temp_wavedata_x[int(i * wave_increment)])
    
    if verbose:
        print(debugtext)
        debugtext = "\n"
        debugtext += "output: "
        
    for i in range(len(temp_wavedata_y)):
        output_wavedata.append(int(temp_wavedata_y[i]))
        if args.verbose:
            debugtext += str(output_wavedata[i]) + " "

    if verbose:
        print(debugtext)
        print("")

    return;



# 1. parse input file's wavetable data
if not args.input_txt.exists():
    error_text += str(args.input_txt) + " does not exist!"
    print(error_text)
    exit()

if args.verbose:
    debugtext = "input file: " + str(os.path.basename(args.input_txt)) + "\n"
    print(debugtext)

print("processing...\n")

file_input = open(args.input_txt, "r")
file_output = open(args.output_txt, "w")

# 1.1. each line is a seperate wave entry
wavecount = 0
for line in file_input:

    wavecount += 1
    debugprint = "writing wave " + str(wavecount)
    print(debugprint)
        
    out_wavedata = []
    in_wavedata = []
    for part in line.split():
        if ";" in part:
            break
        in_wavedata.append(int(part))
    # 2. wavestretch
    wavestretcher(in_wavedata, args.input_depth, out_wavedata, args.output_length, args.output_depth, bool(args.verbose))
    # 3. export wavetable data to output text file
    for index in range(args.output_length):
        # 3.1. each line is a seperate wave entry
        file_output.write(str(out_wavedata[index]) + " ")
    file_output.write(";\n")

print("finished, written " + str(wavecount) + " wave entries to " + str(args.output_txt))
