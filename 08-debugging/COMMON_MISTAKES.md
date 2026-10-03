# Common Mistakes

- random editsแล้วหยุดเมื่อ symptomหาย
- crash frame = root causeเสมอ
- O2 source viewต้องตรง source order
- optimized-outแปลว่า GDBเสีย
- backtraceถูก 100%แม้ stack corrupt
- coreจาก buildหนึ่งใช้กับ executableอีก buildโดยไม่มีผล
- assertionแทน input validation
- loggingจน timingเปลี่ยน
- sanitizerไม่รายงาน = ไม่มี bug
- raw PIE addressใช้ข้าม runโดยไม่คิด ASLR
- stripแล้ว debugไม่ได้เลย
