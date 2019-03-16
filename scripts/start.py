#%%
from gamete import design_space as ds
import deap as dp
NDIM = 3
BOUND_LOW, BOUND_UP = 0.0, 1.0
BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
RES_STR = '0.10'

# --- Variables
basis_variables = list()
for i in range(NDIM):
    this_var = ds.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
    basis_variables.append(this_var)

design_space = ds.DesignSpace(basis_variables)
print(design_space)
design_space.print_design_space()

obj1 = ds.Objective('obj1', 'Max')
obj2 = ds.Objective('obj2', 'Min')
objs = [obj1, obj2]
obj_space1 = ds.ObjectiveSpace(objs)

fitness = ds.Fitness
# ((-1.0, -1.0), ('obj1', 'obj2'))

# --- Mapping
dp.creator.create("FitnessMin", dp.base.Fitness, weights=(-1.0, -1.0))
print(dp.creator.FitnessMin)
dp.creator.create("Individual", ds.Individual, fitness=dp.creator.FitnessMin)
print(dp.creator.Individual)

print(obj_space1)

ds.Variable

ds.Allele
