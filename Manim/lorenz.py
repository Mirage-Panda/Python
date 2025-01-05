import numpy as np
from manim import *
from scipy.integrate import solve_ivp


# Define the Lorenz system
def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):  # rho=28
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


# Solve the Lorenz system
# If rtol = 1e-6 and the current value being solved is x = 10, the acceptable error is approximately 10 * 1e-6 = 1e-5.
# If atol = 1e-9, any error less than this value is acceptable regardless of the magnitude of the solution.
def generate_lorenz_points(starting_state, t_max=10, dt=0.01):
    t_values = np.arange(0, t_max, dt)
    solution = solve_ivp(
        lorenz_system,
        t_span=(0, t_max),
        y0=starting_state,
        t_eval=t_values,
        rtol=1e-8,
        atol=1e-10,
    )
    return np.array(solution.y).T  # Transpose to get (x, y, z) points


class LorenzAttractor(ThreeDScene):  # Use ThreeDScene for 3D rotations

    def construct(self):
        # Time for evolution
        evolution_time = 10
        # Generate points
        starting_state = [10, 10, 10]
        points = generate_lorenz_points(starting_state, t_max=evolution_time)

        # Set up axes
        axes = ThreeDAxes(
            x_range=[-50, 50, 5],
            y_range=[-50, 50, 5],
            z_range=[0, 50, 5],
            axis_config={"color": GRAY, "stroke_width": 2},
        )

        # Create a path for the attractor
        attractor_path = VMobject(color=BLUE, stroke_width=2)
        attractor_path.set_points_smoothly([axes.c2p(*point) for point in points])

        # Add axes to the scene
        self.add(axes)

        # Add rotation to the camera during the attractor animation
        self.move_camera(
            phi=60 * DEGREES,  # Initial elevation angle
            theta=-45 * DEGREES,  # Initial azimuth angle
            zoom=0.75,
            frame_center=(0, 0, 2),
        )
        self.begin_ambient_camera_rotation(rate=0.05)  # Slow continuous rotation

        # Animate the attractor
        self.play(Create(attractor_path), run_time=evolution_time, rate_func=linear)

        # Animation finished indicator
        self.wait(0.5)
        attractor_path.set_color(GREEN)

        # Speed up camera
        self.stop_ambient_camera_rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(0.1)
        self.move_camera(
            zoom=1,
            frame_center=(0, 0, 3),
        )

        # Wait to observe the rotation
        self.wait(10)
