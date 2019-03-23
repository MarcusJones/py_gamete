import pytest
import gamete.design_space as des_space
import gamete.evolution_space as evo_space
import decimal

# def test_variable():

    NDIM = 3
    # BOUND_LOW, BOUND_UP = 0.0, 1.0
    BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
    RES_STR = '0.05'

    vset_bool = des_space.VariableList("boolean set", list())
    vset_ranged = des_space.VariableList("range set", list())

    # Variables
    for i in range(NDIM):
        this_var = des_space.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
        vset_ranged.append(this_var)

    print()
    for var in vset_ranged:
        print(var)

    assert type(vset_ranged[2].variable_tuple[0]) is decimal.Decimal

    for i in range(5):
        vset_bool.append(des_space.Variable.as_bool('This Bool'))

    assert len(vset_ranged) == 3

    variable_lists = [vset_bool, vset_ranged]

    this_ds = des_space.DesignSpace(variable_lists)

    print(this_ds)

    this_ds.print_design_space()

    # this_allele = this_ds.basis_set[0].return_random_allele2()
    # print(this_allele)

    # this_allele.vtype

    this_chromo = this_ds.gen_chromosome()

    this_ind = evo_space.Genome(this_chromo)
    print(this_ind)







