import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SIZE = 200
maxTime = 2500
imp0 = 377.0

ez = np.zeros(SIZE)
hy = np.zeros(SIZE)

fig, ax = plt.subplots()
(line_ez,) = ax.plot(ez, label="Ez (Electric Field)")
(line_hy,) = ax.plot(hy, label="Hy (Magnetic Field)")
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, SIZE - 1)

ax.set_xlabel("Spatial Position (grid index)")
ax.set_ylabel("Field Amplitude")
ax.set_title("1D FDTD Simulation")
ax.legend(loc="upper right", fontsize=10, frameon=True)

def update(qTime):
    global ez, hy

    hy[:-1] += (ez[1:] - ez[:-1]) / imp0
    ez[1:] += (hy[1:] - hy[:-1]) * imp0
    ez[0] = np.exp(-((qTime - 30.0) ** 2) / 100.0)

    line_ez.set_ydata(ez)
    line_hy.set_ydata(hy * imp0)
    ax.set_title(f"1D FDTD Simulation — Time Step: {qTime}")
    return line_ez, line_hy

ani = animation.FuncAnimation(
    fig, update, frames=maxTime, interval=50, blit=True, repeat=False
)
plt.show()
