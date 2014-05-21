from astropy import units as u
from uncertainties import ufloat


class UQuantity(object):

    def __init__(self, value, unit, uncertainty):
        self.value = value
        self.unit = unit
        self.uncertainty = uncertainty

        self.quantity = value * unit
        self.uncertObject = ufloat(value, uncertainty)
