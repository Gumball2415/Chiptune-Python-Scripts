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
