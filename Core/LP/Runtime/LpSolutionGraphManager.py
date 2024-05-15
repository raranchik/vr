import math
import numpy as np

from matplotlib.patches import Patch
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.patches import Polygon

from Core.Helper.math_helper import ABS_TOL
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.LP.Runtime.LpSolutionGraphAnimatedData import LpSolutionGraphAnimatedData
from Core.LP.Runtime.LpSolutionGraphData import LpSolutionGraphData

AXIS_X_LABEL_NAME = 'x'
AXIS_Y_LABEL_NAME = 'y'

AXIS_WIDTH = 1.
AXIS_COLOR = 'black'
AXIS_LINESTYLE = '-'

GRID_WIDTH = 0.25
GRID_LINESTYLE = '--'
GRID_COLOR = 'gray'

ODR_POLYGON_COLOR = 'blue'
ODR_POLYGON_ALPHA = .2

LINES_WIDTH = 0.75
LINES_LINESTYLE = '-'
LINES_COLOR = 'black'

OPTIMAL_SOLUTION_COLOR = 'red'

ODR_POINT_MARKER = 'o'


class LpSolutionGraphManager:
    def __init__(self, problem: LpProblemData, solve_result, controller):
        self.problem = problem
        self.solve_result = solve_result
        self.controller = controller
        self.cache: dict = {}

    def create_default_plot(self):
        if 'default' in self.cache:
            return self.__recreate_default_plot()

        zero = (.0, .0)

        x_lim = [-5., 5.]
        y_lim = [-5., 5.]

        var_consrts_s = self.problem.get_var_consrts_s()

        if var_consrts_s[0] == '>=':
            x_lim[0] = -1.
            y_lim[0] = -1.
            inters = np.array([zero, (.0, y_lim[1]), (x_lim[1], .0), (x_lim[1], y_lim[1])])
        else:
            x_lim[1] = 1.
            y_lim[1] = 1.
            inters = np.array([zero, (.0, y_lim[0]), (x_lim[0], .0), (x_lim[0], y_lim[0])])

        odr_polygons = self.__find_odr_polygons(inters, self.problem.get_var_consrts_c(), var_consrts_s)
        polygons_datas = self.__sort_polygons_points(odr_polygons)

        odr_points = np.array([zero])

        legend_handles = [Patch(color=ODR_POLYGON_COLOR, label='Область допустимых решений')]

        fig, ax = self.__create_plot(x_lim, y_lim, polygons_datas, odr_points, {})
        self.__create_legend(ax, legend_handles)

        self.cache['default'] = LpSolutionGraphData(x_lim, y_lim, polygons_datas, odr_points, {}, legend_handles)

        return fig, ax

    def create_sequence_solution_plots(self):
        plots = []

        n = len(self.problem.get_consrts_c())
        for i in range(n):
            fig, ax = self.create_patch_solution_plot(i)
            plots.append((fig, ax))

        return plots

    def create_patch_solution_plot(self, idx: int):
        if str(idx) in self.cache:
            return self.__recreate_patch_solution_plot(str(idx))

        consrts_c = self.problem.get_consrts_c()
        consrts_s = self.problem.get_consrts_s()

        var_consrts0_c = self.problem.get_var_consrts_c()
        var_consrts0_s = self.problem.get_var_consrts_s()

        rhs_c = var_consrts0_c + consrts_c[0:idx + 1]
        rhs_s = var_consrts0_s + consrts_s[0:idx + 1]

        lhs_c = consrts_c[idx:idx + 1]

        inters0 = self.__find_intersections_between(rhs_c + lhs_c)

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
            var_consrts1_s = ['<=', '<=']
        else:
            y_lim[0] -= offset
            x_lim[0] -= offset
            x_lim[1] += offset
            y_lim[1] += offset
            var_consrts1_c = [(1., .0, x_lim[0]), (0., 1., y_lim[0])]
            inters1 = np.array([[0., y_lim[0]], [x_lim[0], .0], [x_lim[0], y_lim[0]]])
            var_consrts1_s = ['>=', '>=']

        inters2 = self.__find_intersections_with(lhs_c, var_consrts1_c)

        all_inters = np.concatenate((inters0, inters1, inters2, np.array([[.0, .0]])), axis=0)
        all_inters = self.__unique_points(all_inters)

        var_consrts_c = var_consrts0_c + var_consrts1_c
        var_consrts_s = var_consrts0_s + var_consrts1_s
        inters_b = self.__not_satisfy_constraints(all_inters, var_consrts_c, var_consrts_s)

        odr_polygons = self.__find_odr_polygons(inters_b, rhs_c, rhs_s)
        polygons_datas = self.__sort_polygons_points(odr_polygons)
        odr_points = []
        for pol_data in polygons_datas:
            points = pol_data[1]
            odr_points += points.tolist()

        odr_points = np.array(odr_points)
        legend_handles = [Patch(color=ODR_POLYGON_COLOR, label='Область допустимых решений')]

        x = np.linspace(x_lim[0], x_lim[1], 2)
        ys = []
        x_verts = []
        for idx, (a, b, c) in enumerate(rhs_c[2:]):
            if b != 0:
                y = (c - a * x) / b
                ys.append(y)
            else:
                x_vert = c / a
                x_verts.append(x_vert)

            label = self.controller.constraint_to_str(idx, self.problem)
            legend_handles.append(
                Patch(linestyle=LINES_LINESTYLE, color=LINES_COLOR, linewidth=LINES_WIDTH, label=label))

        lines = {
            'x': x,
            'y': ys,
            'x_vert': x_verts
        }

        fig, ax = self.__create_plot(x_lim, y_lim, polygons_datas, odr_points, lines)
        self.__create_legend(ax, legend_handles)
        self.cache[str(idx)] = LpSolutionGraphData(x_lim, y_lim, polygons_datas, odr_points, lines, legend_handles)

        return fig, ax

    def create_solution_result_plot(self):
        if 'last' in self.cache:
            return self.__recreate_solution_result_plot()

        objv_c = self.problem.get_objv_c()

        dir_to = (objv_c[0], objv_c[1])
        dir_to_magnitude = np.linalg.norm(dir_to)
        dir_to_norm = dir_to / dir_to_magnitude

        idx = len(self.problem.get_consrts_c()) - 1
        fig, ax = self.create_patch_solution_plot(idx)

        step = 0.005
        n = int(dir_to_magnitude / step)
        x_lim = ax.get_xlim()
        x = np.linspace(x_lim[0], x_lim[1], n)

        optimal_p = self.solve_result.x

        c = optimal_p[0] * objv_c[0] + optimal_p[1] * objv_c[1]
        y = (c - objv_c[0] * x) / objv_c[1]

        def __update(frame, ln):
            x0 = optimal_p[0] / dir_to_magnitude * (step * frame)
            y0 = optimal_p[1] / dir_to_magnitude * (step * frame)
            c = x0 * objv_c[0] + y0 * objv_c[1]
            y = (c - objv_c[0] * x) / objv_c[1]
            ln.set_data(x, y)

            return ln,

        lines = {
            'x': x,
            'y': y,
        }

        fig, ax, ani = self.__add_solve_result_anim_to_plot(fig, ax, dir_to_norm, __update, lines, optimal_p, n)

        self.cache['last'] = LpSolutionGraphAnimatedData(quiver_data=dir_to_norm, update_callback=__update,
                                                         lines=lines, optimal_point=optimal_p, frames=n)

        return fig, ax, ani

    def __recreate_solution_result_plot(self):
        cache = self.cache['last']

        idx = len(self.problem.get_consrts_c()) - 1
        fig, ax = self.create_patch_solution_plot(idx)

        fig, ax, ani = self.__add_solve_result_anim_to_plot(fig, ax, cache.quiver_data, cache.update_callback,
                                                            cache.lines, cache.optimal_point, cache.frames)

        return fig, ax, ani

    def __recreate_patch_solution_plot(self, key: str):
        cache = self.cache[key]
        fig, ax = self.__create_plot(cache.x_lim, cache.y_lim, cache.polygons_datas, cache.odr_points, cache.lines)

        return fig, ax

    def __add_solve_result_anim_to_plot(self, fig, ax, quiver_data, update_callback, lines, optimal_point, frames):
        ax.quiver(.0, .0, quiver_data[0], quiver_data[1], scale=1, scale_units='xy', angles='xy',
                  color=OPTIMAL_SOLUTION_COLOR)

        ax.scatter(optimal_point[0], optimal_point[1], color=OPTIMAL_SOLUTION_COLOR, marker=ODR_POINT_MARKER)

        ax.plot(lines['x'], lines['y'], color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

        line, = ax.plot([], [], color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
        ani = FuncAnimation(fig, update_callback, frames=frames, blit=True, repeat=True, interval=10, fargs=(line,))

        return fig, ax, ani

    def __create_plot(self, x_lim, y_lim, polygons_datas, odr_points, lines):
        fig, ax = plt.subplots()

        if len(polygons_datas) != 0:
            for polygon_data in polygons_datas:
                points = polygon_data[1]
                polygon = Polygon(points, alpha=ODR_POLYGON_ALPHA, color=ODR_POLYGON_COLOR)
                ax.add_patch(polygon)

        if len(odr_points) != 0:
            ax.scatter(odr_points[:, 0], odr_points[:, 1], marker=ODR_POINT_MARKER, color=ODR_POLYGON_COLOR)

        if len(lines) != 0:
            x = lines['x']
            for i in range(len(lines['y'])):
                y = lines['y'][i]
                ax.plot(x, y, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

            for i in range(len(lines['x_vert'])):
                x_vert = lines['x_vert'][i]
                ax.axvline(x=x_vert, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

        ax.set_xlim(x_lim[0], x_lim[1])
        ax.set_ylim(y_lim[0], y_lim[1])

        self.__add_default_patches(ax)

        return fig, ax

    def __recreate_default_plot(self):
        cache = self.cache['default']
        fig, ax = self.__create_plot(cache.x_lim, cache.y_lim, cache.polygons_datas, cache.odr_points, {})
        self.__create_legend(ax, cache.legend_handles)

        return fig, ax

    def __add_default_patches(self, ax: Axes):
        ax.axhline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)
        ax.axvline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)

        ax.set_xlabel(AXIS_X_LABEL_NAME)
        ax.set_ylabel(AXIS_Y_LABEL_NAME)

        ax.grid(color=GRID_COLOR, linestyle=GRID_LINESTYLE, linewidth=GRID_WIDTH)

    def __create_legend(self, ax, handles):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))

    def __is_satisfy_inequality(self, x01, a, b, c, sign):
        value = a * x01[0] + b * x01[1]
        if sign == '<=':
            return math.isclose(value, c, abs_tol=ABS_TOL) or value < c
        elif sign == '>=':
            return math.isclose(value, c, abs_tol=ABS_TOL) or value > c
        else:
            return math.isclose(value, c, abs_tol=ABS_TOL)

    def __not_satisfy_constraints(self, points, constraints, signs):
        results = []

        for point in points:
            valid = True
            for i, (a0, b0, c0) in enumerate(constraints):
                if not self.__is_satisfy_inequality(point, a0, b0, c0, signs[i]):
                    valid = False
                    break

            if valid:
                results.append(point)

        return np.array(results)

    def __find_intersections(self, lhs, rhs):
        a0, b0, c0 = lhs
        a1, b1, c1 = rhs
        a = np.array([[a0, b0], [a1, b1]])
        b = np.array([c0, c1])
        try:
            return np.linalg.solve(a, b)
        except np.linalg.LinAlgError:
            return None

    def __find_intersections_with(self, lines0, lines1):
        results = []

        for line0 in lines0:
            for line1 in lines1:
                intersection = self.__find_intersections(line0, line1)
                if intersection is None or self.__contains_point(intersection, results):
                    continue

                results.append(intersection)

        return np.array(results)

    def __find_intersections_between(self, lines):
        results = []

        for i, line0 in enumerate(lines):
            for j, line1 in enumerate(lines[i + 1:], start=i + 1):
                intersection = self.__find_intersections(line0, line1)
                if intersection is None or self.__contains_point(intersection, results):
                    continue

                results.append(intersection)

        return np.array(results)

    def __find_odr_polygons(self, points, coeffs, signs):
        results = []

        a = np.ones(points.shape[0], dtype=bool)
        for i, (a0, b0, c0) in enumerate(coeffs):
            b = []
            for point in points:
                b.append(self.__is_satisfy_inequality(point, a0, b0, c0, signs[i]))

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

    def __sort_polygon_points(self, points):
        centroid = np.mean(points, axis=0)
        angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
        sorted_points = points[np.argsort(angles)]

        return centroid, np.vstack([sorted_points, sorted_points[0]])

    def __sort_polygons_points(self, polygons):
        results = []

        for points in polygons:
            results.append(self.__sort_polygon_points(points))

        return results

    def __unique_points(self, points):
        results = []
        for point in points:
            if not self.__contains_point(point, results):
                results.append(point)

        return np.array(results)

    def __contains_point(self, lhs, points):
        for rhs in points:
            if math.isclose(lhs[0], rhs[0], abs_tol=ABS_TOL) and math.isclose(lhs[1], rhs[1], abs_tol=ABS_TOL):
                return True

        return False
