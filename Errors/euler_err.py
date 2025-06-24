import numpy as np
import matplotlib.pyplot as plt

f0 = -1
x_max = 40 * np.pi

x_dense = np.linspace(0, x_max, 1000)
f_exact = -np.cos(x_dense)


def euler_integration(delta):
    x = np.arange(0, x_max + delta, delta)
    f = np.zeros_like(x)
    f[0] = f0
    for i in range(1, len(x)):
        f[i] = f[i - 1] + delta * np.sin(x[i - 1])
    return x, f


x_fine, f_fine = euler_integration(np.pi / 10)
x_alias1, f_alias1 = euler_integration(np.pi)
x_alias2, f_alias2 = euler_integration(3 * np.pi / 2)

plt.rcParams.update({"font.size": 16})
plt.figure(figsize=(12, 4))
plt.plot(x_dense, f_exact, "k", label="Analytisch")
plt.plot(x_fine, f_fine, "o-", label=r"Numerisch ($\delta = \pi/10$)", color="blue")
plt.title("Feines Gitter – gute Approximation")
plt.legend()
plt.grid()

plt.figure(figsize=(12, 4))
plt.plot(x_dense, f_exact, "k", label="Analytisch")
plt.plot(x_alias1, f_alias1, "o-", label=r"Numerisch ($\delta = \pi$)", color="red")
plt.title("Aliasing – konstante numerische Lösung")
plt.legend()
plt.grid()

plt.figure(figsize=(12, 4))
plt.plot(x_dense, f_exact, "k", label="Analytisch")
plt.plot(
    x_alias2, f_alias2, "o-", label=r"Numerisch ($\delta = 3\pi/2$)", color="green"
)
plt.title("Aliasing – numerische Lösung mit niederfrequenter Schwingung")
plt.legend()
plt.grid()

plt.show()
