import random
import numpy as np

def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.choice(['+', 'x']) for _ in range(length)]

def measure_in_basis(bit, basis):
    if basis == '+':
        return bit  # 0 -> 0, 1 -> 1
    else:
        return bit if random.random() < 0.5 else 1 - bit  # 50% chance to flip

def bb84_protocol(length):
    alice_bits = generate_random_bits(length)
    alice_bases = generate_random_bases(length)
    bob_bases = generate_random_bases(length)
    
    bob_measurements = [measure_in_basis(bit, bob_bases[i]) for i, bit in enumerate(alice_bits)]
    
    # Comparing bases
    key = [alice_bits[i] for i in range(length) if alice_bases[i] == bob_bases[i]]
    
    return key

def generate_bb84_key(length=256):
    key_bits = bb84_protocol(length)
    key = np.packbits(key_bits)
    return bytes(key[:32])  # 256 bits -> 32 bytes for AES-256