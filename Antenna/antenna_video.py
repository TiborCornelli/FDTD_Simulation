import fdtd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fdtd.set_backend("numpy")

WAVELENGTH = 1550e-9
c = 3e8


def convert_measurements_to_numpy(measurements):
    return np.array([np.array(m) for m in measurements])


def main():
    grid = fdtd.Grid(
        shape=(25e-6, 15e-6, 1),
        grid_spacing=WAVELENGTH / 20,
    )

    x1_antenna, y1_antenna = 10e-6, 7.5e-6
    x2_antenna, y2_antenna = x1_antenna, y1_antenna + 3e-6
    grid[13e-6:18e-6, 5e-6:8e-6, 0] = fdtd.Object(permittivity=1.5**2)
    grid[x1_antenna:x2_antenna, y1_antenna:y2_antenna, 0] = fdtd.LineSource(
        name="antenna",
        period=WAVELENGTH / c,
        amplitude=1e-3,
    )
    grid[12e-6, :, 0] = fdtd.LineDetector(name="detector")
    detector_length_microns = grid.shape[1] * grid.grid_spacing * 1e6
    print(f"Detector length: {detector_length_microns:.2f} µm")

    grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
    grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
    # grid[0,:,:] = fdtd.PeriodicBoundary(name="xbounds")
    grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
    grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

    detector = grid.detector

    fig1 = plt.figure()

    def update_field(frame):
        grid.step()
        detector.detect_E()
        plt.clf()
        grid.visualize(z=0, animate=False, show=False)
        plt.gca().set_aspect("equal")
        plt.title("Electric Field Intensity")
        plt.xlabel("x (µm)")
        plt.ylabel("y (µm)")
        return plt.gcf().artists

    anim1 = animation.FuncAnimation(fig1, update_field, frames=400, blit=False)
    anim1.save("field_evolution.gif", writer="pillow", fps=10)
    plt.close(fig1)

    E_measurements = convert_measurements_to_numpy(detector.E)
    E_z = E_measurements[:, :, 2]
    x_positions = np.linspace(0, detector_length_microns, E_z.shape[1])

    fig2, ax = plt.subplots()
    (line,) = ax.plot([], [])
    ax.set_xlim(0, detector_length_microns)
    ax.set_ylim(np.min(E_z), np.max(E_z))
    ax.set_xlabel("Position along Detector Line (µm)")
    ax.set_ylabel("Ez")
    ax.set_title("Ez at Detector (Time Evolution)")

    def init():
        line.set_data([], [])
        return (line,)

    def update_ez(i):
        line.set_data(x_positions, E_z[i])
        return (line,)

    anim2 = animation.FuncAnimation(
        fig2, update_ez, frames=len(E_z), init_func=init, blit=True
    )
    anim2.save("ez_time_evolution.gif", writer="pillow", fps=10)
    plt.close(fig2)


if __name__ == "__main__":
    main()
