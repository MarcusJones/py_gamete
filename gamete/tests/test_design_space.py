#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
import unittest

# Utilities
#from config import *
from ExergyUtilities.utility_inspect import get_self
from ExergyUtilities.utility_logger import LoggerCritical, LOGGING_CONFIG_2

# Logging
import logging
logging.basicConfig(format=LOGGING_CONFIG_2, level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")

# Own
#from deap import design_space
#from deap_original import *
import design_space as ds
#from deap import *
#import deap.mj_utilities.util_db_process as util_proc
# from deap.mj_utilities.db_base import DB_Base

# DEAP
import sys

logging.debug(sys.version)

#sys.path.append(r"C:\Users\jon\git\deap")
#for dir in sys.path:
#    print(dir)
#raise
import deap as dp
import deap.creator
import deap.base
import sqlalchemy as sa


#===============================================================================
# Testing
#===============================================================================
class TestDesignSpace(unittest.TestCase):
    def setUp(self):
        pass
    
    def test010_get_pop(self):
        print("**** TEST {} ****".format(get_self()))
        
        NDIM = 3
        BOUND_LOW, BOUND_UP = 0.0, 1.0
        BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
        RES_STR = '0.10'
        
        #--- Variables
        basis_variables = list()
        for i in range(NDIM):
            this_var = ds.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
            basis_variables.append(this_var)
            
        #--- Design space
        thisDspace = ds.DesignSpace(basis_variables)
        D1 = thisDspace
        
        #--- Objective space
        obj1 = ds.Objective('obj1', 'Max')
        obj2 = ds.Objective('obj2', 'Min')
        objs = [obj1, obj2]
        obj_space1 = ds.ObjectiveSpace(objs)

        #--- Fitness
        fitness = ds.Fitness
        #((-1.0, -1.0), ('obj1', 'obj2'))

        #--- Mapping
        dp.creator.create("FitnessMin", dp.base.Fitness, weights=(-1.0, -1.0))
        print(dp.creator.FitnessMin)
        dp.creator.create("Individual", ds.Individual, fitness = dp.creator.FitnessMin)
        print(dp.creator.Individual)

        mapping = ds.Mapping(D1, obj_space1, dp.creator.Individual)

        mapping.get_random_population(20, flg_verbose = True)

class MappingPopulationTests2(unittest.TestCase):
    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        
        my_logger.setLevel("CRITICAL")
        
        #--- Engine
        self.engine = sa.create_engine('sqlite:///:memory:', echo=0)
        #engine = sa.create_engine('sqlite:///{}'.format(self.path_new_sql), echo=self.ECHO_ON)
        Session = sa.orm.sessionmaker(bind=self.engine)
        self.session = Session()
        logging.critical("Initialized session {} with SQL alchemy version: {}".format(self.engine, sa.__version__))
        
        NDIM = 3
        BOUND_LOW, BOUND_UP = 0.0, 1.0
        BOUND_LOW_STR, BOUND_UP_STR = '0.0', '.2'
        RES_STR = '0.10'
        
        #--- Variables
        basis_variables = list()
        for i in range(NDIM):
            this_var = ds.Variable.from_range("{}".format(i), 'float', BOUND_LOW_STR, RES_STR, BOUND_UP_STR)
            basis_variables.append(this_var)
            
        #--- Design space
        thisDspace = ds.DesignSpace(basis_variables)
        D1 = thisDspace
        
        #--- Objective space
        obj1 = ds.Objective('obj1', 'Max')
        obj2 = ds.Objective('obj2', 'Min')
        objs = [obj1, obj2]
        obj_space1 = ds.ObjectiveSpace(objs)

        #--- Fitness
        fitness = ds.Fitness

        #--- Mapping
        dp.creator.create("FitnessMin", dp.base.Fitness, weights=(-1.0, -1.0))
        dp.creator.create("Individual", ds.Individual, fitness = dp.creator.FitnessMin)
        self.mapping = ds.Mapping(D1, obj_space1, dp.creator.Individual)
        
    def test010(self):
        self.mapping.print_summary()
        print(self.mapping.individual)
        print(self.mapping.get_random_mapping())
        print(self.mapping.get_random_population(20, flg_verbose = True))
        #DB_Base.metadata.create_all(self.engine)    
        #self.session.add_all(basis_variables)        
        #self.session.commit()

    def test020_send_pop_DB(self):
        print("**** TEST {} ****".format(whoami()))
        #print(self.mapping)
        res_ORM_table = generate_individuals_table(self.mapping)
        #print(res_ORM_table)

        Results = generate_ORM_individual(self.mapping)
        #print(Results)
        
        sa.orm.mapper(Results, res_ORM_table) 

        DB_Base.metadata.create_all(self.engine)    
        self.session.commit() 
        
        with loggerCritical():
            pop = self.mapping.get_random_population(50)

        results = [convert_individual_DB(Results,ind) for ind in set(pop)]

        self.session.add_all(results)
        self.session.commit()

        #util_sa.print_all_pretty_tables(self.engine)
        
        #print(type(self.mapping.design_space.basis_set[0]))
        
        #raise
        #self.mapping.design_space.basis_set
        
        val_classes = [var.ValueClass for var in self.mapping.design_space.basis_set]
        qry = self.session.query(Results, *val_classes)
        for var in self.mapping.design_space.basis_set:
            #print("J")
            qry = qry.join(var.ValueClass)
        
        print(type(qry))
        
        for res, v1, v2, v3 in qry.all():
            print(res)
            #print(res[0])
            #print(type(res))
            #print(dir(res))
            #print(dir(res))
            #print(res.var_c_0)
            #raise
            #print(res)
            
