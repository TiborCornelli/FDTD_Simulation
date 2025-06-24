import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SIZE = 200
maxTime = 2500
imp0 = 377.0

ez = np.zeros(SIZE)
hy = np.zeros(SIZE)
ez_high = np.zeros(SIZE)
hy_high = np.zeros(SIZE)

cfl_low = 1.000    # Normale Courant-Zahl (stabil)
cfl_high = 1.001   # Größere Courant-Zahl (instabil)

def update_fields(ez, hy, cfl):
    hy[:-1] += cfl * (ez[1:] - ez[:-1]) / imp0
    ez[1:] += cfl * (hy[1:] - hy[:-1]) * imp0
    return ez, hy

fig, ax = plt.subplots()
(line_ez_low,) = ax.plot(ez, label="Ez CFL=1.0")
(line_hy_low,) = ax.plot(hy, label="Hy CFL=1.0")
(line_ez_high,) = ax.plot(ez_high, label="Ez CFL=1.5", linestyle="--")
(line_hy_high,) = ax.plot(hy_high, label="Hy CFL=1.5", linestyle="--")

ax.set_ylim(-3, 3)
ax.set_xlim(0, SIZE - 1)
ax.set_xlabel("Örtliche Koordinate (Index)")
ax.set_ylabel("Feldamplitude")
ax.set_title("1D FDTD Simulation mit verschiedenen Courant-Zahlen")
ax.legend(loc="upper right", fontsize=10, frameon=True)

def update(qTime):
    global ez, hy, ez_high, hy_high

    ez, hy = update_fields(ez, hy, cfl_low)
    ez[0] = np.exp(-((qTime - 30.0) ** 2) / 100.0)

    ez_high, hy_high = update_fields(ez_high, hy_high, cfl_high)
    ez_high[0] = np.exp(-((qTime - 30.0) ** 2) / 100.0)

    line_ez_low.set_ydata(ez)
    line_hy_low.set_ydata(hy * imp0)
    line_ez_high.set_ydata(ez_high)
    line_hy_high.set_ydata(hy_high * imp0)

    ax.set_title(f"1D FDTD Simulation — Zeitpunkt: {qTime}")
    return line_ez_low, line_hy_low, line_ez_high, line_hy_high

ani = animation.FuncAnimation(fig, update, frames=maxTime, interval=20, blit=False, repeat=False)
plt.show()
