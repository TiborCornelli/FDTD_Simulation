import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SIZE = 200
maxTime = 10000
imp0 = 377.0

ez = np.zeros(SIZE)
hy = np.zeros(SIZE)

ez_right_old = 0.0
ez_right_prev = 0.0

fig, ax = plt.subplots()
(line,) = ax.plot(ez)
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, SIZE - 1)

ax.set_xlabel("Spatial Position (grid index)")
ax.set_ylabel("Electric Field Ez")
title_text = ax.set_title("1D FDTD Simulation")  # save title artist


def update(qTime):
    global ez, hy, ez_right_old, ez_right_prev

    hy[:-1] += (ez[1:] - ez[:-1]) / imp0
    ez[1:] += (hy[1:] - hy[:-1]) * imp0

    ez[0] = np.exp(-((qTime - 30.0) ** 2) / 100.0)

    ez[-1] = ez_right_prev + ((imp0 - 1) / (imp0 + 1)) * (ez[-2] - ez_right_old)
    ez_right_prev = ez[-1]
    ez_right_old = ez[-2]

    line.set_ydata(ez)
    title_text.set_text(f"1D FDTD Simulation — Time Step: {qTime}")
    return line, title_text  # return both artists for blitting


ani = animation.FuncAnimation(
    fig, update, frames=maxTime, interval=50, blit=False, repeat=False
)
plt.show()
