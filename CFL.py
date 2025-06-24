import numpy as np
import matplotlib.pyplot as plt

# Gitter und Zeitparameter
L = 2 * np.pi
Nx = 50
x = np.linspace(0, L, Nx, endpoint=False)
dx = x[1] - x[0]
c = 1.0
dt = 1.5 * dx / c  # CFL > 1 -> instabil
lambda_cfl = c * dt / dx

# Initialwert: Sinus
u0 = np.sin(x)

# Exakte Lösung bei t=dt
u_exact = np.sin(x - c * dt)

# Numerisches Upwind-Schema
u_num = u0.copy()
u_num = u_num - lambda_cfl * (u_num - np.roll(u_num, 1))

# Plot
plt.figure(figsize=(8, 4))
plt.plot(x, u0, 'k--', label=r'$u(x, 0)$')
plt.plot(x, u_exact, 'g-', label=r'$u(x, t),\ \text{exakt}$')
plt.plot(x, u_num, 'ro-', label=r'$u(x, t),\ \text{numerisch (CFL} > 1)$')

plt.title(f'Upwind-Verfahren mit CFL = {lambda_cfl:.2f} > 1 (instabil)')
plt.xlabel('x')
plt.ylabel('u')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
