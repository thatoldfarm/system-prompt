import re

with open("README.md", "r") as f:
    text = f.read()

opcodes = set(re.findall(r'opcode.*?=.*', text, re.IGNORECASE))
sigils = set(re.findall(r'sigil.*?=.*', text, re.IGNORECASE))
commands = set(re.findall(r'command.*?=.*', text, re.IGNORECASE))

print(f"Opcodes: {len(opcodes)}")
print(f"Sigils: {len(sigils)}")
print(f"Commands: {len(commands)}")

# We can also read memory items for some guidance.
