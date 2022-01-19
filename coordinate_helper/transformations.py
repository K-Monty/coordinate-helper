#!/usr/bin/env python

# Module level dunder names
__author__ = 'K-Monty'
__copyright__ = 'Copyright 2022,coordinate-helper'
__license__ = 'GNU v3'
__version__ = '0.1.0'
__maintainer__ = 'K-Monty'
__email__ = 'kmgoh1995@gmail.com'


from numbers import Number
from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord


def cartesian_coord_to_euclidean_distance(x: Number, y: Number, z: Number):
    """
    A simple function converting 3D cartesian coordinate into
    euclidean distance

    Parameters
    ----------
    x, y, z: numerical
        x-, y- and z-coordinates

    Returns
    -------
    Eucidean distance
    """
    return ((x ** 2) + (y ** 2) + (z ** 2))**0.5


def galactic_helio_to_galacto(dist_kpc: Number, glon: Number, glat=0.0):
    """
    Convert coordinate from (galactic) heliocentric to galactocentric
    coordinate system, given its heliocentric distance,
    galactic longitude and galactic latitude (optional).

    Parameters
    ----------
    dist_kpc: Number
        Heliocentric distance (kpc)
    glon, glat: Number, Number (optional)
        Galactic longitude and latitude (decimal deg). Galactic latitude is
        set to 0 as default.

    Returns
    -------
    Galactocentric cartesian coordinate (tuple)
    """

    solar_dist = 8.15*u.kpc  # 8.15 kpc from GC
    z_sun = 5.5*u.pc  # 5.5 pc from Galactic mid-plane

    c = SkyCoord(l=glon*u.degree,
                 b=glat*u.degree,
                 frame='galactic',
                 distance=dist_kpc*u.kpc)
    c_galacto = c.transform_to(coord.Galactocentric(
                                            galcen_distance=solar_dist,
                                            z_sun=z_sun))

    # y.value in SkyCoord is x-axis in my galaxy model, and vice versa.
    return c_galacto.y.value, -c_galacto.x.value, c_galacto.z.value


class ConvertUnit:
    """
    Convert a coordinate to other system and/or unit. Can also change the frame
    from icrs (default) to fk5 or fk4 if needed.

    Attributes
    ----------
    xcoord, ycoord: str/ list of string, str/ list of string of x- and y-
        coordinate. The default input is RA and DEC (hourangle); otherwise,
        need to reset self.unit and self.frame.
        See astropy.coordinates.SkyCoord for setting options
    unit: str, tuple
        Units for supplied coordinate values. If only one unit is supplied, it
        will be applied to all values
    frame: str
        default 'icrs'

    Methods
    -------
    to_eq_deg()
        convert the coordinate to equatorial system (deg)
    to_gal_deg()
        convert the coordinate to galactic system (deg)
    """

    def __init__(self, xcoord, ycoord, unit=(u.hourangle,
                 u.deg), frame='icrs'):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.unit = unit
        self.frame = frame
        self.skycoordobj = self._create_skycoordobj()

    def _create_skycoordobj(self):
        return coord.SkyCoord(
                    self.xcoord, self.ycoord, unit=self.unit, frame=self.frame)

    def to_eq_deg(self):
        """
        Returns
        -------
        RA and DEC values.
        If the xcoord and ycoord attributes are strings, a tuple (RA, DEC) will
        be returned. Else, an array of RAs (arr[0]) and DECs (arr[1])
        will be returned.
        """
        return self.skycoordobj.icrs.ra.value, \
            self.skycoordobj.icrs.dec.value

    def to_gal_deg(self):
        """
        Returns
        -------
        GLON and GLAT values.
        If the xcoord and ycoord attributes are strings, a tuple (GLON, GLAT)
        will be returned. Else, an array of GLONs (arr[0]) and GLATs (arr[1])
        will be returned.
        """
        return self.skycoordobj.galactic.l.value, \
            self.skycoordobj.galactic.b.value
