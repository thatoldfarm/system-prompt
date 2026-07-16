---
---

<!-- Source: pi://[3923]{ 0 }<0> | 035_ENCOUNTER_Z80_EMULATOR-->
```assembly
; Simplified Z80 emulation
org 0x7c00
start:
 xor ax, ax
 mov ds, ax
 jmp start
```
