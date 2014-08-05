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

def test_gravitation_uquantity():
    ###
    G = UQuantity(6.67384e-11, 1.2e-4, (u.N * (u.m / u.kg)**2)) # Gravitational constant
    m1 = UQuantity(1e15, 1e5, u.kg)
    m2 = UQuantity(100, 10, u.kg)
    r = UQuantity(10000, 500, u.m)
    F = G * (m1 * m2) / r**2
    ###
    assert F.value == 6.67e-11 * (1e15 * 100) / 10000**2

    assert F.unit == u.N
    # Uncertainties calculated using partial derivative method

