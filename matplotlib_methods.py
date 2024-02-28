import matplotlib.pyplot as plt
import numpy as np
from ortools.linear_solver import pywraplp
import matplotlib.patches as mpatches


def draw2d(data, status, x_values, optimum, solver):
    obj_coeffs = data['obj_coeffs']
    constraint_coeffs = data['constraint_coeffs']
    signs = data['signs']
    bounds = data['bounds']

    size = 200
    x_range = np.linspace(0, max(bounds), size)

    patches = []

    x_min = x_max = y_min = y_max = 0
    num_coeffs = len(constraint_coeffs)
    for i in range(num_coeffs):
        bound = bounds[i]
        coeffs = constraint_coeffs[i]

        y_range = (bound - np.dot(coeffs[0], x_range)) / coeffs[1]
        label = f'C[%d] ' % i + convert2label(coeffs, signs[i], bound)
        line = plt.plot(x_range, y_range, linestyle=':', label=label)
        patches.append(line[0])

        line_color = line[0].get_color()
        x_point, y_point = get_bound(coeffs[0], coeffs[1], bound)
        plt.plot(x_point, y_point, marker='o', linestyle=':', color=line_color)

        if x_point[0] < x_min:
            x_min = x_point[0]
        elif x_point[0] > x_max:
            x_max = x_point[0]

        if y_point[1] < y_min:
            y_min = y_point[1]
        elif y_point[1] > y_max:
            y_max = y_point[1]

    zero_point = [0, 0]
    marker = plt.plot(zero_point[0], zero_point[1], marker='o')
    marker_color = marker[0].get_color()
    plt.annotate(
        "(0;0)",
        xy=(zero_point[0], zero_point[1]),
        textcoords="offset points",
        xytext=(-5, -10),
        ha='right',
        color=marker_color
    )

    polygons = []
    x, y = np.meshgrid(x_range, x_range)
    constraints = np.ones_like(x, dtype=bool)
    for i in range(num_coeffs):
        bound = bounds[i]
        coeffs = constraint_coeffs[i]
        constraint = np.ones_like(x, dtype=bool)
        if signs[i] == '>=':
            constraint &= coeffs[0] * x + coeffs[1] * y >= bound
        elif signs[i] == '<=':
            constraint &= coeffs[0] * x + coeffs[1] * y <= bound
        else:
            constraint &= coeffs[0] * x + coeffs[1] * y == bound

        temp_constraints = np.logical_and(constraints, constraint)
        if np.any(temp_constraints):
            constraints = temp_constraints
        else:
            polygons.append(constraints)
            constraints = constraint

        if i == num_coeffs - 1:
            polygons.append(constraints)

    for i in range(len(polygons)):
        plt.imshow(
            polygons[i].astype(int),
            extent=(x.min(), x.max(), y.min(), y.max()),
            origin='lower',
            cmap='Grays',
            alpha=0.3,
            label='Feasible Region',
        )

    if status == pywraplp.Solver.OPTIMAL:
        y_range = (optimum - obj_coeffs[0] * x_range) / obj_coeffs[1]
        label = 'Obj: ' + convert2label(obj_coeffs, '=', optimum)
        line = plt.plot(x_range, y_range, label=label, linestyle='-')
        patches.append(line[0])
        line_color = line[0].get_color()

        for i in range(len(x_values)):
            point = x_values[i]
            plt.plot(point[0], point[1], marker='o', linestyle=':', color=line_color)
            plt.annotate(
                f'Optimal point: ({point[0]};{point[1]})\nValue:{optimum:0.2f}',
                xy=(point[0], point[1]),
                xytext=(point[0] + 0.15, point[1] + 0.15),
                ha='left'
            )

    x_max = abs(y_min) if abs(y_min) > x_max else x_max
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    plt.axhline(0, color='black', linewidth=1, linestyle=':')
    plt.axvline(0, color='black', linewidth=1, linestyle=':')
    plt.grid(color='gray', linestyle='--', linewidth=0.25)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Graphical method of solving the linear programming problem')

    if len(polygons) > 0:
        fr_patch = mpatches.Patch(color='gray', label='Feasible region')
        patches.append(fr_patch)

    plt.legend(loc='best', handles=patches)

    plt.show()


def convert2label(coeffs, sign, bound):
    label = ''
    for j in range(len(coeffs)):
        if j > 0:
            label += '*'
        label += f'{coeffs[j]:0.2f}x%d' % j
    label += sign + f'{bound:0.2f}'

    return label


def get_bound(x1, x2, limit):
    x_1 = [limit / x1, 0.0]
    x_2 = [0.0, limit / x2]
    return x_1, x_2
