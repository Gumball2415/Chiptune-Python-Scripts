# DPCM splitter
# 
# MIT No Attribution
# 
# Copyright 2021-2025 Persune
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
import sys
droppedFile = sys.argv[1]

#parse dragged file
fo = open(droppedFile, "rb")
inputSize = os.path.getsize(fo.name)

chunksize = input("Enter chunk size in bytes: ")
chunksize = int(chunksize)

chunkFull = inputSize // chunksize
chunkPart = inputSize % chunksize

#diagnostics
print("DIAGNOSTICS:")
print("Name of file:", os.path.split(fo.name)[1])
print("Input filesize:", inputSize)
print("Full chunks:", chunkFull)
print("Size of last non-full chunk:", chunkPart)

#create chunksize byte chunk
print("OUTPUT:")
for x in range(chunkFull):
    outputFilePath = os.path.splitext(fo.name)[0] + " " + str(x+1) + os.path.splitext(fo.name)[1]
    #print(os.path.split(outputFilePath)[1])
    fo.seek(x*chunksize)
    data = fo.read(chunksize)
    outputFile = open(outputFilePath, "wb")
    outputFile.write(data)
    outputFile.close()

#create the final non-full chunk
outputFilePath = os.path.splitext(fo.name)[0] + " " + str(x+2) + os.path.splitext(fo.name)[1]
print(os.path.split(outputFilePath)[1])
fo.seek((x+1)*chunksize)
data = fo.read(chunkPart)
outputFile = open(outputFilePath, "wb")
outputFile.write(data)
outputFile.close()

input("Press Enter to exit.")
fo.close()
