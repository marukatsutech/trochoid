# Trochoid, cycloid
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import matplotlib.patches as patches


def update_arm():
    global x_arm, y_arm, line_arm, circle_arm
    x_arm = p0[0] + r_arm * np.cos(theta0)
    y_arm = p0[1] + r_arm * np.sin(theta0)
    line_arm.set_data([p0[0], x_arm], [p0[1], y_arm])
    circle_arm.set_center([x_arm, y_arm])


def reset():
    global cnt, is_running, x_curve, y_curve, curve, p0, theta0, circle0
    cnt = 0
    is_running = False
    x_curve.clear()
    y_curve.clear()
    curve.set_data(x_curve, y_curve)
    p0[0] = p0_x_init
    theta0 = theta0_init
    circle0.set_center(p0)
    update_arm()


def change_arm(value):
    global r_arm
    r_arm = float(value)
    update_arm()


def switch():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True


def update(f):
    global cnt, theta0, p0, x_arm, y_arm, curve, circle0, circle_arm, x_curve, y_curve, curve
    if is_running:
        tx_step.set_text(' Step=' + str(cnt))
        th = - cnt / 10.
        theta0 = (theta0_init + th) % (2 * np.pi)
        p0_x = p0_x_init - r0 * th
        p0 = [p0_x, r0]
        circle0.set_center(p0)
        x_arm = p0[0] + r_arm * np.cos(theta0)
        y_arm = p0[1] + r_arm * np.sin(theta0)
        line_arm.set_data([p0[0], x_arm], [p0[1], y_arm])
        circle_arm.set_center([x_arm, y_arm])
        x_curve.append(x_arm)
        y_curve.append(y_arm)
        curve.set_data(x_curve, y_curve)
        cnt += 1
        if p0_x > x_max:
            cnt = 0
            x_curve.clear()
            y_curve.clear()


# Global variables
is_running = False

x_min = -1.
x_max = 20.
y_min = -4.
y_max = 6.

cnt = 0

num_of_points = 500

r0 = 1.
r_arm = r0
p0_x_init = 0.
p0 = np.array([p0_x_init, r0])
theta0_init = - np.pi / 2.
theta0 = theta0_init

p1 = np.array([0., 0.])

x_curve = []
y_curve = []

# Generate figure and axes
fig = Figure()
ax1 = fig.add_subplot(111)
ax1.grid()
ax1.set_title('Trochoid, cycloid')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
ax1.set_aspect("equal")

# Generate items
tx_step = ax1.text(x_min, y_max * 0.9, " Step=" + str(0))
line_g, = ax1.plot([x_min, x_max], [0., 0.])
circle0 = patches.Circle(xy=p0, radius=r0, fill=False, color='blue')
ax1.add_patch(circle0)

x_arm = p0[0] + np.cos(theta0)
y_arm = p0[1] + np.sin(theta0)
line_arm, = ax1.plot([p0[0], x_arm], [p0[1], y_arm], color='blue')

circle_arm = patches.Circle(xy=p1, radius=r0*0.08, color='blue')
ax1.add_patch(circle_arm)

curve, = ax1.plot(x_curve, y_curve)

# Embed in Tkinter
root = tk.Tk()
root.title("Trochoid, cycloid")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

label_arm = tk.Label(root, text="Length of arm")
label_arm.pack(side='left')
var_arm = tk.StringVar(root)  # variable for spinbox-value
var_arm.set(r_arm)  # Initial value
s_arm = tk.Spinbox(
    root, textvariable=var_arm, format="%.1f", from_=0.1, to=4, increment=0.1,
    command=lambda: change_arm(var_arm.get()), width=5
    )
s_arm.pack(side='left')

btn = tk.Button(root, text="Play/Pause", command=switch)
btn.pack(side='left')

btn = tk.Button(root, text="Reset", command=reset)
btn.pack(side='left')

# main loop
anim = animation.FuncAnimation(fig, update, interval=50)
root.mainloop()

