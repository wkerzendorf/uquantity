from astropy import units as u
import numpy as np
#import uncertainties as uncert
import uncertlib.uncertainties as uncert

class UQuantity(uncert.Variable, u.Quantity):

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

        wrapped_ufunc = uncert.wrap(ufunc)
        return wrapped_ufunc(*inputs, **kwargs)

    def __repr__(self):
        return '<UQuantity %s+/-%s %s>' % (self.value, self.std_dev, self.unit)

    @property
    def value(self):
        return self._nominal_value


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
