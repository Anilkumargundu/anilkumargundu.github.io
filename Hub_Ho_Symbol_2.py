import numpy as np
import matplotlib.pyplot as plt

# Define the pattern
pattern = "1101000111010101010111100001011"

# Define parameters
symbol_duration = 1e-3  # 1ms
rise_fall_time = 1e-6   # 1us
symbol_1_level = 0.65   # 0.65V for '1'
symbol_0_level = 0.45   # 0.45V for '0'
sampling_rate = 1e6     # 1MHz for better resolution

# Generate time array
total_time = len(pattern) * symbol_duration
time = np.arange(0, total_time, 1/sampling_rate)

# Generate signal
signal = np.zeros_like(time)
current_time = 0

for symbol in pattern:
    if symbol == '1':
        level = symbol_1_level
    else:
        level = symbol_0_level

    start_idx = int(current_time * sampling_rate)
    end_idx = int((current_time + symbol_duration) * sampling_rate)
    rise_end_idx = int((current_time + rise_fall_time) * sampling_rate)
    fall_start_idx = int((current_time + symbol_duration - rise_fall_time) * sampling_rate)

    signal[start_idx:rise_end_idx] = np.linspace(signal[start_idx - 1] if start_idx > 0 else level, level, rise_end_idx - start_idx)
    signal[rise_end_idx:fall_start_idx] = level

    if symbol == pattern[-1]:
        signal[fall_start_idx:end_idx] = level  # Maintain the level for the last symbol
    else:
        signal[fall_start_idx:end_idx] = np.linspace(level, signal[end_idx - 1], end_idx - fall_start_idx)

    current_time += symbol_duration

# Plot the signal
plt.figure(figsize=(12, 6))
plt.plot(time * 1e3, signal)  # Convert time to milliseconds for the X-axis
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Pattern "1101000111010101010111100001010" over Time')
plt.grid(True)
plt.show()
