# C:\Users\Ashutosh Chaturvedi\code_projects\commdsp\run_ofdm_simulation.py
# import sys
# import os

# # Add the path to your new test package root
# # Make sure this matches the folder you created in Step 1
# sys.path.insert(0, 'D:\\my_test_package') 

# print("--- Diagnostic Output ---")
# print(f"Script location: {__file__}")
# print(f"Current Working Directory: {os.getcwd()}")
# print("Content of sys.path:")
# for p in sys.path:
#     print(f"- {p}")
# print("--- End sys.path ---")

# try:
#     import my_test_package.my_module
#     print("SUCCESS: Successfully imported my_test_package.my_module!")
#     print(f"Message from test module: {my_test_package.my_module.test_message}")
# except ModuleNotFoundError as e:
#     print(f"FAILURE: ModuleNotFoundError: {e}")
#     print("This means Python could not find 'my_test_package'.")
# except Exception as e:
#     print(f"UNEXPECTED ERROR: {e}")

# print("--- End Diagnostic Output ---")
import numpy as np
import matplotlib.pyplot as plt
# Corrected import path: commdsp is the top-level package, comms is inside it,
# then ofdm, then transmitter.

from commdsp.comms.ofdm.transmitter import generate_bits, qam_modulate

if __name__ == "__main__":
    # Simulation parameters
    num_bits = 10000 # Number of bits to simulate
    modulation_order = 16 # 16-QAM

    # 1. Generate random bits
    bits = generate_bits(num_bits)
    print(f"Generated {len(bits)} bits.")

    # 2. Perform QAM modulation
    try:
        modulated_symbols = qam_modulate(bits, modulation_order)
        print(f"Modulated {len(modulated_symbols)} symbols.")

        # 3. Plot the constellation
        plt.figure(figsize=(6, 6))
        plt.scatter(modulated_symbols.real, modulated_symbols.imag, alpha=0.7)
        plt.title(f"{modulation_order}-QAM Constellation")
        plt.xlabel("In-phase")
        plt.ylabel("Quadrature")
        plt.grid(True)
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(0, color='gray', lw=0.5)
        plt.axis('equal')
        plt.show()

    except ValueError as e:
        print(f"Error during modulation: {e}")
    except NotImplementedError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")