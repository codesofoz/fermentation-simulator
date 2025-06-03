# 🧬 Bioethanol Fermentation Simulator

![Bioethanol Fermentation Simulator](FS.jpg)

A scientific simulation tool that models the **bioethanol fermentation process**, helping researchers and students understand the relationship between input parameters and ethanol production.

## 🌟 Features

- **🎛️ Interactive Simulation** – Adjust fermentation parameters and see real-time results.
- **📊 Visual Analytics** – Clear graphs showing biomass growth, substrate consumption, and ethanol production.
- **💰 Cost Analysis** – Estimates production costs per gram of ethanol.
- **🔬 Scientific Accuracy** – Based on established biochemical models:
  - Monod Equation
  - Luedeking-Piret Model

## 🧪 How It Works

The simulator calculates ethanol production through **10 key biochemical steps**:

1. Calculates microorganism growth rate based on impeller speed.
2. Determines substrate consumption using Monod kinetics.
3. Models ethanol production with Luedeking-Piret equations.
4. Computes final ethanol concentration and yield.
5. Estimates production costs.
6. Adjusts biomass growth based on time and nutrients.
7. Considers oxygen transfer and agitation rate effects.
8. Simulates product inhibition and saturation kinetics.
9. Analyzes energy inputs based on impeller speed.
10. Outputs visual and numeric results for interpretation.

---

## 🚀 Getting Started

To run the simulation:

```bash
streamlit run app.py

