import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10 * np.pi, 1000)
f = np.sin(x)
g = -np.sin(1 / 3 * x)

# Vielfache von 3/2 pi
x_marks = np.arange(0, 10 * np.pi, 1.5 * np.pi)
y_marks = np.sin(x_marks)  # f(x) == g(x) an diesen Stellen

# Set size of text
plt.rcParams.update({'font.size': 14})
plt.figure(figsize=(12, 6))
plt.plot(x, f, label=r"$f(x) = \sin(x)$", color="blue")
plt.plot(x, g, label=r"$g(x) = -\sin\left(\frac{1}{3}x\right)$", color="orange")
plt.plot(x_marks, y_marks, "ro", label="Gitterpunkte")

# Beschriftung an x-Achse
xticks = x_marks
xtick_labels = [f"{int(n)}·3/2π" if n > 0 else "0" for n in range(len(x_marks))]
plt.xticks(xticks, xtick_labels)

plt.title("Aliasing-Effekt bei Abtastung")
plt.xlabel("x")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
