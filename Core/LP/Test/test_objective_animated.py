from functools import partial

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")

zero = (.0, .0)
solution = (4., 2.)
direction = (solution[0] - zero[0], solution[1] - zero[1])

coeffs = (1., -1.)

distance = np.linalg.norm(direction)
step = 0.005
n = int(distance / step)

x = np.linspace(-5, 5, n)
fig, ax = plt.subplots()


def update(frame, ln):
    x0 = zero[0] + direction[0] / distance * (step * frame)
    y0 = zero[1] + direction[1] / distance * (step * frame)
    c = x0 * coeffs[0] + y0 * coeffs[1]
    y = (c - coeffs[0] * x) / coeffs[1]
    ln.set_data(x, y)

    return ln,


line1, = ax.plot([], [], linestyle='-')
ani = FuncAnimation(fig, partial(update, ln=line1), frames=n + 2, blit=True, repeat=True, interval=1)

ax.plot(zero[0], zero[1], marker='o')
ax.plot(solution[0], solution[1], marker='o')

ax.set_title('Title')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.grid()
plt.show()
