from matplotlib import pyplot as plt
from Core.Helper.lp_bank import get_bank
from Core.Helper.lp_helper import solve_lp
from Core.LP.Runtime.LpGraphBuilder import LpGraphBuilder
from Core.LP.Runtime.LpProblemData import LpProblemData
from Core.Pool import Pool

bank = get_bank()
for key, problem_data in bank.items():
    title = problem_data['title']
    data = problem_data['data']
    problem = LpProblemData(data)
    solve_result = solve_lp(problem)


    def create_plot_instance():
        return plt.subplots()


    graph_builder = LpGraphBuilder(problem, solve_result, Pool(create_plot_instance))
    graph = graph_builder.build_result_graph()
    if graph is None:
        last_idx = len(problem.get_consrts_c()) - 1
        graph = graph_builder.build_patch_graph(last_idx)

    fig = graph[0]
    path = f'{key}_result_graph'
    fig.savefig(path, dpi=100)

    break


