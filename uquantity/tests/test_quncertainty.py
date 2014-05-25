from astropy import units as u
from uquantity import UQuantity
import math


def test_simple_uquantity():
    ###
    a = UQuantity(5, u.km, 2)
    ##
    assert a.value == 5
    assert a.unit == u.km
    assert a.uncertainty == 2

def test_addition_uquantity():
    ###
    a = UQuantity(5, u.km, 2)
    b = UQuantity(12, u.km, 5)
    c = a + b
    ##
    assert c.value == 17
    # Verify that value within Quantity and Uncertainty are correct
    assert c.quantity.value == 17
    assert c.uncertObject.nominal_value == 17
    assert c.unit == u.km
    # Uncertainties under addition add in quadrature
    assert c.uncertainty == math.sqrt(2**2 + 5**2)

def test_subtraction_uquantity():
    ###
    a = UQuantity(5, u.km, 2)
    b = UQuantity(12, u.km, 5)
    c = b - a
    ##
    assert c.value == 7
    # Verify that value within Quantity and Uncertainty are correct
    assert c.quantity.value == 7
    assert c.uncertObject.nominal_value == 7
    assert c.unit == u.km
    # Uncertainties under subtraction add in quadrature
    assert c.uncertainty == math.sqrt(2**2 + 5**2)

def test_multiplication_uquantity():
    ###
    a = UQuantity(8, u.N, 2)
    b = UQuantity(20, u.m, 5)
    c = a * b
    ##
    assert c.value == 160
    assert c.uncertObject.nominal_value == 160
    assert c.quantity.value == 160

    assert c.unit == u.Unit("m N")
    # Fractional uncertainties under multiplication add in quadrature
    assert (c.uncertainty/160) == math.sqrt((2/8)**2+(5/20)^2)
