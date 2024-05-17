def get_bank():
    return {
        '0': {
            'title': '1. Функция достигает наибольшего значения в точке',
            'data': {
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
        },
        '1': {
            'title': '2. Функция достигает наименьшего значения в точке',
            'data': {
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
        },
        '2': {
            'title': '3. Функция достигает наибольшего значения на отрезке',
            'data': {
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
        },
        '3': {
            'title': '4. Функция достигает наименьшего значения на отрезке',
            'data': {
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
        },
        '4': {
            'title': '5. Функция достигает наибольшего значения на луче',
            'data': {
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
        },
        '5': {
            'title': '6. Функция достигает наименьшего значения на луче',
            'data': {
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
        },
        '6': {
            'title': '7. Функция неограниченно возрастает',
            'data': {
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
        },
        '7': {
            'title': '8. Функция неограниченно убывает',
            'data': {
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
        },
        '8': {
            'title': '9. Область допустимых решений точка',
            'data': {
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
        },
        '9': {
            'title': '10. Область допустимых решений - пустое множество',
            'data': {
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
        }
    }
