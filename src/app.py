import streamlit as st
import matplotlib.pyplot as plt
from simulator import BioethanolSimulator

def main():
    st.set_page_config(layout="wide", page_title="Bioethanol Fermentation Simulator")
    st.title("Bioethanol Fermentation Simulator")

    col1, col2 = st.columns(2)

    with col1:
        S0 = st.number_input(
            "Initial Substrate (S₀, g/L):",
            min_value=50.0,
            max_value=200.0,
            value=50.0,
            step=1.0,
        )
        st.caption("Range: 50 to 200 g/L")

        V = st.number_input(
            "Broth Volume (V, L):",
            min_value=1.0,
            max_value=500.0,
            value=100.0,
            step=1.0,
        )
        st.caption("Range: 10 to 500 L")

        X0 = st.number_input(
            "Initial Biomass (X₀, g/L):",
            min_value=0.1,
            max_value=15.0,
            value=1.0,
            step=0.1,
        )
        st.caption("Range: 0.1 to 15.0 g/L")

    with col2:
        N = st.number_input(
            "Impeller Speed (N, rpm):",
            min_value=100,
            max_value=400,
            value=300,
            step=10,
        )
        st.caption("Range: 100 to 400 rpm")

        t = st.number_input(
            "Fermentation Time (t, hrs):",
            min_value=12,
            max_value=120,
            value=72,
            step=1,
        )
        st.caption("Range: 12 to 120 hours")

    if st.button("Run Simulation"):
        if S0 <= 0 or V <= 0 or X0 <= 0 or N <= 0 or t <= 0:
            st.error("All input parameters must be greater than 0.")
            return

        with st.spinner("Running simulation..."):
            inputs = {
                'S0': S0,
                'V': V,
                'X0': X0,
                'N': N,
                't': t
            }
            simulator = BioethanolSimulator()
            results = simulator.run_simulation(inputs)

            st.subheader("Simulation Results")
            st.markdown(f"""
                - **Final Biomass (X):** {results['X']:.2f} g/L
                - **Final Substrate (S):** {results['S']:.2f} g/L  
                - **Ethanol Concentration (P):** {results['P']:.2f} g/L
                - **Total Ethanol Produced:** {results['P_total_L']:.2f} L
                - **Total Cost:** ${results['total_cost']:.2f}
                """)

            # Create plots with a dark theme
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), facecolor='#1e1e1e')
            fig.patch.set_alpha(1.0)

            ax1.set_facecolor('#2e2e2e')
            ax1.plot(results['time'], results['X_series'], 'limegreen', label='Biomass (X)', linewidth=2)
            ax1.plot(results['time'], results['S_series'], 'dodgerblue', label='Substrate (S)', linewidth=2)
            ax1.set_ylabel('Concentration (g/L)', color='white')
            ax1.tick_params(axis='both', colors='white')
            ax1.legend(facecolor='#2e2e2e', edgecolor='white', labelcolor='white')
            ax1.grid(True, linestyle='--', alpha=0.3, color='gray')
            ax1.set_xlim(left=0)
            ax1.set_ylim(bottom=0)

            ax2.set_facecolor('#2e2e2e')
            ax2.plot(results['time'], results['P_series'], 'orangered', label='Ethanol (P)', linewidth=2)
            ax2.set_xlabel('Time (hours)', color='white')
            ax2.set_ylabel('Ethanol (g/L)', color='white')
            ax2.tick_params(axis='both', colors='white')
            ax2.legend(facecolor='#2e2e2e', edgecolor='white', labelcolor='white')
            ax2.grid(True, linestyle='--', alpha=0.3, color='gray')
            ax2.set_xlim(left=0)
            ax2.set_ylim(bottom=0)

            st.pyplot(fig)

if __name__ == "__main__":
    main()
