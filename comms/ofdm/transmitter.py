# C:\Users\Ashutosh Chaturvedi\code_projects\commdsp\comms\ofdm\transmitter.py

import numpy as np
from comms.modulation.interfaces import IModulator
#removed in first refactoring
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
#removed in first refactoring

class OFDMTransmitter:
    """Simulates the OFDM Transmitter operations(still needs full implementation, currently a placeholder)."""
    def __init__(self, num_subcarriers: int, cp_length: int, modulator: IModulator):
        self.num_subcarriers = num_subcarriers
        self.cp_length = cp_length
        self.modulator = modulator

    def process(self, bits: np.ndarray) -> np.ndarray:
        """
        Processes input bits to generate an OFDM time-domain signal.
        Steps: Modulation -> S/P -> IFFT -> CP Addition.
        """
        # 1. Modulate bits to complex symbols
        modulated_symbols = self.modulator.modulate(bits)
        
        # Determine how many OFDM symbols we need to generate
        # (Assuming modulated_symbols are arranged sequentially for subcarriers)
        # need to pad if len(modulated_symbols) is not a multiple of num_subcarriers
        num_ofdm_blocks = len(modulated_symbols) // self.num_subcarriers
        if len(modulated_symbols) % self.num_subcarriers != 0:
            # Handle partial blocks, for simplicity here, we might truncate or pad
            print(f"Warning: Number of modulated symbols ({len(modulated_symbols)}) not a multiple of subcarriers ({self.num_subcarriers}). Truncating.")
            num_ofdm_blocks = len(modulated_symbols) // self.num_subcarriers
            # Or you can pad with zeros:
            # padding_needed = self.num_subcarriers - (len(modulated_symbols) % self.num_subcarriers)
            # modulated_symbols = np.pad(modulated_symbols, (0, padding_needed), 'constant', constant_values=0)
            # num_ofdm_blocks += 1

        tx_time_domain_stream = []

        for i in range(num_ofdm_blocks):
            # Extract symbols for current OFDM block
            current_freq_symbols = modulated_symbols[i * self.num_subcarriers : (i+1) * self.num_subcarriers]
            
            # TODO: Add pilot insertion, data/pilot mapping, DC subcarrier handling here if needed
            # For now, a simple direct IFFT

            # Perform IFFT to convert frequency domain symbols to time domain
            time_domain_symbol = np.fft.ifft(current_freq_symbols, n=self.num_subcarriers)
            
            # Add Cyclic Prefix (CP)
            cp_added_symbol = np.concatenate((time_domain_symbol[-self.cp_length:], time_domain_symbol))
            tx_time_domain_stream.append(cp_added_symbol)
        
        # Concatenate all OFDM symbols to form the continuous transmitted signal
        return np.concatenate(tx_time_domain_stream)