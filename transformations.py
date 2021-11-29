from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord


def cartesian_to_euclidean_distance(x, y, z):
    """
    A simple function converting 3D cartesian coordinate into
    euclidean distance

    Parameters
    ----------
    x, y, z: float, float, float
        x-, y- and z-coordinates

    Returns
    -------
    Eucidean distance
    """
    return ((x ** 2) + (y ** 2) + (z ** 2))**0.5


def helio_to_galacto(dist_kpc, glon, glat=0.0, cartesian=True):
    """
    Convert coordinate from heliocentric to galactocentric system, given its
    heliocentric distance, galactic longitude and galactic latitude (optional).

    Parameters
    ----------
    dist_kpc: float
        Heliocentric distance (kpc)
    glon, glat: float, float
        Galactic longitude and latitude (decimal degrees). Galactic latitude is
        set to 0 as default.
    cartesian: bool
        If set to True, return cartesian coordinate; else, return
        galactocentric distance

    Returns
    -------
    Either galactocentric cartesian coordinate (default) or
    galactocentric distance
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
    if cartesian is True:
        # y.value in SkyCoord is x-axis in our system, and vice versa.
        return c_galacto.y.value, -c_galacto.x.value, c_galacto.z.value
    else:
        return cartesian_to_euclidean_distance(c_galacto.y.value,
                                               -c_galacto.x.value,
                                               c_galacto.z.value)


class ConvertUnit:
    """
    Convert a coordinate to other system and/or unit. Can also change the frame
    from icrs to fk5 or fk4, though not encouraged.

    Attributes
    ----------
    xcoord, ycoord: str/ list of string, str/ list of string
        x- and y- coordinate. Ideally RA and DEC (hour angle)
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

    def __init__(self, xcoord, ycoord, unit=(u.hourangle, u.deg),
                 frame='icrs'):
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


if __name__ == "__main__":
    print(ConvertUnit(['12:28:35.74'], ['-62:58:35.4']).to_eq_deg())
    print(ConvertUnit('12:28:35.74', '-62:58:35.4').to_eq_deg())
