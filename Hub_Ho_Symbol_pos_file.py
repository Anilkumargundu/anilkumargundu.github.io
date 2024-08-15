import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Define the pattern
pattern = "01010101010101010101010101101100001000"


# Define parameters
symbol_duration = 1e-3  # 1ms
rise_fall_time = 100e-6 # 100µs
symbol_1_level = 0.55   # 0.55V for '1'
symbol_0_level = 0.43   # 0.43V for '0'
sampling_rate = 1e6     # 1MHz for better resolution
ringing_frequency = 10e3  # 10 kHz ringing frequency
ringing_amplitude = 0.014  # 5 mV amplitude of the ringing
damping_factor =6500     # Damping factor for the ringing


# Generate time array
total_time = len(pattern) * symbol_duration
time = np.arange(0, total_time, 1/sampling_rate)


# Initialize signals
signal_no_ringing = np.zeros_like(time)
signal_with_ringing = np.zeros_like(time)
current_time = 0
previous_level = symbol_0_level  # Start at the 0.43V level


for i, symbol in enumerate(pattern):
    if symbol == '1':
        level = symbol_1_level
    else:
        level = symbol_0_level


    start_idx = int(current_time * sampling_rate)
    end_idx = int((current_time + symbol_duration) * sampling_rate)
    rise_end_idx = int((current_time + rise_fall_time) * sampling_rate)
    fall_start_idx = int((current_time - rise_fall_time) * sampling_rate)


    # Transition with linear slope
    if previous_level != level:
        # Linear transition for signal without ringing
        transition_signal = np.linspace(previous_level, level, rise_end_idx - start_idx)
        signal_no_ringing[start_idx:rise_end_idx] = transition_signal
        signal_no_ringing[rise_end_idx:end_idx] = level  # Keep level after transition


        # Apply ringing at the end of the transition for signal with ringing
        if previous_level < level:  # Rising edge
            signal_with_ringing[start_idx:rise_end_idx] = transition_signal
            signal_with_ringing[rise_end_idx:end_idx] = level
            ringing_start_time = time[rise_end_idx]  # Start ringing after reaching 0.55V
            ringing_time = time[rise_end_idx:end_idx] - ringing_start_time
            ringing = ringing_amplitude * np.sin(2 * np.pi * ringing_frequency * ringing_time) * np.exp(-damping_factor * ringing_time)
            signal_with_ringing[rise_end_idx:end_idx] = level + ringing[:len(ringing)]
        else:  # Falling edge
            signal_with_ringing[start_idx:fall_start_idx] = level
            ringing_start_time1 = time[fall_start_idx]  # Start ringing after reaching 0.43V
            ringing_time1 = time[fall_start_idx:end_idx] - ringing_start_time1
            ringing1 = -ringing_amplitude * np.sin(2 * np.pi * ringing_frequency * ringing_time1) * np.exp(-damping_factor * ringing_time1)
            signal_with_ringing[fall_start_idx:end_idx] = level + ringing1[:len(ringing1)]
    else:
        # No transition, keep the level
        signal_no_ringing[start_idx:end_idx] = level
        signal_with_ringing[start_idx:end_idx] = level


    previous_level = level
    current_time += symbol_duration


# Save to CSV
df = pd.DataFrame({'Time (s)': time, 'Voltage (V) - No Ringing': signal_no_ringing, 'Voltage (V) - With Ringing': signal_with_ringing})
df.to_csv('waveform.csv', index=False)


# Plot the signal
plt.figure(figsize=(14, 6))


# Plot signal without ringing
plt.subplot(1, 2, 1)
plt.plot(time * 1e3, signal_no_ringing)  # Convert time to milliseconds for the X-axis
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Signal Without Ringing')
plt.grid(True)


# Plot signal with ringing
plt.subplot(1, 2, 2)
plt.plot(time * 1e3, signal_with_ringing)  # Convert time to milliseconds for the X-axis
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('Signal With Ringing')
plt.grid(True)


plt.tight_layout()
plt.show()