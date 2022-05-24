# DPCM splitter
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
