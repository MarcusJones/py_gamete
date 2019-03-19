import pytest
import gamete.design_space as dspace
import decimal
def test_variable():
    assert True

    NDIM = 3
    # BOUND_LOW, BOUND_UP = 0.0, 1.0
    BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
    RES_STR = '0.05'

    # --- Variables
    range_variable_set = list()
    for i in range(NDIM):
        this_var = dspace.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
        range_variable_set.append(this_var)

    assert type(range_variable_set[2].variable_tuple[0]) is decimal.Decimal

    range_variable_set.append(dspace.Variable.as_bool('This Bool'))
    print()
    for var in range_variable_set:
        print(var)

    assert len(range_variable_set) == 4


