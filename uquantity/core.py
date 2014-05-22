from astropy import units as u
from uncertainties import ufloat


class UQuantity(object):

    def __init__(self, value, unit, uncertainty):
        self.value = value
        self.unit = unit
        self.uncertainty = uncertainty

        self.quantity = value * unit
        self.uncertObject = ufloat(value, uncertainty)

    def __add__(self, other):
        self.value = self.value + other.value
        self.uncertObject = self.uncertObject + other.uncertObject

        self.quantity = self.value * self.unit
        self.uncertainty = self.uncertObject.std_dev
        return self

    def __radd__(self, other):
        return other + self

    def __sub__(self, other):
        self.value = self.value - other.value
        self.uncertObject = self.uncertObject - other.uncertObject

        self.quantity = self.value * self.unit
        self.uncertainty = self.uncertObject.std_dev
        return self

    def __rsub__(self, other):
        return other - self


