import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Physics calculations
def calculate_projectile_motion(v0, angle_deg):
    angle_rad = np.radians(angle_deg)
    g = 9.81
    t_flight = 2 * v0 * np.sin(angle_rad) / g
    t = np.linspace(0, t_flight, num=500)
    x = v0 * np.cos(angle_rad) * t
    y = v0 * np.sin(angle_rad) * t - 0.5 * g * t**2
    return x, y, t_flight

def calculate_free_fall(initial_height):
    g = 9.81
    t_fall = np.sqrt(2 * initial_height / g)
    t = np.linspace(0, t_fall, num=500)
    y = initial_height - 0.5 * g * t**2
    return t, y, t_fall

def calculate_linear_motion(v0, a, t):
    x = v0 * t + 0.5 * a * t**2
    return x

def calculate_cooling(temp_init, temp_env, k, duration):
    t = np.linspace(0, duration, num=500)
    temp = temp_env + (temp_init - temp_env) * np.exp(-k * t)
    return t, temp

# GUI setup
class PhysicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics Experiment Visualizer")

        # Experiment selection
        self.experiment_label = ttk.Label(root, text="Choose Experiment:")
        self.experiment_label.grid(column=0, row=0, padx=5, pady=5)

        self.experiment_choice = ttk.Combobox(root, values=["Projectile Motion", "Free Fall", "Linear Motion", "Cooling"])
        self.experiment_choice.grid(column=1, row=0, padx=5, pady=5)
        self.experiment_choice.set("Projectile Motion")
        self.experiment_choice.bind("<<ComboboxSelected>>", self.toggle_inputs)

        # Input fields
        self.inputs = {}
        self.create_input("Initial Velocity (m/s):", 'velocity', 1)
        self.create_input("Launch Angle (degrees):", 'angle', 2)
        self.create_input("Initial Height (m):", 'height', 3)
        self.create_input("Acceleration (m/s^2):", 'accel', 4)
        self.create_input("Initial Temp (C):", 'temp_init', 5)
        self.create_input("Ambient Temp (C):", 'temp_env', 6)
        self.create_input("Cooling Coefficient (k):", 'cool_k', 7)

        self.plot_button = ttk.Button(root, text="Simulate", command=self.plot_trajectory)
        self.plot_button.grid(column=0, row=8, columnspan=2, pady=10)

        self.figure = plt.Figure(figsize=(5.5, 4.5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

        self.toggle_inputs()

    def create_input(self, label, key, row):
        lbl = ttk.Label(self.root, text=label)
        ent = ttk.Entry(self.root)
        lbl.grid(column=0, row=row, padx=5, pady=2)
        ent.grid(column=1, row=row, padx=5, pady=2)
        self.inputs[key] = (lbl, ent)

    def toggle_inputs(self, *args):
        experiment = self.experiment_choice.get()
        # Hide all
        for lbl, ent in self.inputs.values():
            lbl.grid_remove()
            ent.grid_remove()

        # Show relevant ones
        if experiment == "Projectile Motion":
            for key in ['velocity', 'angle']:
                self.inputs[key][0].grid()
                self.inputs[key][1].grid()
        elif experiment == "Free Fall":
            self.inputs['height'][0].grid()
            self.inputs['height'][1].grid()
        elif experiment == "Linear Motion":
            for key in ['velocity', 'accel']:
                self.inputs[key][0].grid()
                self.inputs[key][1].grid()
        elif experiment == "Cooling":
            for key in ['temp_init', 'temp_env', 'cool_k']:
                self.inputs[key][0].grid()
                self.inputs[key][1].grid()

    def plot_trajectory(self):
        experiment = self.experiment_choice.get()
        self.ax.clear()

        try:
            if experiment == "Projectile Motion":
                v0 = float(self.inputs['velocity'][1].get())
                angle = float(self.inputs['angle'][1].get())
                x, y, t_flight = calculate_projectile_motion(v0, angle)
                self.animate_projectile(x, y)

            elif experiment == "Free Fall":
                h = float(self.inputs['height'][1].get())
                t, y, _ = calculate_free_fall(h)
                self.ax.plot(t, y, 'tab:orange')
                self.ax.set_title("Free Fall")
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Height (m)")

            elif experiment == "Linear Motion":
                v0 = float(self.inputs['velocity'][1].get())
                a = float(self.inputs['accel'][1].get())
                t = np.linspace(0, 10, 500)
                x = calculate_linear_motion(v0, a, t)
                self.ax.plot(t, x, 'tab:green')
                self.ax.set_title("Linear Motion")
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Distance (m)")

            elif experiment == "Cooling":
                temp_init = float(self.inputs['temp_init'][1].get())
                temp_env = float(self.inputs['temp_env'][1].get())
                k = float(self.inputs['cool_k'][1].get())
                t, temp = calculate_cooling(temp_init, temp_env, k, 30)
                self.ax.plot(t, temp, 'tab:purple')
                self.ax.set_title("Newton's Law of Cooling")
                self.ax.set_xlabel("Time (min)")
                self.ax.set_ylabel("Temperature (C)")

            self.ax.grid(True)
            self.canvas.draw_idle()

        except ValueError:
            self.ax.set_title("Invalid input. Please enter valid numbers.")
            self.canvas.draw_idle()

    def animate_projectile(self, x, y):
        self.ax.set_xlim(0, max(x)*1.1)
        self.ax.set_ylim(0, max(y)*1.1)
        self.ax.set_title("Projectile Motion")
        self.ax.set_xlabel("Distance (m)")
        self.ax.set_ylabel("Height (m)")
        self.ax.grid(True)

        point, = self.ax.plot([], [], 'ro', markersize=6)

        def init():
            point.set_data([], [])
            return point,

        def update(frame):
            point.set_data(x[frame], y[frame])
            return point,

        self.ani = FuncAnimation(self.figure, update, frames=len(x), init_func=init, interval=10, blit=False, repeat=False)
        self.canvas.draw_idle()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhysicsApp(root)
    root.mainloop()

