def create_data1():
    return {
        'goal': 'max',
        'constraint_coeffs': [
            [5, 4, 3, 7, 8],
            [1, 7, 9, 4, 6],
            [8, 10, 2, 1, 10]
        ],
        'signs': ['<=', '<=', '<='],
        'bounds': [25, 25, 25],
        'obj_coeffs': [20, 40, 20, 15, 30],
    }


def create_data2():
    return {
        'goal': 'max',
        'obj_coeffs': [5, 1],
        'constraint_coeffs': [
            [1, 5],
            [3, -1],
        ],
        'signs': ['<=', '<='],
        'bounds': [10, 6],
    }


def create_data3():
    return {
        'goal': 'max',
        'obj_coeffs': [3, 4],
        'constraint_coeffs': [
            [1, 2],
            [3, -1],
            [1, -1],
        ],
        'signs': ['<=', '>=', '<='],
        'bounds': [14, 0, 2],
    }


def create_data4():
    # unbounded LP problem
    return {
        'goal': 'min',
        'obj_coeffs': [-5, -1],
        'constraint_coeffs': [
            [2, 2],
            [3, -1],
        ],
        'signs': ['>=', '>='],
        'bounds': [5, 6],
    }


def create_data5():
    # set of solutions on the line segment
    return {
        'goal': 'max',
        'obj_coeffs': [1, 5],
        'constraint_coeffs': [
            [1, 5],
            [3, -1],
        ],
        'signs': ['<=', '<='],
        'bounds': [10, 6],
    }


def create_data6():
    # incompatibility constraints
    return {
        'goal': 'max',
        'obj_coeffs': [5, 1],
        'constraint_coeffs': [
            [2, 2],
            [3, -1],
            [1, 2],
        ],
        'signs': ['>=', '>=', '<='],
        'bounds': [5, 6, 2],
    }


def create_data7():
    return {
        'goal': 'max',
        'obj_coeffs': [5, 1],
        'constraint_coeffs': [
            [2, 2],
            [3, -1],
            [1, 2],
        ],
        'signs': ['>=', '>=', '<='],
        'bounds': [5, 6, 2],
    }


def create_data8():
    # incompatibility constraints
    return {
        'goal': 'max',
        'obj_coeffs': [5, 1],
        'constraint_coeffs': [
            [3, 5],
            [4, -3],
            [1, -3],
        ],
        'signs': ['<=', '<=', '>='],
        'bounds': [30, 12, 6],
    }


def create_data9():
    return {
        'goal': 'max',
        'obj_coeffs': [1, 1],
        'constraint_coeffs': [
            [1, 1],
            [0, 1],
            [1, 1],
            [0, 1],
            [1, 0],
        ],
        'signs': ['<=', '<=', '>=', '>=', '<='],
        'bounds': [7, 5, 3, 2, 4],
    }
