# D:\commdsp\comms\channel\interfaces.py
from abc import ABC, abstractmethod
import numpy as np

class IChannel(ABC):
    """Abstract Base Class for Channel models."""
    @abstractmethod
    def apply(self, signal: np.ndarray, snr_db: float, **kwargs) -> np.ndarray:
        """
        Applies channel effects (like noise, fading) to the input signal.

        Args:
            signal (np.ndarray): The complex baseband signal to transmit.
            snr_db (float): Signal-to-Noise Ratio in dB.
            **kwargs: Additional parameters for specific channel types (e.g., fading parameters).

        Returns:
            np.ndarray: The received signal after channel effects.
        """
        pass