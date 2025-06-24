import numpy as np
import matplotlib.pyplot as plt

# Parameter
N = 8
L = 1.0
x = np.linspace(0, L, N, endpoint=False)
dx = L / N
dt = 0.4 * dx
c = 1.0
sigma = 0.1
x0 = 0.5
t = 0  # KEINE Verschiebung, nur Approximation sichtbar

# Anfangszustand
u0 = np.exp(-((x - x0) % L) ** 2 / sigma**2)

# Exakte Lösung (glatt)
x_fine = np.linspace(0, L, 1000)
u_exact = np.exp(-((x_fine - x0) % L) ** 2 / sigma**2)

# Euler-Approximation (eine Zeitschritt, keine Verschiebung)
def euler_step(u):
    dudx = (np.roll(u, -1) - np.roll(u, 1)) / (2 * dx)
    return u - c * dt * dudx

u1 = euler_step(u0)

# Plot
plt.figure(figsize=(8, 4))
plt.plot(x_fine, u_exact, 'k-', label='Exakte Lösung (glatt)')
plt.plot(x, u1, 'ro-', label='Numerisch (Euler, N=8)')
plt.xlabel("x")
plt.ylabel("Amplitude")
plt.title("Exakte vs. numerische Lösung nach einem Euler-Schritt")
plt.ylim(-0.2, 1.2)
plt.legend()
plt.grid(True)
plt.show()
