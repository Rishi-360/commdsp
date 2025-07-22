# D:\commdsp\comms\channel\awgn.py
import numpy as np
from .interfaces import IChannel # Relative import within the 'channel' package

class AWGNChannel(IChannel):
    """Implements an Additive White Gaussian Noise (AWGN) channel."""
    def apply(self, signal: np.ndarray, snr_db: float, **kwargs) -> np.ndarray:
        """
        Applies Additive White Gaussian Noise (AWGN) to the signal.

        Args:
            signal (np.ndarray): The complex baseband signal (e.g., QPSK symbols).
            snr_db (float): Signal-to-Noise Ratio in dB.

        Returns:
            np.ndarray: The signal with AWGN added.
        """
        # Calculate signal power (average power of the complex signal)
        signal_power = np.mean(np.abs(signal)**2)
        
        # Convert SNR from dB to linear scale
        snr_linear = 10**(snr_db / 10)
        
        # Calculate noise power: Noise_Power = Signal_Power / SNR_Linear
        # This is based on SNR = Signal Power / Noise Power
        noise_power = signal_power / snr_linear
        
        # Calculate standard deviation of noise for complex Gaussian noise
        # For complex noise, the total noise power is split equally between real and imaginary parts.
        # So, variance of real part = variance of imag part = noise_power / 2
        # Standard deviation = sqrt(variance)
        noise_std = np.sqrt(noise_power / 2)
        
        # Generate complex Gaussian noise
        # Use np.random.randn for standard normal distribution (mean 0, std 1)
        # Scale by noise_std
        noise = (noise_std * np.random.randn(*signal.shape) +
                 1j * noise_std * np.random.randn(*signal.shape))
        
        # Add noise to the signal
        received_signal = signal + noise
        return received_signal