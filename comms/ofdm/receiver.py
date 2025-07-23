# D:\commdsp\comms\ofdm\receiver.py
import numpy as np
from comms.modulation.interfaces import IModulator # <--- NEW PATH for Modulator Interface

class OFDMReceiver:
    """Simulates the OFDM Receiver operations."""
    def __init__(self,fft_size:int, num_data_subcarriers: int, cp_length: int, modulator: IModulator):
        self.num_data_subcarriers = num_data_subcarriers
        self.cp_length = cp_length
        self.modulator = modulator
        self.fft_size=fft_size

        
        # Pre-calculate indices for data subcarriers (center-loaded for simplicity)
        # Assuming DC (index 0) and the Nyquist frequency (N_fft/2) are unused.
        # We need to place num_data_subcarriers symmetrically around DC.
        
        if num_data_subcarriers % 2 != 0:
            raise ValueError("num_data_subcarriers must be an even number for symmetric placement around DC.")

        # value tells us how many data subcarriers will be on the positive frequency side
        # and how many will be on the negative frequency side of the spectrum.
        half_data_subcarriers = self.num_data_subcarriers // 2  #integer division by 2
        
        # Indices for the positive frequency data subcarriers
        # Start from 1 (avoiding DC) up to half_data_subcarriers
        # If half_data_subcarriers is 24, this creates [1, 2, ..., 24]
        self._data_subcarrier_indices_positive = np.arange(1, half_data_subcarriers + 1)
        
        # Indices for the negative frequency data subcarriers (from the upper half of FFT)
        # These are usually placed from N_fft - half_data_subcarriers to N_fft - 1
        # If half_data_subcarriers is 24, this creates [40, 41, ..., 63]
        self._data_subcarrier_indices_negative = np.arange(self.fft_size - half_data_subcarriers, self.fft_size)

        # Combine all data subcarrier indices and sort them
        self._all_data_subcarrier_indices = np.concatenate((self._data_subcarrier_indices_positive, self._data_subcarrier_indices_negative))
        self._all_data_subcarrier_indices.sort() # Ensure they are sorted
        # This wrap-aroung ordering is a mathematical convention of the DFT. It's computationally efficient to arrange it this way

        print(f"receiver initialized: FFT Size={self.fft_size}, Data Subcarriers={self.num_data_subcarriers}, CP Length={self.cp_length}")
        print(f"Data Subcarrier Indices: {self._all_data_subcarrier_indices}")


    def process(self, received_signal: np.ndarray) -> np.ndarray:
        """
        Processes the received time-domain signal to recover bits.
        Steps: CP Removal -> FFT -> P/S -> Demodulation.
        """
        samples_per_ofdm_symbol = self.num_data_subcarriers + self.cp_length
        
        # Determine how many full OFDM symbols were received
        num_ofdm_symbols_received = len(received_signal) // samples_per_ofdm_symbol
        
        received_bits_stream = []

        for i in range(num_ofdm_symbols_received):
            # Extract current OFDM symbol in time domain (including CP)
            current_received_symbol_time_domain = received_signal[i * samples_per_ofdm_symbol : (i+1) * samples_per_ofdm_symbol]
            
            # Remove Cyclic Prefix
            cp_removed_symbol = current_received_symbol_time_domain[self.cp_length:]
            
            # Perform FFT to convert time domain signal to frequency domain symbols
            freq_domain_symbol = np.fft.fft(cp_removed_symbol, n=self.num_data_subcarriers)
            
            # TODO: Add channel estimation, equalization, pilot extraction here if needed
            # For now, a simple direct demodulation

            # Demodulate frequency domain symbols back to bits
            demodulated_bits = self.modulator.demodulate(freq_domain_symbol)#refer init; during runtime modulator will be passed
            received_bits_stream.append(demodulated_bits)

        # Concatenate all demodulated bit streams
        return np.concatenate(received_bits_stream)