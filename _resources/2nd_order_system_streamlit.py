# app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.signal import TransferFunction, step, tf2zpk, bode

# Streamlit inputs
st.title("Second-Order System Analyzer")

K = st.number_input("DC Gain (K)", value=1000)
omega_0 = st.number_input("Natural Frequency ω₀ (rad/s)", value=2 * math.pi * 1000)
zeta = st.slider("Damping Ratio ζ", min_value=0.0, max_value=2.0, value=0.5, step=0.05)

# Transfer function
numerator = [K * omega_0**2]
denominator = [1, 2 * zeta * omega_0, omega_0**2]
system = TransferFunction(numerator, denominator)

# Step response
time, response = step(system)

# Input signal
input_signal = np.ones_like(time)
input_signal[0] = 0

# Zeros and poles
zeros, poles, _ = tf2zpk(numerator, denominator)

# Bode plot
frequencies = np.logspace(1, 12, 1000)
w, mag, phase = bode(system, frequencies)
cutoff_idx = np.where(mag <= max(mag) - 3)[0][0]
cutoff_frequency = w[cutoff_idx] / (2 * np.pi)

freq_range = (w[cutoff_idx:cutoff_idx + 50] / (2 * np.pi))
mag_range = mag[cutoff_idx:cutoff_idx + 50]
slope = (mag_range[-1] - mag_range[0]) / (np.log10(freq_range[-1]) - np.log10(freq_range[0]))
pole_frequencies = np.abs(poles) / (2 * np.pi)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Input signal
axs[0, 0].plot(time, input_signal, label='Input Signal', color='g')
axs[0, 0].set_title("Input Step Signal")
axs[0, 0].grid(True)

# Step response
axs[0, 1].plot(time, response, label='Response', color='b')
axs[0, 1].set_title("Step Response")
axs[0, 1].grid(True)

# Pole plot
axs[1, 0].plot(np.real(poles), np.imag(poles), 'rx', label='Poles', markersize=10)
axs[1, 0].axhline(0, color='black', lw=0.5)
axs[1, 0].axvline(0, color='black', lw=0.5)
axs[1, 0].set_title("Poles in Complex Plane")
axs[1, 0].grid(True)

# Bode plot
axs[1, 1].semilogx(w / (2 * np.pi), mag, label='Magnitude (dB)', color='orange')
axs[1, 1].semilogx(w / (2 * np.pi), phase, label='Phase (°)', color='purple')
axs[1, 1].set_title("Frequency Response")
axs[1, 1].grid(True)

for freq in pole_frequencies:
    axs[1, 1].plot(freq, np.interp(freq, w / (2 * np.pi), mag), 'o', color='red')

axs[1, 1].text(1e7, max(mag) - 10, f'Cutoff: {cutoff_frequency:.2e} Hz', color='blue')
axs[1, 1].text(1e8, max(mag) - 20, f'Slope: {slope:.2f} dB/dec', color='red')

plt.tight_layout()
st.pyplot(fig)
