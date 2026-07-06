with open("pi.txt", "r") as f:
    pi = f.read().strip()[1:88] # first 87 digits after 3.

print("Pi 87 digits:", pi)

binary_pi = "".join([str(int(d) % 2) for d in pi])
print("Binary pi:", binary_pi)

found = set()
for i in range(len(binary_pi) - 3):
    chunk = binary_pi[i:i+4]
    found.add(chunk)

print("Found 4-bit strings:", sorted(list(found)))
print("Number of unique 4-bit strings:", len(found))
