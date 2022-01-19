# Coordinate Helper
Small commonly-used snippets for ALMAGAL date, to help with transformation between different coordinate systems.

Credit of the code in coordinate_helper/kdist.py goes to [tvwenger](https://github.com/tvwenger/kd)

## Requirements
The following packages are required for this module to work:

- `astropy`
- `numpy`

As for the versions used here, please refer to requirements.txt or pyproject.toml.

This module, along with the dependencies stated in pyproject.toml, can be installed directly by  

```
pip install git+https://github.com/K-Monty/coordinate-helper.git
```

The source code can also be downloaded [here](https://github.com/K-Monty/coordinate-helper/releases).

## How to use
See [Galaxy model example](https://github.com/K-Monty/galaxy-model/blob/main/example.py) for a use case.

Individual functions within the `transformation` module (coordinate_helper/transformation.py):

1. `cartesian_coord_to_euclidean_distance(x: Number, y: Number, z: Number)` converts a 3D cartesian coordinate to euclidean distance from (0, 0, 0)

2. `galactic_helio_to_galacto(dist_kpc: Number, glon: Number, glat=0.0)` converts a 2D or 3D heliocentric (galactic) coordinate to galactocentric coordinate. If glat is set as default (0.0) the z-coordinate of the output will also be 0.0.

3. `ConvertUnit(xcoord, ycoord, unit=(u.hourangle, u.deg), frame='icrs')` class takes in xcoord (default: RA in string or a list of RA strings) and ycoord (default: Dec in string or a list of Dec strings), and convert them to either equatorial degrees (`.to_eq_deg()`) or galactic degrees (`.to_gal_deg()`). If the input is not RA & Dec ('hh:mm:ss'), the unit and/or frame need to be changed accordingly.  See [SkyCoord](https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html) for more details. 
