"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
import unittest
import os

# Logging
import logging
logging.basicConfig(format='%(funcName)-20s %(levelno)-3s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")


# External 
#import xxx

# Own
from ExergyUtilities.utility_inspect import get_self, get_parent

#===============================================================================
# Testing
#===============================================================================
"""
creator

:param name: The name of the class to create.
:param base: A base class from which to inherit.
:param attribute: One or more attributes to add on instanciation of this
                  class, optional.

The following is used to create a class :class:`Foo` inheriting from the
standard :class:`list` and having an attribute :attr:`bar` being an empty
dictionary and a static attribute :attr:`spam` initialized to 1. ::

    create("Foo", list, bar=dict, spam=1)
    
This above line is exactly the same as defining in the :mod:`creator`
module something like the following. ::

    class Foo(list):
        spam = 1
        
        def __init__(self):
            self.bar = dict()

The :ref:`creating-types` tutorial gives more examples of the creator
usage.
"""

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        
    def test010_empty(self):
        print("**** TEST {} ****".format(get_self()))
