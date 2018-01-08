BOOL_TYPE = 0
FLOAT_TYPE = 1
STRING_TYPE = 2

BOOL_TYPE_NAME = u'0/1'
FLOAT_TYPE_NAME = u'12.5'
STRING_TYPE_NAME = u'abc'


def get_name_type(data_type):
    if data_type == 0:
        return BOOL_TYPE_NAME
    if data_type == 1:
        return FLOAT_TYPE_NAME
    if data_type == 2:
        return STRING_TYPE_NAME


def is_number(test_value):
    try:
        float(test_value)
        return True
    except ValueError:
        return False


def is_bool(test_value):
    try:
        bool_number = str(test_value)
        if bool_number == '0' or bool_number == '1':
            return True
        else:
            return False
    except ValueError:
        return False


def get_type(test_value):
    if is_bool(test_value):
        return BOOL_TYPE
    if is_number(test_value):
        return FLOAT_TYPE

    return STRING_TYPE
