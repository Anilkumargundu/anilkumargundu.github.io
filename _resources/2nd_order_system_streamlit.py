import streamlit as st
import numpy as np
import math
from scipy.signal import TransferFunction, step, tf2zpk, bode
import plotly.graph_objs as go
import plotly.subplots as sp

# Title and user inputs
st.markdown("""
### From Oscillations to Stability: The Influence of Damping   
<sub>Adjust the damping factor (or Q-factor) and visually explore how it influences the transient response, magnitude response, and the pole locations of a second-order system. </sub>

**Transfer Function**  
H(s) = K·ω₀² / (s² + 2·ζ·ω₀·s + ω₀²)
""", unsafe_allow_html=True)



K = st.number_input("DC Gain (K)", value=1000)
omega_0 = st.number_input("Natural Frequency ω₀ (rad/s)", value=2 * math.pi * 1000)
zeta = st.slider("Damping Ratio ζ", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

try:
    # Transfer function
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
    fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=("Input Step Signal", "Step Response", "Poles", "Bode Plot")
    )

    # Plot traces
    fig.add_trace(go.Scatter(x=time, y=input_signal, name="Input Signal", line=dict(color="green")), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=response, name="Step Response", line=dict(color="blue")), row=1, col=2)
    fig.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode="markers", name="Poles", marker=dict(size=10, color='red')), row=2, col=1)

    freqs_Hz = w / (2 * np.pi)
    fig.add_trace(go.Scatter(x=freqs_Hz, y=mag, name="Magnitude (dB)", line=dict(color='orange')), row=2, col=2)
    fig.add_trace(go.Scatter(x=freqs_Hz, y=phase, name="Phase (°)", line=dict(color='purple')), row=2, col=2)

    fig.add_trace(go.Scatter(
        x=[cutoff_frequency], y=[mag[cutoff_idx]],
        mode="markers+text",
        text=[f"Cutoff: {cutoff_frequency:.2e} Hz"],
        textposition="top right",
        marker=dict(size=8, color='blue')
    ), row=2, col=2)

    # Axis labels and enhancements
    for row in range(1, 3):
        for col in range(1, 3):
            fig.update_xaxes(
                showline=True, linewidth=2, linecolor='black',
                showgrid=True, zeroline=True, zerolinewidth=1, zerolinecolor='gray',
                row=row, col=col
            )
            fig.update_yaxes(
                showline=True, linewidth=2, linecolor='black',
                showgrid=True, zeroline=True, zerolinewidth=1, zerolinecolor='gray',
                row=row, col=col
            )

    # Individual axis titles
    fig.update_xaxes(title_text="Time (s)", row=1, col=1)
    fig.update_yaxes(title_text="Amplitude", row=1, col=1)
    fig.update_xaxes(title_text="Time (s)", row=1, col=2)
    fig.update_yaxes(title_text="Amplitude", row=1, col=2)
    fig.update_xaxes(title_text="Real Part", row=2, col=1)
    fig.update_yaxes(title_text="Imaginary Part", row=2, col=1)
    fig.update_xaxes(title_text="Frequency (Hz)", type="log", row=2, col=2)
    fig.update_yaxes(title_text="Magnitude / Phase", row=2, col=2)

    # Layout settings
    fig.update_layout(
        height=850, width=1100,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.25,
            xanchor="center", x=0.5
        ),
        margin=dict(t=80, b=100),
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ An error occurred: {e}")

st.markdown(
    """
    <hr style="margin-top: 3em; margin-bottom: 0.5em">
    <div style='text-align: center; font-size: 1em; color: black;'>
        © 2025 Anil Kumar Gundu | 
        <a href="https://anilkumargundu.github.io" target="_blank">navigate to my website</a>
    </div>
    """,
    unsafe_allow_html=True)

