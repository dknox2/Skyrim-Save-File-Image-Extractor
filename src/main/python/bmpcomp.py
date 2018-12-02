import sys
try:
    from PIL import Image
except ImportError:
    print('PIL module not found. Please run "python -m pip install pillow" then re-run bmpcomp.py')

usage = '''python3 bmpcomp.py reference.bmp testfile.bmp
Compares two bitmap (BMP) images. Images must be pixel-for-pixel the same for
a 'true' comparison. Returns exit status 0 on success, non-zero otherwise (to conform to
Unix conventions).

reference.bmp is a known 'good' bitmap
testfile.bmp is the bitmap being compared against the reference

This module requires the PIL (pillow) library.
'''

INCORRECT_USAGE = -1
MATCH_FAILURE = 1
EXIT_SUCCESS = 0

def main():
    if len(sys.argv) != 3:
        print(usage, file=sys.stderr)
        exit(INCORRECT_USAGE)

    referenceFilename = sys.argv[1]
    testFilename = sys.argv[2]

    refImg = openBmpFile(referenceFilename)
    testImg = openBmpFile(testFilename)

    if areEquivalentBmpImages(refImg, testImg):
        print('Files match')
        exit(EXIT_SUCCESS)
    else:
        print('Files do not match')
        exit(MATCH_FAILURE)

def areEquivalentBmpImages(ref, test):
    print('reference file (width, height)=' + str(ref.size))
    print('test file (width, height)=' + str(test.size))
    if ref.size != test.size:
        exitWithFailure('Test image dimensions do not match')

    for row in range(ref.height):
        for col in range(ref.width):
            refPixel = ref.getpixel((col, row))
            testPixel = test.getpixel((col, row))
            if refPixel != testPixel:
                exitWithFailure('Test image pixel data does not match.')

    return True
        

def exitWithFailure(msg, status=MATCH_FAILURE):
    print(msg, file=sys.stderr)
    exit(status)

def openBmpFile(filename):
    try:
        img = Image.open(filename)
        return img
    except IOError:
        exitWithFailure(filename + ' is either not found or, possibly, not a valid bitmap (header data may be incorrect)', INCORRECT_USAGE)

if __name__ == "__main__":
    main()
