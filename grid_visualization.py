import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 5)
t = np.arange(0, 5)
x_half = np.arange(0.5, 5)
t_half = np.arange(0.5, 5)

X, T = np.meshgrid(x, t)
X_half, T_half = np.meshgrid(x_half, t_half)

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

axs[0].scatter(X, T, color='black')
axs[0].set_title('Standard-Gitter')
axs[0].set_xlabel('x')
axs[0].set_ylabel('t')
axs[0].set_aspect('equal')

axs[1].scatter(X_half, T_half, color='black', label='H-Feld')
axs[1].scatter(X, T, color='red', label='E-Feld')
axs[1].set_title('Yee-Gitter mit Versatz')
axs[1].set_xlabel('x')
axs[1].set_ylabel('t')
axs[1].set_aspect('equal')
axs[1].legend()

plt.tight_layout()
plt.show()
