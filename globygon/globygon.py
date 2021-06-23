import numpy as np

class Catalog:
    def __init__(self, RA, Dec):
        
        self.RA = RA
        self.Dec = Dec

        self.center_of_mass = None

    def _convert_RADec_to_Cartesian(self):
        '''
        RA/Dec should be in radians
        '''
    
        x = np.cos(self.Dec)*np.cos(self.RA)
        y = np.cos(self.Dec)*np.sin(self.RA)
        z = np.sin(self.Dec)
    
        return x, y, z

    def _convert_Cartesian_to_RADec(self, x, y, z):
    
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
        x, y, z = self._convert_RADec_to_Cartesian()

        mean_x, mean_y, mean_z = x.mean(), y.mean(), z.mean()

        self.center_of_mass = self._convert_Cartesian_to_RADec(mean_x, mean_y, mean_z)
        return self.center_of_mass

if __name__ == "__main__":
    import pandas as pd
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="File name containing three columns with the last two containing RA/Dec values")
    args = parser.parse_args()

    filename = args.file
    data = pd.read_csv(filename, comment='#', names=['ID', 'RA', 'Dec'], delimiter=' ')
    degtorad = np.pi/180.

    our_catalog = Catalog(data['RA']*degtorad, data['Dec']*degtorad)
    print(our_catalog.calculate_center_of_mass())
