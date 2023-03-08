# This set of tests aims to ensure consistency between MS2732B_DRIVER 
# and MS2732B_VISA_DRIVER implementations.

import pytest
import inspect
from qodevices.anritsu.MS2732B_driver import AnritsuMS2732BDriver as tmc_d
from qodevices.anritsu.MS2732B_VISA_driver import AnritsuMS2732BDriver as visa_d

def test_class_method_1():
    """tmc_d should not have more methods than visa_d"""
    p = set(tmc_d.__dict__.keys()).difference(set(visa_d.__dict__.keys()))
    assert len(p) == 0

def test_class_method_2():
    """tmc_d should have 2 less method than visa_d"""
    p = set(visa_d.__dict__.keys()).difference(set(tmc_d.__dict__.keys()))
    assert p == {'__getattr__', 'ask'}

def test_equal_method_docstring():
    """Ensure functions and docstrings are same."""
    methods = set(visa_d.__dict__.keys()).intersection(set(tmc_d.__dict__.keys()))
    # ensure identical doc string for everything except init
    assert all([getattr(tmc_d, m).__doc__ == getattr(visa_d, m).__doc__ for m in methods.difference({'__init__'})])
        
def test_equal_method_source():
    """Ensure functions and source are same."""
    # methods = set(visa_d.__dict__.keys()).intersection(set(tmc_d.__dict__.keys()))
    # ensure identical doc string for everything except init
    # assert all([inspect.getsource(getattr(tmc_d, m)) == inspect.getsource(getattr(visa_d, m)) for m in methods.difference({'__init__'}) if callable(getattr(visa_d, m))])
    visa_l, _ = inspect.getsourcelines(visa_d)
    tmc_l, _ = inspect.getsourcelines(tmc_d)
    start_line = '    def write_to_device(self) -> None:\n'
    # init methods are different from write_to_device method down.
    visa_l_st = visa_l.index(start_line)
    tmc_l_st = tmc_l.index(start_line)
    assert visa_l[visa_l_st:] == tmc_l[tmc_l_st:]
