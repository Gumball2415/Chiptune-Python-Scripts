# MML wavetable converter
#
# Copyright (C) 2021-2022 Persune
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
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
