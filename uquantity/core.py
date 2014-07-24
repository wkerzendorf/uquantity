from astropy import units as u
import numpy as np
from uncertlib.uncertainties import Variable, ufloat


class UQuantity(Variable, u.Quantity):

    def __new__(cls, value, uncertainty, unit=None, dtype=None, copy=True):

        if hasattr(value, 'unit'):
            unit = value.unit
            value = value.value

        value = float(value) # Makes uncertainties happy
        self = super(UQuantity, cls).__new__(
                cls, value, unit, dtype=dtype, copy=copy)

        self._std_dev = uncertainty

        return self



    def __array_finalize__(self, obj):

        if obj is None:
            return

        self._std_dev = getattr(obj, 'std_dev', None)

        self.__slots__ =  ('_std_dev', 'tag', '_nominal_value', 'derivatives')

    def __numpy_ufunc__(self, ufunc, method, i, inputs, **kwargs):
        print 'In UQuantity.__numpy_ufunc__'

        return super(UQuantity, self).__numpy_ufunc__(ufunc, method, i, inputs, **kwargs)

    def __repr__(self):
        return '<UQuantity %s+/-%s %s>' % (self.value, self.std_dev, self.unit)



    def __add__(self, other):
        return np.add(self, other)

    def __radd__(self, other):
        return other + self

    def __sub__(self, other):
        return np.subtract(self, other)

    def __rsub__(self, other):
        return other - self

    def __mul__(self, other):
        return np.multiply(self, other)

    def __rmul__(self, other):
        return other * self

    def __div__(self, other):
        return np.divide(self, other)
