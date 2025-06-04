import fdtd
import matplotlib.pyplot as plt
import time
import numpy as np

fdtd.set_backend("numpy")

WAVELENGTH = 1550e-9
c = 3e8


def convert_measurements_to_numpy(measurements):
    """
    Convert FDTD measurements to a NumPy array.
    1st index: time step
    2nd index: position along the detector line
    3rd index: field component (Ex, Ey, Ez)
    """
    return np.array([np.array(m) for m in measurements])


def main():
    grid = fdtd.Grid(
        shape=(25e-6, 15e-6, 1),  # 25um x 15um x 1 (grid_spacing) --> 2D FDTD
        grid_spacing=WAVELENGTH / 20,  # 1um grid spacing
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
    detector_length_microns = (
        grid.shape[1] * grid.grid_spacing * 1e6
    )  # Convert to microns
    print(f"Detector length: {detector_length_microns:.2f} µm")

    grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
    grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

    # y boundaries
    # grid[:, 0, :] = fdtd.PeriodicBoundary(name="ybounds")
    grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
    grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

    detector = grid.detector

    for _ in range(100):
        grid.step()
        detector.detect_E()
        plt.clf()
        grid.visualize(z=0, animate=False, show=False)

        plt.gca().set_aspect("equal")
        plt.title("Electric Field Intensity")
        plt.xlabel("x (µm)")
        plt.ylabel("y (µm)")

        plt.pause(0.02)
        time.sleep(0.01)
    plt.ioff()

    E_measurements = convert_measurements_to_numpy(detector.E)
    E_z = E_measurements[:, :, 2]

    plt.figure()
    for E in E_z:
        plt.clf()
        plt.plot(np.linspace(0, detector_length_microns, len(E)), E)
        plt.title("Ez at Detector (Time Evolution)")
        plt.xlabel("Position along Detector Line (µm)")
        plt.ylabel("Ez")
        plt.ylim(np.min(E_z), np.max(E_z))
        plt.pause(0.05)
        time.sleep(0.01)

    plt.show()


if __name__ == "__main__":
    main()
