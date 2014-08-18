************************************************************
Automatic Uncertainty Propagation for Quantity (`uquantity`)
************************************************************

Introduction
============

The `uquantity` package modifies `astropy.units.Quantity` to implement automatic
propagation of uncertainties using the package `uncertainties`.

Getting Started
===============

|UQuantity| uses the `astropy.units` package to represent a value with a unit and standard deviation.

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
Gaussian distribution of that standard deviation that is centered on the value having physical units. The 
value (or center), standard deviation, and unit are accessed through the fields value, std_dev, and unit respectively.

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

Operations from `numpy` work on |UQuantity| objects, with proper propagation of uncertainty.

    >>> import numpy as np

    >>> angle = UQuantity(1.32, 0.01, u.rad)
    >>> np.sin(angle)
    <UQuantity 0.968715+/-0.002481 rad>

Independent variables are tracked when calculating the uncertainty. A simple example is where a
variable is subtracted from itself, the expected uncertainty should be zero, rather than its
uncertainty propagated.

    >>> a = UQuantity(1.0, 0.2, u.km)
    >>> a - a
    <UQuantity 0.0+/-0.0 km>

The tracking carries across multiple independent operations.

    >>> a = UQuantity(1.0, 0.2, u.km)
    >>> b = UQuantity(8.0, 2.1, u.Unit("km2"))
    >>> area = a**2
    >>> area_2 = area + b
    >>> area_2
    <UQuantity 9.0+/-2.13775583264 km2>
    >>> (area_2 - b) / a
    <UQuantity 1.0+/-0.2 km>

Technical Guide
===============

|UQuantity| is a mixin class that inherits |Quantity| from Astropy and |Variable| from `uncertainties`.
|Quantity| is part of the `units` package and is Astropy's class for representing physical quantities
with units. |Quantity| inherits from Numpy's class |ndarray| and provides all of the machinery needed
for working with n-dimensional arrays of physical quantities. |UQuantity| preserves this compatibility
with Numpy by implementing the method __numpy_ufunc__ for handling Numpy's universal functions.

|Variable| is a class within `uncertainties` that represents a Gaussian probability distribution with
a center and standard deviation. |Variable| uses automatic differentiation to propagate uncertainties
and tracks the calculated derivatives of variables through chains of operations. Because the variables
that go into an end result are tracked, correlations are handled transparently.

Non-cooporative multiple inheritance in Python does present some difficulties. Luckily in this case 
|Quantity| inheriting from |ndarray| meant that it uses the methods __new__ and __array_finalize__ for
initialization while |Variable| uses __init__. This allows |UQuantity| to call each parent initializer
seperately, rather than having to use wrappers around each parent to get super() to work.

One rather severe issue that arises from the two parent classes not being written to work with eachother
is their treatment of the __slots__ field. The field __slots__ is a special field that causes the object
defining it to be stored statically, rather than as a dynamic dictionary. Space savings from this can be
quite large, but it does not interact well with inheritance. Specifically, inheriting from |Quantity| and
|Variable| causes a base layout error. To get around this a metaclass is used that removes the __slots__
definition from any parent; __slots__ is then redefined in |UQuantity|.
