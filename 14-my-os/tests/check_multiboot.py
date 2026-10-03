#!/usr/bin/env python3
import struct
import sys

MAGIC = 0xE85250D6
LIMIT = 32768

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} KERNEL")
        return 2

    with open(sys.argv[1], "rb") as handle:
        data = handle.read(LIMIT)

    needle = struct.pack("<I", MAGIC)
    found = None

    for offset in range(0, max(0, len(data) - 16) + 1, 8):
        if data[offset:offset + 4] == needle:
            found = offset
            break

    if found is None:
        print("multiboot2 header not found in first 32 KiB")
        return 1

    magic, arch, length, checksum = struct.unpack_from("<4I", data, found)

    if length < 24 or found + length > len(data):
        print("invalid multiboot2 header length")
        return 1

    if (magic + arch + length + checksum) & 0xFFFFFFFF:
        print("invalid multiboot2 checksum")
        return 1

    end_type, end_flags, end_size = struct.unpack_from("<HHI", data, found + length - 8)
    if (end_type, end_flags, end_size) != (0, 0, 8):
        print("missing multiboot2 end tag")
        return 1

    print(f"multiboot2 header OK at file offset {found}, length={length}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
