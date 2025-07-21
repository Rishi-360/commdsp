# C:\Users\Ashutosh Chaturvedi\code_projects\commdsp\comms\ofdm\transmitter.py

import numpy as np

def generate_bits(num_bits):
    """Generates a random stream of binary bits."""
    return np.random.randint(0, 2, num_bits)

def qam_modulate(bits, modulation_order):
    """
    Performs QAM modulation on a stream of bits.
    For simplicity, this example only includes 16-QAM mapping.
    """
    if not (modulation_order > 0 and (modulation_order & (modulation_order - 1) == 0)):
        raise ValueError("Modulation order must be a power of 2.")

    bits_per_symbol = int(np.log2(modulation_order))
    if len(bits) % bits_per_symbol != 0:
        raise ValueError(f"Number of bits ({len(bits)}) must be a multiple of bits per symbol ({bits_per_symbol}) for {modulation_order}-QAM.")

    # Define 16-QAM mapping (for instance)
    if modulation_order == 16:
        qam_mapping = {
            (0, 0, 0, 0): (-3 - 3j), (0, 0, 0, 1): (-3 - 1j),
            (0, 0, 1, 0): (-3 + 3j), (0, 0, 1, 1): (-3 + 1j),
            (0, 1, 0, 0): (-1 - 3j), (0, 1, 0, 1): (-1 - 1j),
            (0, 1, 1, 0): (-1 + 3j), (0, 1, 1, 1): (-1 + 1j),
            (1, 0, 0, 0): (3 - 3j),  (1, 0, 0, 1): (3 - 1j),
            (1, 0, 1, 0): (3 + 3j),  (1, 0, 1, 1): (3 + 1j),
            (1, 1, 0, 0): (1 - 3j),  (1, 1, 0, 1): (1 - 1j),
            (1, 1, 1, 0): (1 + 3j),  (1, 1, 1, 1): (1 + 1j)
        }
    else:
        raise NotImplementedError(f"{modulation_order}-QAM mapping not implemented yet for this example.")

    bit_groups = bits.reshape(-1, bits_per_symbol)
    qam_symbols = np.array([qam_mapping[tuple(group)] for group in bit_groups])
    return qam_symbols