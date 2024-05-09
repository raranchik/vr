import pyomo.environ
import builtins
from pyomo.common.tempfiles import TempfileManager
from pyomo.opt import TerminationCondition


def cos(arg):
    return pyomo.environ.cos(arg)


def sin(arg):
    return pyomo.environ.sin(arg)


def pow(arg0, arg1):
    return builtins.pow(arg0, arg1)


def exp(arg):
    return pyomo.environ.exp(arg)


def create_func_ref_dict():
    return {'sin': sin, 'cos': cos, 'pow': pow, 'exp': exp}


def solve_and_extract_iter_results_ipopt(m, s, max_iter, max_cpu_time):
    TempfileManager.push()
    tempfile = TempfileManager.create_tempfile(suffix='ipopt_out', text=True)
    opts = {'output_file': tempfile, 'max_iter': max_iter, 'max_cpu_time': max_cpu_time}

    status_obj = s.solve(m, options=opts, tee=True)
    solved = True
    if status_obj.solver.termination_condition != TerminationCondition.optimal:
        solved = False

    iters = 0
    time = 0
    line_m_2 = None
    line_m_1 = None
    with open(tempfile, 'r') as f:
        for line in f:
            if line.startswith('Number of Iterations....:'):
                tokens = line.split()
                iters = int(tokens[3])
                tokens_m_2 = line_m_2.split()
                regu = str(tokens_m_2[6])
            elif line.startswith(
                    'Total CPU secs in IPOPT (w/o function evaluations)   ='
            ):
                tokens = line.split()
                time += float(tokens[9])
            elif line.startswith(
                    'Total CPU secs in NLP function evaluations           ='
            ):
                tokens = line.split()
                time += float(tokens[8])
            line_m_2 = line_m_1
            line_m_1 = line

    TempfileManager.pop(remove=True)
