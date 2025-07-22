# D:\commdsp\comms\ofdm\modulation\interfaces.py
from abc import ABC, abstractmethod
import numpy as np

class IModulator(ABC):
    M: int # Modulation order (e.g., 4 for QPSK, 16 for 16QAM)
    BITS_PER_SYMBOL: int

    @abstractmethod
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """Maps bits to complex constellation symbols."""
        pass

    @abstractmethod
    def demodulate(self, symbols: np.ndarray) -> np.ndarray:
        """Maps complex constellation symbols back to bits."""
        pass