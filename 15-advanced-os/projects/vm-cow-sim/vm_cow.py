#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass

PAGE = 4096

@dataclass
class Mapping:
    frame: int
    writable: bool
    cow: bool

class PhysicalMemory:
    def __init__(self):
        self.next_frame = 1
        self.data: dict[int, bytearray] = {}
        self.refs: dict[int, int] = {}

    def alloc(self) -> int:
        frame = self.next_frame
        self.next_frame += 1
        self.data[frame] = bytearray(PAGE)
        self.refs[frame] = 1
        return frame

    def retain(self, frame: int) -> None:
        self.refs[frame] += 1

    def release(self, frame: int) -> None:
        self.refs[frame] -= 1
        if self.refs[frame] == 0:
            del self.refs[frame]
            del self.data[frame]

class AddressSpace:
    def __init__(self, pmem: PhysicalMemory):
        self.pmem = pmem
        self.pages: dict[int, Mapping] = {}

    def map_zero(self, va: int, writable: bool = True) -> None:
        assert va % PAGE == 0
        self.pages[va // PAGE] = Mapping(self.pmem.alloc(), writable, False)

    def fork(self) -> "AddressSpace":
        child = AddressSpace(self.pmem)
        for vpn, mapping in self.pages.items():
            mapping.writable = False
            mapping.cow = True
            self.pmem.retain(mapping.frame)
            child.pages[vpn] = Mapping(mapping.frame, False, True)
        return child

    def _resolve(self, va: int) -> tuple[Mapping, int]:
        vpn = va // PAGE
        if vpn not in self.pages:
            raise KeyError("page not mapped")
        return self.pages[vpn], va % PAGE

    def read8(self, va: int) -> int:
        mapping, offset = self._resolve(va)
        return self.pmem.data[mapping.frame][offset]

    def write8(self, va: int, value: int) -> None:
        mapping, offset = self._resolve(va)
        if not mapping.writable:
            if not mapping.cow:
                raise PermissionError("write denied")
            old = mapping.frame
            if self.pmem.refs[old] > 1:
                new = self.pmem.alloc()
                self.pmem.data[new][:] = self.pmem.data[old]
                self.pmem.release(old)
                mapping.frame = new
            mapping.writable = True
            mapping.cow = False
        self.pmem.data[mapping.frame][offset] = value & 0xFF

def selftest() -> None:
    pm = PhysicalMemory()
    parent = AddressSpace(pm)
    parent.map_zero(0x400000)
    parent.write8(0x400000, 7)

    child = parent.fork()
    shared = parent.pages[0x400000 // PAGE].frame
    assert child.pages[0x400000 // PAGE].frame == shared
    assert pm.refs[shared] == 2

    child.write8(0x400000, 99)
    assert parent.read8(0x400000) == 7
    assert child.read8(0x400000) == 99
    assert parent.pages[0x400000 // PAGE].frame != child.pages[0x400000 // PAGE].frame
    assert pm.refs[parent.pages[0x400000 // PAGE].frame] == 1
    assert pm.refs[child.pages[0x400000 // PAGE].frame] == 1

    print("vm-cow-sim: OK")

if __name__ == "__main__":
    selftest()
