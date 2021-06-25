import numpy as np
""" 
Brian Jackson & Dida Markovic, 2021
"""

class Catalog:
    """Catalog class containing the astronomical coordinates for a set of points on the sky.
    
    Args:
        RA: the right ascension in radians as an array or float 
        Dec: the declination in radians as an array or float
    """


    def __init__(self, RA, Dec):
        
        self.RA = RA
        self.Dec = Dec

        self.center_of_mass = None

    def _convert_RADec_to_Cartesian(self):
        """(Private) Converts right ascension (RA) and declination (Dec) into Cartesian 
        coordinates (x,y,z) assuming a radius = 1.
        
        The x-axis runs along a line of zero degrees Dec and RA, the y-axis
        along zero degrees Dec and 90 degrees RA, and the z-axis along 90
        degrees Dec.

        Args:
            None

        Returns:
            x: Cartesian x coordinate
            y: Cartesian y coordinate
            z: Cartesian z coordinate
        
        """
    
        x = np.cos(self.Dec)*np.cos(self.RA)
        y = np.cos(self.Dec)*np.sin(self.RA)
        z = np.sin(self.Dec)
    
        return x, y, z

    def _convert_Cartesian_to_RADec(self, x, y, z):
        """(Private) Converts Cartesian x, y, and z coordinates into right ascension (RA) and
        declination (Dec) as measured in radians

        The x-axis runs along a line of zero degrees Dec and RA, the y-axis
        along zero degrees Dec and 90 degrees RA, and the z-axis along 90
        degrees Dec.

        Args:
            x/y/z: floats or vectors of Cartesian coordinates

        Returns:
            list: the RA and Dec corresponding to the given x, y, and z
            coordinates
        """

        # Check that there are not any points with (x, y, z) = (0, 0, 0)
        if(isinstance(x, np.ndarray)):
            ind = np.argwhere((x == 0.) & (y == 0.) & (z == 0.))
            if(len(x[ind]) > 0):
                raise(ValueError("Cartesian coordinates are all zero!"))
        elif(isinstance(x, float)):
            if((x == 0.) & (y == 0.) & (z == 0.)):
                raise(ValueError("Cartesian coordinates are all zero!"))
        
        # Normalize back to unit sphere
        R = np.sqrt(x**2 + y**2 + z**2)
        
        Dec = np.arcsin(z/R)
        RA = np.arctan2(y/R,x/R)
        # Check to make sure RA is the right data type & make sure we return the angle in the right quadrant
        try:
            RA[RA<0]+=2.*np.pi
        except TypeError:
            if RA<0: RA+=2.*np.pi
            
        return RA, Dec

    def calculate_center_of_mass(self):
        """With a Catalog class instantiated and a list of RA/Dec values
        initialized, this method returns the RA/Dec of the center-of-mass for
        the RA/Dec points

        Args:
            None

        Returns: 
            list: RA/Dec of center-of-mass in radians
        """
        x, y, z = self._convert_RADec_to_Cartesian()

        mean_x, mean_y, mean_z = x.mean(), y.mean(), z.mean()

        self.center_of_mass = self._convert_Cartesian_to_RADec(mean_x, mean_y, mean_z)
        return self.center_of_mass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="File name containing three columns with the last two containing RA/Dec values")
    args = parser.parse_args()

    filename = args.file
    data = np.readfromtxt(filename, comment='#', names=['ID', 'RA', 'Dec'], delimiter=' ')
    degtorad = np.pi/180.

    our_catalog = Catalog(data['RA']*degtorad, data['Dec']*degtorad)
    print(our_catalog.calculate_center_of_mass())
