import pytest
import gamete.design_space as dspace
import decimal
def test_variable():

    NDIM = 3
    # BOUND_LOW, BOUND_UP = 0.0, 1.0
    BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
    RES_STR = '0.05'

    vset_bool = dspace.VariableList("boolean set",list())
    vset_ranged = dspace.VariableList("range set",list())

    # Variables
    for i in range(NDIM):
        this_var = dspace.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
        vset_ranged.append(this_var)

    print()
    for var in vset_ranged:
        print(var)

    assert type(vset_ranged[2].variable_tuple[0]) is decimal.Decimal

    for i in range(5):
        vset_bool.append(dspace.Variable.as_bool('This Bool'))

    assert len(vset_ranged) == 3

    variable_lists = [vset_bool, vset_ranged]

    this_ds = dspace.DesignSpace(variable_lists)

    print(this_ds)

    this_ds.print_design_space()





