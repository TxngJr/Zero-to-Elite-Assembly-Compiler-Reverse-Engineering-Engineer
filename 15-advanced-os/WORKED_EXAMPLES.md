# Worked Examples — Advanced OS Models & Integration Design

Projectsบทนี้เป็น host-side deterministic models. อย่าอ้างว่า integrateเข้า EliteOS64แล้ว.

## Example 1 — Round-robin scheduler

**Goal:** trace task statesและ quantum.

**Command / action:**

```bash
make -C 15-advanced-os/projects/scheduler-sim clean test
15-advanced-os/projects/scheduler-sim/scheduler-sim
```

**Prediction:** tasks 5/3/4 work unitsกับ quantum 2จบรวม 12 ticksและสลับตาม ready queue.

**Expected key evidence:** traceมี slices; final `completed=3 ticks=12`.

**What may vary:** noneใน simulator.

**Explain:** READY taskถูกเลือก, RUNNINGใช้ slice, unfinishedกลับ READY, finished→DONE.

**Modification:** เปลี่ยน quantum 1และ4แล้วทำนาย sequence; total workต้องยัง 12.

**Failure mode:** blocked taskไม่ควรอยู่ runnable queueใน real scheduler extension.

**Reflection:** fairness/latency/context-switch overhead trade-offของ quantum.

---

## Example 2 — fork + Copy-on-Write

**Goal:** เห็น shared frame refcountก่อนและหลัง write.

**Command / action:**

```bash
python3 15-advanced-os/projects/vm-cow-sim/vm_cow.py
```

**Prediction:** หลัง fork parent/childชี้ frameเดียว refcount=2; child writeทำ copyและค่าของ parentไม่เปลี่ยน.

**Expected key evidence:** selftestจบ `vm-cow-sim: OK`.

**What may vary:** frame IDsหาก allocatorเปลี่ยน.

**Explain:** mappingsต้อง read-only+COWเพื่อให้ write faultเป็น trigger; refcountป้องกัน free shared frameเร็วเกิน.

**Modification:** เพิ่ม second pageแล้วให้ childแก้เพียงหน้าเดียว.

**Failure mode:** mark COWแต่ยัง writableจะไม่มี faultให้ kernel intercept.

**Reflection:** real kernelต้องทำอะไรเพิ่ม: page-fault handler, physical copy, PTE update, TLB invalidation.

---

## Example 3 — Bounded pipe wrap-around

**Goal:** เข้าใจ ring bufferก่อนผูกกับ scheduler blocking.

**Command / action:**

```bash
make -C 15-advanced-os/projects/ipc-sim clean test
15-advanced-os/projects/ipc-sim/ipc-sim
```

**Prediction:** capacity 8; write 9 bytesรับได้ 8; read 3แล้วเขียนเพิ่ม 3ต้อง wrap tailและรักษาลำดับ bytes.

**Expected key evidence:** final `ipc-sim: OK`.

**What may vary:** none.

**Explain:** head/tail/countเป็น buffer state; “full/empty” policyแยกจาก schedulerว่าจะ blockหรือ partial return.

**Modification:** เพิ่ม test empty readและmultiple wraps.

**Failure mode:** ใช้ head==tailอย่างเดียวแยก full/emptyไม่ได้ถ้าไม่มี count/extra state.

**Reflection:** real blocking pipeต้องมี wait queue/wakeupที่ไหน?

---

## Example 4 — VFS path lookup

**Goal:** แยก path traversal, inode-like node และ open-file state.

**Command / action:**

```bash
make -C 15-advanced-os/projects/vfs-sim clean test
15-advanced-os/projects/vfs-sim/vfs-sim
```

**Prediction:** `/etc/motd` traverse root→etc→motd; missing pathคืน NULL/error.

**Expected key evidence:** content `Welcome to EliteOS` และ testผ่าน.

**What may vary:** none.

**Explain:** current simulatorเป็น tree lookup; real VFSต้องเพิ่ม mounts, symlinks, permissions, races, open offsets.

**Modification:** เพิ่ม nested directoryและfileใหม่พร้อม negative lookup.

**Failure mode:** inode/node metadataกับ open descriptor offsetไม่ควรเป็น objectเดียวกัน.

**Reflection:** เขียน integration orderถ้าจะย้าย VFS modelเข้า kernelหลัง processes/syscalls.
