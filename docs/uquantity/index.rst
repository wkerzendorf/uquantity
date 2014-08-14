************************************************************
Automatic Uncertainty Propagation for Quantity (`uquantity`)
************************************************************

Introduction
============

The `uquantity` package modifies `astropy.units.Quantity` to implement automatic
propagation of uncertainties using the package `uncertainties`.

Getting Started
===============

`uquantity` uses the `astropy.units` package to represent a value with a unit and standard deviation.

    >>> from uquantity import UQuantity
    >>> from astropy import units as u

    >>> a = UQuantity(15.5, 0.3, u.m)
    >>> a
    <UQuantity 15.5+/-0.3 m>
    >>> a.value
    15.5
    >>> a.std_dev
    0.3
    >>> a.unit
    Unit("m")

The constructor UQuantity takes a value, an uncertainty, and a unit and returns an object representing a
Gaussian distribution of that standard deviation that is centered on the value having physical units.

Using the python package `uncertainties` the standard deviation is propagated through mathematical operations.
Likewise units are handled just as they would be in Quantity.

    >>> a = UQuantity(15.5, 0.3, u.m)
    >>> b = UQuantity(12.1, 0.6, u.m)
    >>> sum = a + b
    >>> sum      # Under addition uncertainties add in quadrature
    <UQuantity 27.6+/-0.67082 m>
    >>> c = UQuantity(5.0, 0.1, u.s)
    >>> sum / c
    <UQuantity 5.52+/-0.173747403359 m / s>
