# Study Guide

## วงจรการเรียนต่อหนึ่งหัวข้อ

1. **Read** — อ่านแนวคิดให้จบหนึ่งช่วง
2. **Predict** — เขียนสิ่งที่คิดว่าจะเกิดก่อนรัน
3. **Build** — compile/build ด้วยคำสั่งที่อธิบายได้
4. **Run** — รันและบันทึก output สำคัญ
5. **Observe** — แยก observation ออกจาก assumption
6. **Inspect** — ใช้ `file`, `readelf`, `objdump`, GDB หรือ raw bytes ตามบท
7. **Debug** — หาสาเหตุ ไม่ลบ error แล้วข้าม
8. **Modify** — เปลี่ยน input/codeหนึ่งอย่างเพื่อพิสูจน์ mental model
9. **Explain** — สรุปด้วยภาษาของตัวเอง
10. **Test** — exercises/challenges/mastery test

## สมุดทดลอง

แนะนำ:

```text
notes/
predictions/
experiments/
reports/
```

ต่อหนึ่ง lab:

```text
Prediction:
Observed:
Why:
Evidence:
What I changed:
What I still do not understand:
```

## อย่าเรียนแบบ copy/paste

Copy commandเพื่อลดงานพิมพ์ได้ แต่ต้องอธิบาย optionและผลกระทบต่อ pipelineได้.

## Mastery Gate

ผ่าน chapter เมื่อ:

- concept questions ≥85%
- required labs/build/testsผ่าน
- อธิบายด้วย evidenceได้
- เปลี่ยนตัวอย่างแล้วทำนายผลใหม่ได้
- ระบุ limitations/uncertaintyได้

## Final Capstone Gate

หลัง Chapter 17:

```bash
make -C 18-capstone clean test
```

จากนั้นทำ:
- `18-capstone/FINAL_CHECKLIST.md`
- `18-capstone/MASTERY_TEST.md`
- `18-capstone/REPORT_TEMPLATE.md`
- `18-capstone/PORTFOLIO_TEMPLATE.md`

Automated testsไม่แทน oral/written explanation. จุดจบของหลักสูตรคือสามารถเชื่อม representation→contract→mechanism→evidence→test→explanation ได้ด้วยตัวเอง.
