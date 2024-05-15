# import math
# from functools import partial
#
# import matplotlib
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation
# from matplotlib.axes import Axes
# from matplotlib.patches import Polygon
#
# from Core.LP.Runtime.LpProblemData import LpProblemData, ABS_TOL
#
# AXIS_X_LABEL_NAME = 'x'
# AXIS_Y_LABEL_NAME = 'y'
#
# AXIS_WIDTH = 1.
# AXIS_COLOR = 'black'
# AXIS_LINESTYLE = '-'
#
# GRID_WIDTH = 0.25
# GRID_LINESTYLE = '--'
# GRID_COLOR = 'gray'
#
# ODR_POLYGON_COLOR = 'blue'
# ODR_POLYGON_ALPHA = .2
#
# LINES_WIDTH = 0.75
# LINES_LINESTYLE = '-'
# LINES_COLOR = 'black'
#
# OPTIMAL_SOLUTION_COLOR = 'red'
#
# POINT_MARKER = 'o'
#
#
# def get_default_plot(problem: LpProblemData):
#     x_lim = [-5., 5.]
#     y_lim = [-5., 5.]
#
#     var_consrts_s = problem.get_var_consrts_s()
#
#     if var_consrts_s[0] == '>=':
#         x_lim[0] = -1.
#         y_lim[0] = -1.
#         inters = np.array([(.0, .0), (.0, y_lim[1]), (x_lim[1], .0), (x_lim[1], y_lim[1])])
#     else:
#         x_lim[1] = 1.
#         y_lim[1] = 1.
#         inters = np.array([(.0, .0), (.0, y_lim[0]), (x_lim[0], .0), (x_lim[0], y_lim[0])])
#
#     fig, ax = plt.subplots()
#
#     polygon_data = sort_polygon_points(inters)
#     points = polygon_data[1]
#     polygon = Polygon(points, alpha=ODR_POLYGON_ALPHA, color=ODR_POLYGON_COLOR)
#     ax.add_patch(polygon)
#
#     ax.set_xlim(x_lim[0], x_lim[1])
#     ax.set_ylim(y_lim[0], y_lim[1])
#
#     add_default_patches(ax)
#
#     return fig, ax
#
#
# def get_sequence_solution_plots(problem: LpProblemData):
#     plots = []
#
#     n = len(problem.get_consrts_c())
#     for i in range(n):
#         fig, ax = get_sequence_solution_plot(i, problem)
#         plots.append((fig, ax))
#
#     return plots
#
#
# def get_sequence_solution_plot(i: int, problem: LpProblemData):
#     fig, ax = plt.subplots()
#
#     consrts_c = problem.get_consrts_c()
#     consrts_s = problem.get_consrts_s()
#
#     var_consrts0_c = problem.get_var_consrts_c()
#     var_consrts0_s = problem.get_var_consrts_s()
#
#     rhs_c = var_consrts0_c + consrts_c[0:i + 1]
#     rhs_s = var_consrts0_s + consrts_s[0:i + 1]
#
#     lhs_c = consrts_c[i:i + 1]
#
#     inters0 = find_intersections_between(rhs_c + lhs_c)
#
#     x_lim = [np.min(inters0[:, 0]), np.max(inters0[:, 0])]
#     y_lim = [np.min(inters0[:, 1]), np.max(inters0[:, 1])]
#
#     offset = 2.
#     if var_consrts0_s[0] == '>=':
#         x_lim[0] -= offset
#         y_lim[0] -= offset
#         x_lim[1] += offset
#         y_lim[1] += offset
#         var_consrts1_c = [(1., .0, x_lim[1]), (0., 1., y_lim[1])]
#         inters1 = np.array([[0., y_lim[1]], [x_lim[1], .0], [x_lim[1], y_lim[1]]])
#         var_consrts1_s = ['<=', '<=']
#     else:
#         y_lim[0] -= offset
#         x_lim[0] -= offset
#         x_lim[1] += offset
#         y_lim[1] += offset
#         var_consrts1_c = [(1., .0, x_lim[0]), (0., 1., y_lim[0])]
#         inters1 = np.array([[0., y_lim[0]], [x_lim[0], .0], [x_lim[0], y_lim[0]]])
#         var_consrts1_s = ['>=', '>=']
#
#     inters2 = find_intersections_with(lhs_c, var_consrts1_c)
#
#     all_inters = np.concatenate((inters0, inters1, inters2, np.array([[.0, .0]])), axis=0)
#     all_inters = unique_points(all_inters)
#
#     var_consrts_c = var_consrts0_c + var_consrts1_c
#     var_consrts_s = var_consrts0_s + var_consrts1_s
#     inters_b = not_satisfy_constraints(all_inters, var_consrts_c, var_consrts_s)
#
#     odr_pols = find_odr_polygons(inters_b, rhs_c, rhs_s)
#     sorted_odr_pols = sort_polygons_points(odr_pols)
#     for pol_data in sorted_odr_pols:
#         points = pol_data[1]
#         polygon = Polygon(points, alpha=ODR_POLYGON_ALPHA, color=ODR_POLYGON_COLOR)
#         ax.add_patch(polygon)
#         ax.scatter(points[:, 0], points[:, 1], marker=POINT_MARKER, color=ODR_POLYGON_COLOR)
#
#     x = np.linspace(x_lim[0], x_lim[1], 2)
#     for i, (a, b, c) in enumerate(rhs_c[2:]):
#         if b != 0:
#             y = (c - a * x) / b
#             ax.plot(x, y, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
#         else:
#             x_vert = c / a
#             ax.axvline(x=x_vert, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
#
#     add_default_patches(ax)
#
#     return fig, ax
#
#
# def get_last_sequence_solution_plot_animated(problem: LpProblemData, solve_result):
#     objv_c = problem.get_objv_c()
#
#     dir_to = (objv_c[0], objv_c[1])
#     dir_to_magnitude = np.linalg.norm(dir_to)
#     dir_to_norm = dir_to / dir_to_magnitude
#
#     last_solution_i = len(problem.get_consrts_c()) - 1
#     fig, ax = get_sequence_solution_plot(last_solution_i, problem)
#
#     ax.quiver(.0, .0, dir_to_norm[0], dir_to_norm[1], scale=1, scale_units='xy', angles='xy',
#               color=OPTIMAL_SOLUTION_COLOR)
#
#     step = 0.005
#     n = int(dir_to_magnitude / step)
#     x_lim = ax.get_xlim()
#     x = np.linspace(x_lim[0], x_lim[1], n)
#
#     optimal_p = solve_result.x
#     ax.scatter(optimal_p[0], optimal_p[1], color=OPTIMAL_SOLUTION_COLOR, marker=POINT_MARKER)
#
#     c = optimal_p[0] * objv_c[0] + optimal_p[1] * objv_c[1]
#     y = (c - objv_c[0] * x) / objv_c[1]
#     ax.plot(x, y, color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
#
#     def update(frame):
#         x0 = optimal_p[0] / dir_to_magnitude * (step * frame)
#         y0 = optimal_p[1] / dir_to_magnitude * (step * frame)
#         c = x0 * objv_c[0] + y0 * objv_c[1]
#         y = (c - objv_c[0] * x) / objv_c[1]
#         line.set_data(x, y)
#
#         return line,
#
#     line, = ax.plot([], [], color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
#     ani = FuncAnimation(fig, update, frames=n, blit=True, repeat=True, interval=10)
#
#     return fig, ax, ani
#
#
# def add_default_patches(ax: Axes):
#     ax.axhline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)
#     ax.axvline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)
#
#     ax.set_xlabel(AXIS_X_LABEL_NAME)
#     ax.set_ylabel(AXIS_Y_LABEL_NAME)
#
#     ax.grid(color=GRID_COLOR, linestyle=GRID_LINESTYLE, linewidth=GRID_WIDTH)
#
#
# def is_satisfy_inequality(x01, a, b, c, sign):
#     value = a * x01[0] + b * x01[1]
#     if sign == '<=':
#         return math.isclose(value, c, abs_tol=ABS_TOL) or value < c
#     elif sign == '>=':
#         return math.isclose(value, c, abs_tol=ABS_TOL) or value > c
#     else:
#         return math.isclose(value, c, abs_tol=ABS_TOL)
#
#
# def not_satisfy_constraints(points, constraints, signs):
#     results = []
#
#     for point in points:
#         valid = True
#         for i, (a0, b0, c0) in enumerate(constraints):
#             if not is_satisfy_inequality(point, a0, b0, c0, signs[i]):
#                 valid = False
#                 break
#
#         if valid:
#             results.append(point)
#
#     return np.array(results)
#
#
# def find_intersections(lhs, rhs):
#     a0, b0, c0 = lhs
#     a1, b1, c1 = rhs
#     a = np.array([[a0, b0], [a1, b1]])
#     b = np.array([c0, c1])
#     try:
#         return np.linalg.solve(a, b)
#     except np.linalg.LinAlgError:
#         return None
#
#
# def find_intersections_with(lines0, lines1):
#     results = []
#
#     for line0 in lines0:
#         for line1 in lines1:
#             intersection = find_intersections(line0, line1)
#             if intersection is None or contains_point(intersection, results):
#                 continue
#
#             results.append(intersection)
#
#     return np.array(results)
#
#
# def find_intersections_between(lines):
#     results = []
#
#     for i, line0 in enumerate(lines):
#         for j, line1 in enumerate(lines[i + 1:], start=i + 1):
#             intersection = find_intersections(line0, line1)
#             if intersection is None or contains_point(intersection, results):
#                 continue
#
#             results.append(intersection)
#
#     return np.array(results)
#
#
# def find_odr_polygons(points, coeffs, signs):
#     results = []
#
#     a = np.ones(points.shape[0], dtype=bool)
#     for i, (a0, b0, c0) in enumerate(coeffs):
#         b = []
#         for point in points:
#             b.append(is_satisfy_inequality(point, a0, b0, c0, signs[i]))
#
#         compatibility = np.logical_and(a, b)
#         if np.any(compatibility):
#             a = compatibility
#         else:
#             polygon = points[np.where(a)[0]]
#             if polygon.size != 0:
#                 results.append(polygon)
#
#             a = np.array(b)
#
#     results.append(points[np.where(a)[0]])
#
#     return results
#
#
# def sort_polygon_points(points):
#     centroid = np.mean(points, axis=0)
#     angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
#     sorted_points = points[np.argsort(angles)]
#
#     return centroid, np.vstack([sorted_points, sorted_points[0]])
#
#
# def sort_polygons_points(polygons):
#     results = []
#
#     for points in polygons:
#         results.append(sort_polygon_points(points))
#
#     return results
#
#
# def unique_points(points):
#     results = []
#     for point in points:
#         if not contains_point(point, results):
#             results.append(point)
#
#     return np.array(results)
#
#
# def contains_point(lhs, points):
#     for rhs in points:
#         if math.isclose(lhs[0], rhs[0], abs_tol=ABS_TOL) and math.isclose(lhs[1], rhs[1], abs_tol=ABS_TOL):
#             return True
#
#     return False
