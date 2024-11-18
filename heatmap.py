import math
import sys
import struct
import zlib

def makeGrayPNG(data, height = None, width = None):
    """ Converts a list of list into gray-scale PNG image. """
    __copyright__ = "Copyright (C) 2014 Guido Draheim"
    __licence__ = "Public Domain"

    def I1(value):
        return struct.pack("!B", value & (2**8-1))
    def I4(value):
        return struct.pack("!I", value & (2**32-1))
    # compute width&height from data if not explicit
    if height is None:
        height = len(data) # rows
    if width is None:
        width = 0
        for row in data:
            if width < len(row):
                width = len(row)
    # generate these chunks depending on image type
    makeIHDR = True
    makeIDAT = True
    makeIEND = True
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')
    if makeIHDR:
        colortype = 0 # true gray image (no palette)
        bitdepth = 8 # with one byte per pixel (0..255)
        compression = 0 # zlib (no choice here)
        filtertype = 0 # adaptive (each scanline seperately)
        interlaced = 0 # no
        IHDR = I4(width) + I4(height) + I1(bitdepth)
        IHDR += I1(colortype) + I1(compression)
        IHDR += I1(filtertype) + I1(interlaced)
        block = "IHDR".encode('ascii') + IHDR
        png += I4(len(IHDR)) + block + I4(zlib.crc32(block))
    if makeIDAT:
        raw = b""
        for y in range(height):
            raw += b"\0" # no filter for this scanline
            for x in range(width):
                c = b"\0" # default black pixel
                if y < len(data) and x < len(data[y]):
                    c = I1(data[y][x])
                raw += c
        compressor = zlib.compressobj()
        compressed = compressor.compress(raw)
        compressed += compressor.flush() #!!
        block = "IDAT".encode('ascii') + compressed
        png += I4(len(compressed)) + block + I4(zlib.crc32(block))
    if makeIEND:
        block = "IEND".encode('ascii')
        png += I4(0) + block + I4(zlib.crc32(block))
    return png


def heatmap(data,png):
    # Read the file.  We are assuming that all the plates are square here
    with open(data,'rb') as raw:
        data = []
        while 1:
            word = raw.read(8)
            if not word: break
            x = struct.unpack(b'd',word)[0]
            data.append(x)
    mx = max(data)
    for i in range(len(data)):
        data[i] = int(data[i]/mx*255)

    N = int(math.sqrt(len(data))+.5)
    assert len(data) == N**2,'should be a square plate'
    grid = []
    for i in range(N):
        grid.append(data[i*N:i*N+N])

    with open(png,'wb') as output:
        out = makeGrayPNG(grid)
        output.write(out)

    return 

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='convert raw data to a pretty heatmap')
    parser.add_argument('--data',type=str,help='raw data file.  Local endian floats')
    parser.add_argument('--png',type=str,help='output .png file for the heatmap')
    args = parser.parse_args()
    sys.exit(heatmap(args.data,args.png))
