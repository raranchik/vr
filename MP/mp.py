import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1,
                         n_obj=2,
                         n_constr=0,
                         xl=np.array([0]),
                         xu=np.array([4]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0] ** 2
        f2 = (x[0] - 2) ** 2
        out["F"] = [f1, f2]


problem = MyProblem()

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               termination=('n_gen', 40),
               seed=1,
               save_history=True,
               verbose=True)

plot = Scatter()
plot.add(res.F, color="red")
plot.show()
