import math

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

data0 = {
    'constraints': {
        'coefficients': [
            (3, 5, 30),
            (4, -3, 12),
            (1, -3, 6)
        ],
        'signs': ['<=', '<=', '>=']
    }
}

data1 = {
    'constraints': {
        'coefficients': [
            (2, 2, 5),
            (3, -1, 6),
            (1, 2, 2)
        ],
        'signs': ['>=', '>=', '<=']
    }
}

data2 = {
    'constraints': {
        'coefficients': [
            (1, 1, 7),
            (0, 1, 5),
            (1, 1, 3),
            (0, 1, 2),
            (1, 0, 4),
        ],
        'signs': ['<=', '<=', '>=', '>=', '<=']
    }
}

data3 = {
    'constraints': {
        'coefficients': [
            (1, 5, 10),
            (3, -1, 6),
        ],
        'signs': ['<=', '<=']
    }
}


def unique_points(points):
    results = []
    for point in points:
        if not contains_point(point, results):
            results.append(point)

    return np.array(results)


def contains_point(lhs, points):
    for rhs in points:
        if math.isclose(lhs[0], rhs[0]) and math.isclose(lhs[1], rhs[1]):
            return True

    return False


def find_intersections_between(lines):
    results = []

    for i, (a0, b0, c0) in enumerate(lines):
        for j, (a1, b1, c1) in enumerate(lines[i + 1:], start=i + 1):
            a = np.array([[a0, b0], [a1, b1]])
            b = np.array([c0, c1])

            try:
                intersection = np.linalg.solve(a, b)
                if not contains_point(intersection, results):
                    results.append(intersection)
            except np.linalg.LinAlgError:
                continue

    return np.array(results)


def find_intersections_with(lines0, lines1):
    results = []

    for i, (a0, b0, c0) in enumerate(lines0):
        for j, (a1, b1, c1) in enumerate(lines1):
            a = np.array([[a0, b0], [a1, b1]])
            b = np.array([c0, c1])

            try:
                intersection = np.linalg.solve(a, b)
                if not contains_point(intersection, results):
                    results.append(intersection)
            except np.linalg.LinAlgError:
                continue

    return np.array(results)


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


def is_satisfy_inequality(x01, a, b, c, sign):
    value = a * x01[0] + b * x01[1]
    if sign == '<=':
        return math.isclose(value, c, abs_tol=1e-10) or value < c
    elif sign == '>=':
        return math.isclose(value, c, abs_tol=1e-10) or value > c
    else:
        return math.isclose(value, c, abs_tol=1e-10)


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


def sort_polygon_points(polygons):
    results = []

    for points in polygons:
        centroid = np.mean(points, axis=0)
        angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
        sorted_points = points[np.argsort(angles)]
        results.append((centroid, np.vstack([sorted_points, sorted_points[0]])))

    return results


def draw_polygons_test(polygons, title):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    for polygon in polygons:
        centroid = polygon[0]
        points = polygon[1]
        polygon = Polygon(points)
        ax.add_patch(polygon)
        ax.plot(centroid[0], centroid[1], marker='o', color='red')

    plt.grid()
    plt.show()


def draw_intersections_and_lines_test(lines, intersections, title):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    x_min, x_max = np.min(intersections[:, 0]), np.max(intersections[:, 0])
    y_min, y_max = np.min(intersections[:, 1]), np.max(intersections[:, 1])
    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)
    x = np.linspace(x_min - 1, x_max + 1, 10)
    for i, (a, b, c) in enumerate(lines):
        if b != 0:
            y = (c - a * x) / b
            ax.plot(x, y, linestyle=':')
        else:
            x_vert = c / a
            ax.axvline(x=x_vert, linestyle=':')

    for x0, y0 in intersections:
        ax.plot(x0, y0, marker='o')

    ax.grid()
    plt.show()


def draw_intersections_and_lines_and_polygons_test(lines, intersections, polygons, title=''):
    x_min, x_max = np.min(intersections[:, 0]), np.max(intersections[:, 0])
    y_min, y_max = np.min(intersections[:, 1]), np.max(intersections[:, 1])

    fig, ax = plt.subplots()
    x = np.linspace(x_min - 1, x_max + 1, 10)
    for i, (a, b, c) in enumerate(lines):
        if b != 0:
            y = (c - a * x) / b
            ax.plot(x, y, linestyle=':')
        else:
            x_vert = c / a
            ax.axvline(x=x_vert, linestyle=':')

    for x0, y0 in intersections:
        ax.plot(x0, y0, marker='o')

    for polygon in polygons:
        centroid = polygon[0]
        points = polygon[1]
        polygon = Polygon(points)
        ax.add_patch(polygon)
        ax.plot(centroid[0], centroid[1], marker='o')

    ax.set_title(title)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(x_min - 1, x_max + 1)
    ax.set_ylim(y_min - 1, y_max + 1)

    ax.grid()
    plt.show()


data = data2

constraints = data['constraints']['coefficients']
signs = data['constraints']['signs']
c_intersections = find_intersections_between(constraints)
draw_intersections_and_lines_test(constraints, c_intersections, 'constraints vs constraints')

var_constraints0 = [
    (0, 1, 0),
    (1, 0, 0)
]
var_signs0 = ['>=', '>=']
v0_intersections = find_intersections_with(constraints, var_constraints0)
draw_intersections_and_lines_test(var_constraints0, v0_intersections, 'constraints vs v0_constraints')

c_intersections = np.concatenate((c_intersections, [[.0, .0]]), axis=0)
intersections = np.concatenate((c_intersections, v0_intersections), axis=0)

x_min, x_max = np.min(intersections[:, 0]), np.max(intersections[:, 0])
y_min, y_max = np.min(intersections[:, 1]), np.max(intersections[:, 1])

var_constraints1 = [
    (0, 1, y_max),
    (1, 0, x_max)
]
var_signs1 = ['<=', '<=']
v1_intersections = find_intersections_with(constraints, var_constraints1)
draw_intersections_and_lines_test(var_constraints1, v1_intersections, 'constraints vs v1_constraints')

v1_intersections = np.concatenate((v1_intersections, [[0., y_max], [x_max, .0], [x_max, y_max]]), axis=0)

all_intersections = np.concatenate((c_intersections, v0_intersections, v1_intersections), axis=0)
all_intersections = unique_points(all_intersections)
all_constraints = constraints + var_constraints0 + var_constraints1
draw_intersections_and_lines_test(all_constraints, all_intersections,
                                  'constraints vs constraints & v0_constraints & v1_constraints')

var_constraints = var_constraints0 + var_constraints1
var_signs = var_signs0 + var_signs1
boundary_points = not_satisfy_constraints(all_intersections, var_constraints, var_signs)
draw_intersections_and_lines_test(constraints, boundary_points, 'constraints vs boundary box')

odr_polygons = find_odr_polygons(boundary_points, constraints, signs)
sorted_odr_polygons = sort_polygon_points(odr_polygons)
draw_polygons_test(sorted_odr_polygons, 'polygons')

draw_intersections_and_lines_and_polygons_test(constraints, boundary_points, sorted_odr_polygons)

g = 1
