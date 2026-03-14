import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SIZE = 200
maxTime = 1000
imp0 = 377.0

ez = np.zeros(SIZE)
hy = np.zeros(SIZE)

fig, ax = plt.subplots()
(line_ez,) = ax.plot(ez, label="Ez (Elektrisches Feld)")
(line_hy,) = ax.plot(hy, label="Hy (Magnetisches Feld)")
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, SIZE - 1)

ax.set_xlabel("Örtliche Koordinate (Index)")
ax.set_ylabel("Feldamplitude")
ax.set_title("1D FDTD Simulation")
ax.legend(loc="upper right", fontsize=10, frameon=True)


def update(q):
    global ez, hy

    hy[:-1] += (ez[1:] - ez[:-1]) / imp0
    ez[1:] += (hy[1:] - hy[:-1]) * imp0
    ez[0] = np.exp(-((q - 30.0) ** 2) / 100.0)

    line_ez.set_ydata(ez)
    line_hy.set_ydata(hy * imp0)
    ax.set_title(f"1D FDTD Simulation — Zeitpunkt: {q}")
    return line_ez, line_hy


ani = animation.FuncAnimation(
    fig, update, frames=maxTime, interval=50, blit=False, repeat=False
)
# ani.save("fdtd_simulation.gif", writer="pillow", fps=20)
plt.show()

# ez[0] = np.sin(2 * np.pi * qTime / 100.0)  # Example source term
