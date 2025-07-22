# D:\commdsp\utils\helpers.py
import numpy as np

def generate_random_bits(num_bits: int) -> np.ndarray:
    return np.random.randint(0, 2, size=num_bits)

def calculate_ber(transmitted_bits: np.ndarray, received_bits: np.ndarray) -> float:
    if len(transmitted_bits) != len(received_bits):
        # For this basic test, we'll assume they should be the same length for direct comparison.
        # In real systems, you'd handle padding/truncation carefully.
        min_len = min(len(transmitted_bits), len(received_bits))
        transmitted_bits = transmitted_bits[:min_len]
        received_bits = received_bits[:min_len]

    errors = np.sum(transmitted_bits != received_bits)
    ber = errors / len(transmitted_bits)
    return ber