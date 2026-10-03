# Challenges

- **04-A Ten args:** assembly functionรับ 10 integer argsและคืน weighted sum; testsพิสูจน์ stack offsets.
- **04-B Recursive ABI:** factorial recursionที่ preserve/alignmentถูก; harnessจำกัด inputเพื่อหลีกเลี่ยง overflow.
- **04-C EINTR-aware cat:** retry read/writeเมื่อ raw return = `-EINTR` พร้อม partial writes.
- **04-D No-libc byte counter:** `_start` รับ filename, open/readนับ bytes, exit codesชัดเจน.
- **04-E Callback table:** C ส่ง function pointersหลายตัวเข้า assembly dispatcher; verify indirect-call ABI.
