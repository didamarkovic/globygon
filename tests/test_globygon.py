"""
Test the functionality of globygon
"""
import numpy as np
from globygon import globygon as gb
import matplotlib.pyplot as plt

def test__convert_Cartesian_to_RADec():
    """
    Testing the method that converts Cartesian coordinates to RA/Dec
    """

    # One point right at the center - This calculation should throw an
    # exception!
    x = np.array([0., 1.])
    y = np.array([0., 1.])
    z = np.array([0., 1.])
    ct = gb.Catalog(None, None)
    try:
        ct._convert_Cartesian_to_RADec(x, y, z)
    except:
        pass

    # Points at the poles
    x = np.array([1., 0., 0.])
    y = np.array([0., 1., 0.])
    z = np.array([0., 0., 1.])
    ct = gb.Catalog(None, None)
    RA, Dec = ct._convert_Cartesian_to_RADec(x, y, z)
    assert np.all(np.equal(RA, [0., np.pi/2, 0.]) & np.equal(Dec, [0., 0., np.pi/2.]))

def test_calculate_center_of_mass():
    """
    Testing that the center-of-mass calculation actually works
    """
    
    # Symmetric RA/Decs should give center-of-mass for points as (0, 0)
    RA_list = np.array([-np.pi/4, np.pi/4, 0., 0.])
    Dec_list = np.array([0., 0., 0., 0.])
    ct = gb.Catalog(RA_list, Dec_list)
    assert ct.calculate_center_of_mass() == (0., 0.)

    # Single RA/Dec point should give center-of-mass as the point itself
    RA_list = np.array([0.])
    Dec_list = np.array([0.])
    ct = gb.Catalog(RA_list, Dec_list)
    assert ct.calculate_center_of_mass() == (0., 0.)

#test_calculate_center_of_mass()
test__convert_Cartesian_to_RADec()
