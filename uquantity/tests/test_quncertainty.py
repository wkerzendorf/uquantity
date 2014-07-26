from astropy import units as u
from uquantity import UQuantity
import math


def test_simple_uquantity():
    ###
    a = UQuantity(5, 2, u.km)
    ##
    assert a.value == 5
    assert a.unit == u.km
    assert a.std_dev == 2

def test_init_from_quantity_uquantity():
    ###
    a = 5 * u.km
    b = UQuantity(a, 2)
    ##
    assert b.value == 5
    assert b.unit == u.km
    assert b.std_dev == 2

def test_addition_uquantity():
    ###
    a = UQuantity(5, 2, u.km)
    b = UQuantity(12, 5, u.km)
    c = a + b
    ##
    assert c.value == 17
    # Verify that value within Uncertainty is correct
    assert c.unit == u.km
    # Uncertainties under addition add in quadrature
    assert c.std_dev == math.sqrt(2**2 + 5**2)

def test_subtraction_uquantity():
    ###
    a = UQuantity(5, 2, u.km)
    b = UQuantity(12, 5, u.km)
    c = b - a
    ##
    assert c.value == 7
    # Verify that value within Uncertainty is correct
    assert c.unit == u.km
    # Uncertainties under subtraction add in quadrature
    assert c.std_dev == math.sqrt(2**2 + 5**2)

def test_multiplication_uquantity():
    ###
    a = UQuantity(8, 2, u.N)
    b = UQuantity(20, 5, u.m)
    c = a * b
    ##
    assert c.value == 160

    assert c.unit == u.Unit("m N")
    # Fractional uncertainties under multiplication add in quadrature
    assert (c.std_dev/160) == math.sqrt((2/8.0)**2+(5/20.0)**2)

def test_division_uquantity():
    ###
    a = UQuantity(20, 3, u.m)
    b = UQuantity(5, 2, u.s)
    c = a / b
    ##
    assert c.value == 4

    assert c.unit == u.Unit("m / s")
    # Fractional uncertainties under division add in quadrature
    assert (c.std_dev/4.0) == math.sqrt((3/20.0)**2 + (2/5.0)**2)
