import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameter
SIZE = 200
L = 1.0
dx = L / SIZE
x = np.linspace(0, L, SIZE, endpoint=False)

c = 1.0
dt = 0.4 * dx / c  # CFL-konform
maxTime = 600
sigma = 0.05
x0 = 0.25

# Anfangszustand
u = np.exp(-((x - x0) ** 2) / sigma**2)


# Exakte Lösung
def exact_solution(x, t):
    pos = (x - x0 - c * t) % L
    # Summe über mehrere "Perioden" für besseren periodischen Peak
    res = np.zeros_like(x)
    for shift in (-L, 0, L):
        res += np.exp(-((pos - shift) ** 2) / sigma**2)
    return res


fig, ax = plt.subplots()
(line_num,) = ax.plot(x, u, label="Numerisch")
(line_ex,) = ax.plot(x, exact_solution(x, 0), "--k", label="Exakt")
(line_err,) = ax.plot(x, u - exact_solution(x, 0), "r", label="Fehler")
ax.set_ylim(-0.2, 1.2)
ax.set_xlim(0, L)
ax.set_xlabel("x")
ax.set_ylabel("Amplitude")
ax.set_title("Fehlerentwicklung bei Advektion (Lax-Friedrichs)")
ax.legend()


# Lax-Friedrichs Scheme (periodisch)
def lax_friedrichs(u):
    u_right = np.roll(u, -1)
    u_left = np.roll(u, 1)
    return 0.5 * (u_right + u_left) - 0.5 * c * dt / dx * (u_right - u_left)


# Animation Update
def update(n):
    global u
    u = lax_friedrichs(u)
    t = n * dt
    u_ex = exact_solution(x, t)
    line_num.set_ydata(u)
    line_ex.set_ydata(u_ex)
    line_err.set_ydata(u - u_ex)
    ax.set_title(f"Zeit t = {t:.3f}")
    return line_num, line_ex, line_err


ani = animation.FuncAnimation(
    fig, update, frames=maxTime, interval=50, blit=False, repeat=False
)
plt.show()
