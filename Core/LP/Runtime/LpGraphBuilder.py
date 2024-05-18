import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.patches import Polygon

from Core.Helper.math_helper import ABS_TOL
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.LP.Runtime.LpResultGraphAnimatedData import LpResultGraphAnimatedData
from Core.LP.Runtime.LpPatchGraphData import LpPatchGraphData
from Core.LP.Runtime.LpResultGraphData import LpResultGraphData

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

LINES_WIDTH = 1.25
LINES_LINESTYLE = '-'
LINES_COLOR = 'black'

OPTIMAL_SOLUTION_COLOR = 'red'

ODR_POINT_MARKER = 'o'

DEFAULT_GRAPH_NAME = 'DEFAULT_GRAPH'
RESULT_GRAPH_NAME = 'RESULT_GRAPH'
RESULT_ANIMATED_GRAPH_NAME = 'RESULT_ANIMATED_GRAPH'

TEXT_BBOX_ALPHA = 0.5


class LpGraphBuilder:
    def __init__(self, problem: LpProblemData, solve_result, plot_pool):
        self.problem = problem
        self.solve_result = solve_result
        self.plot_pool = plot_pool
        self.cache: dict = {}

    def release_graph(self, plot):
        if len(plot) == 3:
            ani = plot[2]
            ani.event_source.stop()

        fig = plot[0]
        fig.clf()
        ax = plot[1]
        ax.cla()
        ax = fig.add_subplot()
        self.plot_pool.release((fig, ax))

    def build_default_graph(self):
        if DEFAULT_GRAPH_NAME in self.cache:
            return self.__rebuild_default_graph()

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

        legend_handles = []
        legend_handles.append(Patch(color=ODR_POLYGON_COLOR, label='Область допустимых решений'))
        legend_handles.append(Line2D([.0], [.0],
                                     linestyle=LINES_LINESTYLE, color=LINES_COLOR, linewidth=LINES_WIDTH,
                                     label=self.var_constraints_to_str()))

        fig, ax = self.__create_plot(x_lim, y_lim, polygons_datas, odr_points, {})
        title = 'ЛП - ОДР при добавлении ограничений переменных'
        ax.set_title(title)
        self.__create_legend(ax, fig, legend_handles)

        self.cache[DEFAULT_GRAPH_NAME] = LpPatchGraphData(x_lim, y_lim, polygons_datas, odr_points, {},
                                                          legend_handles, inters, title)

        return fig, ax

    def build_patch_graphs(self):
        plots = []

        n = len(self.problem.get_consrts_c())
        for i in range(n):
            fig, ax = self.build_patch_graph(i)
            plots.append((fig, ax))

        return plots

    def build_patch_graph(self, idx: int):
        if str(idx) in self.cache:
            return self.__rebuild_patch_graph(str(idx))

        consrts_c = self.problem.get_consrts_c()
        consrts_s = self.problem.get_consrts_s()

        var_consrts0_c = self.problem.get_var_consrts_c()
        var_consrts0_s = self.problem.get_var_consrts_s()

        rhs_c = var_consrts0_c + consrts_c[0:idx + 1]
        rhs_s = var_consrts0_s + consrts_s[0:idx + 1]

        lhs_c = consrts_c[idx:idx + 1]

        inters0 = self.__find_intersections_between(rhs_c + lhs_c)
        inters0 = self.__not_satisfy_constraints(inters0, var_consrts0_c, var_consrts0_s)

        x_lim = [np.min(inters0[:, 0]), np.max(inters0[:, 0])]
        y_lim = [np.min(inters0[:, 1]), np.max(inters0[:, 1])]

        offset = 1.
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

        inters2 = self.__find_intersections_with(rhs_c + lhs_c, var_consrts1_c)

        all_inters = np.concatenate((inters0, inters1, inters2, np.array([[.0, .0]])), axis=0)
        all_inters = self.__unique_points(all_inters)

        var_consrts_c = var_consrts0_c + var_consrts1_c
        var_consrts_s = var_consrts0_s + var_consrts1_s
        inters_b = self.__not_satisfy_constraints(all_inters, var_consrts_c, var_consrts_s)

        odr_polygons = self.__find_odr_polygons(inters_b, rhs_c, rhs_s)
        polygons_datas = self.__sort_polygons_points(odr_polygons)
        polygons_points = []
        for pol_data in polygons_datas:
            points = pol_data[1]
            polygons_points += points.tolist()

        odr_points = self.__exclude_points(polygons_points, np.concatenate((inters1, inters2), axis=0))
        legend_handles = [Patch(color=ODR_POLYGON_COLOR, label='Область допустимых решений')]

        x = np.linspace(x_lim[0], x_lim[1], 2)
        y_verts = []
        x_verts = []
        ys = []
        for idx, (a, b, c) in enumerate(rhs_c[2:]):
            if math.isclose(a, 0., abs_tol=ABS_TOL):
                y_vert = c / b
                text_p = [x_lim[1], y_vert]
                y_verts.append((f'({idx + 1})', text_p, y_vert))
            elif math.isclose(b, 0., abs_tol=ABS_TOL):
                x_vert = c / a
                text_p = [x_vert, y_lim[0]]
                x_verts.append((f'({idx + 1})', text_p, x_vert))
            else:
                y = (c - a * x) / b
                text_p = self.__find_intersections((a, b, c), var_consrts0_c[1])
                ys.append((f'({idx + 1})', text_p, y))

            label = self.constraint_to_str(idx)
            legend_handles.append(Line2D([.0], [.0],
                                         linestyle=LINES_LINESTYLE, color=LINES_COLOR, linewidth=LINES_WIDTH,
                                         label=label))

        lines = {
            'x': x,
            'y': ys,
            'x_vert': x_verts,
            'y_vert': y_verts
        }

        fig, ax = self.__create_plot(x_lim, y_lim, polygons_datas, odr_points, lines)
        title = f'ЛП - ОДР при добавлении ограничения №{idx + 1}'
        ax.set_title(title)
        self.__create_legend(ax, fig, legend_handles)
        self.cache[str(idx)] = LpPatchGraphData(x_lim, y_lim, polygons_datas, odr_points, lines, legend_handles,
                                                polygons_points, title)

        return fig, ax

    def build_result_graph(self):
        if not self.solve_result.success and self.solve_result.status != 3:
            return None

        if RESULT_GRAPH_NAME in self.cache:
            return self.__rebuild_result_graph()

        objv_c = self.problem.get_objv_c()

        dir_to = (objv_c[0], objv_c[1])
        dir_to_magnitude = np.linalg.norm(dir_to)
        dir_to_norm = dir_to / dir_to_magnitude

        idx = len(self.problem.get_consrts_c()) - 1
        fig, ax = self.build_patch_graph(idx)

        legend = ax.get_legend()
        legend_handles = legend.legend_handles

        x_lim = ax.get_xlim()
        x = np.linspace(x_lim[0], x_lim[1], 2)

        if self.solve_result.success:
            optimal_point = self.solve_result.x
        else:
            y_lim = ax.get_ylim()
            quarters = (0 if math.copysign(1, dir_to[0]) < .0 else 1,
                        0 if math.copysign(1, dir_to[1]) < .0 else 1)
            optimal_point = [x_lim[quarters[0]], y_lim[quarters[1]]]

        c = optimal_point[0] * objv_c[0] + optimal_point[1] * objv_c[1]
        y = (c - objv_c[0] * x) / objv_c[1]

        lines = {
            'x': x,
            'y': y,
        }

        legend_handles.append(Line2D([.0], [.0], linestyle=LINES_LINESTYLE,
                                     color=OPTIMAL_SOLUTION_COLOR, label=self.objective_to_str(),
                                     linewidth=LINES_WIDTH))

        text = r'$\overline{C}$ - Градиент целевой функции'
        legend_handles.append(Line2D([.0], [.0], label=text, marker=r'$\longrightarrow$',
                                     color=OPTIMAL_SOLUTION_COLOR, linestyle='', markersize=20.))

        if self.solve_result.success:
            optimal_value = self.solve_result.fun if self.problem.get_goal() == 'min' else -self.solve_result.fun
            cache = self.cache[str(idx)]
            odr_points = cache.odr_points
            polygons_points = cache.polygons_points
            n = len(polygons_points)
            for i in range(n - 1):
                lhs = polygons_points[i]
                rhs = polygons_points[i + 1]
                lhs_is_optimal = False
                rhs_is_optimal = False
                if self.__equal_points(lhs, rhs):
                    continue

                lhs_value = objv_c[0] * lhs[0] + objv_c[1] * lhs[1]
                lhs_is_optimal = math.isclose(lhs_value, optimal_value, abs_tol=ABS_TOL)
                if not lhs_is_optimal:
                    continue

                rhs_value = objv_c[0] * rhs[0] + objv_c[1] * rhs[1]
                rhs_is_optimal = math.isclose(rhs_value, optimal_value, abs_tol=ABS_TOL)
                if rhs_is_optimal:
                    break

            lhs_in_odr = self.__contains_point(lhs, odr_points) and lhs_is_optimal
            rhs_in_odr = self.__contains_point(rhs, odr_points) and rhs_is_optimal
            symbols = ['(A)']
            if lhs_in_odr and rhs_in_odr:
                optimal_point = np.array([lhs, rhs])
                symbols.append('(B)')
            elif lhs_in_odr and not rhs_in_odr:
                optimal_point = np.array([lhs])
            elif not lhs_in_odr and rhs_in_odr:
                optimal_point = np.array([rhs])
            else:
                optimal_point = np.array([optimal_point])

            text = 'Оптимальное значение ' + ", ".join(symbols)
            legend_handles.append(Line2D([.0], [.0], label=text, marker='o',
                                         color=OPTIMAL_SOLUTION_COLOR, linestyle=''))
        else:
            optimal_point = []

        fig, ax = self.__add_result_data_to_plot(fig, ax, dir_to_norm, lines, optimal_point)
        ax.set_title('ЛП - Результат решения задачи')
        self.__create_legend(ax, fig, legend_handles)

        self.cache[RESULT_GRAPH_NAME] = LpResultGraphData(dir_to_norm, lines, optimal_point, legend_handles)

        return fig, ax

    def build_animated_result_graph(self):
        if not self.solve_result.success and self.solve_result.status != 3:
            return None

        if RESULT_ANIMATED_GRAPH_NAME in self.cache:
            return self.__rebuild_animated_result_graph()

        fig, ax = self.build_result_graph()

        objv_c = self.problem.get_objv_c()

        dir_to = (objv_c[0], objv_c[1])
        dir_to_magnitude = np.linalg.norm(dir_to) / 2.

        step = 0.005
        n = int(dir_to_magnitude / step)
        x_lim = ax.get_xlim()
        x = np.linspace(x_lim[0], x_lim[1], n)

        if self.solve_result.success:
            optimal_point = self.solve_result.x
        else:
            y_lim = ax.get_ylim()
            quarters = (0 if math.copysign(1, dir_to[0]) < .0 else 1,
                        0 if math.copysign(1, dir_to[1]) < .0 else 1)
            optimal_point = [x_lim[quarters[0]], y_lim[quarters[1]]]

        def animation_update(frame, ln):
            if ax is None:
                print('HELLO')

            x0 = optimal_point[0] / dir_to_magnitude * (step * frame)
            y0 = optimal_point[1] / dir_to_magnitude * (step * frame)
            c = x0 * objv_c[0] + y0 * objv_c[1]
            y = (c - objv_c[0] * x) / objv_c[1]
            ln.set_data(x, y)

            return ln,

        fig, ax, ani = self.__add_result_data_animated_to_plot(fig, ax, animation_update, n)
        title = ('ЛП - Результат решения задачи.'
                 '\nАнимация движения целевой функции вдоль градиента'
                 r' $\overline{C}$ '
                 'до точки оптимума')
        ax.set_title(title)
        fig.tight_layout()

        self.cache[RESULT_ANIMATED_GRAPH_NAME] = LpResultGraphAnimatedData(update_callback=animation_update, frames=n)

        return fig, ax, ani

    def __rebuild_default_graph(self):
        cache = self.cache[DEFAULT_GRAPH_NAME]
        fig, ax = self.__create_plot(cache.x_lim, cache.y_lim, cache.polygons_datas, cache.odr_points, {})
        ax.set_title(cache.title)
        self.__create_legend(ax, fig, cache.legend_handles)

        return fig, ax

    def __rebuild_patch_graph(self, key: str):
        cache = self.cache[key]
        fig, ax = self.__create_plot(cache.x_lim, cache.y_lim, cache.polygons_datas, cache.odr_points, cache.lines)
        ax.set_title(cache.title)
        self.__create_legend(ax, fig, cache.legend_handles)

        return fig, ax

    def __rebuild_result_graph(self):
        cache = self.cache[RESULT_GRAPH_NAME]

        idx = len(self.problem.get_consrts_c()) - 1
        fig, ax = self.build_patch_graph(idx)

        fig, ax = self.__add_result_data_to_plot(fig, ax, cache.quiver_data, cache.lines, cache.optimal_point)
        ax.set_title('ЛП - Результат решения задачи')
        self.__create_legend(ax, fig, cache.legend_handles)

        return fig, ax

    def __rebuild_animated_result_graph(self):
        cache = self.cache[RESULT_ANIMATED_GRAPH_NAME]

        fig, ax = self.build_result_graph()
        title = ('ЛП - Результат решения задачи.'
                 '\nАнимация движения целевой функции вдоль градиента'
                 r' $\overline{C}$ '
                 'до точки оптимума')
        ax.set_title(title)
        fig, ax, ani = self.__add_result_data_animated_to_plot(fig, ax, cache.update_callback, cache.frames)
        fig.tight_layout()

        return fig, ax, ani

    def __add_result_data_animated_to_plot(self, fig, ax, update_callback, frames):
        line, = ax.plot([], [], color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)
        ani = FuncAnimation(fig, update_callback, frames=frames, blit=True, repeat=True, interval=10, fargs=(line,))

        return fig, ax, ani

    def __add_result_data_to_plot(self, fig, ax, quiver_data, lines, optimal_point):
        ax.quiver(.0, .0, quiver_data[0], quiver_data[1], scale=1, scale_units='xy', angles='xy',
                  color=OPTIMAL_SOLUTION_COLOR)

        ax.text(quiver_data[0] + .15, quiver_data[1] + .15, r'$\overline{C}$', fontsize=16,
                ha='right', va='bottom', bbox=dict(facecolor='white', alpha=TEXT_BBOX_ALPHA, edgecolor='none'))

        if len(optimal_point) > 0:
            symbols = ['(A)', '(B)']
            for i in range(len(optimal_point)):
                ax.text(optimal_point[i][0] + .15, optimal_point[i][1] + .15, symbols[i], fontsize=16, ha='right',
                        va='bottom', bbox=dict(facecolor='white', alpha=TEXT_BBOX_ALPHA, edgecolor='none'))

            ax.scatter(optimal_point[:, 0], optimal_point[:, 1], color=OPTIMAL_SOLUTION_COLOR, marker=ODR_POINT_MARKER)

        ax.plot(lines['x'], lines['y'], color=OPTIMAL_SOLUTION_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

        return fig, ax

    def __create_plot(self, x_lim, y_lim, polygons_datas, odr_points, lines):
        fig, ax = self.plot_pool.acquire()
        fig.set_figheight(8)
        fig.set_figwidth(8)

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
                y = lines['y'][i][2]
                text = lines['y'][i][0]
                text_p = lines['y'][i][1]
                ax.text(text_p[0] + .15, text_p[1] + .15, text, fontsize=16,
                        ha='right', va='bottom', bbox=dict(facecolor='white', alpha=TEXT_BBOX_ALPHA, edgecolor='none'))
                ax.plot(x, y, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

            for i in range(len(lines['x_vert'])):
                x_vert = lines['x_vert'][i][2]
                text = lines['x_vert'][i][0]
                text_p = lines['x_vert'][i][1]
                ax.text(text_p[0] + .15, text_p[1] + .15, text, fontsize=16,
                        ha='right', va='bottom', bbox=dict(facecolor='white', alpha=TEXT_BBOX_ALPHA, edgecolor='none'))
                ax.axvline(x=x_vert, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

            for i in range(len(lines['y_vert'])):
                y_vert = lines['y_vert'][i][2]
                text = lines['y_vert'][i][0]
                text_p = lines['y_vert'][i][1]
                ax.text(text_p[0] + .15, text_p[1] + .15, text, fontsize=16,
                        ha='right', va='bottom', bbox=dict(facecolor='white', alpha=TEXT_BBOX_ALPHA, edgecolor='none'))
                ax.axhline(y=y_vert, color=LINES_COLOR, linewidth=LINES_WIDTH, linestyle=LINES_LINESTYLE)

        ax.set_xlim(x_lim[0], x_lim[1])
        ax.set_ylim(y_lim[0], y_lim[1])

        self.__add_default_patches(ax)

        return fig, ax

    def __add_default_patches(self, ax: Axes):
        ax.axhline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)
        ax.axvline(0, color=AXIS_COLOR, linewidth=AXIS_WIDTH, linestyle=AXIS_LINESTYLE)

        ax.set_xlabel(AXIS_X_LABEL_NAME)
        ax.set_ylabel(AXIS_Y_LABEL_NAME)

        ax.grid(color=GRID_COLOR, linestyle=GRID_LINESTYLE, linewidth=GRID_WIDTH)

        ax.set_aspect(aspect='auto', adjustable='box', share=False)

    def __create_legend(self, ax, fig, handles):
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                  fancybox=True, shadow=False, ncol=2, handles=handles)

        fig.tight_layout()

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
            if self.__equal_points(lhs, rhs):
                return True

        return False

    def __equal_points(self, lhs, rhs):
        return math.isclose(lhs[0], rhs[0], abs_tol=ABS_TOL) and math.isclose(lhs[1], rhs[1], abs_tol=ABS_TOL)

    def __exclude_points(self, lhs, rhs):
        result = []

        for point in lhs:
            if self.__contains_point(point, rhs):
                continue

            result.append(point)

        return np.array(result)

    def objective_to_str(self):
        objv_c = self.problem.get_objv_c()
        objv_g = self.problem.get_goal()

        terms = [f"{coef}x_{i + 1}" for i, coef in enumerate(objv_c)]
        terms_str = " + ".join(terms)
        result = f"$F(x_1,x_2) = {terms_str} \\rightarrow {objv_g}$"

        return result

    def constraint_to_str(self, idx):
        consrt_c = self.problem.get_consrts_c()[idx]
        consrt_s = self.problem.get_consrts_s()[idx]

        terms = []
        for i, coef in enumerate(consrt_c[:-1]):
            if math.isclose(coef, .0, abs_tol=ABS_TOL):
                continue

            terms.append(f"{coef}x_{i + 1}")

        terms_str = " + ".join(terms)

        if consrt_s == '>=':
            sign = '\\geq'
        elif consrt_s == '<=':
            sign = '\\leq'
        else:
            sign = consrt_s

        result = f"$({idx + 1}) {terms_str} {sign} {consrt_c[-1]}$"

        return result

    def var_constraints_to_str(self):
        var_consrts_s = self.problem.get_var_consrts_s()[0]

        n = 2
        variables = [f"x_{i + 1}" for i in range(n)]
        variables_str = ", ".join(variables)

        if var_consrts_s == '>=':
            sign = '\\geq'
        elif var_consrts_s == '<=':
            sign = '\\leq'
        else:
            sign = var_consrts_s

        result = f"${variables_str} {sign} 0$"

        return result
