import math
from functools import partial

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from Core.Helper.lp_bank import *
from Core.Helper.lp_helper import solve_lp

# matplotlib.use('TkAgg')


def unique_points(points):
    results = []
    for point in points:
        if not contains_point(point, results):
            results.append(point)

    return np.array(results)


def contains_point(lhs, points):
    for rhs in points:
        if math.isclose(lhs[0], rhs[0], abs_tol=1e-10) and math.isclose(lhs[1], rhs[1], abs_tol=1e-10):
            return True

    return False


def is_satisfy_inequality(x01, a, b, c, sign):
    value = a * x01[0] + b * x01[1]
    if sign == '<=':
        return math.isclose(value, c, abs_tol=1e-10) or value < c
    elif sign == '>=':
        return math.isclose(value, c, abs_tol=1e-10) or value > c
    else:
        return math.isclose(value, c, abs_tol=1e-10)


def find_intersections_between(lines):
    results = []

    for i, line0 in enumerate(lines):
        for j, line1 in enumerate(lines[i + 1:], start=i + 1):
            intersection = find_intersections(line0, line1)
            if intersection is None or contains_point(intersection, results):
                continue

            results.append(intersection)

    return np.array(results)


def not_satisfy_constraints(points, constraints, signs):
    results = []

    for point in points:
        valid = True
        for i, (a0, b0, c0) in enumerate(constraints):
            if not is_satisfy_inequality(point, a0, b0, c0, signs[i]):
                valid = False
                break

        if valid:
            results.append(point)

    return np.array(results)


def find_intersections_with(lines0, lines1):
    results = []

    for line0 in lines0:
        for line1 in lines1:
            intersection = find_intersections(line0, line1)
            if intersection is None or contains_point(intersection, results):
                continue

            results.append(intersection)

    return np.array(results)


def find_intersections(lhs, rhs):
    a0, b0, c0 = lhs
    a1, b1, c1 = rhs
    a = np.array([[a0, b0], [a1, b1]])
    b = np.array([c0, c1])
    try:
        return np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        return None


def find_odr_polygons(points, coeffs, signs):
    results = []

    a = np.ones(points.shape[0], dtype=bool)
    for i, (a0, b0, c0) in enumerate(coeffs):
        b = []
        for point in points:
            b.append(is_satisfy_inequality(point, a0, b0, c0, signs[i]))

        compatibility = np.logical_and(a, b)
        if np.any(compatibility):
            a = compatibility
        else:
            polygon = points[np.where(a)[0]]
            if polygon.size != 0:
                results.append(polygon)

            a = np.array(b)

    results.append(points[np.where(a)[0]])

    return results


def sort_polygon_points(points):
    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    sorted_points = points[np.argsort(angles)]

    return centroid, np.vstack([sorted_points, sorted_points[0]])


def sort_polygons_points(polygons):
    results = []

    for points in polygons:
        results.append(sort_polygon_points(points))

    return results


if __name__ == "__main__":
    problem = problem1
    result = solve_lp(problem)

    zero = (.0, .0)

    objv = problem['objective']
    objv_g = objv['goal']
    objv_c = objv['coefficients']

    consrts = problem['constraints']
    consrts_c = consrts['coefficients']
    consrts_s = consrts['signs']

    var_consrts0 = problem['vars_constraints']
    var_consrts0_c = var_consrts0['coefficients']
    var_consrts0_s = var_consrts0['signs']

    fig, ax = plt.subplots()
    ax.scatter(zero[0], zero[1], marker='o', color='b')
    ax.axhline(0, color='black', linewidth=1, linestyle='-')
    ax.axvline(0, color='black', linewidth=1, linestyle='-')

    x_lim = [-5., 5.]
    y_lim = [-5., 5.]

    if var_consrts0_s[0] == '>=':
        x_lim[0] = -1.
        y_lim[0] = -1.
        var_consrts1_c = [(1., .0, x_lim[1]), (0., 1., y_lim[1])]
        var_consrts1_s = ['<=', '<=']
        inters0 = np.array([zero, (.0, y_lim[1]), (x_lim[1], .0), (x_lim[1], y_lim[1])])
    else:
        x_lim[1] = 1.
        y_lim[1] = 1.
        var_consrts1_c = [(1., .0, x_lim[0]), (0., 1., y_lim[0])]
        var_consrts1_s = ['>=', '>=']
        inters0 = np.array([zero, (.0, y_lim[0]), (x_lim[0], .0), (x_lim[0], y_lim[0])])

    iteration = 0
    pol_data = sort_polygons_points(np.array([inters0]))[0]
    points = pol_data[1]
    polygon = Polygon(points, alpha=0.2)
    ax.add_patch(polygon)

    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylim(y_lim[0], y_lim[1])
    ax.set_title(f'Iteration - {iteration}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(color='gray', linestyle='--', linewidth=0.25)
    plt.show()
    iteration += 1

    rhs_c = []
    rhs_c.extend(var_consrts0_c)
    rhs_s = []
    rhs_s.extend(var_consrts0_s)
    n = len(consrts_c)
    for i in range(n):
        lhs = consrts_c[i]

        fig, ax = plt.subplots()
        ax.axhline(0, color='black', linewidth=1, linestyle='-')
        ax.axvline(0, color='black', linewidth=1, linestyle='-')

        inters0 = find_intersections_between(rhs_c + [lhs])
        x_lim = [np.min(inters0[:, 0]), np.max(inters0[:, 0])]
        y_lim = [np.min(inters0[:, 1]), np.max(inters0[:, 1])]

        offset = 2.
        if var_consrts0_s[0] == '>=':
            x_lim[0] -= offset
            y_lim[0] -= offset
            x_lim[1] += offset
            y_lim[1] += offset
            var_consrts1_c = [(1., .0, x_lim[1]), (0., 1., y_lim[1])]
            inters1 = np.array([[0., y_lim[1]], [x_lim[1], .0], [x_lim[1], y_lim[1]]])
        else:
            y_lim[0] -= offset
            x_lim[0] -= offset
            x_lim[1] += offset
            y_lim[1] += offset
            var_consrts1_c = [(1., .0, x_lim[0]), (0., 1., y_lim[0])]
            inters1 = np.array([[0., y_lim[0]], [x_lim[0], .0], [x_lim[0], y_lim[0]]])

        inters2 = find_intersections_with([lhs], var_consrts1_c)

        all_inters = np.concatenate((inters0, inters1, inters2, np.array([zero])), axis=0)
        all_inters = unique_points(all_inters)
        var_consrts_c = var_consrts0_c + var_consrts1_c
        var_consrts_s = var_consrts0_s + var_consrts1_s
        inters_b = not_satisfy_constraints(all_inters, var_consrts_c, var_consrts_s)

        rhs_c.append(lhs)
        rhs_s.append(consrts_s[i])
        odr_pols = find_odr_polygons(inters_b, rhs_c, rhs_s)
        sorted_odr_pols = sort_polygons_points(odr_pols)
        for pol_data in sorted_odr_pols:
            points = pol_data[1]
            polygon = Polygon(points, alpha=0.2)
            ax.add_patch(polygon)
            ax.scatter(points[:, 0], points[:, 1], marker='o', color='b')

        x = np.linspace(x_lim[0], x_lim[1], 10)
        for i, (a, b, c) in enumerate(rhs_c[2:]):
            if b != 0:
                y = (c - a * x) / b
                ax.plot(x, y, color='black', linewidth=0.75, linestyle='-')
            else:
                x_vert = c / a
                ax.axvline(x=x_vert, color='black', linewidth=0.75, linestyle='-')

        ax.set_xlim(x_lim[0], x_lim[1])
        ax.set_ylim(y_lim[0], y_lim[1])
        ax.set_title(f'Iteration - {iteration}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(color='gray', linestyle='--', linewidth=0.25)
        plt.show()
        iteration += 1



    fig1, ax1 = plt.subplots()

    ax1.axhline(0, color='black', linewidth=1, linestyle='-')
    ax1.axvline(0, color='black', linewidth=1, linestyle='-')

    lines = ax.get_lines()
    for line in lines:
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        label = line.get_label()
        color = line.get_color()
        linestyle = line.get_linestyle()
        linewidth = line.get_linewidth()
        ax1.plot(x_data, y_data, label=label, color=color, linestyle=linestyle, linewidth=linewidth)

    for pol_data in sorted_odr_pols:
        points = pol_data[1]
        polygon = Polygon(points, alpha=0.2)
        ax1.add_patch(polygon)
        ax1.scatter(points[:, 0], points[:, 1], marker='o', color='b')

    dir_to = (objv_c[0] - zero[0], objv_c[1] - zero[1])
    dir_to_magnitude = np.linalg.norm(dir_to)
    dir_to_norm = dir_to / dir_to_magnitude
    plt.quiver(zero[0], zero[1], dir_to_norm[0], dir_to_norm[1], scale=1, scale_units='xy', angles='xy', color='r')

    step = 0.005
    n = int(dir_to_magnitude / step)
    x = np.linspace(x_lim[0], x_lim[1], n)

    optimal_p = result.x
    ax1.scatter(optimal_p[0], optimal_p[1], color='red', marker='o')

    a, b = objv_c
    c = optimal_p[0] * objv_c[0] + optimal_p[1] * objv_c[1]
    y = (c - objv_c[0] * x) / objv_c[1]
    ax1.plot(x, y, color='red', linewidth=0.75, linestyle='-')


    def update(frame, ln):
        x0 = zero[0] + optimal_p[0] / dir_to_magnitude * (step * frame)
        y0 = zero[1] + optimal_p[1] / dir_to_magnitude * (step * frame)
        c = x0 * objv_c[0] + y0 * objv_c[1]
        y = (c - objv_c[0] * x) / objv_c[1]
        ln.set_data(x, y)
        return ln,


    line, = ax1.plot([], [], color='red', linewidth=0.75, linestyle='-')
    args = partial(update, ln=line)
    ani = FuncAnimation(fig, args, frames=n, blit=True, repeat=True, interval=1)

    ax1.set_xlim(x_lim[0], x_lim[1])
    ax1.set_ylim(y_lim[0], y_lim[1])
    ax1.set_title(f'Iteration - {iteration}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(color='gray', linestyle='--', linewidth=0.25)
    plt.show()
    iteration += 1
