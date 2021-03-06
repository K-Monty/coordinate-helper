import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  # noqa
                                                '..')))

from coordinate_helper.transformations import cartesian_coord_to_euclidean_distance  # noqa
from coordinate_helper.transformations import galactic_helio_to_galacto  # noqa
from coordinate_helper.transformations import ConvertUnit  # noqa
from coordinate_helper.kdist import kdist  # noqa


class TestKdist(unittest.TestCase):
    def test_calc(self):
        self.assertEqual(round(kdist(45.071249509, 0.132582371, 60.0), 2),
                         4607.52)
        list1 = [round(x, 2) for x in kdist([32.796533448, 45.071249509],
                                            [0.191154023, 0.132582371],
                                            [15.0, 60.0])]
        list2 = [1217.29, 4607.52]
        self.assertEqual(list1, list2)


class TestCoordinateConversions(unittest.TestCase):
    def test_eq_deg_conversion(self):
        eq_deg_results = ConvertUnit(['13:11:14.44', '16:39:57.78'],
                                     ['-62:47:25.5', '-50:00:51.40']
                                     ).to_eq_deg()
        self.assertEqual(round(eq_deg_results[0][0], 2), 197.81)
        self.assertEqual(round(eq_deg_results[0][1], 2), 249.99)
        self.assertEqual(round(eq_deg_results[1][0], 2), -62.79)
        self.assertEqual(round(eq_deg_results[1][1], 2), -50.01)

    def test_gal_deg_conversion(self):
        gal_deg_results = ConvertUnit(['13:11:14.44', '16:39:57.78'],
                                      ['-62:47:25.5', '-50:00:51.40']
                                      ).to_gal_deg()
        self.assertEqual(round(gal_deg_results[0][0], 2), 305.19)
        self.assertEqual(round(gal_deg_results[0][1], 2), 335.62)
        self.assertEqual(round(gal_deg_results[1][0], 2), -0.01)
        self.assertEqual(round(gal_deg_results[1][1], 2), -2.23)


class TestHelioToGalacto(unittest.TestCase):
    def test_with_and_without_glat(self):
        self.assertNotEqual(galactic_helio_to_galacto(1.32, 351.416778966),
                            galactic_helio_to_galacto(1.32, 351.416778966,
                                                      0.645254241))

    def test_string_arg(self):
        self.assertRaises(TypeError, galactic_helio_to_galacto, (1.32,
                          '351.416778966'))

    def test_cartesian_bool(self):
        self.assertEqual(len(galactic_helio_to_galacto(1.32, 351.416778966)
                             ), 3)
        self.assertEqual(len([galactic_helio_to_galacto(
            1.32, 351.416778966,)]), 1)

    def test_conversion_values(self):
        test_case = galactic_helio_to_galacto(1.32, 351.416778966, 0.645254241)
        self.assertEqual(round(test_case[0], 2), -0.20)
        self.assertEqual(round(test_case[1], 2), 6.84)
        self.assertEqual(round(test_case[2], 2), 0.02)


class TestCartesianToEuclidean(unittest.TestCase):
    def test_dist(self):
        self.assertEqual(cartesian_coord_to_euclidean_distance(1, 1, 1),
                         (3)**0.5)

    def test_string_arg(self):
        self.assertRaises(TypeError, cartesian_coord_to_euclidean_distance,
                          ('1', '1', '1'))


if __name__ == "__main__":
    unittest.main()
