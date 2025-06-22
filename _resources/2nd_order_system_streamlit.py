import streamlit as st
import numpy as np
import math
from scipy.signal import TransferFunction, step, tf2zpk, bode
import plotly.graph_objs as go
import plotly.subplots as sp

# Streamlit inputs
st.title("Second-Order System Analyzer")

K = st.number_input("DC Gain (K)", value=1000)
omega_0 = st.number_input("Natural Frequency ω₀ (rad/s)", value=2 * math.pi * 1000)
zeta = st.slider("Damping Ratio ζ", min_value=0.0, max_value=2.0, value=0.5, step=0.05)

st.markdown("### Legend")
st.markdown("""
- <span style="color:green">■</span> **Input Signal**  
- <span style="color:blue">■</span> **Step Response**  
- <span style="color:red">●</span> **Poles**  
- <span style="color:orange">■</span> **Magnitude (dB)**  
- <span style="color:purple">■</span> **Phase (°)**  
""", unsafe_allow_html=True)

# Define the system
numerator = [K * omega_0**2]
denominator = [1, 2 * zeta * omega_0, omega_0**2]
system = TransferFunction(numerator, denominator)

# Step response
time, response = step(system)
input_signal = np.ones_like(time)
input_signal[0] = 0

# Poles and zeros
zeros, poles, _ = tf2zpk(numerator, denominator)
pole_frequencies = np.abs(poles) / (2 * np.pi)

# Bode plot
frequencies = np.logspace(1, 12, 1000)
w, mag, phase = bode(system, frequencies)
cutoff_idx = np.where(mag <= max(mag) - 3)[0][0]
cutoff_frequency = w[cutoff_idx] / (2 * np.pi)

freq_range = (w[cutoff_idx:cutoff_idx + 50] / (2 * np.pi))
mag_range = mag[cutoff_idx:cutoff_idx + 50]
slope = (mag_range[-1] - mag_range[0]) / (np.log10(freq_range[-1]) - np.log10(freq_range[0]))

# Create 2x2 subplots
fig = sp.make_subplots(rows=2, cols=2, subplot_titles=(
    "Input Step Signal", "Step Response",
    "Poles in Complex Plane", "Frequency Response (Bode)"
))

# Plot 1: Input signal
fig.add_trace(go.Scatter(x=time, y=input_signal, mode='lines', name='Input Signal', line=dict(color='green')),
              row=1, col=1)

# Plot 2: Step response
fig.add_trace(go.Scatter(x=time, y=response, mode='lines', name='Step Response', line=dict(color='blue')),
              row=1, col=2)

# Plot 3: Poles
fig.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode='markers',
                         marker=dict(color='red', size=10), name='Poles'), row=2, col=1)

# Plot 4: Bode plot
freqs_Hz = w / (2 * np.pi)
fig.add_trace(go.Scatter(x=freqs_Hz, y=mag, mode='lines', name='Magnitude (dB)', line=dict(color='orange')),
              row=2, col=2)
fig.add_trace(go.Scatter(x=freqs_Hz, y=phase, mode='lines', name='Phase (°)', line=dict(color='purple')),
              row=2, col=2)

# Annotations
fig.add_trace(go.Scatter(
    x=[cutoff_frequency],
    y=[mag[cutoff_idx]],
    mode="markers+text",
    text=[f"Cutoff: {cutoff_frequency:.2e} Hz"],
    textposition="top right",
    marker=dict(color="blue", size=8)
), row=2, col=2)

# Axis labels
fig.update_xaxes(title_text="Time (s)", row=1, col=1)
fig.update_yaxes(title_text="Amplitude", row=1, col=1)

fig.update_xaxes(title_text="Time (s)", row=1, col=2)
fig.update_yaxes(title_text="Amplitude", row=1, col=2)

fig.update_xaxes(title_text="Real Part", row=2, col=1)
fig.update_yaxes(title_text="Imaginary Part", row=2, col=1)

fig.update_xaxes(title_text="Frequency (Hz)", type="log", row=2, col=2)
fig.update_yaxes(title_text="Magnitude (dB) / Phase (°)", row=2, col=2)

fig.update_layout(height=800, width=1000, showlegend=True)


