# Worked Examples — OS Foundations

## Example 1 — Split x86-64 virtual address

**Goal:** คำนวณ PML4/PDPT/PD/PT/offsetจาก virtual address.

**Command / action:**

```bash
python3 13-os-foundations/projects/page-walk-sim/page_walk.py \
  split 0x00007fffffffffff
```

**Prediction:** 4 KiB offset = low 12 bits; indicesแต่ละระดับ 9 bits.

**Expected key evidence:** simulatorแสดง 4 indices + offsetและ reject non-canonical address.

**What may vary:** noneใน deterministic calculation.

**Explain:** without LA57, canonical addressต้อง sign-extend bit47ไป bits63..48.

**Modification:**

```bash
set +e
python3 13-os-foundations/projects/page-walk-sim/page_walk.py \
  split 0x0000800000000000
echo "status=$?"
set -e
```

**Failure mode:** TLB missไม่เท่ากับ page fault; page walkอาจสำเร็จ.

**Reflection:** วาด translation path VA→PML4→PDPT→PD→PT→frame.

---

## Example 2 — IDT gate bytes

**Goal:** map 64-bit handler addressลง 16-byte interrupt gate.

**Command / action:**

```bash
make -C 13-os-foundations/projects/descriptor-lab clean test
13-os-foundations/projects/descriptor-lab/descriptor-lab
```

**Prediction:** gate size 16 bytes; handler addressถูก split low/mid/high fieldsแล้ว reconstructได้เท่าเดิม.

**Expected key evidence:** test assert size/address/selector/attributes.

**What may vary:** printed example addressถ้า sourceเปลี่ยน.

**Explain:** IDT entryเป็น packed hardware-defined layout ไม่ใช่ C pointer array.

**Modification:** เปลี่ยน handler constantแล้วคำนวณ fieldsด้วยมือก่อนรัน.

**Failure mode:** C struct paddingถ้าไม่ packed/field orderผิดจะทำ hardware layoutพัง.

**Reflection:** ทำไมต้อง inspect `sizeof`/raw bytesเมื่อติดต่อ hardware structures?

---

## Example 3 — 2 MiB early identity mapping

**Goal:** คำนวณว่าทำไม 4 page directories map 4 GiBได้.

**Prediction / calculation:**

```text
1 PD = 512 entries
1 huge PDE = 2 MiB
512 * 2 MiB = 1 GiB
4 PDs = 4 GiB
```

**Command / action:**

```bash
grep -n -E 'setup_pdpt|map_pd|2048|0x83|cr3|wrmsr' \
  14-my-os/kernel/boot.s
```

**Expected key evidence:** loopสร้าง 2048 huge PDEsและใช้ flags Present|Writable|PageSize.

**What may vary:** source line numbers.

**Explain:** identity mappingทำให้ early virtual==physicalสำหรับ mapped range; ไม่ใช่ long-term isolation design.

**Modification:** คำนวณ tablesที่ต้องใช้ถ้าใช้ 4 KiB pagesเต็ม 4 GiB.

**Failure mode:** CR3ต้องชี้ physical rootของ page tablesใน early mapping contract.

**Reflection:** PMM, VMM, heapตอบคำถามคนละระดับอะไร?
