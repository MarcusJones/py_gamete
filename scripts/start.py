#%%
from gamete import design_space as ds
import deap as dp
import deap.creator
import deap.base
#%%
NDIM = 3
BOUND_LOW, BOUND_UP = 0.0, 1.0
BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
RES_STR = '0.10'

# --- Variables
basis_variables = list()
# for i in range(NDIM):
#     this_var = ds.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
#     basis_variables.append(this_var)

for i in range(23):
    basis_variables.append(ds.Variable.as_bool('{}'.format(i)))

# r = ds.Variable.as_bool('test')

#%%
design_space = ds.DesignSpace(basis_variables)
print(design_space)
raise
design_space.print_design_space()

obj1 = ds.Objective('obj1', 'Max')
obj2 = ds.Objective('obj2', 'Min')
objs = [obj1, obj2]
obj_space1 = ds.ObjectiveSpace(objs)

fitness = ds.Fitness
# ((-1.0, -1.0), ('obj1', 'obj2'))
#%%

# --- Mapping
dp.creator.create("FitnessMin", dp.base.Fitness, weights=(-1.0, -1.0))
print(dp.creator.FitnessMin)
dp.creator.create("Individual", ds.Individual, fitness=dp.creator.FitnessMin)
print(dp.creator.Individual)

mapping = ds.Mapping(design_space, obj_space1, dp.creator.Individual)

#%%

pop = mapping.get_random_population(20, flg_verbose=True)

r = pop[1]
print(r)
dir(dp)
print(obj_space1)

ds.Variable

ds.Allele
