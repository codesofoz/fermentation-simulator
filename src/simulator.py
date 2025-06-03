import numpy as np

class BioethanolSimulator:
    # Kinetic and process parameters (literature-based)
    Ks = 1.0                     # g/LAdd commentMore actions
    Ksi = 50.0                   # g/L
    Yxs = 0.5                    # g biomass/g glucose
    Yps = 0.48                   # g ethanol/g glucose
    mu_max_base = 0.4            # 1/h
    P_max = 90.0                 # g/L
    ethanol_density = 0.789      # g/mL = 789 g/L
    cost_per_liter = 5.00        # $ per liter ethanol produced

    def run_simulation(self, inputs):
        S0, V, X0, N, t = (
            inputs['S0'], inputs['V'], inputs['X0'], inputs['N'], inputs['t']
        )

        if any(val <= 0 for val in [S0, V, X0, N, t]):
            raise ValueError("All input parameters must be greater than 0.")

        mu_max = self.mu_max_base * (N / 400) ** 0.6

        time_points = np.linspace(0, t, int(t * 10) + 1)
        X_total_t = np.zeros_like(time_points)
        S_total_t = np.zeros_like(time_points)
        P_total_t = np.zeros_like(time_points)
        X_total_t[0] = X0 * V
        S_total_t[0] = S0 * V
        P_total_t[0] = 0.0

        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            X_total = X_total_t[i-1]
            S_total = S_total_t[i-1]
            P_total = P_total_t[i-1]
            S = S_total / V
            P = P_total / V

            substrate_inhibition = 1 / (1 + (S / self.Ksi))
            ethanol_inhibition = max(0, 1 - (P / self.P_max))
            mu = mu_max * (S / (self.Ks + S)) * substrate_inhibition * ethanol_inhibition

            dX_total_dt = mu * X_total
            dS_total_dt = -(1 / self.Yxs) * dX_total_dt
            dP_total_dt = -self.Yps * dS_total_dt

            if S_total + dS_total_dt * dt < 0:
                dS_total_dt = -S_total / dt
                dX_total_dt = self.Yxs * -dS_total_dt
                dP_total_dt = self.Yps * -dS_total_dt

            X_total_t[i] = max(X_total + dX_total_dt * dt, 0)
            S_total_t[i] = max(S_total + dS_total_dt * dt, 0)
            P_total_t[i] = max(P_total + dP_total_dt * dt, 0)

        X_final = X_total_t[-1] / V
        S_final = S_total_t[-1] / V
        P_final = P_total_t[-1] / V

        P_total_g = P_final * V
        P_total_L = P_total_g / (self.ethanol_density * 1000)

        # Total cost is now only based on total ethanol produced
        total_cost = self.cost_per_liter * P_total_L

        return {
            'time': time_points,
            'X': X_final,
            'S': S_final,
            'P': P_final,
            'X_series': X_total_t / V,
            'S_series': S_total_t / V,
            'P_series': P_total_t / V,
            'P_total_g': P_total_g,
            'P_total_L': P_total_L,
            'total_cost': total_cost
        }
