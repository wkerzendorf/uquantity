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
