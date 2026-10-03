# Common Mistakes

- sanitizer crash = remote code executionแน่นอน
- crash instruction = root causeเสมอ
- check destination capacityแต่ไม่ check input available bytes
- check multiplicationหลัง overflowเกิดแล้ว
- castให้ typeเล็กก่อน validate
- set freed pointerหนึ่งตัว NULLแล้วถือว่า UAFหมด
- hardening flagแทน source fix
- fuzzingไม่มี crash = secure
- random bytesอย่างเดียว = coverageดี
- regression testที่ยัง invoke UB
- report impactเกิน evidence
- ทดสอบ third-party targetโดยไม่มี authorization
