# D:\commdsp\comms\ofdm\receiver.py
import numpy as np
from comms.modulation.interfaces import IModulator # <--- NEW PATH for Modulator Interface

class OFDMReceiver:
    """Simulates the OFDM Receiver operations."""
    def __init__(self, num_subcarriers: int, cp_length: int, modulator: IModulator):
        self.num_subcarriers = num_subcarriers
        self.cp_length = cp_length
        self.modulator = modulator

    def process(self, received_signal: np.ndarray) -> np.ndarray:
        """
        Processes the received time-domain signal to recover bits.
        Steps: CP Removal -> FFT -> P/S -> Demodulation.
        """
        samples_per_ofdm_symbol = self.num_subcarriers + self.cp_length
        
        # Determine how many full OFDM symbols were received
        num_ofdm_symbols_received = len(received_signal) // samples_per_ofdm_symbol
        
        received_bits_stream = []

        for i in range(num_ofdm_symbols_received):
            # Extract current OFDM symbol in time domain (including CP)
            current_received_symbol_time_domain = received_signal[i * samples_per_ofdm_symbol : (i+1) * samples_per_ofdm_symbol]
            
            # Remove Cyclic Prefix
            cp_removed_symbol = current_received_symbol_time_domain[self.cp_length:]
            
            # Perform FFT to convert time domain signal to frequency domain symbols
            freq_domain_symbol = np.fft.fft(cp_removed_symbol, n=self.num_subcarriers)
            
            # TODO: Add channel estimation, equalization, pilot extraction here if needed
            # For now, a simple direct demodulation

            # Demodulate frequency domain symbols back to bits
            demodulated_bits = self.modulator.demodulate(freq_domain_symbol)
            received_bits_stream.append(demodulated_bits)

        # Concatenate all demodulated bit streams
        return np.concatenate(received_bits_stream)