from astropy import units as u
import uncertainties
import numpy as np


class UQuantity(u.Quantity):

    def __new__(cls, value, uncertainty, unit=None, dtype=None, copy=True):

        self = super(UQuantity, cls).__new__(
                cls, value, unit, dtype=dtype, copy=copy)

        self.uncertainty = uncertainty
        self.uncert_object = uncertainties.ufloat(self.value, self.uncertainty)

        return self



    def __array_finalize__(self, obj):

        if obj is None:
            return

        self.uncertainty = getattr(obj, 'uncertainty', None)

        if isinstance(obj, UQuantity):
            self.uncert_object = uncertainties.ufloat(getattr(obj, 'value'), self.uncertainty)
        else:
            # ufloat is not defined for ufloat(None, None) so we set uncert_object to None
            self.uncert_object = None



    def __add__(self, other):
        output_object = super(UQuantity, self).__add__(other)

        output_object.uncert_object = self.uncert_object + other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __radd__(self, other):
        return other + self

    def __sub__(self, other):
        output_object = super(UQuantity, self).__sub__(other)

        output_object.uncert_object = self.uncert_object - other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __rsub__(self, other):
        return other - self

    def __mul__(self, other):
        output_object = super(UQuantity, self).__mul__(other)

        output_object.uncert_object = self.uncert_object * other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __rmul__(self, other):
        return other * self
