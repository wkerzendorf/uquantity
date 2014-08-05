from astropy import units as u
import numpy as np
import uncertainties as uncert
#import uncertlib.uncertainties as uncert


class SlotlessMeta(type):
    def __new__(meta, name, bases, dct):

        new_bases = ()

        for base in bases:
            #print "Dict of %s: %s" % (base, base.__dict__)
            new_base_dict = base.__dict__.copy()
            try:
                del new_base_dict['__slots__']
                new_base = type(str(base), (), new_base_dict)
            except KeyError:
                print "No __slots__ in %s" % base
                new_base = base


            new_bases = new_bases + (new_base,)

        new = type(name, new_bases, dct)
        return new


class UQuantity(uncert.Variable, u.Quantity):

    __metaclass__ = SlotlessMeta

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


    def __numpy_ufunc__(self, ufunc, method, i, inputs, **kwargs):
        print 'In UQuantity.__numpy_ufunc__'
        print inputs

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
