# 1. Функция достигает наибольшего значения в точке
problem1 = {
    'objective': {
        'goal': 'max',
        'coefficients': (1., -1.)
    },
    'constraints': {
        'coefficients': [
            (1., 1., 7.),
            (.0, 1., 5.),
            (1., 1., 3.),
            (.0, 1., 2.),
            (1., .0, 4.)
        ],
        'signs': ['<=', '<=', '>=', '>=', '<=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 2. Функция достигает наименьшего значения в точке
problem2 = {
    'objective': {
        'goal': 'min',
        'coefficients': (2., 2.)
    },
    'constraints': {
        'coefficients': [
            (1., 2., 8.),
            (1., -1., 2.),
            (1., 2., 4.),
            (1., 0., 1.)
        ],
        'signs': ['<=', '<=', '>=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 3. Функция достигает наибольшего значения на отрезке
problem3 = {
    'objective': {
        'goal': 'max',
        'coefficients': (1., 2.)
    },
    'constraints': {
        'coefficients': [
            (1., 2., 10.),
            (1., 2., 2.),
            (2., 1., 10.),
            (3., 1., 3.)
        ],
        'signs': ['<=', '>=', '<=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 4. Функция достигает наименьшего значения на отрезке
problem4 = {
    'objective': {
        'goal': 'min',
        'coefficients': (2., 2.)
    },
    'constraints': {
        'coefficients': [
            (1., 1., 6.),
            (3., -1., 3.),
            (1., -1., 2.),
            (.0, 1., 6.),
            (1., .0, 5.)
        ],
        'signs': ['>=', '>=', '<=', '<=', '<=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 5. Функция достигает наибольшего значения на луче
problem5 = {
    'objective': {
        'goal': 'max',
        'coefficients': (-1., 1.)
    },
    'constraints': {
        'coefficients': [
            (1., -2., 4.),
            (1., -1., 1.),
            (1., 1., 2.)
        ],
        'signs': ['<=', '>=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 6. Функция достигает наименьшего значения на луче
problem6 = {
    'objective': {
        'goal': 'min',
        'coefficients': (3., -1.)
    },
    'constraints': {
        'coefficients': [
            (1., -1., 8.),
            (3., -1., 3.),
            (2., 1., 4.)
        ],
        'signs': ['<=', '>=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 7. Функция неограниченно возрастает
problem7 = {
    'objective': {
        'goal': 'max',
        'coefficients': (1., 1.)
    },
    'constraints': {
        'coefficients': [
            (3., 2., 6.),
            (-1., 1., 1.),
            (1., -2., 1.)
        ],
        'signs': ['>=', '<=', '<=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 8. Функция неограниченно убывает
problem8 = {
    'objective': {
        'goal': 'min',
        'coefficients': (1., -2.)
    },
    'constraints': {
        'coefficients': [
            (2., 1., 2.),
            (4., -6., 12.),
            (0., 1., 1.)
        ],
        'signs': ['>=', '<=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 9. Область допустимых решений точка
problem9 = {
    'objective': {
        'goal': 'max',
        'coefficients': (1., 1.)
    },
    'constraints': {
        'coefficients': [
            (1., 1., 1.),
            (1., -1., 1.),
            (1., .0, 1.),
            (2., 1., 1.),
            (1., 2., 7.)
        ],
        'signs': ['>=', '>=', '<=', '>=', '<=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}

# 10. Область допустимых решений - пустое множество
problem10 = {
    'objective': {
        'goal': 'max',
        'coefficients': (1., 1.)
    },
    'constraints': {
        'coefficients': [
            (3., 5., 30.),
            (4., -3., 12.),
            (1., -3., 6.)
        ],
        'signs': ['<=', '<=', '>=']
    },
    'vars_constraints': {
        'coefficients': [
            (1., .0, .0),
            (.0, 1., .0)
        ],
        'signs': ['>=', '>=']
    }
}
