#!/bin/sh
# Rebuild the two encoders patch_rom.py needs (needs g++/gcc with libpng + zlib).
set -e
cd "$(dirname "$0")/.."
mkdir -p hood/bin
g++ -std=c++17 -O1 -static -Itools/msgenc tools/msgenc/*.cpp -o hood/bin/msgenc.exe
gcc -O1 -static tools/nitrogfx/*.c -lpng -lz -o hood/bin/nitrogfx.exe
echo "built hood/bin/msgenc.exe and hood/bin/nitrogfx.exe"
