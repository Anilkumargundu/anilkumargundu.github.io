import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define the pattern
pattern = "110100011101010101011110000101100001010001010101110101011101010001010101010101110101010001010101"

# Define parameters
symbol_duration = 1e-3  # 1ms
rise_fall_time = 100e-6 # 100µs
symbol_1_level = 0.55   # 0.65V for '1'
symbol_0_level = 0.43   # 0.45V for '0'
sampling_rate = 1e6    # 10MHz for better resolution

# Generate time array
total_time = len(pattern) * symbol_duration
time = np.arange(0, total_time, 1/sampling_rate)

# Generate signal
signal = np.zeros_like(time)
current_time = 0
previous_level = symbol_0_level  # Start at the 0.45V level

for i, symbol in enumerate(pattern):
    if symbol == '1':
        level = symbol_1_level
    else:
        level = symbol_0_level

    start_idx = int(current_time * sampling_rate)
    end_idx = int((current_time + symbol_duration) * sampling_rate)
    rise_end_idx = int((current_time + rise_fall_time) * sampling_rate)
    fall_start_idx = int((current_time + symbol_duration - rise_fall_time) * sampling_rate)

    # Smooth transition from the previous level to the current level
    if previous_level != level:
        signal[start_idx:rise_end_idx] = np.linspace(previous_level, level, rise_end_idx - start_idx)
        signal[rise_end_idx:fall_start_idx] = level
        previous_level = level
    else:
        signal[start_idx:fall_start_idx] = level

    # Check if next symbol requires a transition and avoid spikes
    if i == len(pattern) - 1:
        # Last symbol handling
        signal[fall_start_idx:end_idx] = level
    elif pattern[i + 1] == symbol:
        signal[fall_start_idx:end_idx] = level
    else:
        next_level = symbol_1_level if pattern[i + 1] == '1' else symbol_0_level
        signal[fall_start_idx:end_idx] = np.linspace(level, next_level, end_idx - fall_start_idx)
        previous_level = next_level

    current_time += symbol_duration

# Save to CSV
df = pd.DataFrame({'Time (s)': time, 'Voltage (V)': signal})
df.to_csv('waveform.csv', index=False)

# Plot the signal
plt.figure(figsize=(12, 6))
plt.plot(time * 1e3, signal)  # Convert time to milliseconds for the X-axis
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title(f'Pattern "{pattern}" over Time')
plt.grid(True)
plt.show()
