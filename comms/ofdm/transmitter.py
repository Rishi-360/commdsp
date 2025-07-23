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

# Modulation Scheme: QPSK (2 bits/symbol)
# Number of Subcarriers (N_fft/FFT Size): N=64
# Number of Used Subcarriers (N_data): Ndata=48 
# Cyclic Prefix Length (N_cp): N_cp=16
# OFDM Symbol Length (Time Domain): N_symbol=N+N_cp 
# Channel Type: AWGN (Additive White Gaussian Noise) Channel
# Pilot Subcarriers: None (for basic simulation
# Error Correction Coding: None (Uncoded)
# Simulation Parameters: Vary SNR from −5 dB to 20 dB, transmit 1,000 to 10,000 OFDM symbols per SNR point.
    def __init__(self, fft_size: int,num_data_subcarriers: int, cp_length: int, modulator: IModulator):
       #members of odfmtransmitter class
        self.num_data_subcarriers = num_data_subcarriers
        self.cp_length = cp_length
        self.modulator = modulator
        self.fft_size=fft_size

        # Pre-calculate indices for data subcarriers (center-loaded for simplicity)
        # Assuming DC (index 0) and the Nyquist frequency (N_fft/2) are unused.
        # We need to place num_data_subcarriers symmetrically around DC.
        
        if num_data_subcarriers % 2 != 0:
            raise ValueError("num_data_subcarriers must be an even number for symmetric placement around DC.")

        half_data_subcarriers = self.num_data_subcarriers // 2
        
        # Indices for the positive frequency data subcarriers
        # Start from 1 (avoiding DC) up to half_data_subcarriers
        self._data_subcarrier_indices_positive = np.arange(1, half_data_subcarriers + 1)
        
        # Indices for the negative frequency data subcarriers (from the upper half of FFT)
        # These are usually placed from N_fft - half_data_subcarriers to N_fft - 1
        self._data_subcarrier_indices_negative = np.arange(self.fft_size - half_data_subcarriers, self.fft_size)

        # Combine all data subcarrier indices and sort them
        self._all_data_subcarrier_indices = np.concatenate((self._data_subcarrier_indices_positive, self._data_subcarrier_indices_negative))
        self._all_data_subcarrier_indices.sort() # Ensure they are sorted

        print(f"Transmitter initialized: FFT Size={self.fft_size}, Data Subcarriers={self.num_data_subcarriers}, CP Length={self.cp_length}")
        print(f"Data Subcarrier Indices: {self._all_data_subcarrier_indices}")



    

    def process(self, bits: np.ndarray) -> np.ndarray:
        """
        Processes input bits to generate an OFDM time-domain signal.
        Steps: Modulation -> S/P -> IFFT -> CP Addition.
        """
        # 1. Modulate bits to complex symbols
        modulated_symbols = self.modulator.modulate(bits)
        
        # Determine how many OFDM symbols we need to generate
        # (Assuming modulated_symbols are arranged sequentially for subcarriers)
        # need to pad if len(modulated_symbols) is not a multiple of num_data_subcarriers
        num_ofdm_blocks = len(modulated_symbols) // self.num_data_subcarriers
        if len(modulated_symbols) % self.num_data_subcarriers != 0:
            # Handle partial blocks, for simplicity here, we might truncate or pad
            print(f"Warning: Number of modulated symbols ({len(modulated_symbols)}) not a multiple of subcarriers ({self.num_data_subcarriers}). Truncating.")
            num_ofdm_blocks = len(modulated_symbols) // self.num_data_subcarriers
            # Or you can pad with zeros:
            # padding_needed = self.num_data_subcarriers - (len(modulated_symbols) % self.num_data_subcarriers)
            # modulated_symbols = np.pad(modulated_symbols, (0, padding_needed), 'constant', constant_values=0)
            # num_ofdm_blocks += 1

        tx_time_domain_stream = []

        for i in range(num_ofdm_blocks):
            # Extract symbols for current OFDM block
            current_freq_symbols = modulated_symbols[i * self.num_data_subcarriers : (i+1) * self.num_data_subcarriers]
            
            # TODO: Add pilot insertion, data/pilot mapping, DC subcarrier handling here if needed
            # For now, a simple direct IFFT

            # Perform IFFT to convert frequency domain symbols to time domain
            time_domain_symbol = np.fft.ifft(current_freq_symbols, n=self.num_data_subcarriers)
            
            # Add Cyclic Prefix (CP)
            cp_added_symbol = np.concatenate((time_domain_symbol[-self.cp_length:], time_domain_symbol))
            tx_time_domain_stream.append(cp_added_symbol)
        
        # Concatenate all OFDM symbols to form the continuous transmitted signal
        return np.concatenate(tx_time_domain_stream)