# D:\commdsp\main.py
import numpy as np

# Import QPSKModulator
from comms.modulation.qpsk import QPSKModulator
# You won't use other imports from the full main.py yet, just this one for now.

if __name__ == "__main__":
    print("Starting QPSK Modulator Test...")

    # 1. an instance of your QPSK Modulator
    modulator = QPSKModulator()

    # 2. Generate dummy bits (must be an even number for QPSK)
    #  generate 8 bits, which will form 4 QPSK symbols
    test_bits = np.array([0, 0, 0, 1, 1, 0, 1, 1])
    print(f"\nTest Bits (8 bits): {test_bits}")

    # 3. Modulate the bits
    try:
        modulated_symbols = modulator.modulate(test_bits)
        print(f"Modulated Symbols (4 symbols): {modulated_symbols}")

        # Expected output (approx after normalization by sqrt(2) ~ 1.414):
        # 00 -> -0.707 - 0.707j
        # 01 -> -0.707 + 0.707j
        # 10 ->  0.707 - 0.707j
        # 11 ->  0.707 + 0.707j

        # Print their real and imaginary parts to inspect
        print("\nReal Parts:", modulated_symbols.real)
        print("Imag Parts:", modulated_symbols.imag)

        # Quick check on the shape and data type
        print("Shape of symbols:", modulated_symbols.shape)
        print("Data type of symbols:", modulated_symbols.dtype)

    except ValueError as e:
        print(f"Error during modulation: {e}")
    except NotImplementedError as e:
        print(f"Error: {e}. (This is expected for demodulate, but not for modulate if you called it)")

    print("\nQPSK Modulator Test Finished.")