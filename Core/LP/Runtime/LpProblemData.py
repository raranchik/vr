import math

from Core.Helper.math_helper import ABS_TOL


class LpProblemData:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        lhs_objv = self.data['objective']
        rhs_objv = other.data['objective']

        eq_objv = self.__equal_objv(lhs_objv['coefficients'], rhs_objv['coefficients'])
        eq_objv &= lhs_objv['goal'] == rhs_objv['goal']

        lhs_consrts = self.data['constraints']
        rhs_consrts = other.data['constraints']
        eq_consrts = self.__equal_consrts(lhs_consrts['coefficients'], rhs_consrts['coefficients'],
                                          lhs_consrts['signs'],
                                          rhs_consrts['signs'])

        lhs_var_consrts = self.data['vars_constraints']
        rhs_var_consrts = other.data['vars_constraints']
        eq_var_consrts = self.__equal_consrts(lhs_var_consrts['coefficients'], rhs_var_consrts['coefficients'],
                                              lhs_var_consrts['signs'],
                                              rhs_var_consrts['signs'])

        return eq_objv and eq_consrts and eq_var_consrts

    def __ne__(self, other):
        eq = self.__eq__(other)

        return not eq

    def get_goal(self):
        return self.data['objective']['goal']

    def get_objv_c(self):
        return self.data['objective']['coefficients']

    def get_consrts_c(self):
        return self.data['constraints']['coefficients']

    def get_consrts_s(self):
        return self.data['constraints']['signs']

    def get_var_consrts_c(self):
        return self.data['vars_constraints']['coefficients']

    def get_var_consrts_s(self):
        return self.data['vars_constraints']['signs']

    def is_invalid(self):
        objv_c = self.get_objv_c()
        if math.isclose(objv_c[0], .0, abs_tol=ABS_TOL) or math.isclose(objv_c[1], .0, abs_tol=ABS_TOL):
            return True

        consrts_c = self.get_consrts_c()
        if len(consrts_c) == 0:
            return True

        for i, (a0, b0, c0) in enumerate(consrts_c):
            if (math.isclose(a0, .0, abs_tol=ABS_TOL)
                    and math.isclose(b0, .0, abs_tol=ABS_TOL)
                    and math.isclose(c0, .0, abs_tol=ABS_TOL)):
                return True

        return False

    def __equal_objv(self, lhs, rhs):
        return math.isclose(lhs[0], rhs[0], abs_tol=ABS_TOL) and math.isclose(lhs[1], rhs[1], abs_tol=ABS_TOL)

    def __equal_consrts(self, lhs_c, rhs_c, lhs_s, rhs_s):
        lhs_n = len(lhs_c)
        rhs_n = len(rhs_c)
        if lhs_n != rhs_n:
            return False

        c = 0
        for i, (a0, b0, c0) in enumerate(lhs_c):
            for j, (a1, b1, c1) in enumerate(rhs_c):
                eq_c = math.isclose(a0, a1, abs_tol=ABS_TOL) and math.isclose(b0, b1, abs_tol=ABS_TOL) and math.isclose(
                    c0, c1, abs_tol=ABS_TOL)
                eq_s = lhs_s[i] == rhs_s[j]
                if eq_c and eq_s:
                    c += 1
                    break

        return c == lhs_n
