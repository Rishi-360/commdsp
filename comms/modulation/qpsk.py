# D:\commdsp\comms\ofdm\modulation\qpsk.py
import numpy as np
from .interfaces import IModulator # Relative import for the interface

class QPSKModulator(IModulator):
    def __init__(self):
        self.M = 4 # QPSK (4-ary modulation)
        self.BITS_PER_SYMBOL = int(np.log2(self.M)) # log2(4) = 2 bits per symbol
        self._norm_factor = np.sqrt(2) # For average power normalization (1+1j squared gives 2, we want avg power 1)

    def modulate(self, bits: np.ndarray) -> np.ndarray:
        # Ensure bits length is a multiple of BITS_PER_SYMBOL (2 for QPSK)
        if len(bits) % self.BITS_PER_SYMBOL != 0:
            raise ValueError(f"Number of bits ({len(bits)}) must be a multiple of {self.BITS_PER_SYMBOL} for QPSK.")

        # Reshape bits into pairs (e.g., [0,1,1,0] -> [[0,1], [1,0]]) or[[0,1]
        #                                                                [1,0]]
        bit_pairs = bits.reshape(-1, self.BITS_PER_SYMBOL)
        # -1 for one of the dimensions=> NumPy automatically calculates the size of that dimension 

        # Map bit pairs to complex QPSK symbols:
        # 00 -> -1 - 1j
        # 01 -> -1 + 1j
        # 10 ->  1 - 1j
        # 11 ->  1 + 1j

        # Convert 0s to -1 and 1s to 1 for real/imag parts
        # (bit_pairs[:, 0] gives first bit of each pair, etc.)
        # bit_pairs[:,0] means all rows, first column     
        real_part = (bit_pairs[:, 0] * 2 - 1)  # If bit is 0 -> -1, if bit is 1 -> 1
        #yes, operation is element-wise, first cordinate of the pair/ first column of the list

        # bit_pairs[:,1] means all rows, second column/second cordinate
        imag_part = (bit_pairs[:, 1] * 2 - 1)  # If bit is 0 -> -1, if bit is 1 -> 1
        #yes, operation is element-wise,

        # Combine into complex symbols and normalize
        symbols = (real_part + 1j * imag_part) / self._norm_factor
        return symbols

    def demodulate(self, symbols: np.ndarray) -> np.ndarray:
         
                  
        """
        Maps complex constellation symbols back to bits using a nearest-neighbor approach.
        Assumes symbols are normalized.
        """
        # Reverse normalization done in modulate
        symbols_unnorm = symbols * self._norm_factor

        # Demap to real and imaginary parts based on constellation quadrants (nearest neighbour)
        # If real part > 0, original I-bit was 1, else 0
        # If imag part > 0, original Q-bit was 1, else 0

        # Map back to 0/1 based on the sign of real/imag parts
        # [False, True].astype(int) would result in [0, 1]
        # .real or .imag can convert resolve complex numbers in real and imaginary
        demod_bits_real = (symbols_unnorm.real > 0).astype(int) # -1 -> 0, 1 -> 1
        demod_bits_imag = (symbols_unnorm.imag > 0).astype(int) # -1 -> 0, 1 -> 1

        # Interleave the real (I) and imaginary (Q) bits back into a single stream
        # Example: [I1, Q1, I2, Q2, ...]
        bits = np.empty((len(symbols) * self.BITS_PER_SYMBOL,), dtype=int)
        bits[0::self.BITS_PER_SYMBOL] = demod_bits_real # Place I bits
        bits[1::self.BITS_PER_SYMBOL] = demod_bits_imag # Place Q bits

        return bits