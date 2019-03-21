#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
# 02 - 2012JUN15 - Major overhaul of all code, simplification
#===============================================================================

"""This module does stuff
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
# from __future__ import division
# from __future__ import print_function

# Setup
import logging.config

# Standard library
from decimal import Decimal
import random
# from gamete import evolution_space
from gamete.evolution_space import Allele
#import time
# import itertools
# import sys
#import imp
# import datetime

# External library
#import numpy as np

# Utilites
# import sqlalchemy as sa
#import ExergyUtilities.utility_SQL_alchemy as util_sa
#from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from copy import deepcopy

# from gamete.mj_utilities.db_base import DB_Base

# from operator import mul, truediv
#===============================================================================
# Code
#===============================================================================


def generate_chromosome(basis_set):
    """Simple utility to order the values and names
    """
    variable_names = tuple([var.name for var in  basis_set])
    variable_indices = tuple([var.index for var in  basis_set])
    variableValues = tuple([var.value for var in basis_set])

    return zip(variable_names,variable_indices,variableValues)

#--- Design space
class VariableList(list):
    def __init__(self, name, list_items):
        self.name = name
        super().__init__(list_items)


class Variable():
    """
    A general variable object, inherited by specific types

    Init Attributes
    name - A label for the variable. Required.
    variable_tuple - The k-Tuple of possible values
    ordered= True - Flag

    Internal Attributes
    index = None - The corresponding index of the generated value
    value = The current value of the variable, defined by the index

    Possible types:
        - int
        - float
        - string
        - bool
    """

    def __init__(self, name, vtype, variable_tuple, ordered):
        self.vtype = vtype
        self.name = name
        self.locus = -1

        assert variable_tuple
        assert len(variable_tuple)

        if isinstance(variable_tuple,tuple):
            pass
        elif isinstance(variable_tuple,int):
            variable_tuple = (variable_tuple,)
        elif isinstance(variable_tuple, list):
            variable_tuple = tuple(variable_tuple)
        elif isinstance(variable_tuple, str):
            variable_tuple = tuple([variable_tuple])
        elif isinstance(variable_tuple, float):
            variable_tuple = (variable_tuple,)
        else:
            raise Exception("Need a list, int, float, or tuple")

        self.variable_tuple = variable_tuple

        # TODO: Assertion?
        try:
            len(variable_tuple)
        except:
            print('Initialize with a list or tuple')
            raise

        self.ordered = ordered

        self._index = None

        logging.debug("{}".format(self))

    @property
    def val_str(self):
        return str(self.variable_tuple[self._index])

    @property
    def value(self):
        return self.variable_tuple[self._index]

    @classmethod
    def as_bool(cls, name):
        return cls(name, 'bool', [True, False], False)

    @classmethod
    def from_range(cls, name, vtype, lower, resolution, upper):
        """
        Init overload - easy creation from a lower to upper decimal with a step size
        Arguments are string for proper decimal handling!
        """
        # Make sure we have STRING inputs for the decimal case
        if (not (isinstance(lower,str) or isinstance(lower,unicode) )or
            not (isinstance(resolution,str) or isinstance(resolution,unicode) ) or
            not (isinstance(upper,str)or isinstance(upper,unicode) ) ):
            raise TypeError("""Expect all numbers as strings,
            i.e. "0.01" with quotes. This is to ensure decimal precision.\n
            Your input: {} - {} - {} Var: {}
            Types: {}, {}, {}
            """.format(lower, resolution, upper, name , type(lower), type(resolution), type(upper)))


        lower = Decimal(lower)
        resolution = Decimal(resolution)
        upper = Decimal(upper)

        assert upper > lower, "Upper range must be > lower"
        assert not (upper - lower) % resolution, "Variable range is not evenly divisble by step size this is not supported.".format(upper,lower, resolution)

        # Assemble a list
        length = (upper - lower) / resolution + 1
        vTuple = [lower + i * resolution for i in range(0,int(length))]

        return cls(name, vtype, vTuple, True)

    @classmethod
    def ordered(cls, name, vtype, vTuple):
        """
        Init overload - the variable is ordered (default)
        """
        return cls(name, vtype, vTuple, True)

    @classmethod
    def unordered(cls,name, vtype, vTuple):
        """
        Init overload - the variable has no ordering
        """
        return cls(name, vtype, vTuple, False)

    def get_random(self):
        """
        Return a random value from all possible values
        """
        self._index = random.choice(range(len(self)))
        return self

    def get_indexed_obj(self, index):
        #raise
        self._index = index
        return Allele(self.name,
                      self.locus,
                      self.vtype,
                      self.val_str,
                      self._index,
                      self.ordered)

    def return_allele(self):
        return Allele(self.name,
                      self.locus,
                      self.vtype,
                      self.val_str,
                      self._index,
                      self.ordered)

    def return_closest_allele(self,target_value):
        
        assert self.vtype == 'float'

        # Get values as list of floats for comparison
        possible_values = [float(val.value) for val in  self.variable_tuple]
        # Get closest
        closest = min(possible_values, key=lambda x:abs(x-target_value))
        
        # Get the index of this value and update variable index to match
        closest_index= possible_values.index(closest)
        self._index = closest_index
        
        return Allele(self.name,
                      self.locus,
                      self.vtype,
                      self.val_str,
                      self._index,
                      self.ordered)

    # TODO: REMOVE
    def return_random_allele(self):
        """
        Return a random value from all possible values
        """
        raise Exception("depreciated")
        self._index = random.choice(range(len(self)))
        
        return Allele(self.name,
                      self.locus,
                      self.vtype,
                      self.val_str,
                      self._index,
                      self.ordered)

    def return_random_allele2(self, chromo_name):
        """
        Return a random value from all possible values
        """

        self._index = random.choice(range(len(self)))

        return Allele(self.name,
                      chromo_name,
                      self.locus,
                      self.vtype,
                      self.value,
                      self._index,
                      self.ordered)

    def get_new_random(self):
        """
        Return a new random value from all possible values
        """
        raise Exception("Obselete??")
        assert(len(self) > 1)

        if self.value == "<UNINITIALIZED>" :
            raise Exception("This variable is not initialized, can't step")
        valueList = list(self.variable_tuple)

        valueList.remove(self.value)
        self.value = random.choice(valueList)

        return self

    def step_random(self, start_index, step_size = 1):
        """ Step in a random direction (up or down) step_size within the possible values
        Must be ordered, otherwise this makes no sense

        """

        assert(self.ordered), "Stepping in variable only makes sense for an ordered list -change to ORDERED"

        if self.value == "<UNINITIALIZED>" :
            raise Exception("This variable is not initialized, can't step without a starting point")

        if self.ordered:
            upperIndexBound = len(self) - 1
            lowerIndexBound = 0
            currentIndex = self._index

            move = random.choice([    1 * step_size   ,   -1 * step_size   ])
            newIndex = currentIndex + move

            if newIndex < lowerIndexBound:
                newIndex = lowerIndexBound
            elif newIndex > upperIndexBound:
                newIndex = upperIndexBound
            else:
                pass

            self._index = newIndex

            return self

    def this_val_str(self):
        
        """
        String for current name and current value
        """
        return "{}[{}] := {}".format(self.name, self._index, self.val_str)

    def __len__(self):
        """
        The number of possible values
        """
        return len(self.variable_tuple)

    def long_str(self):
        """
        Print all info in variable
        """
        shortTupleString = str(self.variable_tuple)
        maxStrLen = 40
        if len(shortTupleString) > maxStrLen:
            try:
                shortTupleString = "({}, {}, ..., {})".format(str(self.variable_tuple[0]),str(self.variable_tuple[1]),str(self.variable_tuple[-1]))
            except:
                pass

        if self._index == None:
            generatedValueStr = "<UNINITIALIZED>"
        else:
            generatedValueStr = self.val_str

        if self.ordered:
            ordStr = "Ordered"
        elif not self.ordered:
            ordStr = "Unordered"

        return "{} = {} length: '{}', {}, {}".format(
                                 self.name,
                                 generatedValueStr,
                                 len(self.variable_tuple),
                                 shortTupleString,
                                 # id(self),
                                 self.vtype,
                                 )

    def __str__(self):
        return self.long_str()
    
    def __repr__(self):
        return self.long_str()

    def next(self):
        """
        Iterator over tuple of values
        Ordering does not matter, will simply return values in the order of the tuple regardless
        """
        if self.iterIndex < len(self.variable_tuple):
            self._index = self.iterIndex
        else:
            raise StopIteration

        self.iterIndex += 1

        return self

    def __iter__(self):
        self.iterIndex = 0
        return self




class DesignSpace(object):

    def __init__(self, variable_lists):
        """
        The DSpace

        Creation:
        variable_lists, a list of lists of Variable objects

        Attr:
        dimension: Number of Basis sets
        cardinality: The total number of points
        """

        self.basis_set = list()
        self.variable_set = list()
        self.positions = list()
        cnt = 0
        for v_list in variable_lists:
            this_name = v_list.name
            for var in v_list:

                self.basis_set.append(var)
                self.variable_set.append(this_name)
                self.positions.append(cnt)
                cnt +=1

        for var in self.basis_set:
            assert var.name not in ["hash", "start", "finish"]

    def print_design_space(self):
        for var_def in zip(self.positions, self.variable_set, self.basis_set):
            print(var_def)

    def __str__(self):
        return "DesignSpace: Dimension: {0}, Cardinality: {1}".format(self.dimension, self.cardinality)

    def __repr__(self):
        return self.__str__()

    @property
    def cardinality(self):
        """
        The cardinality of a set is a measure of the "number of elements of the set"
        """
        size = 1
        for var in self.basis_set:
            size *= len(var)
        return size

    @property
    def dimension(self):
        """
        The definition of dimension of a space is the number of vectors in a basis
        The dimension of a vector space is the number of vectors in any basis for the space
        """
        return len(self.basis_set)

    def gen_chromosome(self):
        chromosome = list()
        for var, chromo_name in zip(self.basis_set, self.variable_set):
            this_allele = var.return_random_allele2(chromo_name)
            chromosome.append(this_allele)
        return chromosome
        # this_ind = self.individual(chromosome=chromosome)


