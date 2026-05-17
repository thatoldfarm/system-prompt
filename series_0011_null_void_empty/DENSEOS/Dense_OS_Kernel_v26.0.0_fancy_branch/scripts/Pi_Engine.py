from mpmath import mp

def get_pi_hex(offset, length):
    mp.dps = length + 100  # High precision
    pi_hex = mp.nstr(mp.pi, length + 100)[2:]  # Skip "0x"
    return pi_hex[offset:offset + length]
