from astropy import units as u
import numpy as np
import uncertlib


class UQuantity(u.Quantity, uncertlib.Variable):

    def __new__(cls, value, uncertainty, unit=None, dtype=None, copy=True):

        self = u.Quantity.__new__(
                cls, value, unit, dtype=dtype, copy=copy)
        if isinstance(value, u.Quantity):
            # Handles the case of value being a Quantity by view casting
            uquant = self.view(cls)
            uquant._unit = self.unit
            self = uquant


        self.uncertainty = uncertainty
        self.uncert_object = uncertlib.ufloat(self.value, self.uncertainty)

        return self



    def __array_finalize__(self, obj):

        if obj is None:
            return

        self.uncertainty = getattr(obj, 'uncertainty', None)

        self.__slots__ =  ('_std_dev', 'tag', '_nominal_value', 'derivatives')

        if self.uncertainty is not None:
            self.uncert_object = uncertlib.ufloat(getattr(obj, 'value'), self.uncertainty)
        else:
            # ufloat is not defined for ufloat(None, None) so we set uncert_object to None
            self.uncert_object = None



    def __add__(self, other):
        output_object = super(UQuantity, self).__add__(other)
        output_object = output_object.view(UQuantity)
        output_object._unit = self.unit

        output_object.uncert_object = self.uncert_object + other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __radd__(self, other):
        return other + self

    def __sub__(self, other):
        output_object = super(UQuantity, self).__sub__(other)
        output_object = output_object.view(UQuantity)
        output_object._unit = self.unit

        output_object.uncert_object = self.uncert_object - other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __rsub__(self, other):
        return other - self

    def __mul__(self, other):
        output_object = super(UQuantity, self).__mul__(other)
        output_object = output_object.view(UQuantity)
        output_object._unit = self.unit * other.unit

        output_object.uncert_object = self.uncert_object * other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object

    def __rmul__(self, other):
        return other * self

    def __div__(self, other):
        output_object  = super(UQuantity, self).__div__(other)
        output_object = output_object.view(UQuantity)
        output_object._unit = self.unit / other.unit

        output_object.uncert_object = self.uncert_object / other.uncert_object
        output_object.uncertainty = output_object.uncert_object.std_dev

        return output_object
