from astropy import units as u
import numpy as np
import uncertainties as uncert
#import uncertlib.uncertainties as uncert


# Eliminates base layout conflict by removing __slots__ fields from parent classes
class SlotlessMeta(type):
    def __new__(meta, name, bases, dct):

        new_bases = ()

        # Iterates through each parent class
        for base in bases:
            new_base_dict = base.__dict__.copy()
            try:
                del new_base_dict['__slots__']
                new_base = type(str(base), (), new_base_dict)
            except KeyError:
                # Avoids touching parents that do not need to be modified
                new_base = base

            new_bases = new_bases + (new_base,)

        return type(name, new_bases, dct)

class SlotlessVariable(uncert.Variable):
    __metaclass__ = SlotlessMeta

class UQuantity(SlotlessVariable, u.Quantity):

    __slots__ = ('_std_dev', 'tag')

    def __new__(cls, value, uncertainty, unit=None, tag=None, dtype=None, copy=True):

        if hasattr(value, 'unit'):
            unit = value.unit
            value = value.value

        value = float(value) # Makes uncertainties happy
        #self = super(UQuantity, cls).__new__(
        #        cls, value, unit, dtype=dtype, copy=copy)

        self = u.Quantity.__new__(cls, value, unit)
        self.isscalar = True

        # Recreation of code in Variable.__init__ and AffineScalarFunc.__init__
        # because the metaclass breaks super() calls
        self._nominal_value = value
        self.std_dev = uncertainty
        self.tag = tag
        self.derivatives = {self:1.}

        return self

    def __init__(self, *args, **kwargs):
        # Prevents Variable's __init__ from getting called
        pass

    def __array_finalize__(self, obj):

        if obj is None:
            return

    def __float__(self):
        return float(self.value)

    def __numpy_ufunc__(self, ufunc, method, i, inputs, **kwargs):
        print 'In UQuantity.__numpy_ufunc__'
        print inputs

        wrapped_ufunc = uncert.wrap(ufunc)
        var_inputs = uquantity_to_variable(inputs)
        print var_inputs

        return wrapped_ufunc(*var_inputs, **kwargs)

    def __repr__(self):
        return '<UQuantity %s+/-%s %s>' % (self.value, self.std_dev, self.unit)

    @property
    def value(self):
        return self.nominal_value

    @property
    def nominal_value(self):
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

def uquantity_to_variable(uquantities):
    out = ()
    # Likely needs optimization
    for uquan in uquantities:
        var = uncert.Variable(uquan.value, uquan.std_dev)
        out = out + (var,)
    return out

