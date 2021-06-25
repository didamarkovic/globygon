"""
Test the functionality of globygon
"""
import numpy as np
from globygon import globygone as gb
import matplotlib.pyplot as plt

def test_Catalog_init():
    """
    Unit test for catalogue
    """
    
    n = 20
    test_RA = np.arange(0,np.pi*2,n)
    test_Dec = np.arange(0,np.pi,n)-np.pi/2
    
    cat = gb.Catalog(test_RA,test_Dec)
    
    assert hasattr(cat, 'RA')
    assert hasattr(cat, 'Dec')

def test_convert_RADec_to_Cartesian():
    """
    Testing the method that converts RA/Dec coordinates to Cartesian.
    """

    # Is r = 1?
    RA = np.pi*np.arange(0,100,1.)/50
    Dec = np.pi**np.arange(-50,50,1.)/100
    ct = gb.Catalog(RA,Dec)
    x,y,z = ct._convert_RADec_to_Cartesian()
    R = np.sqrt(x**2 + y**2 + z**2)

    assert np.all(np.isclose(R,1.))

    # Check equations setting RA=0 to simplify
    RA = np.array([0])
    Dec = np.array([np.pi/4, 0.2, 0.0]) # a bunch of arbitrary values
    ct = gb.Catalog(RA,Dec)
    x,y,z = ct._convert_RADec_to_Cartesian()
    assert np.all(np.isclose(x,np.cos(Dec)) & np.isclose(y,0.) & np.isclose(z,np.sin(Dec)))
   
    
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
    else:
        assert False, 'Point at origin should not work when converting to spherical'
    
    # Points at the poles
    x = np.array([1., 0., 0.])
    y = np.array([0., 1., 0.])
    z = np.array([0., 0., 1.])
    ct = gb.Catalog(None, None)
    RA, Dec = ct._convert_Cartesian_to_RADec(x, y, z)
    assert np.all(np.equal(RA, [0., np.pi/2, 0.]) & np.equal(Dec, [0., 0., np.pi/2.]))

def test_calculate_center_of_mass():
    """
    Testing that the center-of-mass calculation actually works (e2e test)
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

if __name__ == '__main__':
    test_Catalog_init()
    test_calculate_center_of_mass()
    test__convert_Cartesian_to_RADec()
    test_convert_RADec_to_Cartesian()
