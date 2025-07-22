# model_powerlaw.py
import numpy as np
from scipy.optimize import curve_fit

def power_law_model(gamma_dot, k, n):
    return k * gamma_dot ** n

def fit_power_law(shear_rates, shear_stresses, flow_rate, diameter, density):
    try:
        popt, _ = curve_fit(power_law_model, shear_rates, shear_stresses, bounds=(0, np.inf))
        k, n = popt
        predictions = power_law_model(np.array(shear_rates), k, n)
        ss_res = np.sum((shear_stresses - predictions) ** 2)
        ss_tot = np.sum((shear_stresses - np.mean(shear_stresses)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

        mean_gamma = np.mean(shear_rates)
        mu_app = k * mean_gamma ** (n - 1)

        # Power Law Reynolds number formula
        re = (8 * density * flow_rate) / (np.pi * diameter * mu_app)

        return {
            "k": k,
            "n": n,
            "r2": r2,
            "mu_app": mu_app,
            "re": re,
            "equation": f"τ = {k:.4f}·γ̇^{n:.4f}"
        }
    except Exception as e:
        return {"error": str(e)}

