# D:\commdsp\comms\ofdm\simulator.py
import numpy as np
# Import OFDM-specific components (Tx, Rx)
from comms.ofdm.transmitter import OFDMTransmitter
from comms.ofdm.receiver import OFDMReceiver
# Import general Channel interface
from comms.channel.interfaces import IChannel
# Import general utility functions
from utils.helpers import calculate_ber, generate_random_bits

class OFDMSimulator:
    """Orchestrates the OFDM simulation process."""
    def __init__(self, transmitter: OFDMTransmitter, channel: IChannel, receiver: OFDMReceiver):
        self.transmitter = transmitter
        self.channel = channel
        self.receiver = receiver

    def run_ber_simulation(self, snr_db_range: np.ndarray, total_bits_per_snr: int, num_runs_per_snr: int = 1):
        """
        Runs a Bit Error Rate (BER) simulation across a range of SNRs.

        Args:
            snr_db_range (np.ndarray): Array of SNR values in dB to simulate.
            total_bits_per_snr (int): Total number of bits to transmit at each SNR point.
            num_runs_per_snr (int): Number of independent simulation runs at each SNR to average BER.

        Returns:
            list: A list of BER values corresponding to each SNR in snr_db_range.
        """
        bers = []
        print(f"Starting BER simulation across {len(snr_db_range)} SNR points.")
        for snr_db in snr_db_range:
            total_errors_at_snr = 0
            total_bits_at_snr = 0
            
            # Run multiple times to average BER for better statistics
            for run in range(num_runs_per_snr):
                # 1. Generate random bits
                transmitted_bits = generate_random_bits(total_bits_per_snr)
                
                # 2. Transmitter processing
                tx_signal = self.transmitter.process(transmitted_bits)
                
                # 3. Channel processing
                rx_signal = self.channel.apply(tx_signal, snr_db)
                
                # 4. Receiver processing
                received_bits = self.receiver.process(rx_signal)
                
                # 5. Calculate errors for this run
                errors = np.sum(transmitted_bits != received_bits)
                total_errors_at_snr += errors
                total_bits_at_snr += len(transmitted_bits) # Ensure correct length

            current_ber = total_errors_at_snr / total_bits_at_snr
            bers.append(current_ber)
            print(f"  SNR: {snr_db} dB, BER: {current_ber:.4e}")
        return bers