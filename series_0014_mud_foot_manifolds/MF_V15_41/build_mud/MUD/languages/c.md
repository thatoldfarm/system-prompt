---
---

<!-- Source: pi://[542063]{ 0 }<0> | 002_extracted_block-->
```c
volatile uint16_t* CSR_MAP = (uint16_t*)0x800;
void unibus_route(uint32_t octal_addr) {
  if(octal_addr == 0177700) { QFT11_LSZ_REDUCE(); }
  else if(octal_addr == 0177600) { SED16_MULTIPLY(); }
  else if(octal_addr == 0160000) { VAULT_GATEWAY_OPEN(); }
  CSR_MAP[0] = (uint16_t)octal_addr;
}
int main() { unibus_route(0177700); return 0; }
```
