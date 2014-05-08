from astropy import units as u
from uquantity import UQuantity


def test_simple_uquantity():
    ###
    a = UQuantity(5, u.km, 2)
    ##
    assert a.value == 5
    assert a.unit == u.km
    assert a.uncertainty == 2

