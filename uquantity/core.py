from astropy import units as u
import uncertainties
import numpy as np


class UQuantity(u.Quantity):

    def __new__(cls, value, uncertainty, unit=None, dtype=None, copy=True):

        if isinstance(value, u.Quantity):
            if unit is not None:
                value = value.to(unit).value
            else:
                unit = value.unit
                value = value.value

        if isinstance(uncertainty, uncertainties.Variable):
            uncertainty = uncertainty.std_dev


        try:
            value = np.asarray(value)
        except ValueError as e:
            raise TypeError(str(e))

        if unit is None:
            raise u.UnitsError("No unit was specified")

        self = super(UQuantity, cls).__new__(
                cls, value, uncertainty, unit, dtype=dtype, copy=copy)

        return self

    def __array_finalize__(self, obj):

        if obj is None:
            return

        self.uncert_object = ufloat(getattr(obj, 'value', None),
                getattr(obj, 'uncertainty', None))

        self.quantity = getattr(obj, 'value', None) * getattr(obj, 'unit', None)

    # To be replaced by __new__ and __array_finalize__
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

    def __mul__(self, other):
        self.value = self.value * other.value
        self.uncertObject = self.uncertObject * other.uncertObject

        self.quantity = self.value * self.unit * other.unit
        self.unit = self.quantity.unit
        self.uncertainty = self.uncertObject.std_dev
        return self
