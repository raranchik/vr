import re


def validate_float(string):
    regex = re.compile(r"(\+|\-)?[0-9.]*$")
    result = regex.match(string)
    return (string == "" or (string.count('+') <= 1
                             and string.count('-') <= 1
                             and string.count('.') <= 1
                             and result is not None
                             and result.group(0) != ""))


def on_validate_float(p):
    return validate_float(p)


def floatize(value):
    if value == '':
        return .0

    return float(value)
